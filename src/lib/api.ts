import { SearchResponse } from "@/types";

// Vercel の API 関数は /api/*.py が自動的にマッピングされます
// ローカルと本番の両方で動作するように調整
const API_BASE_URL = "/api";

export async function searchSpots(userInput: string): Promise<SearchResponse> {
  // 末尾のスラッシュなしで /api/search を呼び出す
  const url = `${API_BASE_URL}/search`;
  
  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ user_input: userInput }),
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error(`API response was not ok: ${response.status} ${errorText.substring(0, 100)}`);
      throw new Error(`Failed to fetch search results: ${response.status}`);
    }

    return response.json();
  } catch (error) {
    console.error("fetch error in searchSpots:", error);
    throw error;
  }
}
