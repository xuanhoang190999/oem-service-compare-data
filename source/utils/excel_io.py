import os
import pandas as pd
from datetime import datetime

INPUT_DIR = os.path.join(os.getcwd(), "Input")
OUTPUT_DIR = os.path.join(os.getcwd(), "Output")

def read_input_excel(filename: str) -> pd.DataFrame:
    filepath = os.path.join(INPUT_DIR, filename)
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Cannot find file input: {filepath}")

    df = pd.read_excel(filepath)
    print(f"[ExcelIO] Read {len(df)} row from {filepath}")
    return df

def write_output_excel(df: pd.DataFrame, base_filename: str = "compare_result"):
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{base_filename}_{timestamp}.xlsx"
    filepath = os.path.join(OUTPUT_DIR, filename)

    df.to_excel(filepath, index=False)
    print(f"[ExcelIO] Print results in {filepath}")
    return filepath
