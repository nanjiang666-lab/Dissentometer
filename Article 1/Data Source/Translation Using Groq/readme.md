# Wikipedia Translation Pipeline (Ideologies Dataset)

## Overview

This script automatically **translates multilingual Wikipedia-style datasets** into standardized bilingual CSV files.  
It is designed for use after the *CSV combination stage*, where multilingual article `.txt` files have already been consolidated into per-topic CSVs (e.g., `History_of_Ideologies_zh.csv`).  

Each source CSV is assumed to contain:
- **filename** — the language of the file 
- **content** — the text content extracted from that file  

The script then translates the `content` field into English, creating a new output CSV with aligned bilingual fields.

---

## Data Source

The data source originates from the **“CSV Combination” section** of this project’s GitHub repository.  
Refer to the `README` in that section for details on how raw Wikipedia article folders were merged into the intermediate CSV format used here.  
In summary:
- Each topic directory contains multiple preprocessed CSVs created from article-level `.txt` data.
- These CSVs already include the `filename` and `content` columns produced by the **combination pipeline** (see `dates packing/README.md` on GitHub for provenance and preprocessing notes).

---

## Translation Logic

### Core Functionality

For each CSV file in the input directory (sorted alphabetically by filename), the script performs the following steps:

1. **Iterate over each row** in the CSV file.  
2. **Flatten** the `content` text by removing newlines and extra whitespace.  
3. **Translate** the flattened content into English using the Groq API (`llama-3.1-8b-instant` model).  
   - Texts longer than 20,000 characters are automatically **split into chunks**.  
   - If a translation request fails, the chunk is **recursively subdivided** until every non-empty segment is translated (down to single characters if necessary).  
4. **Preserve the original filename** from the CSV’s `filename` column.  
5. **Ensure Excel compatibility** by splitting rows if any cell exceeds Excel’s 32,767-character limit (both original and translated text are evenly partitioned).  
6. **Cache identical sentences** so that repeated content isn’t retranslated.  

---

## Output Format

Each output file follows this naming pattern:

### Output Schema

| Column Name | Description |
|--------------|-------------|
| `filename` | language of the file from the source CSV |
| `content` | Original text (flattened, whitespace-normalized) |
| `English translation` | Model-generated English translation |
