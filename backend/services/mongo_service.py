import base64
import certifi
import os
from pymongo import MongoClient
from dotenv import load_dotenv
from bson import ObjectId
from services.gemini_service import extract_keywords_with_gemini
from sentence_transformers import SentenceTransformer
from datetime import datetime, timezone


text_model = SentenceTransformer("all-MiniLM-L6-v2")

load_dotenv()

MONGO_URI = os.getenv("MONGODB_CONNECTION_STR")
client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
db = client["outfitDB"]
clothes_collection = db["clothes"]

ALLOWED_CATEGORIES = {"top", "bottom", "dress"}


def insert_clothing(item: dict):
    """
    Inserts a clothing item into mongoDB collection
    """
    return clothes_collection.insert_one(item)


def delete_clothing(item_id: str):
    """
    Delete a clothing item from the collection by its ObjectId
    """
    obj_id = ObjectId(item_id)
    return clothes_collection.delete_one({"_id": obj_id})


def get_all_clothing():
    """
    Return all clothing items from the collection
    """
    items = list(clothes_collection.find())
    for item in items:
        item["_id"] = str(item["_id"])
    return items


def get_closet_grouped():
    """
    Return all clothing items grouped by category
    """
    items = get_all_clothing()
    closet = {cat: [] for cat in ALLOWED_CATEGORIES}
    for item in items:
        closet[item["category"]].append(item)
    for item in items:
        print(item["name"])
    
    return closet


def get_closet_grouped_no_embeddings():
    """
    Return all clothing items grouped by category except embedded vectors
    """
    items = get_all_clothing()
    closet = {cat: [] for cat in ALLOWED_CATEGORIES}
    for item in items:
        if "text_embedding" in item:
            del item["text_embedding"]
        closet[item["category"]].append(item)

    return closet


def serialize_item(item: dict):
    """
    Serialize a MongoDB item dictionary by converting its "_id" to a string
    """
    item["_id"] = str(item["_id"])
    return item


def create_clothing_item(file_bytes: bytes, content_type: str):
    """
    Create a new clothing item from uploaded image bytes, extract metadata using Gemini,
    and insert it into the MongoDB collection
    """
    metadata = extract_keywords_with_gemini(file_bytes)
    category = metadata.get("category")
    if category not in ALLOWED_CATEGORIES:
        category = "top"

    img_base64 = base64.b64encode(file_bytes).decode("utf-8")
    img_data_uri = f"data:{content_type or 'image/jpeg'};base64,{img_base64}"

    # cache text vector embeddings
    keywords = metadata.get("keywords", "")
    text_embedding = text_model.encode(keywords, convert_to_tensor=False)

    item = {
        "name": metadata.get("name", "Unknown"),
        "category": category,
        "keywords": metadata.get("keywords", ""),
        "text_embedding": text_embedding.tolist(),
        "created_at": datetime.now(timezone.utc),
        "image_base64": img_data_uri,
    }

    result = insert_clothing(item)
    item["_id"] = str(result.inserted_id)
    print(item["name"])
    return item


def update_text_embedding(obj_id: str, embedding: list[float]):
    """
    Update the text_embedding of a clothing item in MongoDB
    """
    # Convert torch.Tensor to list if needed
    mongo_id = ObjectId(obj_id)

    return clothes_collection.update_one(
        {"_id": mongo_id}, {"$set": {"text_embedding": embedding}}
    )


def get_sorted_time_closet():
    """
    Return all clothing items sorted by created_at time (newest first).
    Items without created_at appear last in database order
    """
    items_with_time = list(clothes_collection.find(
        {"created_at": {"$exists": True, "$ne": None}},
        {"text_embedding": 0}
    ).sort("created_at", -1))

    items_without_time = list(clothes_collection.find(
        {"$or": [
            {"created_at": {"$exists": False}},
            {"created_at": None}
        ]},
        {"text_embedding": 0}
    ))

    all_items = items_with_time + items_without_time
    for item in all_items:
        item["_id"] = str(item["_id"])
    
    return all_items
