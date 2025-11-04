# Wikipedia Category Scraper

This module provides a recursive Wikipedia scraper that downloads text content from multilingual category trees using the official Wikipedia and Wikidata APIs.

> **Note:**  
> This README describes only the functionality in this directory.  
> The repository is modular — each subfolder should include its own short README describing the scripts inside.

---

## 🧩 Overview

The script recursively scrapes articles from a given **Wikipedia category** (for example, *History of Sports*),  
following **interlanguage links** and **subcategories** up to a specified depth.

For each article:
- It fetches the plain-text extract using the Wikipedia API.  
- It saves all language versions as `.txt` files within a structured hierarchy.  
- It preserves multi-level subcategories, limited by a user-defined depth.

This scraper supports automatic Wikidata lookups, allowing it to follow equivalent categories across different language editions.

---

## 🗂 Directory Usage

Each run of the script creates an output structure like this:

```text
/Outputs/
├── en_History_of_Sports/
│   ├── Baseball/
│   │   ├── en.txt
│   │   ├── zh.txt
│   │   ├── fr.txt
│   │   └── ...
│   ├── Basketball/
│   │   ├── en.txt
│   │   ├── de.txt
│   │   └── ...
│   └── ...
