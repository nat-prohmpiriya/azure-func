from typing import Optional
import os
from dotenv import load_dotenv

env_path: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', '.env.local')
load_dotenv(dotenv_path=env_path)

MONGODB_URI: str = os.getenv("MONGODB_URI", "")
MONGODB_DB: str = os.getenv("MONGODB_DB", "etl_db")
MONGODB_COLLECTION: str = os.getenv("MONGODB_COLLECTION", "card_delivery_status")