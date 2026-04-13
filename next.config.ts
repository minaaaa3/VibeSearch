import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async rewrites() {
    if (process.env.NODE_ENV === "development") {
      return [
        {
          // ローカル: /api/search -> http://127.0.0.1:8000/search
          source: "/api/:path*",
          destination: "http://127.0.0.1:8000/:path*",
        },
      ];
    }
    return [];
  },
};

export default nextConfig;
