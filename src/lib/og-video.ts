import type { Metadata } from "next";

// Selected brand animation. Keep the filename content-addressed when replacing it.
const videoUrl = "https://getagentfarm.com/og/agent-farm-b2b3106810c2.mp4";

export const OG_VIDEO = {
  url: videoUrl,
  secureUrl: videoUrl,
  type: "video/mp4",
  width: 1200,
  height: 630,
};

// Check the descriptor against the installed Next.js metadata contract.
export const OG_VIDEOS = [OG_VIDEO] satisfies NonNullable<Metadata["openGraph"]>["videos"];
