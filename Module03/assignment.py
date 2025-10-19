"""
DATA 304 - Module 3 • Assignment

You will implement FOUR small functions:
1) read_csv_basic
2) read_excel_two_sheets
3) read_csv_chunks_keep_column
4) optimize_dtypes

Edit ONLY inside the blocks:
# ===== TASK STARTS HERE =====
# ===== TASK ENDS HERE =====
"""

from pathlib import Path
from typing import Optional
import pandas as pd


def read_csv_basic(
    path: str | Path,
    *,
    sep: str = ",",
    encoding: Optional[str] = None,
) -> pd.DataFrame:
    """
    Goal: Read a small CSV file.

    Requirements:
    - Use the provided `sep` (default comma).
    - Handle common NA markers: "", " ", "NA", "N/A", "NaN".
    - If `encoding` is given, use it.
    - If `encoding` is not given, try in order: "utf-8", then "utf-8-sig", then "latin-1".
    """

    # ===== TASK 1 STARTS HERE =====
    na_values = ["", " ", "NA", "N/A", "NaN"]

    # If an encoding was provided, try once with it.
    if encoding is not None:
        return pd.read_csv(path, sep=sep, na_values=na_values, encoding=encoding)

    # Otherwise try a short list in order.
    for enc in ["utf-8", "utf-8-sig", "latin-1"]:
        try:
            return pd.read_csv(path, sep=sep, na_values=na_values, encoding=enc)
        except UnicodeDecodeError:
            continue

    # If all failed, let pandas raise a normal error.
    return pd.read_csv(path, sep=sep, na_values=na_values)
    # ===== TASK 1 ENDS HERE =====


def read_excel_two_sheets(
    path: str | Path,
    sheet1: int | str,
    sheet2: int | str,
) -> pd.DataFrame:
    """
    Goal: Read two Excel sheets and stack them.

    Requirements:
    - Read `sheet1` and `sheet2` using `pd.read_excel`.
    - Vertically concatenate the two DataFrames. (axis=0)
    - Keep the row index simple (0..n-1) by using `ignore_index=True`.
    """

    # ===== TASK 2 STARTS HERE =====
    df1 = pd.read_excel(path, sheet_name=sheet1)
    df2 = pd.read_excel(path, sheet_name=sheet2)
    out = pd.concat([df1,df2], axis=0, ignore_index=True)
    return out
    # ===== TASK 2 ENDS HERE =====


def read_csv_chunks_keep_column(
    path: str | Path,
    column: str,
    value,
    *,
    chunksize: int = 50_000,
) -> pd.DataFrame:
    """
    Goal: Read a larger CSV in pieces and keep only rows where `column == value`.

    Requirements:
    - Use `pd.read_csv(..., chunksize=chunksize)` to stream the file.
    - For each chunk, filter rows where `chunk[column] == value`.
    - Collect filtered chunks and concatenate them into one DataFrame.
    - If no rows match, return an empty DataFrame with correct columns.
    """

    # ===== TASK 3 STARTS HERE =====
    kept = []
    for chunk in pd.read_csv(path, chunksize=chunksize):
        if column in chunk.columns:
            kept.append(chunk[chunk[column] == value]) #task

    if not kept:
        # If we never read any chunks or nothing matched, return empty.
        try:
            # Try to get columns from the header only (fast).
            cols_only = pd.read_csv(path, nrows=0).columns
            return pd.DataFrame(columns=cols_only)
        except Exception:
            return pd.DataFrame()

    return pd.concat(kept, axis=0, ignore_index=True)
    # ===== TASK 3 ENDS HERE =====


def optimize_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Goal: Reduce memory by downcasting numerics and using category for low-cardinality text.

    Requirements:
    - Work on a COPY. Do not modify the input `df`.
    - Integers: downcast to the smallest integer subtype. 
    - Floats: downcast to the smallest float subtype. 
    - Objects: if unique_ratio ≤ 0.5 (unique / len), convert to category.
    - Return the optimized DataFrame.

    Hints:
    - Use `pd.to_numeric(col, downcast="integer"/"float")`.
    - Use `df.select_dtypes(include=["number"/"object"]).columns` to find numeric or object columns.
    - Handle empty columns safely to avoid ZeroDivisionError.
    """

    # ===== TASK 4 STARTS HERE =====
    out = df.copy()

    # Downcast numeric columns
    num_cols = df.select_dtypes(include=["number"]).columns
    for c in num_cols:
        if pd.api.types.is_integer_dtype(out[c]):
            out[c] = pd.to_numeric(out[c], downcast="integer")
        else:
            out[c] = pd.to_numeric(out[c], downcast="float")

    # Convert low-cardinality object columns to category
    obj_cols = df.select_dtypes(include=["object"]).columns
    for c in obj_cols:
        n = len(out[c])
        if n == 0:
            continue
        unique_ratio = out[c].nunique(dropna=True) / n
        if unique_ratio <= 0.5:
            out[c] = out[c].astype("category")

    return out
    # ===== TASK 4 ENDS HERE =====
