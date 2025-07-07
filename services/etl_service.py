import logging
from typing import Any, Dict, Optional
import pandas as pd
from pymongo import MongoClient
import io

class ETLService:
    def __init__(self, mongo_uri: str, mongo_db: str, mongo_collection: str) -> None:
        self.mongo_uri: str = mongo_uri
        self.mongo_db: str = mongo_db
        self.mongo_collection: str = mongo_collection
        self.tracking_collection_name: str = "etl_file_tracking"

    def has_processed(self, filename: str) -> bool:
        try:
            client: MongoClient = MongoClient(self.mongo_uri)
            db = client[self.mongo_db]
            tracking = db[self.tracking_collection_name]
            exists: bool = tracking.find_one({"filename": filename}) is not None
            client.close()
            logging.info(f"Check if '{filename}' has been processed: {exists}")
            return exists
        except Exception as e:
            logging.error(f"Error in has_processed for '{filename}': {e}")
            return False

    def mark_processed(self, filename: str) -> None:
        try:
            client: MongoClient = MongoClient(self.mongo_uri)
            db = client[self.mongo_db]
            tracking = db[self.tracking_collection_name]
            tracking.insert_one({"filename": filename})
            client.close()
            logging.info(f"Marked '{filename}' as processed.")
        except Exception as e:
            logging.error(f"Error in mark_processed for '{filename}': {e}")

    def extract(self, file_content: bytes) -> pd.DataFrame:
        try:
            df: pd.DataFrame = pd.read_csv(io.BytesIO(file_content))
            logging.info(f"Extracted {len(df)} rows from file.")
            return df
        except Exception as e:
            logging.error(f"Error in extract: {e}")
            raise

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        try:
            df['processed'] = True
            logging.info("Transformed data: added 'processed' column.")
            return df
        except Exception as e:
            logging.error(f"Error in transform: {e}")
            raise

    def load(self, df: pd.DataFrame) -> None:
        try:
            client: MongoClient = MongoClient(self.mongo_uri)
            db = client[self.mongo_db]
            collection = db[self.mongo_collection]
            records = df.to_dict(orient='records')
            if records:
                collection.insert_many(records)
                logging.info(f"Loaded {len(records)} records to MongoDB.")
            client.close()
        except Exception as e:
            logging.error(f"Error in load: {e}")
            raise

    def run_etl(self, file_content: bytes, filename: Optional[str] = None) -> None:
        if filename and self.has_processed(filename):
            logging.info(f"Skip {filename}: already processed.")
            return
        df = self.extract(file_content)
        df = self.transform(df)
        self.load(df)
        if filename:
            self.mark_processed(filename)
