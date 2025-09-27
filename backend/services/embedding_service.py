import cohere
import requests
import base64
import os

from dotenv import load_dotenv
load_dotenv()
from generate_image_service import convert_prompt_to_images

co = cohere.ClientV2(api_key=os.environ["COHERE_API_KEY"])

def get_image_embedding(base64string: str, image_format: str):
    """
    Takes an image as a base 64 string
    Returns semantic vector embedding using Cohere embed model
    """

    image_uri = f"data:image/{image_format};base64,{base64string}" #data:[<media-type>][;base64],<data>

    image_inputs = [
        {
            "content": [
                {
                    "type": "image_url",
                    "image_url": {"url": image_uri}
                }
            ]
        }
    ]
    response = co.embed(
        model="embed-v4.0",
        input_type="image",
        embedding_types=["float"],
        inputs=image_inputs #default size 1024
    )

    return response.embeddings.float[0]

def url_to_base64(url: str) -> str:
    """
    Takes a list of image URLs and returns a list of base64-encoded strings.
    """
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # ensure the request succeeded
        # Encode image content to base64
        encoded = base64.b64encode(response.content).decode("utf-8")
        print(f"Got prompt image from: {url}")
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
    
    return encoded

image64 = url_to_base64("https://i.pinimg.com/564x/ec/da/dc/ecdadce599781e96487e27c6f7ac3040.jpg")
embedding_vector = get_image_embedding(image64, "jpeg")
print(embedding_vector)
