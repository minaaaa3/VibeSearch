export interface Spot {
  id: string;
  name: string;
  address: string;
  image_url?: string;
  vibe_summary?: string;
  status?: string; // 営業中, 営業時間外, まもなく終了
  crowd?: string;  // 空いています, やや混雑, 混雑しています
  metadata: {
    price_range?: string;
    hours?: string;
    [key: string]: any;
  };
}

export interface SearchResponse {
  intent: {
    location: string;
    vibe: string[];
    usage: string;
  };
  recommendations: Spot[];
  log: string[];
}
