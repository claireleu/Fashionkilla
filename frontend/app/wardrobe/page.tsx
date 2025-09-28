"use client";

import Image from "next/image";
import { useEffect, useState, ChangeEvent, FormEvent } from "react";
import ClothingCard from "../components/ClothingCard";

export interface ClosetItem {
  _id: string;
  name: string;
  category: string;
  keywords: string;
  image_base64: string;
}

export default function Wardrobe() {
  const [closet, setCloset] = useState<Record<string, ClosetItem[]>>({});
  const [showUpload, setShowUpload] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [loadingUpload, setLoadingUpload] = useState(false);

  const fetchCloset = async () => {
    try {
      const res = await fetch("/api/closet");
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

  return (
    <div className="min-h-screen bg-striped p-8 relative">
      <header className="w-full flex justify-between items-center p-6 bg-white shadow-md mb-8 rounded-lg">
        <div className="flex items-center">
          <Image
            src="/bunny-icon.png"
            alt="Bunny Icon"
            width={60}
            height={60}
          />
          <h1 className="text-2xl font-pixel ml-2">Fashionkilla Closet</h1>
        </div>
      </header>

      {/* Categories */}
      {Object.keys(closet).map((category) => (
        <div key={category} className="mb-12">
          <h2 className="text-2xl font-bold mb-4 capitalize">{category}</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            {closet[category]?.map((item) => (
              <ClothingCard key={item._id} item={item} />
            ))}
          </div>
        </div>
      ))}

      {/* Upload Modal */}
      {showUpload && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <form
            className="bg-white rounded-lg p-6 flex flex-col gap-4 w-80"
            onSubmit={handleUpload}
          >
            <h2 className="text-xl font-bold mb-2">Upload Clothing</h2>
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
        className="fixed left-1/2 bottom-5 transform -translate-x-1/2 bg-[#FFEAEC] rounded-lg shadow-lg flex flex-col items-center justify-center p-2 cursor-pointer hover:bg-[#e8d7d8] transition border-[1.5px] border-black"
        onClick={() => setShowUpload(true)}
      >
        <span className="text-4xl text-black">+</span>
        <span className="text-black text-sm">Add Item</span>
      </div>
    </div>
  );
}
