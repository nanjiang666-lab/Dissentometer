# 🧠 Folder Translation and CSV Generation Pipeline

## **Overview**

This script automates the **translation and conversion** of **multilingual Wikipedia-style datasets** into **standardized English CSV files**.  
Each subfolder in the source directory represents a **topic** (e.g., *“中国篮球史” → “History of Chinese Basketball”*), containing multiple `.txt` files of textual content.

The script uses **OpenAI’s GPT models** to translate folder names into English, **detects duplicates automatically**, **dynamically adjusts batch sizes** for translation requests, and **merges all text files under each folder into one structured CSV file**.

---

## **Key Features**
- 🚀 **Automated translation** of folder names (multi-language → English)  
- ⚙️ **Dynamic batching** for efficient OpenAI API usage  
- 🔁 **Automatic duplicate detection** and skipping  
- 📄 **Consolidation** of multiple `.txt` files into a single CSV per topic  
- 💓 **Continuous live logging** and heartbeat monitoring for progress tracking  

---

## **Input Data**

### **Directory Structure**

The script expects the following format under the base directory:

/local/scratch/group/guldigroup/climate_change/wiki_history_nan/History of sports/
│
├── 中国篮球史/
│   ├── 001_intro.txt
│   ├── 002_development.txt
│   └── 003_teams.txt
│
├── 日本柔道史/
│   ├── 001_origin.txt
│   ├── 002_training.txt
│   └── 003_championships.txt
│
└── Футбольная история/
    ├── 001_early.txt
    ├── 002_worldcup.txt
    └── 003_rules.txt


Each folder:

Represents one topic (often non-English)

Contains .txt files with UTF-8 text content

Configuration
Parameter	Description
BASE_DIR	Source directory containing multilingual folders
OUTPUT_DIR	Destination directory for English-translated CSVs
API_MODEL	OpenAI model used (gpt-4o-mini)
BATCH_SIZES	Adaptive batch sizes: [200, 100, 50, 20, 5, 1]
SKIP_COUNT	Index to resume from (useful for restarting large runs)
Processing Workflow
Scanning and Grouping

All .txt files under BASE_DIR are recursively scanned and grouped by their parent folder name.
Each group represents one concept/topic.

Translation Phase
Step 1 — Single Translation Mode

Each folder name is translated individually via OpenAI’s ChatCompletion API.

Prompt:

Translate to English; return ONLY the translation.


Retries automatically on rate limit errors (HTTP 429) with 20-second delays.

If the translated English name already exists in the output directory, it is logged as 🔄 DUPLICATE and skipped.

The first new translation triggers the switch to batch mode.

Step 2 — Dynamic Batch Translation

Translations proceed in adaptive batches for efficiency.

Batch sizes follow this hierarchy:
200 → 100 → 50 → 20 → 5 → 1

On JSON parsing or API errors, the batch size is reduced and retried.

Each batch request expects a strict JSON array of English strings.

CSV Assembly

After translation:

All .txt files within each folder are concatenated into a single CSV file with the following structure:

filename	content
001_intro.txt	full text content...
002_development.txt	full text content...
003_teams.txt	full text content...

CSVs are saved under OUTPUT_DIR, named after the English translation (e.g., History of Chinese Basketball.csv).

Example output:

/home/njian29/Desktop/history of sport/
│
├── History of Chinese Basketball.csv
├── History of Judo in Japan.csv
└── History of Football.csv

Logging and Monitoring

A background thread continuously prints real-time progress:

[14:33:05] translate_batch: 50 items


Console logs include:

NEW → new English translation and CSV written

DUPLICATE → already processed topic

429 or JSON error → retry or reduce batch size

All remaining folders done → successful completion

Output Summary
Output Type	Description
CSV files, one per topic, contain all text files combined
File naming: English translation of the folder name
Encoding	UTF-8
Logs	Real-time print output (status messages + progress)
System Behavior
Function	Description
translate_single()	Translates a single folder name using GPT
translate_batch()	Translates multiple folder names in one request (adaptive)
write_csv()	Combines all .txt files into a CSV file
csv_path_from_eng()	Builds safe, ASCII-only output paths
status_printer()	Heartbeat thread printing live progress
main()	Orchestrates scanning → translating → writing
Final Result

After completion, the output directory (/home/njian29/Desktop/history of sport/) will contain:

Clean, English-labeled CSV files, one for each multilingual topic

Each CSV is ready for downstream use in:

Topic modeling/clustering

Language reuse analysis

Cross-language comparison

Visualization or digital humanities pipelines

Example Log Snippet
Distinct folders: 31,450; starting at #31,307
→ 开始 translate_single('中国篮球史')
← 完成 translate_single('中国篮球史') → 'History of Chinese Basketball'
[31307/31450] 中国篮球史 → History of Chinese Basketball  NEW

──── Switching to dynamic batch mode ────
Trying batch size 200: items 31308–31507
← 完成 translate_batch
   日本柔道史 → History of Judo in Japan  written
   Футбольная история → History of Football  DUPLICATE
All remaining folders are done.

Notes

The script does not currently persist progress. Restarting will reprocess from the beginning unless SKIP_COUNT is adjusted.

flush=True ensures console outputs appear immediately (important on HPC systems).

If running in VS Code or Jupyter, wrap the line:

if hasattr(sys.stdout, "reconfigure"):
    sys. stdout.reconfigure(line_buffering=True)


to prevent compatibility errors.

Author

Samuel Jiang (2025)
Emory University – Climate Change / Dissentometer Lab
Department of Economics & History
Research Automation and Language Pipeline Development
