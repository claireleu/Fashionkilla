from google import genai
import json
import os

gemini_client = genai.Client(api_key="AIzaSyDBom4TCnt2QVDKavdmLP0vm846akOTgSY")
os.environ["GOOGLE_API_KEY"] = "YOUR_GEMINI_API_KEY"
gemini_client = genai.Client(api_key="AIzaSyDBom4TCnt2QVDKavdmLP0vm846akOTgSY")


def extract_keywords_with_gemini(img_bytes: bytes) -> dict:
    """Send image to Gemini and get structured clothing metadata"""
    response = gemini_client.models.generate_content(
        model="models/gemini-2.5-flash",  # note full path
        contents=[
            {
                "role": "user",
                "parts": [
                    {
                        "text": (
                            "Describe the clothing in this image and return three fields as JSON: "
                            "{keywords: keywords, category: category, name: name}. "
                            "Keywords should describe the clothing in this image and give keywords about appropriate events to wear the clothing and its design. Keep concise, returning keywords and description in 1-2 sentences. Category must be one of: top, bottom, dress. "
                            "Name is a short descriptive label."
                        )
                    },
                    {"inline_data": {"mime_type": "image/jpeg", "data": img_bytes}},
                ],
            }
        ],
    )

    raw_text = response.text.strip()

    # clean Markdown fences if Gemini wrapped JSON in ```json … ```
    if raw_text.startswith("```"):
        raw_text = raw_text.strip("`").strip()
        if raw_text.lower().startswith("json"):
            raw_text = raw_text[4:].strip()

    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        # fallback: wrap result in dict if parsing failed
        return {"keywords": raw_text, "category": None, "name": None}


def get_event_description_from_image(img_bytes: bytes) -> str:
    """
    Send an event image to Gemini and get a textual description / keywords.
    """
    response = gemini_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            {
                "role": "user",
                "parts": [
                    {
                        "text": "Describe the event in this image in 1-2 sentences, focusing on setting, theme, and clothing style. Return a concise textual description suitable for semantic matching."
                    },
                    {"inline_data": {"mime_type": "image/jpeg", "data": img_bytes}},
                ],
            }
        ],
    )
    
    return response.text.strip()
