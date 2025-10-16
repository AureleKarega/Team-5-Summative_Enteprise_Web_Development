#!/usr/bin/env python3
import os
import sys
import argparse
import logging

# Add the parent directory (project root) to Python path
# This allows us to import from 'src' as an absolute import
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# Now use absolute imports
from src.services.etl import run_etl_from_csv
from src.config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", help="Path to raw CSV", required=True)
    parser.add_argument("--out", help="Path output processed CSV", default="data/processed/trips_cleaned.csv")
    args = parser.parse_args()
    chunksize = Config.CHUNK_SIZE
    logger.info(f"Starting ETL: {args.csv} -> {args.out} with chunksize={chunksize}")
    run_etl_from_csv(args.csv, args.out, chunksize=chunksize)
    logger.info("ETL complete.")

if __name__ == "__main__":
    main()