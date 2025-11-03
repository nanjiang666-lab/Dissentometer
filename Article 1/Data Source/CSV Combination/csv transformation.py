import sys
import json
import time
import threading
from pathlib import Path
from collections import defaultdict
from typing import List, Optional

import pandas as pd
from openai import OpenAI

sys.stdout.reconfigure(line_buffering=True)

BATCH_SIZES = [200, 100, 50, 20, 5, 1]

API_MODEL  = "gpt-4o-mini"
OPENAI_API_KEY = ""
client = OpenAI(api_key=OPENAI_API_KEY)

SKIP_COUNT = 31306                   
BASE_DIR   = Path("/local/scratch/group/guldigroup/climate_change/wiki_history_nan/History of sports")
OUTPUT_DIR = Path("/home/njian29/Desktop/history of sport")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

status =
done   = False

def status_printer():
    while not done:
        print(f"[{time.strftime('%H:%M:%S')}] 💓 {status}", flush=True)
        time.sleep(1)

def translate_single(text: str) -> Optional[str]:
    global status
    status = f"translate_single: '{text}'"
    while True:
        print(f"→ 开始 translate_single('{text}')", flush=True)
        try:
            rsp = client.chat.completions.create(
                model=API_MODEL,
                messages=[
                    {"role": "system", "content": "Translate to English; return ONLY the translation."},
                    {"role": "user",   "content": text},
                ],
                temperature=0.0,
            )
            content = rsp.choices[0].message.content.strip()
            print(f"← 完成 translate_single('{text}') → '{content}'", flush=True)
            return content
        except Exception as e:
            msg = str(e)
            if "429" in msg or "Rate limit" in msg:
                print(f"⚠️ 429 error on single '{text}': {e} — 等待20秒", flush=True)
                time.sleep(20)
                continue
            else:
                print(f"⚠️ single error on '{text}': {e} — 忽略并返回空", flush=True)
                return ""

def translate_batch(lines: List[str]) -> Optional[List[str]]:
    global status
    status = f"translate_batch: {len(lines)} 条"
    print(f"→ 开始 translate_batch ({len(lines)} items)", flush=True)
    prompt = "\n".join(lines)
    try:
        rsp = client.chat.completions.create(
            model=API_MODEL,
            messages=[
                {"role": "system", "content": (
                    "Translate each line to English. Return ONLY a JSON array, one string per input line."
                )},
                {"role": "user", "content": prompt},
            ],
            temperature=0.0,
        )
    except Exception as e:
        print(f"⚠️ Batch call exception: {e}", flush=True)
        return None

    print("← 完成 translate_batch", flush=True)
    status = "translate_batch: completed"

    raw = rsp.choices[0].message.content.strip()
    if raw.startswith("```"):
        raw = "\n".join(raw.splitlines()[1:-1])
    raw = raw[raw.find("["): raw.rfind("]")+1]
    try:
        arr = json.loads(raw)
        if not isinstance(arr, list) or len(arr) != len(lines):
            raise ValueError("返回长度不匹配")
        return [s.strip() for s in arr]
    except Exception as e:
        print(f"⚠️ parse batch JSON failed: {e}", flush=True)
        return None

def csv_path_from_eng(eng: str) -> Path:
    if "/" in eng:
        first, rest = eng.split("/", 1)
        dir_ = OUTPUT_DIR / first.strip()
        fname = rest.strip().replace("/", "_").replace("\\", "_") + ".csv"
        return dir_ / fname
    return OUTPUT_DIR / (eng.replace("/", "_").replace("\\", "_") + ".csv")

def write_csv(out_path: Path, txt_list: List[Path]) -> None:
    global status
    status = f"write_csv: '{out_path.name}'"
    rows = []
    for t in sorted(txt_list, key=lambda p: str(p).lower()):
        if not t.stem.isascii():
            continue
        try:
            rows.append({
                "filename": t.name,
                "content":  t.read_text(encoding="utf-8", errors="ignore")
            })
        except Exception:
            continue
    if rows:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        pd.DataFrame(rows).to_csv(out_path, index=False)

def main():
    global status, done
    status = "扫描 .txt 文件"
    txt_files = sorted(BASE_DIR.rglob("*.txt"), key=lambda p: str(p).lower())
    if not txt_files:
        print("No .txt files found.", flush=True)
        done = True
        return

    status = "按父文件夹分组"
    groups = defaultdict(list)
    for p in txt_files:
        groups[p.parent.name].append(p)
    orig_names = sorted(groups, key=lambda n: n.lower())

    total = len(orig_names)
    i = SKIP_COUNT
    print(f"Distinct folders: {total:,}; starting at #{i+1:,}", flush=True)

    status = f"STEP1 individual start #{i+1}"
    while i < total:
        name = orig_names[i]
        eng = translate_single(name)
        if not eng.isascii():
            i += 1
            continue
        out_path = csv_path_from_eng(eng)
        if out_path.exists():
            print(f"[{i+1}/{total}] {name} → {eng}  🔄 DUPLICATE", flush=True)
            i += 1
            continue
        write_csv(out_path, groups[name])
        print(f"[{i+1}/{total}] {name} → {eng}  ✅ NEW", flush=True)
        i += 1
        break

    if i >= total:
        print("All processed.", flush=True)
        done = True
        return

    print("\n──── Switching to dynamic batch mode ────", flush=True)
    status = "STEP2 batch init"
    while i < total:
        for size in BATCH_SIZES:
            batch = orig_names[i : i + size]
            if not batch:
                continue
            print(f"\n▶️ Trying batch size {size}: items {i+1}–{i+len(batch)}", flush=True)
            trans = translate_batch(batch)
            if trans is None:
                print(f"⚠️ Batch size {size} failed, reducing...", flush=True)
                continue
            for name, eng in zip(batch, trans):
                if not eng or not eng.isascii():
                    continue
                out_path = csv_path_from_eng(eng)
                if out_path.exists():
                    print(f"   {name} → {eng}  🔄 DUPLICATE", flush=True)
                else:
                    write_csv(out_path, groups[name])
                    print(f"   {name} → {eng}  ✅ written", flush=True)
            i += size
            break
        else:
            name = orig_names[i]
            print(f"‼️ All batch sizes failed for '{name}', skipping.", flush=True)
            i += 1

    print("\n🎉 All remaining folders done.", flush=True)
    done = True

if __name__ == "__main__":
    threading.Thread(target=status_printer, daemon=True).start()
    main()