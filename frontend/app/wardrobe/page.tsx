"use client";

import Image from "next/image";
import { useEffect, useState, ChangeEvent, FormEvent } from "react";
import ClothingCard from "../components/ClothingCard";
import { Plus } from "lucide-react";

export interface ClosetItem {
  _id: string;
  name: string;
  category: string;
  keywords: string;
  created_at?: string;
  image_base64: string;
}

export default function Wardrobe() {
  const [closet, setCloset] = useState<ClosetItem[]>([]);
  const [showUpload, setShowUpload] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [loadingUpload, setLoadingUpload] = useState(false);
  const [activeTab, setActiveTab] = useState<
    "all" | "top" | "bottom" | "dress"
  >("all");

  const fetchCloset = async () => {
    try {
      const res = await fetch("/api/sorted_closet");
      const data = await res.json();
      setCloset(data);
    } catch (err) {
      console.error("Failed to fetch closet:", err);
    }
  };

  useEffect(() => {
    fetchCloset();
  }, []);

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files || e.target.files.length === 0) return;
    setSelectedFile(e.target.files[0]);
  };

  const handleUpload = async (e: FormEvent) => {
    e.preventDefault();
    if (!selectedFile) {
      alert("Please select a file");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      setLoadingUpload(true);
      const res = await fetch("/api/upload", {
        method: "POST",
        body: formData,
      });
      console.log(res);
      if (!res.ok) throw new Error("Upload failed");

      const data = await res.json();
      setShowUpload(false);
      setSelectedFile(null);
      fetchCloset(); // refresh closet
      console.log("Upload response:", data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoadingUpload(false);
    }
  };

  const filteredCloset =
    activeTab === "all"
      ? closet
      : closet.filter((item) => item.category.toLowerCase() === activeTab);

  return (
    <div className="min-h-screen bg-striped relative">
      <header className="w-full flex justify-between items-center p-6 bg-white shadow-md mb-8">
        <div className="flex items-center">
          <Image
            src="/bunny-icon.png"
            alt="Bunny Icon"
            width={60}
            height={60}
          />
          <p className="text-2xl font-pixel ml-2">Fashionkilla Closet</p>
        </div>
      </header>

      <div className="mb-6 flex items-center justify-center">
        <p className="text-black text-5xl">Total items: {closet.length}</p>
      </div>

      {/* Clothes */}
      <div className="flex justify-between">
        {["all", "top", "bottom", "dress"].map((cat) => (
          <button
            key={cat}
            className={`w-full text-3xl rounded-tl-[45px] p-5 rounded-tr-[45px] ${
              activeTab === cat
                ? "bg-white text-black"
                : "bg-white/50 text-gray-500 hover:bg-white/70"
            }`}
            onClick={() => setActiveTab(cat as typeof activeTab)}
          >
            {cat.charAt(0).toUpperCase() + cat.slice(1)}
          </button>
        ))}
      </div>

      <div
        className={`${closet.length === 0 ? "" : "bg-white min-h-screen"} p-20`}
      >
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
          {filteredCloset?.map((item) => (
            <ClothingCard
              key={item._id}
              item={item}
              onDelete={(itemId) => {
                setCloset((prev) => prev.filter((i) => i._id !== itemId));
              }}
            />
          ))}
        </div>
        {filteredCloset?.length === 0 && (
          <div className="text-center py-12 w-full h-full">
            <p className="text-gray-500 text-lg">
              This section of your closet is empty
            </p>
            <p className="text-gray-400">Add some items to get started!</p>
          </div>
        )}
      </div>

      {/* Show message if no items */}
      {closet.length === 0 && (
        <div className="text-center py-12">
          <p className="text-gray-500 text-lg">Your closet is empty</p>
          <p className="text-gray-400">Add some items to get started!</p>
        </div>
      )}

      {/* Upload Modal */}
      {showUpload && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <form
            className="bg-white rounded-lg p-6 flex flex-col gap-4 w-80"
            onSubmit={handleUpload}
          >
            <p className="text-xl font-bold mb-2">Upload Clothing</p>
            <input
              type="file"
              accept="image/*"
              onChange={handleFileChange}
              className="border p-2 rounded cursor-pointer"
            />
            <div className="flex justify-end gap-2">
              <button
                type="button"
                className="px-4 py-2 bg-gray-300 rounded hover:bg-gray-400"
                onClick={() => setShowUpload(false)}
              >
                Cancel
              </button>
              <button
                type="submit"
                className={`px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 ${
                  loadingUpload ? "bg-[#686f9c]" : "bg-blue-500"
                }`}
                disabled={loadingUpload}
              >
                {loadingUpload ? "Uploading..." : "Upload"}
              </button>
            </div>
          </form>
        </div>
      )}
      {/* Upload button */}
      <div
        className="fixed left-1/2 bottom-5 transform -translate-x-1/2 bg-[#FFEAEC] rounded-2xl shadow-xl flex flex-col items-center justify-center p-4 cursor-pointer hover:bg-[#e8d7d8] transition border-[1.5px] border-black"
        onClick={() => setShowUpload(true)}
      >
        <Plus className="text-black w-6 h-6" strokeWidth={3} />
      </div>
    </div>
  );
}
