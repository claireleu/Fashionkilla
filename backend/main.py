from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

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
