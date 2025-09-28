import { NextResponse } from "next/server";

export const POST = async (req: Request) => {
  try {
    const formData = await req.formData();
    const file = formData.get("file") as File | null;

    if (!file) {
      return NextResponse.json({ error: "No file provided" }, { status: 400 });
    }
    /*

    const maxSize = 10 * 1024 * 1024; // 10MB limit
    if (file.size > maxSize) {
      return NextResponse.json(
        { error: "File too large (max 10MB)" },
        { status: 400 }
      );
    }

    // Optional: Check file type
    const allowedTypes = ["image/jpeg", "image/png", "image/webp", "image/gif"];
    if (!allowedTypes.includes(file.type)) {
      return NextResponse.json(
        { error: "Invalid file type. Only images allowed." },
        { status: 400 }
      );
    }
      */

    const forwardData = new FormData();
    forwardData.append("file", file, file.name);

    console.log(`Uploading file: ${file.name} (${file.size} bytes) to FastAPI`);

    const res = await fetch("http://localhost:8000/upload", {
      method: "POST",
      body: forwardData,
    });

    console.log(res)
    if (!res.ok)
      throw new Error(`Upload failed: ${res.status} ${res.statusText}`);

    const data = await res.json();
    console.log("Upload successful:", data);
    return NextResponse.json(data);
  } catch (err: any) {
    console.error("Upload error:", err.message);
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
};
