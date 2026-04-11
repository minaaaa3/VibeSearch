import { SearchResponse } from "@/types";

// Vercel のデプロイ構成に合わせて相対パスを基本にする
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "/api/v1";

export async function searchSpots(userInput: string): Promise<SearchResponse> {
  // ブラウザでの実行時に /api/v1/search となるように、末尾のスラッシュに気をつける
  const url = `${API_BASE_URL.replace(/\/$/, "")}/search`;
  
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ user_input: userInput }),
  });

  if (!response.ok) {
    const errorText = await response.text();
    console.error(`API response was not ok: ${response.status} ${errorText}`);
    throw new Error(`Failed to fetch search results: ${response.status}`);
  }

  return response.json();
}
