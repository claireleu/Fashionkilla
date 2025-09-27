import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
import io
from services.generate_image_service import decode_base64_image
model = CLIPModel.from_pretrained("patrickjohncyh/fashion-clip")
processor = CLIPProcessor.from_pretrained("patrickjohncyh/fashion-clip")


def best_item_in_category(category_items, reference_embedding, category_name):
    print(f"\n=== Evaluating {category_name} ===")

    if not category_items:
        print(f"No items in {category_name} category")
        return None, -1.0
    best_item, best_score = None, -1.0
    for item in category_items:
        try:
            image = decode_base64_image(item["image_base64"])
            image_input = processor(images=image, return_tensors="pt")
            image_embedding = model.get_image_features(**image_input)
            image_embedding = image_embedding / image_embedding.norm(
                p=2, dim=-1, keepdim=True
            )
            similarity = torch.nn.functional.cosine_similarity(
                reference_embedding, image_embedding
            )
            print(f"item {item['name']}: {similarity}")
            score = similarity.item()
            if score > best_score:
                best_score = score
                best_item = item
        except Exception as e:
            print(f"Error processing {item['name']}: {e}")
    if best_item:
        print(f"Best {category_name}: {best_item['name']} (score: {best_score:.4f})")
    else:
        print(f"No valid items found in {category_name}")
    return best_item, best_score

    