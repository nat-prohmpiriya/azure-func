import logging
from typing import Any, List, Dict
import azure.functions as func
from config.setting import MONGODB_URI, MONGODB_DB, MONGODB_COLLECTION
from services.etl_service import ETLService

def main(myblob: func.InputStream) -> None:
    logging.info(f"Processing blob: {myblob.name}, Size: {myblob.length} bytes")
    etl_service: ETLService = ETLService(MONGODB_URI, MONGODB_DB, MONGODB_COLLECTION)
    file_content: bytes = myblob.read()
    etl_service.run_etl(file_content)
    logging.info("ETL process completed for blob trigger.")
