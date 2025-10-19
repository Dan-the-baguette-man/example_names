import pandas as pd
from pathlib import Path

INPUT = Path("data/messy.csv")
OUTPUT_DIR = Path("output")
OUTPUT = OUTPUT_DIR / "cleaned.csv"

def main():
    # Load the CSV into a DataFrame
    df = pd.read_csv(INPUT)

    # === YOUR TASKS ===
    # 1) id: convert to integer
    #    - use pd.to_numeric(df["id"], errors="coerce") to turn bad values into NaN
    #    - drop rows where id is NaN
    #    - finally convert to int
    df["id"] = pd.to_numeric(df["id"], errors="coerce")
    df = df.dropna(subset=["id"])
    df["id"] = df["id"].astype(int)

    # 2) date: normalize to YYYY-MM-DD
    #    - use pd.to_datetime(df["date"], errors="coerce") to turn bad dates into NaT
    #    - drop rows where date is NaT
    #    - convert to string with .dt.strftime("%Y-%m-%d")
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])
    df["date"] = df["date"].dt.strftime("%Y-%m-%d")

    # 3) category: trim spaces and lowercase
    #    - use .str.strip() to trim spaces
    #    - use .str.lower() to lowercase
    df["category"] = df["category"].str.strip().str.lower()

    # 4) amount: remove "$" and spaces, convert to float
    #    - use .str.replace("$", "", regex=False).str.replace(" ", "")
    #    - then pd.to_numeric(..., errors="coerce") and round to 2 decimals using .round(2)
    #    - drop rows where amount is NaN
    df["amount"] = df["amount"].str.replace("$", "", regex=False).str.replace(" ", "")
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").round(2)
    df = df.dropna(subset=["amount"])

    # 5) Sort by id ascending
    df = df.sort_values(by="id")

    # Save cleaned data to output file
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT, index=False)

if __name__ == "__main__":
    main()
