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

Each row in those files contains:

- **filename** — the article or language file name (e.g., en_football.txt, zh_篮球史.txt)  
- **parsed_years** — the list of years extracted from the article text (e.g., "1901, 1912, 2008")

---

## Step-by-Step Explanation

### 1. Read and Identify Language

Reads the input CSV.  
Extracts the language label from each filename (by stripping `.txt`).

    df = pd.read_csv(in_path)
    df["language"] = df["filename"].apply(filename_to_language)

---

### 2. Extract Valid Years

Uses a regular expression to find all 1–4 digit numbers (potential years).  
Keeps only those between 32 CE and 2025 CE.  
Stores (language, year) pairs.

    for y in re.findall(r"-?\d{1,4}", years_str):
        y = int(y)
        if MIN_NUM_AS_YEAR <= y <= END_YEAR:
            records.append((lang, y))

---

### 3. Count Frequencies

Computes how many times each language mentions each year.

    years_df = pd.DataFrame(records, columns=["language", "year"])
    counts = years_df.groupby(["language", "year"]).size().reset_index(name="count")

---

### 4. Pivot into Matrix Form

Reshapes into a matrix where:  
Rows = languages  
Columns = years (1900–2025)  
Values = frequency counts  
Missing cells are filled with zeros.

    pivot = counts_window.pivot(index="language", columns="year", values="count")

---

### 5. Sort Languages by Weighted Mean Year

Calculates each language’s temporal center (weighted average of years).  
Sorts languages so that those focused on more recent periods appear higher.

    weighted_means = pivot.apply(
        lambda row: np.average(pivot.columns, weights=row) if row.sum() > 0 else START_YEAR,
        axis=1
    )
    pivot = pivot.loc[weighted_means.sort_values(ascending=False).index]

---

### 6. Normalize and Apply Gamma Correction

Normalizes each language’s row so that its peak year = 1.  
Applies a gamma (0.4) power transform to enhance low-value contrast.

    row_max = pivot.max(axis=1).replace(0, 1)
    mat_norm = pivot.div(row_max, axis=0)
    mat_gamma = np.power(mat_norm.values.astype(float), GAMMA)

---

### 7. Draw Combined Heatmaps

To ensure colorblind accessibility and perceptual uniformity,  
the visualization uses a **discrete, reversed “magma” colormap (`magma_r`)**,  
where **dark purple indicates fewer mentions** and **bright yellow indicates higher frequency**.  
This choice makes the heatmap readable for both normal and color-deficient vision users.

    def make_discrete_cmap(n_colors=15):
        # Colorblind-safe, perceptually uniform colormap
        base = plt.cm.magma_r(np.linspace(0.06, 1.0, n_colors))
        return ListedColormap(base, name=f"magma_r_{n_colors}")

    draw_combined_heatmaps(pivots, START_YEAR, END_YEAR, out_path)

Each panel (Sports, Objects, Ideologies) is drawn side by side,  
with titles, labels, and a shared legend showing normalized frequencies.

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
