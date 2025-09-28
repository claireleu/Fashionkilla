import { NextResponse, NextRequest } from "next/server";

export const DELETE = async (req: NextRequest) => {
  try {
    const body = await req.json();
    const { id } = body;
    if (!id)
      return NextResponse.json(
        { error: "Item ID is required" },
        { status: 400 }
      );

    const res = await fetch(`http://127.0.0.1:8000/delete?item_id=${id}`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
    });
    if (!res.ok) {
      const errorData = await res.json();
      throw new Error(errorData.detail || "Failed to delete item");
    }
    const data = await res.json();
    return NextResponse.json(data);
  } catch (err: any) {
    console.error("Delete error: ", err.message);
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
};
