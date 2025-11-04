# Overview

This Python script builds a Cross-Language Historical Heatmap Pipeline, designed to visualize how often different languages mention specific years (e.g., 1900–2025) across three Wikipedia-derived topic groups:

- Sports  
- Objects  
- Ideologies  

It reads pre-processed CSV files containing extracted year data, aggregates them by language and year, normalizes the frequencies, and produces a combined, publication-ready multi-panel heatmap figure.

The final output is a high-resolution PNG file saved to the desktop:  
~/Desktop/combined_heatmap_1900-2025.png

---

## Data Source

The datasets come from the Wikipedia Year Extraction and Tagging Pipeline, documented in the “dates_packing” section of the GitHub repository’s README.  
That section explains how Wikipedia text files (organized by topic folders) were parsed to extract all four-digit numeric years and then stored in tagged CSV files.

The three input CSVs are:

- parsed_years_history_of_sports_tagged.csv  
- parsed_years_historical_objects_tagged.csv  
- parsed_years_history_of_ideologies_tagged.csv

(The parts are from the Data Source/Dates Packing section)

Each row in those files contains:

- **filename** — the language under the category (e.g., English.txt, Chinese.txt)  
- **parsed_years** — the list of years extracted from the article text (e.g., "1901, 1912, 2008")

---

## Output Visualization

The resulting figure shows:

| History of Sports | Historical Objects | History of Ideologies |
|--------------------|--------------------|-----------------------|
| Each row = a language | Each column = a year | Color = normalized frequency |

- Bright yellow zones mark years most frequently mentioned for that language/topic.  
- Dark purple zones indicate minimal mentions.  
- The colormap (`magma_r`) provides clear contrast while remaining colorblind-friendly.  
- The layout provides a comparative view of how different languages emphasize historical time periods across topics.

---

## Summary Flow

    Wikipedia CSVs
       ↓
    Parse years & filter (32–2025)
       ↓
    Group by language × year
       ↓
    Pivot to matrix (rows=language, cols=year)
       ↓
    Normalize + gamma correction
       ↓
    Draw combined heatmaps (magma_r colorblind-safe)
       ↓
    Output: combined_heatmap_1900-2025.png
