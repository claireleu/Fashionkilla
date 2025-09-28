"use client";

import Image from "next/image";
import { useState } from "react";
import { useRouter } from "next/navigation";

export default function MainPage() {
  const [inputValue, setInputValue] = useState("");
  const [responseData, setResponseData] = useState<any | null>(null);
  const [responseState, setResponseState] = useState<any | false>(false);
  const router = useRouter();

  const handleSuggestionClick = (suggestion: string) => {
    console.log(`Suggestion clicked: ${suggestion}`);
    // Placeholder function to handle suggestion click
  };

  

  const submitPrompt = async () => {
    console.log("submitting response")


    if (!inputValue.trim()) return; // ignore empty input

    setResponseState(true);

    try {
      const response = await fetch("http://localhost:8000/submit_outfit_request", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ prompt: inputValue }),
      });

      if (!response.ok) {
        throw new Error("Failed to send prompt");
      }

      const data = await response.json();
      console.log("Backend response:", data);
      setResponseData(data);

    } catch (error) {
      console.error("Error:", error);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      submitPrompt();
    }
  };


  const handleCloseResponse = () => {
    setResponseData(null);
    setResponseState(false);
    setInputValue("");
  }

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
        {/* Conditional rendering */}
        {responseData ? (
          <div className="relative w-[700px] h-[500px] bg-white flex items-center justify-center border-8 border-white rounded-lg shadow-lg">
            <button
              onClick={handleCloseResponse}
              className="absolute top-4 right-4 text-xl font-bold px-3 py-1 bg-gray-300 rounded-lg hover:bg-gray-400"
            >
              X
            </button>
            <div className="text-center">
              <h2 className="text-2xl font-bold mb-4">Outfit Suggestions</h2>
              <pre className="text-left text-sm">{JSON.stringify(responseData.outfit.top.name, null, 2)}</pre>
              <pre className="text-left text-sm">{JSON.stringify(responseData.outfit.bottom.name, null, 2)}</pre>
            </div>
          </div>
        ) : (
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
        )}

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
              onKeyPress={handleKeyPress}
              placeholder="Enter a style or event..."
              readOnly={responseState}
              className={`w-full px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-300 mb-6 text-lg ${
              responseState ? "text-gray-400 bg-gray-100 cursor-not-allowed" : "text-black bg-white"
              }`}
            />
            <button
              onClick={submitPrompt}
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
