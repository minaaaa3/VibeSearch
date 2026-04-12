import { SearchResponse } from "@/types";

// Vercel の API 関数（api/index.py）は自動的に /api/v1/search にマッピングされるようにします
// (vercel.json を消したので、Vercel の標準マッピングを使います)
const API_BASE_URL = "/api";

export async function searchSpots(userInput: string): Promise<SearchResponse> {
  const url = `${API_BASE_URL}/search`; // api/index.py 内の FastAPI ルーターが /search を持っている前提
  
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ user_input: userInput }),
  });

  if (!response.ok) {
    const errorText = await response.text();
    console.error(`API response was not ok: ${response.status} ${errorText.substring(0, 200)}`);
    throw new Error(`Failed to fetch search results: ${response.status}`);
  }

  return response.json();
}
