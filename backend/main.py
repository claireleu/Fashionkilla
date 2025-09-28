from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sentence_transformers import SentenceTransformer
from services.generate_image_service import convert_prompt_to_images
from services.mongo_service import (
    delete_clothing,
    get_closet_grouped,
    get_closet_grouped_no_embeddings,
    serialize_item,
    create_clothing_item,
    get_image_by_id,
    get_sorted_time_closet
)
from services.recommendation_service import recommend_best_items
from services.gemini_service import (
    get_generated_image_description,
)


# model configuration
text_model = SentenceTransformer("all-MiniLM-L6-v2")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PromptRequest(BaseModel):  # string: user asks for outfit based on this scenario
    prompt: str


class ImageResponse(
    BaseModel
):  # list of images: service converts text prompt to 5 outfit inspo pics
    images: List[str]  # base 64 image strings


last_generated_prompt: List[str] = []  # keep track of generated image prompt


@app.get("/")
def root():
    return {"Hello": "World"}


# handles all of turning prompt into image
@app.post("/submit_outfit_request")
def submit_outfit_request(prompt: PromptRequest):
    global last_generated_prompt
    last_generated_prompt = convert_prompt_to_images(prompt.prompt)[:5]
    closet = get_closet_grouped()
    # calculate best matching clothing for each category
    best_items, scores = recommend_best_items(
        last_generated_prompt, closet, get_generated_image_description, prompt
    )
    return JSONResponse({"outfit": best_items, "scores": scores})


@app.get(
    "/get_image/{image_index}"
)  # testing: to see images generated from text prompt
def get_image(image_index: int) -> str:
    global last_generated_prompt
    if 0 <= image_index < len(last_generated_prompt):
        return last_generated_prompt[image_index]
    return {"error": "Invalid index"}


# ********* DB Endpoints ***********
@app.post("/upload")
async def upload_outfit(
    file: UploadFile = File(...),
):
    try:
        file.file.seek(0)
        img_bytes = await file.read()
        item = create_clothing_item(img_bytes, file.content_type)
        return {"status": "success", "item": serialize_item(item)}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


# get closet grouped by category
@app.get("/closet")
async def get_closet():
    return get_closet_grouped_no_embeddings()


@app.get("/sorted_closet")
async def get_sorted_closet():
    return get_sorted_time_closet()


# delete clothing item
@app.delete("/delete")
async def delete_outfit(item_id: str):
    try:
        print(f"Received - id: {item_id}")
        result = delete_clothing(item_id)

        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Item not found")

        return {"status": "success", "deleted_count": result.deleted_count}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# get image by id
@app.get("/get_item_image/{item_id}")
async def getting_image_by_id(item_id: str):
    image_base64 = get_image_by_id(item_id)
    if image_base64 is None:
        raise HTTPException(status_code=404, detail="Image not found")
    return {"image_base64": image_base64}
