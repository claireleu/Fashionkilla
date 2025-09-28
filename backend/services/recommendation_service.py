from sentence_transformers import SentenceTransformer, util
import base64
import torch
import copy

text_model = SentenceTransformer("all-MiniLM-L6-v2")


def recommend_best_items(
    last_generated_prompt: list, closet: dict, get_generated_image_description
):
    """
    Recommend the best matching clothing items from a user's closet based on generated outfit images.

    Computes semantic similarity between embeddings of the generated outfit images and each item's keywords.
    Returns the top-matching items per category (top, bottom, dress) with their similarity scores.
    """
    image_embeddings = []
    for img_base64 in last_generated_prompt:
        img_bytes = base64.b64decode(img_base64.split(",")[-1])
        event_description = get_generated_image_description(img_bytes)
        embedding = text_model.encode(event_description, convert_to_tensor=True)
        image_embeddings.append(embedding)

    best_items = {}
    scores_per_cat = {cat: 0.0 for cat in closet.keys()}

    for category, items_list in closet.items():
        max_score = 0
        best_item = None
        for item in items_list:
            keywords = item.get("keywords", "").strip()
            if not item.get("text_embedding") and not keywords:
                continue
            item_embedding = (
                torch.tensor(item["text_embedding"], device=text_model.device)
                if item.get("text_embedding") and len(item["text_embedding"]) > 0
                else text_model.encode(item.get("keywords", ""), convert_to_tensor=True)
            )
            max_item_score = max(
                util.cos_sim(item_embedding, img_emb).item()
                for img_emb in image_embeddings
            )
            if max_item_score > max_score:
                max_score = max_item_score
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
