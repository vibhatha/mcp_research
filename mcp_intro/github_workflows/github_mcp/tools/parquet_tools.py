# tools/parquet_tools.py

from server import mcp
from ..utils.file_reader import read_parquet_summary
import pandas as pd
from pathlib import Path
import os

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
EXTERNAL_DATA_DIR = os.getenv('EXTERNAL_DATA_DIR')

@mcp.tool()
def summarize_parquet_file(filename: str) -> str:
    """
    Summarize a Parquet file by reporting its number of rows and columns.
    Args:
        filename: Name of the Parquet file in the /data directory (e.g., 'sample.parquet')
    Returns:
        A string describing the file's dimensions.
    """
    return read_parquet_summary(filename)


@mcp.tool()
def read_parquet_file(filename: str) -> str:
    """
    Read a Parquet file and return the contents.
    Args:
        filename: Name of the Parquet file in the /data directory (e.g., 'sample.parquet')
    Returns:
        A string describing the file's contents.
    """
    file_path = DATA_DIR / filename
    df = pd.read_parquet(file_path)
    return df.to_string()