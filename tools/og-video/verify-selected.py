#!/usr/bin/env python3
"""Verify the approved clip without network access. Requires ffmpeg and ffprobe."""
from pathlib import Path
import hashlib
import json
import struct
import subprocess

HERE = Path(__file__).resolve().parent
selected = json.loads((HERE / "selected.json").read_text())
asset = (HERE / selected["asset"]).resolve()
data = asset.read_bytes()
assert hashlib.sha256(data).hexdigest() == selected["sha256"], "Not the approved video"
assert len(data) == selected["bytes"] < 1_000_000
assert selected["url"].startswith("https://") and selected["url"].endswith(asset.name)
probe = json.loads(subprocess.check_output([
    "ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(asset)
]))
assert len(probe["streams"]) == 1, "Must be silent with one video stream"
video = probe["streams"][0]
assert video["codec_name"] == "h264" and video["pix_fmt"] == "yuv420p"
assert (video["width"], video["height"]) == (1200, 630)
assert video["r_frame_rate"] == "24/1"
assert 7 <= float(probe["format"]["duration"]) <= 10
# Faststart is required so an unfurler need not download the whole clip to begin.
at, atoms = 0, []
while at + 8 <= len(data):
    size, kind = struct.unpack_from(">I4s", data, at)
    if size == 1:
        size = struct.unpack_from(">Q", data, at + 8)[0]
    if size == 0:
        size = len(data) - at
    assert size >= 8 and at + size <= len(data)
    atoms.append(kind)
    at += size
assert atoms.index(b"moov") < atoms.index(b"mdat"), "MP4 must use faststart"
subprocess.run(["ffmpeg", "-v", "error", "-xerror", "-i", str(asset), "-f", "null", "-"], check=True)
print(f"PASS: {asset.name} ({len(data):,} bytes), approved SHA-256, H.264, silent, 1200x630, 24fps, faststart and full decode")
