"use client";

import Image from "next/image";
import { useRouter } from "next/navigation";
import { useState } from "react";

interface AuthFormProps {
  buttonText: string;
  linkText: string;
  linkHref: string;
  linkDescription: string;
  buttonHref: string; // Add a prop for the button's navigation target
}

export default function AuthForm({
  buttonText,
  linkText,
  linkHref,
  linkDescription,
  buttonHref,
}: AuthFormProps) {
  const router = useRouter();
  const [passwordVisible, setPasswordVisible] = useState(false);
  const [passwordInput, setPasswordInput] = useState(""); // Track password input

  const handleButtonClick = () => {
    router.push(buttonHref); // Navigate to the specified page
  };

  const togglePasswordVisibility = () => {
    setPasswordVisible((prev) => !prev); // Toggle password visibility
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-striped">
      <div className="flex items-center justify-center mb-8">
        <Image
          src="/bunny-icon.png"
          alt="Bunny Icon"
          width={200}
          height={200}
        />
        <h1 className="text-7xl font-pixel ml-4">Fashionkilla</h1>
      </div>
      <form className="bg-white p-6 rounded-lg shadow-md w-80 justify-center">
        <div className="mb-4">
          <label className="block text-sm font-medium mb-2" htmlFor="username">
            Username
          </label>
          <input
            id="username"
            type="text"
            className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-300"
          />
        </div>
        <div className="mb-6">
          <label className="block text-sm font-medium mb-2" htmlFor="password">
            Password
          </label>
          <div className="relative">
            <input
              id="password"
              type={passwordVisible ? "text" : "password"} // Toggle between text and password
              value={passwordInput}
              onChange={(e) => setPasswordInput(e.target.value)} // Track input changes
              className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-300"
            />
            {passwordInput && ( // Show toggle button only if input is not empty
              <button
                type="button"
                onClick={togglePasswordVisibility}
                className="absolute right-2 top-2 text-sm text-gray-500 hover:text-gray-700"
              >
                {passwordVisible ? "Hide" : "Show"}
              </button>
            )}
          </div>
        </div>
        <button
          type="button"
          onClick={handleButtonClick}
          className="w-full bg-[#d4bfa3] text-white py-2 rounded-lg hover:shadow-lg transition-all hover:cursor-pointer hover:bg-[#c2b499]"
        >
          {buttonText}
        </button>
        <p className="text-sm text-center mt-4">
          {linkDescription}{" "}
          <a href={linkHref} className="text-link-blue hover:underline">
            {linkText}
          </a>
        </p>
      </form>
    </div>
  );
}
