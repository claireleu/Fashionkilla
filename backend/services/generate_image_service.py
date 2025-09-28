import requests
from dotenv import load_dotenv
import os
import base64
from typing import List

load_dotenv()

# Replace with your own API key and Custom Search Engine ID
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")


def get_urls(prompt: str, num_images: int = 5) -> List[str]:
    """
    Query Google Programmable Search API to get top image URLs for a prompt.

    Args:
        prompt (str): The search query, e.g., "dinner formal wear"
        num_images (int): Number of image URLs to return (default 5)

    Returns:
        List[str]: List of image URLs
    """
    url = "https://www.googleapis.com/customsearch/v1"

    pinterest_query = f"{prompt} site:pinterest.com"

    params = {
        "key": GOOGLE_API_KEY,
        "cx": SEARCH_ENGINE_ID,
        "q": pinterest_query,
        "searchType": "image",  # ensures images are returned
        "num": num_images,
    }

    response = requests.get(url, params=params)

    # Raise error if request failed
    response.raise_for_status()

    data = response.json()
    items = data.get("items", [])

    # Extract the 'link' field which is the direct image URL
    image_urls = [item["link"] for item in items]

    return image_urls


def get_images_as_base64(urls: List[str]) -> List[str]:
    """
    Takes a list of image URLs and returns a list of base64-encoded strings.
    """
    base64_images = []

    for url in urls:
        try:
            response = requests.get(url)
            response.raise_for_status()  # ensure the request succeeded
            # Encode image content to base64
            encoded = base64.b64encode(response.content).decode("utf-8")
            base64_images.append(encoded)
            print(f"Got prompt image from: {url}")
        except Exception as e:
            print(f"Failed to fetch {url}: {e}")

    return base64_images


def convert_prompt_to_images(prompt: str, num_images: int = 5) -> List[str]:
    list_urls = get_urls(prompt, num_images)
    list_base64 = get_images_as_base64(list_urls)
    return list_base64


"""""
 test_prompt = "dinner formal wear male"
    image_urls = get_top_images(test_prompt)
    print(f"Top images for '{test_prompt}':")
    for i, url in enumerate(image_urls):
        print(f"{i+1}: {url}")
""" ""
# --- For testing the service locally ---
if __name__ == "__main__":
    test_prompt = "winter outfit acubi"
    convert_prompt_to_images(test_prompt)
    # image_urls = ["https://i.pinimg.com/564x/ec/da/dc/ecdadce599781e96487e27c6f7ac3040.jpg", "https://i.pinimg.com/564x/ec/da/dc/ecdadce599781e96487e27c6f7ac3040.jpg"]
