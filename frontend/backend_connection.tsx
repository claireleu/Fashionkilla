/*
'use client';

import Image from "next/image";
import { useState } from "react";

export default function Home() {
  const [inputValue, setInputValue] = useState("");

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(e.target.value);
  };

  const handleKeyPress = async (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && inputValue.trim() !== "") {
      try {
        const response = await fetch("http://localhost:8000/submit_outfit_request", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({prompt: inputValue}),
        });

        if (!response.ok) {
          throw new Error("Failed to send prompt");
        }

        const data = await response.json();
        console.log("Backend response:", data);
  
      } catch (error) {
        console.error("Error:", error);
      }
    }
  };

  const handleSuggestionClick = (suggestion: string) => {
    // TODO: Add functionality for suggestion buttons
    console.log('Suggestion clicked:', suggestion);
  };

  const handleWardrobeClick = () => {
    // TODO: Add functionality for wardrobe button
    console.log('View wardrobe clicked');
  };

  return (
    <div className="min-h-screen">
      {/* Header */ /*
      <header className="bg-white border-b-2 border-black px-4 py-3 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Image
            src="/logo.svg"
            alt="Fashionkilla Logo"
            width={32}
            height={32}
            className="image-rendering-pixelated"
          />
          <span className="pixel-text text-black text-lg">Fashionkilla</span>
        </div>
        <button className="pixel-button">
          <div className="flex flex-col gap-1">
            <div className="w-4 h-0.5 bg-black"></div>
            <div className="w-4 h-0.5 bg-black"></div>
            <div className="w-4 h-0.5 bg-black"></div>
          </div>
        </button>
      </header>

      {/* Main Content */ /*
      <main className="flex justify-center items-center min-h-[calc(100vh-80px)] p-8">
        <div className="flex gap-8 max-w-6xl w-full">
          {/* Left Card - Avatar and Bedroom Scene */ /*
          <div className="bg-white border-2 border-black rounded-lg p-6 flex-1 max-w-md">
            <div className="relative">
              {/* Bedroom Background */ /*
              <Image
                src="/bedroom-background.svg"
                alt="Bedroom Background"
                width={400}
                height={300}
                className="w-full h-auto image-rendering-pixelated"
              />
              
              {/* Avatar */ /*
              <div className="absolute top-4 left-4">
                <Image
                  src="/avatar.svg"
                  alt="Avatar"
                  width={120}
                  height={120}
                  className="image-rendering-pixelated"
                />
              </div>
            </div>
          </div>

          {/* Right Card - Input and Suggestions */ /*
          <div className="bg-white border-2 border-black rounded-lg p-6 flex-1 max-w-md">
            <div className="space-y-4">
              <h2 className="pixel-text text-black text-sm">
                What would you like to wear today?
              </h2>
              
              <input
                type="text"
                value={inputValue}
                onChange={handleInputChange}
                onKeyPress={handleKeyPress}
                className="pixel-input w-full"
                placeholder="Type your outfit request..."
              />
              
              <div className="space-y-2">
                <p className="pixel-text text-black text-xs">Suggestions</p>
                <div className="grid grid-cols-2 gap-2">
                  <button
                    onClick={() => handleSuggestionClick('streetwear')}
                    className="pixel-button text-xs"
                  >
                    streetwear
                  </button>
                  <button
                    onClick={() => handleSuggestionClick('y2k')}
                    className="pixel-button text-xs"
                  >
                    y2k
                  </button>
                  <button
                    onClick={() => handleSuggestionClick('business casual')}
                    className="pixel-button text-xs"
                  >
                    business casual
                  </button>
                  <button
                    onClick={() => handleSuggestionClick('acubi')}
                    className="pixel-button text-xs"
                  >
                    acubi
                  </button>
                  <button
                    onClick={() => handleSuggestionClick('coquette')}
                    className="pixel-button text-xs col-span-2"
                  >
                    coquette
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* View Wardrobe Button */ /*
      <div className="absolute bottom-8 right-8">
        <button
          onClick={handleWardrobeClick}
          className="pixel-button flex items-center gap-2 bg-white"
        >
          <Image
            src="/hanger.svg"
            alt="Clothing Hanger"
            width={16}
            height={16}
            className="image-rendering-pixelated"
          />
          <span className="pixel-text text-xs">View wardrobe</span>
        </button>
      </div>
    </div>
  );
}

*/