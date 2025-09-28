import base64
import numpy as np
from rembg import remove
from PIL import Image
import io

def remove_bg_base64(input_base64: str, content_type: str) -> str:
    # Validate content type
    content_type = content_type.lower()
    if content_type not in ["png", "jpeg"]:
        raise ValueError("content_type must be 'png' or 'jpeg'")

    # Decode base64 to bytes
    img_bytes = base64.b64decode(input_base64)

    # Open image with PIL and ensure RGBA
    img = Image.open(io.BytesIO(img_bytes)).convert("RGBA")

    # Remove background using rembg
    result = remove(np.array(img))  # RGBA NumPy array
    result_img = Image.fromarray(result)

    # Prepare output buffer
    buffer = io.BytesIO()

    if content_type == "png":
        # Keep transparency
        result_img.save(buffer, format="PNG")
    else:
        # For JPEG: paste RGBA on white background
        background = Image.new("RGBA", result_img.size, (255, 255, 255, 255))  # white bg
        background.paste(result_img, mask=result_img.split()[3])  # use alpha as mask
        background = background.convert("RGB")  # JPEG doesn't support alpha
        background.save(buffer, format="JPEG")

    # Encode to base64
    output_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return f"data:image/{content_type};base64,{output_base64}"