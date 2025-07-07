from typing import Optional
from pymongo import MongoClient
from pymongo.collection import Collection

def delete_collection(
    uri: str,
    db_name: str,
    collection_name: str
) -> Optional[bool]:
    """
    Delete a collection from MongoDB.

    Args:
        uri (str): MongoDB connection URI.
        db_name (str): Database name.
        collection_name (str): Collection name to delete.

    Returns:
        Optional[bool]: True if deleted, False if not found, None on error.
    """
    try:
        client: MongoClient = MongoClient(uri)
        db = client[db_name]
        collection: Collection = db[collection_name]
        if collection_name in db.list_collection_names():
            collection.drop()
            print(f"Collection '{collection_name}' deleted successfully.")
            return True
        else:
            print(f"Collection '{collection_name}' does not exist.")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    # Example usage
    MONGO_URI: str = "mongodb+srv://admin_aisandbox:47CA6ybdKb8Lu2xF@cluster0.j6wrw1r.mongodb.net"
    DATABASE_NAME: str = "AISandbox"
    COLLECTION_NAME: str = "card_delivery_status"

    delete_collection(MONGO_URI, DATABASE_NAME, COLLECTION_NAME)