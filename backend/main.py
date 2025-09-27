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
MONGO_URI = "mongodb+srv://outfitDB:technova25@fashionkilla.mllcjg1.mongodb.net/?retryWrites=true&w=majority&appName=fashionkilla"
ALLOWED_CATEGORIES = {"top", "bottom", "dress"}
client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
db = client["outfitDB"]
clothes_collection = db["clothes"]

# model configuration
model_name = "patrickjohncyh/fashion-clip"
model = CLIPModel.from_pretrained(model_name)
processor = CLIPProcessor.from_pretrained(model_name)


from services.generate_image_service import convert_prompt_to_images
from services.recommendation_service import best_item_in_category
from services.base64_service import image_to_base64, decode_base64_image

app = FastAPI()


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


class PromptRequest(BaseModel): # string: user asks for outfit based on this scenario
    prompt: str

class ImageResponse(BaseModel): #list of images: service converts text prompt to 5 outfit inspo pics
    images: List[str] #base 64 image strings

last_generated_prompt: List[str] = [] #keep track of generated image prompt

@app.get("/")
def root():
    return {"Hello" : "World"}

@app.post("/submit_outfit_request", response_model=ImageResponse) #handles all of turning prompt into image
def generate_images(request: PromptRequest): #json input
    prompt = request.prompt
    global last_generated_prompt
    prompt_images64 = convert_prompt_to_images(prompt)
    last_generated_prompt = prompt_images64[:5]
    return {"images": last_generated_prompt}
 
@app.get("/get_image/{image_index}") #testing: to see images generated from text prompt
def get_image(image_index: int) -> str:
    global last_generated_prompt
    if 0 <= image_index < len(last_generated_prompt):
        return last_generated_prompt[image_index]
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
