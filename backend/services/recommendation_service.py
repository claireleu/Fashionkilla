import base64
import torch
import copy
from sentence_transformers import SentenceTransformer, util
from services.mongo_service import update_text_embedding
from pydantic import BaseModel

text_model = SentenceTransformer("all-MiniLM-L6-v2")


class PromptRequest(BaseModel):  # string: user asks for outfit based on this scenario
    prompt: str


def recommend_best_items(
    closet: dict,
    prompt: PromptRequest,
):
    """
    Recommend the best matching clothing items from a user's closet based on generated outfit images.

    Computes semantic similarity between embeddings of the generated outfit images and each item's keywords.
    Returns the top-matching items per category (top, bottom, dress) with their similarity scores.
    """
    prompt_emb = text_model.encode(prompt.prompt, convert_to_tensor=True)

    best_items = {}
    scores_per_cat = {cat: 0.0 for cat in closet.keys()}

    for category, items_list in closet.items():
        max_score = 0
        best_item = None
        for item in items_list:
            keywords = item.get("keywords", "").strip()
            if not item.get("text_embedding") and not keywords:
                continue
            if item.get("text_embedding") and len(item["text_embedding"]) > 0:
                # Use cached embedding
                item_embedding = torch.tensor(
                    item["text_embedding"], device=text_model.device
                )
            else:
                # Compute embedding from keywords
                item_embedding = text_model.encode(keywords, convert_to_tensor=True)
                # Save embedding back to DB (cache it)
                update_text_embedding(item["_id"], item_embedding.cpu().tolist())
            score = util.cos_sim(item_embedding, prompt_emb).item()
            if score > max_score:
                max_score = score
                best_item = item

        # Make a copy and remove embeddings before returning
        if best_item:
            item_copy = copy.deepcopy(best_item)
            item_copy.pop("text_embedding", None)
            best_items[category] = item_copy
            scores_per_cat[category] = max_score

    dress_score = scores_per_cat.get("dress", 0.0)
    top_score = scores_per_cat.get("top", 0.0)
    bottom_score = scores_per_cat.get("bottom", 0.0)
    avg_top_bottom = (top_score + bottom_score) / 2

    if "dress" in best_items and dress_score > avg_top_bottom:
        # Return only dress if dress score higher than average of top + bottom
        best_items = {"dress": best_items["dress"]}
    else:
        # Otherwise return top + bottom outfit
        best_items = {k: v for k, v in best_items.items() if k in ["top", "bottom"]}

    return best_items, scores_per_cat
