import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /*
   * Next 16 blocks dev resources requested from an origin it does not
   * recognise, which silently stops the client bundle loading when the dev
   * server is opened on 127.0.0.1 rather than localhost — as headless browsers
   * driving screenshots tend to do.
   */
  allowedDevOrigins: ["127.0.0.1", "localhost"],
};

export default nextConfig;
