import os
from ..etl_steps.loader import iter_csv_in_chunks, extract_csv_from_zip
from ..etl_steps.cleaner import basic_clean
from ..etl_steps.feature_engineering import apply_feature_engineering
from logging import getLogger

logger = getLogger(__name__)

def run_etl_from_csv(csv_path, output_path, chunksize=50000):
    """
    Read csv in chunks, clean, enrich, and append to a processed CSV.
    Keeps a log of removed rows counts via logger.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    first_write = True
    total_in = 0
    total_out = 0
    for chunk in iter_csv_in_chunks(csv_path, chunksize=chunksize):
        total_in += len(chunk)
        cleaned_chunk, removed_df, reasons = basic_clean(chunk)
        if cleaned_chunk.empty:
            logger.info("Chunk cleaned to empty; skipping.")
            continue
        enriched = apply_feature_engineering(cleaned_chunk)
        # write to CSV (append)
        if first_write:
            enriched.to_csv(output_path, index=False, mode='w')
            first_write = False
        else:
            enriched.to_csv(output_path, index=False, header=False, mode='a')
        total_out += len(enriched)
        logger.info(f"Processed chunk: input {len(chunk)} -> output {len(enriched)}")
    logger.info(f"ETL finished. Total in {total_in}, total out {total_out}")
    return True
