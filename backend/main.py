from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from services.generate_image_service import convert_prompt_to_images

app = FastAPI()

class PromptRequest(BaseModel): # string: user asks for outfit based on this scenario
    prompt: str

class ImageResponse(BaseModel): #list of images: service converts text prompt to 5 outfit inspo pics
    images: List[str] #base 64 image strings

last_generated_prompt: List[str] = [] #keep track of generated image prompt

@app.get("/")
def root():
    return {"Hello" : "World"}

@app.post("/generate_prompt_images", response_model=ImageResponse) #handles all of turning prompt into image
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
