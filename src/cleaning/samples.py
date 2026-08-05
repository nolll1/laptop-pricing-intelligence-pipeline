# (.venv) PS D:\project\laptop_pricing_intelligence_pipeline\src> python -m cleaning.samples      

from pathlib import Path
import pandas as pd

df = pd.read_csv(r"D:\project\laptop_pricing_intelligence_pipeline\data\raw\raw_laptops.csv")
cleaned_df = pd.read_csv(r"D:\project\laptop_pricing_intelligence_pipeline\data\processed\cleaned_laptops.csv")

sample_df = df.sample(100, random_state=42)
cleaned_sample_df = cleaned_df.sample(100, random_state=42)

BASE_DIR = Path(__file__).resolve().parents[2]

output_dir = BASE_DIR / "data" / "samples"
output_dir.mkdir(parents=True, exist_ok=True)

sample_df.to_csv(output_dir / "raw_sample_laptops.csv", index=False)
cleaned_sample_df.to_csv(output_dir / "cleaned_sample_laptops.csv", index=False)