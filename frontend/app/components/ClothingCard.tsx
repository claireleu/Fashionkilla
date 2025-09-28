import { useState } from "react";
import { ClosetItem } from "../wardrobe/page";
import { Trash2 } from "lucide-react";

interface ClothingCardProps {
  item: ClosetItem;
  onDelete?: (itemId: string) => void;
}

export default function ClothingCard({ item, onDelete }: ClothingCardProps) {
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);

  const handleDeleteClick = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setShowDeleteModal(true);
  };

  const handleConfirmDelete = async () => {
    try {
      setIsDeleting(true);

      const response = await fetch(`/api/delete`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ id: item._id }),
      });

      if (!response.ok) {
        throw new Error("Failed to delete item");
      }

      // Call parent callback to refresh the list
      if (onDelete) {
        onDelete(item._id);
      }

      setShowDeleteModal(false);
    } catch (error) {
      console.error("Error deleting item:", error);
      alert("Failed to delete item. Please try again.");
    } finally {
      setIsDeleting(false);
    }
  };

  const handleCancelDelete = () => {
    setShowDeleteModal(false);
  };

  return (
    <>
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
        <button
          className="flex flex-row gap-3 justify-center items-center hover:cursor-pointer group"
          onClick={handleDeleteClick}
        >
          <p className="text-lg font-semibold">{item.name}</p>
          <Trash2 className="text-red-400 w-6 h-6 group-hover:text-red-600 transition-colors" />
        </button>
      </div>

      {/* Delete Confirmation Modal */}
      {showDeleteModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 flex flex-col gap-4 w-80">
            <h2 className="text-xl font-bold mb-2">Delete Item</h2>
            <p className="text-gray-600 mb-4">
              Are you sure you want to delete "{item.name}"? This action cannot
              be undone.
            </p>

            <div className="flex justify-end gap-2">
              <button
                type="button"
                className="px-4 py-2 bg-gray-300 rounded hover:bg-gray-400 transition-colors hover:cursor-pointer"
                onClick={handleCancelDelete}
                disabled={isDeleting}
              >
                Cancel
              </button>
              <button
                type="button"
                className={`px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 transition-colors ${
                  isDeleting
                    ? "bg-red-400 cursor-not-allowed"
                    : "hover:cursor-pointer"
                }`}
                onClick={handleConfirmDelete}
                disabled={isDeleting}
              >
                {isDeleting ? "Deleting..." : "Delete"}
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
