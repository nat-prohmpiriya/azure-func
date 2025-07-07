import logging
from typing import Any, Dict
import azure.functions as func
from config.setting import MONGODB_URI, MONGODB_DB, MONGODB_COLLECTION
from services.etl_service import ETLService

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("HTTP trigger function processed a request.")
    try:
        # รับไฟล์ csv ที่ส่งมาทาง body (เช่น multipart/form-data หรือ raw bytes)
        if req.headers.get("Content-Type", "").startswith("application/json"):
            data: Dict[str, Any] = req.get_json()
            # กรณีนี้ mock: ไม่ทำ ETL จริง
            return func.HttpResponse(f"Received data: {data}", status_code=200)
        else:
            file_content: bytes = req.get_body()
            etl_service: ETLService = ETLService(MONGODB_URI, MONGODB_DB, MONGODB_COLLECTION)
            etl_service.run_etl(file_content)
            return func.HttpResponse("ETL process completed via HTTP trigger.", status_code=200)
    except ValueError:
        return func.HttpResponse("Invalid payload.", status_code=400)
    except Exception as e:
        logging.error(f"Error: {e}")
        return func.HttpResponse(f"Internal server error: {e}", status_code=500)
