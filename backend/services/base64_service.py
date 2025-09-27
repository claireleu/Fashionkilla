import base64
from fastapi import UploadFile
from PIL import Image
import io

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
    