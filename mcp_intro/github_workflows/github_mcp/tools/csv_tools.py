# tools/csv_tools.py

# Try to import MCP server, but make it optional
try:
    from server import mcp
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    # Create a dummy decorator for when MCP is not available
    class DummyMCP:
        def tool(self):
            def decorator(func):
                return func
            return decorator
    mcp = DummyMCP()

from ..utils.file_reader import read_csv_summary
import pandas as pd
from pathlib import Path
import os

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
EXTERNAL_DATA_DIR = os.getenv('EXTERNAL_DATA_DIR')

@mcp.tool()
def summarize_csv_file(filename: str) -> str:
    """
    Summarize a CSV file by reporting its number of rows and columns.
    Args:
        filename: Name of the CSV file in the /data directory (e.g., 'sample.csv')
    Returns:
        A string describing the file's dimensions.
    """
    return read_csv_summary(filename)


@mcp.tool()
def read_csv_file(filename: str) -> str:
    """
    Read a CSV file and return the contents.
    Args:
        filename: Name of the CSV file in the /data directory (e.g., 'sample.csv')
    Returns:
        A string describing the file's contents.
    """
    file_path = DATA_DIR / filename
    df = pd.read_csv(file_path)
    return df.to_string()