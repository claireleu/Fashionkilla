from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from pydantic import BaseModel
from typing import List
import base64
import certifi
from fastapi.responses import JSONResponse
from pymongo import MongoClient
from bson import ObjectId
import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
import io

# configure mongodb connection
MONGO_URI = ""
ALLOWED_CATEGORIES = {"top", "bottom", "dress"}
client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
db = client["outfitDB"]
clothes_collection = db["clothes"]

# model configuration
model_name = "patrickjohncyh/fashion-clip"
model = CLIPModel.from_pretrained(model_name)
processor = CLIPProcessor.from_pretrained(model_name)


app = FastAPI()


# ****** Helper functions for db ********
def image_to_base64(file: UploadFile) -> str:
    img_bytes = file.file.read()
    base64_string = base64.b64encode(img_bytes).decode("utf-8")

    # Use the content type from the uploaded file
    content_type = file.content_type or "image/jpeg"  # fallback
    return f"data:{content_type};base64,{base64_string}"


def decode_base64_image(base64_str):
    try:
        # Remove the prefix if it exists
        if "," in base64_str:
            base64_str = base64_str.split(",")[1]

        image_data = base64.b64decode(base64_str)
        return Image.open(io.BytesIO(image_data)).convert("RGB")
    except Exception as e:
        raise ValueError(f"Error decoding base64 image: {e}")
    

def load_reference_image(base64_str):
    try:
        reference_image = decode_base64_image(base64_str)
        image_input = processor(images=reference_image, return_tensors="pt")
        reference_embedding = model.get_image_features(**image_input)
        reference_embedding = reference_embedding / reference_embedding.norm(
            p=2, dim=-1, keepdim=True
        )
        print(f"Successfully loaded reference image (base64)")
        return reference_embedding
    except Exception as e:
        raise Exception(f"Error processing reference image: {e}")


def best_item_in_category(category_items, reference_embedding, category_name):
    print(f"\n=== Evaluating {category_name} ===")

    if not category_items:
        print(f"No items in {category_name} category")
        return None, -1.0
    best_item, best_score = None, -1.0
    for item in category_items:
        try:
            image = decode_base64_image(item["image_base64"])
            image_input = processor(images=image, return_tensors="pt")
            image_embedding = model.get_image_features(**image_input)
            image_embedding = image_embedding / image_embedding.norm(
                p=2, dim=-1, keepdim=True
            )
            similarity = torch.nn.functional.cosine_similarity(
                reference_embedding, image_embedding
            )
            print(f"item {item['name']}: {similarity}")
            score = similarity.item()
            if score > best_score:
                best_score = score
                best_item = item
        except Exception as e:
            print(f"Error processing {item['name']}: {e}")
    if best_item:
        print(f"Best {category_name}: {best_item['name']} (score: {best_score:.4f})")
    else:
        print(f"No valid items found in {category_name}")
    return best_item, best_score


def serialize_item(item):
    if not item:
        return None
    return {**item, "_id": str(item["_id"])}


class PromptRequest(BaseModel):
    prompt: str


class ImageResponse(BaseModel):
    images: List[str] #image urls


last_generated_images: List[str] = []


@app.get("/")
def root():
    return {"Hello" : "World"}


@app.post("/generate_prompt_images", response_model=ImageResponse)
def generate_images(request: PromptRequest): #json body
    prompt = request.prompt
    global last_generated_images
    last_generated_images = [
        prompt for i in range(1, 6)
    ]
    return {"images": last_generated_images}


@app.get("/get_image/{image_index}")
def get_image(image_index: int) -> str: #gives url or base64
    global last_generated_images
    if 0 <= image_index < len(last_generated_images):
        return last_generated_images[image_index]
    return {"error": "Invalid index"}


# ********* DB Endpoints ***********
@app.post("/upload")
async def upload_clothing(
    name: str = Form(...),
    category: str = Form(...),  # top, bottom, dress (onesey)
    file: UploadFile = File(...),
):
    try:
        if category not in ALLOWED_CATEGORIES:
            return JSONResponse(
                status_code=400,
                content={
                    "error": f"Invalid category. Must be one of {list(ALLOWED_CATEGORIES)}"
                },
            )
        img_base64 = image_to_base64(file)
        item = {"name": name, "category": category, "image_base64": img_base64}
        clothes_collection.insert_one(item)
        return {"status": "success", "item": {"name": name, "category": category}}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


# get closet grouped by category
@app.get("/closet")
async def get_closet():
    items = list(clothes_collection.find())
    closet = {"top": [], "bottom": [], "dress": []}
    for item in items:
        item["_id"] = str(item["_id"])
        closet[item["category"]].append(item)
    return closet


# delete clothing item
@app.delete("/delete")
async def delete_clothing(item_id: str):
    try:
        print(f"Received - id: {item_id}")
        obj_id = ObjectId(item_id)
        result = clothes_collection.delete_one({"_id": obj_id})

        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Item not found")

        return {"status": "success", "deleted_count": result.deleted_count}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.post("/recommend")
async def recommend_outfit(file: UploadFile = File(...)):
    try:
        # Convert uploaded image to base64
        event_image_base64 = image_to_base64(file)

        # Load embedding
        reference_embedding = load_reference_image(event_image_base64)

        # Fetch closet from MongoDB
        items = list(clothes_collection.find())
        closet = {"top": [], "bottom": [], "dress": []}
        for item in items:
            cat = item["category"]
            if cat == "top":
                closet["top"].append(item)
            elif cat == "bottom":
                closet["bottom"].append(item)
            elif cat == "dress":
                closet["dress"].append(item)

        # Evaluate
        best_dress, dress_score = best_item_in_category(
            closet["dress"], reference_embedding, "dress"
        )
        best_top, top_score = best_item_in_category(
            closet["top"], reference_embedding, "top"
        )
        best_bottom, bottom_score = best_item_in_category(
            closet["bottom"], reference_embedding, "bottom"
        )

        # Outfit decision
        outfit = {}
        if best_dress and (dress_score > (top_score + bottom_score) / 2):
            outfit["dress"] = serialize_item(best_dress)
        else:
            if best_top:
                outfit["top"] = serialize_item(best_top)
            if best_bottom:
                outfit["bottom"] = serialize_item(best_bottom)

        return JSONResponse(
            {
                "outfit": outfit,
                "scores": {
                    "dress": dress_score,
                    "top": top_score,
                    "bottom": bottom_score,
                },
            }
        )

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
