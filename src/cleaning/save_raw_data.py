# (.venv) PS D:\project\laptop_pricing_intelligence_pipeline\src  python -m cleaning.save_raw_data.py  

from scraping.scraper import run_scraper
import pandas as pd
from pathlib import Path

if __name__ == "__main__":
    laptops = run_scraper()
    df = pd.DataFrame(laptops)

    BASE_DIR = Path(__file__).resolve().parents[2]
    output_dir = BASE_DIR / "data" / "raw"
    output_dir.mkdir(parents=True, exist_ok=True)

    df.to_csv(output_dir / "raw_laptops.csv", index=False)

      