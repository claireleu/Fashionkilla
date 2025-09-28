import { ClosetItem } from "../wardrobe/page";

interface ClothingCardProps {
  item: ClosetItem;
}

export default function ClothingCard({ item }: ClothingCardProps) {
  return (
    <div className="bg-white rounded-lg shadow-lg overflow-hidden flex flex-col items-center p-4">
      {item.image_base64 ? (
        <img
          src={item.image_base64}
          alt={item.name}
          className="rounded-lg w-full h-52 object-cover mb-4"
        />
      ) : (
        <div className="w-full h-48 bg-gray-200 flex items-center justify-center mb-4">
          No Image
        </div>
      )}
      <h3 className="text-lg font-semibold mb-2">{item.name}</h3>
    </div>
  );
}
