from sentence_transformers import SentenceTransformer, util
import base64


text_model = SentenceTransformer("all-MiniLM-L6-v2")


def recommend_best_items(
    last_generated_prompt: list, closet: dict, get_event_description_from_image
):
    """ """
    image_embeddings = []
    for img_base64 in last_generated_prompt:
        img_bytes = base64.b64decode(img_base64.split(",")[-1])
        event_description = get_event_description_from_image(img_bytes)
        embedding = text_model.encode(event_description, convert_to_tensor=True)
        image_embeddings.append((embedding, event_description))

    best_items = {}
    scores_per_cat = {cat: 0.0 for cat in closet.keys()}

    for category, items_list in closet.items():
        max_score = 0
        best_item = None
        for item in items_list:
            item_embedding = text_model.encode(
                item.get("keywords", ""), convert_to_tensor=True
            )
            max_item_score = max(
                util.cos_sim(item_embedding, img_emb[0]).item()
                for img_emb in image_embeddings
            )
            if max_item_score > max_score:
                max_score = max_item_score
                best_item = item
        if best_item:
            best_items[category] = best_item
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
