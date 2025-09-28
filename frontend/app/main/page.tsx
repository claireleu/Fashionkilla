"use client";

import Image from "next/image";
import { useState } from "react";
import { useRouter } from "next/navigation";

export default function MainPage() {
  const [inputValue, setInputValue] = useState("");
  const router = useRouter();

  const handleSuggestionClick = (suggestion: string) => {
    console.log(`Suggestion clicked: ${suggestion}`);
    // Placeholder function to handle suggestion click
  };

  const handleSubmit = () => {
    console.log(`User input submitted: ${inputValue}`);
    // Placeholder function to send inputValue to the backend
  };

  const handleViewWardrobe = () => {
    router.push("/wardrobe"); // Navigate to the wardrobe page
  };

  const handleLogout = () => {
    console.log("User logged out");
    // Placeholder function for logout logic
  };

  return (
    <div className="min-h-screen bg-striped flex flex-col items-center">
      {/* Header */}
      <header className="w-full flex justify-between items-center p-6 bg-white shadow-md">
        <div className="flex items-center">
          <Image
            src="/bunny-icon.png"
            alt="Bunny Icon"
            width={60}
            height={60}
          />
          <h1 className="text-2xl font-pixel ml-2">Fashionkilla</h1>
        </div>
        <button
          onClick={handleLogout}
          className="text-lg bg-gray-200 px-6 py-3 rounded-lg hover:bg-gray-300 hover:shadow-lg transition-all"
        >
          Log out
        </button>
      </header>

      {/* Main Content */}
      <div className="flex flex-col md:flex-row items-center justify-center mt-12 gap-12">
        {/* Avatar and Bedroom */}
        <div className="relative border-8 border-white rounded-lg shadow-lg w-[700px]">
          <Image
            src="/bedroom-background.png"
            alt="Bedroom Background"
            width={700}
            height={500}
            className="rounded-lg"
          />
          <Image
            src="/avatar.png"
            alt="Avatar"
            width={300}
            height={300}
            className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2"
          />
        </div>

        {/* Prompt Section */}
        <div className="flex flex-col items-center bg-white p-8 rounded-lg shadow-lg w-[350px]">
          <div className="w-full">
            <h2 className="text-2xl font-bold mb-6">
              What would you like to wear today?
            </h2>
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="Enter a style or event..."
              className="w-full px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-300 mb-6 text-lg"
            />
            {/* Suggestions */}
            {!inputValue && (
              <div className="flex flex-wrap gap-4 mb-6">
                {[
                  "streetwear",
                  "y2k",
                  "business casual",
                  "acubi",
                  "coquette",
                ].map((suggestion) => (
                  <button
                    key={suggestion}
                    onClick={() => handleSuggestionClick(suggestion)}
                    className="px-6 py-3 bg-gray-200 rounded-lg hover:bg-pink-200 hover:shadow-lg transition-all text-lg"
                  >
                    {suggestion}
                  </button>
                ))}
              </div>
            )}
            <button
              onClick={handleSubmit}
              className="w-full bg-beige text-white py-3 rounded-lg hover:bg-beige-dark hover:shadow-lg transition-all text-lg"
            >
              Submit
            </button>
          </div>
          <button
            onClick={handleViewWardrobe}
            className="mt-6 w-full bg-beige text-white py-3 rounded-lg hover:bg-beige-dark hover:shadow-lg transition-all text-lg"
          >
            <Image
              src="/hanger-icon.png"
              alt="Hanger Icon"
              width={30}
              height={30}
              className="mr-2 inline"
            />
            View Wardrobe
          </button>
        </div>
      </div>
    </div>
  );
}
