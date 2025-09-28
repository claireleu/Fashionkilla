import { NextResponse } from "next/server";

export const GET = async () => {
  try {
    const res = await fetch("http://localhost:8000/closet");
    if (!res.ok) throw new Error("Failed to fetch closet");
    const data = await res.json();
    return NextResponse.json(data);
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
};
