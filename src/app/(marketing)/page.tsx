import Image from "next/image";
import imageAssets from "@/components/landing/image-assets.json";
import Link from "next/link";
import { ArrowDown, ArrowRight, ArrowUpRight } from "lucide-react";
import { FieldLines } from "@/components/landing/artwork";
import { GardenMotion } from "@/components/landing/garden-motion";
import {
  CopyButton,
  ScrollReveals,
  TerminalDemo,
} from "@/components/landing/interactions";
import { CodeBlock } from "@/components/landing/code-block";

import { SiteHeader, SiteFooter } from "@/components/site-chrome";
import { pageMetadata, siteUrl } from "@/lib/site";

export const metadata = pageMetadata(
  "Harness Configurator for Claude Code & Codex",
  "Save profiles with the right models, skills, and project tools. Launch Claude Code or Codex in your native terminal with Agent Farm.",
  "/",
);

const repository = "https://github.com/dcouple/agent-farm";

const install = "npm install -g @greenfieldco/agent-farm";
const blocks = [
  ["Profile", "a saved setup"],
  ["Agent", "the worker"],
  ["Skill", "the playbook"],
  ["Workspace", "the tools"],
];

export default function Home() {
  return (
    <>
      <a className="skip-link" href="#main">
        Skip to content
      </a>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",
            "@type": "SoftwareApplication",
            name: "Agent Farm",
            url: siteUrl,
            image: `${siteUrl}/opengraph-image.png`,
            description:
              "Save agent profiles, shared skills, and workspace connections. Launch Claude Code or Codex in your native terminal.",
            applicationCategory: "DeveloperApplication",
            operatingSystem: "macOS, Linux",
            isAccessibleForFree: true,
            sameAs: [repository],
            author: {
              "@type": "Person",
              name: "dcouple",
              url: "https://github.com/dcouple",
            },
          }).replace(/</g, "\\u003c"),
        }}
      />
      <ScrollReveals />
      <div className="hero-shell">
        <SiteHeader home />
        <main id="main">
          <section className="hero container" aria-labelledby="hero-title">
            <div className="hero-copy">
              <a href={repository} className="open-source-badge">
                <span aria-hidden="true" /> Open source
                <ArrowUpRight size={13} aria-hidden="true" />
              </a>
              <h1 id="hero-title">
                Your agents.
                <br />
                Your setup.
              </h1>
              <p className="hero-description">
                Switch setups for Claude Code and Codex.
                <br className="desktop-break" /> Save a profile, pick it, launch
                in your native terminal.
              </p>
              <div className="hero-actions">
                <a href="#get-started" className="button button-primary">
                  Get started <ArrowRight size={19} aria-hidden="true" />
                </a>
                <a href={repository} className="button button-outline">
                  View on GitHub <ArrowUpRight size={18} aria-hidden="true" />
                </a>
              </div>
              <div className="hero-command">
                <span className="command-label">After installation</span>
                <div className="command-line">
                  <code>
                    <span aria-hidden="true">$ </span>agent-farm init
                  </code>
                  <CopyButton
                    text="agent-farm init"
                    label="Copy agent-farm init"
                  />
                </div>
              </div>
              <a className="text-link hero-explore" href="#how-it-works">
                Meet the building blocks{" "}
                <ArrowDown size={15} aria-hidden="true" />
              </a>
            </div>
            <div className="workbench">
              <div className="workbench-scene">
                <picture className="select-none">
                  <source
                    media="(max-width: 760px)"
                    srcSet={imageAssets.workbench[768].src}
                  />
                  <Image
                    src={imageAssets.workbench[1254].src}
                    alt="A cozy pixel-art workbench: four setup cards connect to a cream terminal, framed by plants, books, and a sleeping cat."
                    fill
                    sizes="(max-width: 760px) 100vw, (max-width: 1100px) 54vw, 700px"
                    loading="eager"
                    fetchPriority="high"
                    className="workbench-background select-none"
                    draggable={false}
                  />
                </picture>
                <GardenMotion />
                <div
                  className="mobile-screen-text select-none"
                  aria-hidden="true"
                >
                  <span>$ agent-farm</span>
                  <span>› planner</span>
                  <span> implementer</span>
                  <span> reviewer</span>
                </div>
              </div>
              <TerminalDemo />
            </div>
          </section>
          <section
            id="how-it-works"
            className="section paper-section"
            aria-labelledby="blocks-title"
          >
            <div className="container" data-reveal>
              <p className="eyebrow">01 / Overview</p>
              <h2 id="blocks-title">Your setup, in one place.</h2>
              <div className="shed-layout">
                <picture className="select-none">
                  <source
                    media="(max-width: 760px)"
                    srcSet={imageAssets.configuration[768].src}
                  />
                  <Image
                    src={imageAssets.configuration[1400].src}
                    alt="A pixel-art farm shed with four compartments: profile cards, robot agents, skill books, and workspace toolboxes."
                    width={1774}
                    height={887}
                    sizes="(max-width: 760px) 100vw, 65vw"
                    className="shed-art select-none"
                    draggable={false}
                  />
                </picture>
                <dl className="setup-definitions">
                  {blocks.map(([name, description]) => (
                    <div key={name}>
                      <dt>{name}</dt>
                      <dd>— {description}</dd>
                    </div>
                  ))}
                </dl>
              </div>
            </div>
          </section>
          <section
            id="get-started"
            className="section session-section"
            aria-labelledby="session-title"
          >
            <FieldLines className="session-lines" />
            <div className="container session-layout" data-reveal>
              <div className="session-copy">
                <p className="eyebrow">02 / Get started</p>
                <h2 id="session-title">From setup to session.</h2>
                <p>
                  Save a profile. Point it at your repo. Launch Claude Code or
                  Codex.
                </p>
              </div>
              <div className="session-commands">
                <CodeBlock code={install} title="Install" />
                <CodeBlock code="agent-farm init" title="Set up once" />
                <CodeBlock
                  code="agent-farm run greenfield/orchestrator"
                  title="Start with the orchestrator"
                />
                <p className="session-note">
                  Requires Node.js 22.15+, macOS or Linux, and an authenticated
                  Claude Code or Codex CLI.{" "}
                  <Link href="/docs/getting-started" className="text-link">
                    Get started guide <ArrowRight size={14} aria-hidden="true" />
                  </Link>
                </p>
              </div>
            </div>
          </section>
        </main>
      </div>
      <SiteFooter />
    </>
  );
}
