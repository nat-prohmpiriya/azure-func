import logging
from typing import List
from azure.storage.blob import BlobServiceClient
from config.setting import MONGODB_URI, MONGODB_DB, MONGODB_COLLECTION
from services.etl_service import ETLService
import os

def main(mytimer) -> None:
    logging.info("Timer trigger function started.")
    storage_conn_str: str = os.getenv("AzureWebJobsStorage", "")
    container_name: str = os.getenv("BLOB_CONTAINER", "card-delivery-status")
    etl_service: ETLService = ETLService(MONGODB_URI, MONGODB_DB, MONGODB_COLLECTION)

    try:
        blob_service_client = BlobServiceClient.from_connection_string(storage_conn_str)
        container_client = blob_service_client.get_container_client(container_name)
        blob_list: List = list(container_client.list_blobs())
        logging.info(f"Found {len(blob_list)} blobs in container '{container_name}'")
    except Exception as e:
        logging.error(f"Error connecting to storage or listing blobs: {e}")
        return

    success_count: int = 0
    fail_count: int = 0

    for blob in blob_list:
        try:
            blob_client = container_client.get_blob_client(blob)
            file_content: bytes = blob_client.download_blob().readall()
            etl_service.run_etl(file_content, filename=blob.name)
            logging.info(f"ETL process completed for blob: {blob.name}")
            success_count += 1
        except Exception as e:
            logging.error(f"Error processing blob {blob.name}: {e}")
            fail_count += 1

    logging.info(f"ETL process completed via timer trigger. Success: {success_count}, Fail: {fail_count}")