import pandas as pd
from logging import getLogger

logger = getLogger(__name__)

def iter_csv_in_chunks(csv_path, chunksize=50000, **read_csv_kwargs):
    """
    Yield pandas DataFrame chunks
    """
    for chunk in pd.read_csv(csv_path, chunksize=chunksize, low_memory=False, **read_csv_kwargs):
        yield chunk
