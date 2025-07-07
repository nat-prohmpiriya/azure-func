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
        client: MongoClient = MongoClient(self.mongo_uri)
        db = client[self.mongo_db]
        tracking = db[self.tracking_collection_name]
        exists: bool = tracking.find_one({"filename": filename}) is not None
        client.close()
        return exists

    def mark_processed(self, filename: str) -> None:
        client: MongoClient = MongoClient(self.mongo_uri)
        db = client[self.mongo_db]
        tracking = db[self.tracking_collection_name]
        tracking.insert_one({"filename": filename})
        client.close()

    def extract(self, file_content: bytes) -> pd.DataFrame:
        df: pd.DataFrame = pd.read_csv(io.BytesIO(file_content))
        return df

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df['processed'] = True
        return df

    def load(self, df: pd.DataFrame) -> None:
        client: MongoClient = MongoClient(self.mongo_uri)
        db = client[self.mongo_db]
        collection = db[self.mongo_collection]
        records = df.to_dict(orient='records')
        if records:
            collection.insert_many(records)
        client.close()

    def run_etl(self, file_content: bytes, filename: Optional[str] = None) -> None:
        if filename and self.has_processed(filename):
            logging.info(f"Skip {filename}: already processed.")
            return
        df = self.extract(file_content)
        df = self.transform(df)
        self.load(df)
        if filename:
            self.mark_processed(filename)
