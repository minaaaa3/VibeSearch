import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async rewrites() {
    // 開発環境 (npm run dev) の時だけ 8000 番ポートにプロキシする
    if (process.env.NODE_ENV === "development") {
      return [
        {
          source: "/api/:path*",
          destination: "http://127.0.0.1:8000/api/:path*",
        },
      ];
    }
    // 本番環境 (Vercel) では Vercel 自身の api フォルダ（api/*.py）が動くため、リライトは不要
    return [];
  },
};

export default nextConfig;
