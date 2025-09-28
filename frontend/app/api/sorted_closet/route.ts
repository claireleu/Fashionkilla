import { NextResponse } from "next/server";

export const GET = async () => {
  try {
    const res = await fetch("http://localhost:8000/sorted_closet", {
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
    });

    if (!res.ok) {
      throw new Error(
        `Failed to fetch closet: ${res.status} ${res.statusText}`
      );
    }

    const data = await res.json();
    return NextResponse.json(data);
  } catch (err: any) {
    console.error("Get sorted closet error:", err.message);
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
};
