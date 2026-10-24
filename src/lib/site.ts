import { OG_VIDEOS } from "@/lib/og-video";
import type { Metadata } from "next";

export const siteUrl = "https://getagentfarm.com";
export const repository = "https://github.com/dcouple/agent-farm";
export const configurationUrl = `${repository}/blob/main/CONFIGURATION.md`;
export const operationsUrl = `${repository}/blob/main/docs/operations.md`;
export const sitePages = [
  "/",
  "/guide",
  "/configuration",
  "/compare",
  "/resources",
];

export function pageMetadata(
  title: string,
  description: string,
  path: string,
): Metadata {
  return {
    title: path === "/" ? `${title} | Agent Farm` : title,
    description,
    alternates: {
      canonical: path,
      types: { "text/markdown": `/raw/${path === "/" ? "index" : path.slice(1)}.md` },
    },
    openGraph: {
      videos: OG_VIDEOS,
      title: `${title} | Agent Farm`,
      description,
      url: path,
      siteName: "Agent Farm",
      type: "website",
      images: [
        {
          url: "/opengraph-image.png",
          width: 1200,
          height: 630,
          alt: "Agent Farm — Your agents. Your setup.",
        },
      ],
    },
    twitter: {
      card: "summary_large_image",
      title: `${title} | Agent Farm`,
      description,
      images: ["/opengraph-image.png"],
    },
  };
}
