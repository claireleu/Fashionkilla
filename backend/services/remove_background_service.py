import base64
import numpy as np
import cv2
from rembg import remove

def remove_bg_base64(input_base64: str, content_type: str) -> str:
    # Validate content type
    content_type = content_type.lower()
    if content_type not in ["png", "jpeg"]:
        raise ValueError("content_type must be 'png' or 'jpeg'")

    # Decode base64 to bytes
    img_bytes = base64.b64decode(input_base64)

    # Convert bytes to NumPy array for OpenCV
    nparr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)  # BGR or BGRA

    # Convert BGR → RGB if needed
    if img.shape[2] == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Remove background
    result = remove(img)  # returns RGBA

    # Encode result back to memory
    if content_type == "png":
        # Keep alpha channel
        result_bgra = cv2.cvtColor(result, cv2.COLOR_RGBA2BGRA)
        _, buffer = cv2.imencode(".png", result_bgra)
    else:
        # Convert RGBA → RGB for JPEG
        result_rgb = cv2.cvtColor(result, cv2.COLOR_RGBA2RGB)
        _, buffer = cv2.imencode(".jpg", result_rgb)

    # Encode to base64
    output_base64 = base64.b64encode(buffer).decode("utf-8")

    # Return data URI
    return f"data:image/{content_type};base64,{output_base64}"
