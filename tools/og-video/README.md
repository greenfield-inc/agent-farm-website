# Open Graph video

Selected: **B — Keep your terminal**. The MP4 in `../../public/og/` is the exact approved review clip; `selected.json` records its SHA-256 and public URL.

[Watch the approved selection](https://og-motion-review-parsa.sleekhen8.chatgpt.site/#farm). The review Site retains all earlier rounds and the portable renderers, assets and font licenses in its source repository (`source/round-two` and `source/round-three`, source commit `f56a530be9e9d3fd2a3c0496cf0229acfc16be30`). Superseded first-round files were removed from this PR.

## Verify

With Python 3, FFmpeg and FFprobe installed, run from this directory:

```sh
python3 verify-selected.py
```

The check verifies the exact selected bytes, a single silent H.264/yuv420p stream, dimensions, frame rate, duration, faststart and a full decode. This is an illustrative brand animation, not a recording of private app data.

## Delivery

Metadata uses an absolute HTTPS MP4 URL with secure URL, MIME type and dimensions. Page titles, descriptions, canonical URLs, website/article types, existing Open Graph images and Twitter summary-image cards stay intact. Receiving apps choose whether to animate; image-only clients continue to use the existing still.

The content-addressed filename avoids stale video caches. Replace the filename and metadata URL together when changing the clip. After deploying, verify the public URL without cookies (200 GET/HEAD, video/mp4, byte-range playback and cache headers), then test an actual message unfurl. These production/client checks cannot be completed before the app is deployed.
