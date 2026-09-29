import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Bundle only the files needed at runtime, so the Docker image stays small
  // (see Dockerfile). Docs: node_modules/next/dist/docs/01-app/02-guides/building.md
  output: "standalone",
};

export default nextConfig;
