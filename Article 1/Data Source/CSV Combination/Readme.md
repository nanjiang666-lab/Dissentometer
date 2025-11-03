# convert_txt_to_csv.py — Folder Translation and CSV Conversion Pipeline

## Overview
This Python script (`convert_txt_to_csv.py`) automates the translation and conversion of multilingual Wikipedia-style `.txt` files into standardized English CSV files.  
Each subfolder in the input directory represents a topic (e.g., “中国篮球史” → “History of Chinese Basketball”) containing multiple `.txt` documents.  
The script translates folder names, merges all `.txt` contents, and outputs one CSV file per topic for downstream text analysis.

---

## 1. Input Data

### Directory Structure
The input directory contains multiple subfolders (each representing a topic), with several `.txt` files per folder:

    /home/njian29/Desktop/wiki_history/
    │
    ├── History of ideologies/
    │   ├── Afrikaans.txt
    │   ├── Arabic.txt
    │   ├── Chinese.txt
    │   └── French.txt
    │
    ├── History of sports/
    │   ├── Japanese.txt
    │   ├── Russian.txt
    │   └── Spanish.txt
    │
    └── Historical objects/
        ├── Korean.txt
        ├── Turkish.txt
        └── German.txt

Each `.txt` file is UTF-8 encoded and represents textual data from a particular language.

---

## 2. Configuration Parameters
| Parameter | Description |
|------------|-------------|
| **BASE_DIR** | Source directory containing multilingual folders |
| **OUTPUT_DIR** | Destination directory for translated CSVs |
| **API_MODEL** | OpenAI model used for translation (e.g., `gpt-4o-mini`) |
| **BATCH_SIZES** | Adaptive translation batch sizes: [200, 100, 50, 20, 5, 1] |
| **SKIP_COUNT** | Optional resume index for restarting large runs |

---

## 3. Processing Workflow

### Step 1 — Directory Scanning
All `.txt` files under the base directory are recursively detected and grouped by their parent folder (each group = one topic).

### Step 2 — Folder Translation
- Each folder name is translated from its original language into English.  
- Duplicate English names are automatically skipped.  
- Translation requests dynamically adjust their batch size to handle API rate limits or errors.

### Step 3 — File Consolidation
All `.txt` files in a folder are merged into one CSV file under the translated folder name.

| filename | content | English translation |
|-----------|----------|--------------------|
| Chinese.txt | .cs原先是捷克斯洛伐克地区顶级域名... | .cs domain used before 1993 |
| Arabic.txt | .cs مرجع إلى الجمهورية التشيكوسلوفاكية ... | Former Czechoslovakia’s domain |
| French.txt | .cs fut le domaine de premier niveau... | Czechoslovakia national domain |

---

## 4. Output
The script writes one `.csv` per topic into the output directory:

    /home/njian29/Desktop/wiki_history_output/
    │
    ├── History of Ideologies.csv
    ├── History of Sports.csv
    └── Historical Objects.csv

Each CSV contains:
- All combined text files per topic
- Optional English translation column
- UTF-8 encoding, ready for downstream analysis

---

## 5. Logging and Monitoring
The script prints real-time progress (e.g., translation batches, duplicates, and retries).  
Example log snippet:

    [14:33:05] translate_batch: 50 items
    → 开始 translate_single('中国篮球史')
    ← 完成 translate_single → 'History of Chinese Basketball'
    [31307/31450] 中国篮球史 → History of Chinese Basketball NEW

    ─── Switching to dynamic batch mode ───
    Trying batch size 200: items 31308–31507
    ← translate_batch success
    日本柔道史 → History of Judo in Japan written
    Футбольная история → History of Football DUPLICATE

---

## 6. System Behavior
| Function | Description |
|-----------|-------------|
| **translate_single()** | Translates one folder name via GPT |
| **translate_batch()** | Translates multiple folder names adaptively |
| **write_csv()** | Writes all `.txt` files in a folder to one `.csv` |
| **csv_path_from_eng()** | Builds safe ASCII output paths |
| **status_printer()** | Prints live progress updates |
| **main()** | Orchestrates scanning → translation → CSV writing |

---

## 7. Result Summary
After successful execution, the output directory contains English-named CSVs that standardize multilingual Wikipedia-style datasets.  
These files are directly usable for:
- Topic modeling and clustering  
- Language reuse or diffusion analysis  
- Cross-lingual historical comparison  
- Visualization in digital humanities projects

---

**Author:** Samuel Jiang (2025)  
Emory University – Data Science Lab, Department of Economics & Mathematics
