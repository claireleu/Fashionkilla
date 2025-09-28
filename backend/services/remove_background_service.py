import base64
import numpy as np
import cv2
from rembg import remove

def remove_bg_base64(input_base64: str) -> str:
    # Decode base64 string to bytes
    img_bytes = base64.b64decode(input_base64)
    
    # Convert bytes to NumPy array for OpenCV
    nparr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)  # Can read RGB or RGBA
    
    # Remove background
    result = remove(img)  # returns NumPy array (H, W, 4)
    
    # Encode result back to PNG in memory
    _, buffer = cv2.imencode(".png", result)
    output_base64 = base64.b64encode(buffer).decode("utf-8")
    
    return output_base64
