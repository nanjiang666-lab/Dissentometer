---

## Key Parameters

This section documents the key configuration parameters used by the Wikipedia Category Scraper.  
Each variable can be customized at the top of the Python script before execution.

---

| Variable | Description |
|-----------|--------------|
| `MAIN_LANG` | Root Wikipedia language edition (e.g. `"en"`) |
| `MAIN_CAT` | The category to start from (e.g. `"History of Sports"`) |
| `MAX_DEPTH` | How many subcategory levels to explore (default `4`) |
| `OUTPUT_ROOT` | Output folder where all texts are saved |
| `SLEEP` | Delay between API requests to avoid throttling |
| `HEADERS` | Custom User-Agent header for polite API access |

---

## Notes

- **`MAIN_LANG`** determines the base Wikipedia edition (English `"en"`, French `"fr"`, Chinese `"zh"`, etc.).  
- **`MAIN_CAT`** is the root category name used as the entry point of scraping.  
- **`MAX_DEPTH`** controls recursion depth — higher values collect more subcategories but increase runtime.  
- **`OUTPUT_ROOT`** defines where the entire multilingual dataset will be stored.  
- **`SLEEP`** sets a delay between API requests to prevent server overload (default is a few milliseconds).  
- **`HEADERS`** should include a descriptive User-Agent, e.g. `"MyWikiScraper/1.0 (contact@example.com)"`,  
  to comply with Wikimedia’s fair-use policy.

---

## Example Configuration

```python
MAIN_LANG   = "en"
MAIN_CAT    = "History of Sports"
MAX_DEPTH   = 4
OUTPUT_ROOT = Path.cwd() / "Outputs"
SLEEP       = 1e-5
HEADERS     = {"User-Agent": "MyWikiScraper/1.0"}
