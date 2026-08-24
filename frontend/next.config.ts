import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  images: {
    remotePatterns: [
      // Cloudflare R2 public bucket URLs
      { protocol: "https", hostname: "*.r2.dev" },
      { protocol: "https", hostname: "*.r2.cloudflarestorage.com" },
      // Backblaze B2 public/presigned URLs
      { protocol: "https", hostname: "*.backblazeb2.com" },
      { protocol: "https", hostname: "f001.backblazeb2.com" },
      { protocol: "https", hostname: "f002.backblazeb2.com" },
      { protocol: "https", hostname: "f003.backblazeb2.com" },
      { protocol: "https", hostname: "f004.backblazeb2.com" },
      { protocol: "https", hostname: "s3.us-west-004.backblazeb2.com" },
    ],
  },
};

export default nextConfig;
