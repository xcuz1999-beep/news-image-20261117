# THE WORLD TODAY — 17 November 2026

A make.fun entry for **news-image-20261117**: "Sum up 17 November's world news in one image."

The program draws a dense, one-page newspaper front page — **THE WORLD TODAY**,
dated **Tuesday 17 November 2026** — entirely in code: a hand-authored 5x7 bitmap
font and a small software rasterizer over a bytearray framebuffer, encoded as a
PNG with `zlib` + `struct`. No third-party libraries, no network, no randomness,
no clock — the output is byte-for-byte deterministic.

The page carries a lead story (Ukraine / Crimea Bridge, with a drawn bridge
illustration), a coarse dot-matrix world map, 6 top stories, 18 numbered briefs
from around the world, and a bottom ticker — 25 stories plus 4 ticker items in
total. Unverified claims are labelled as claims in the text itself.

## Run it

```sh
python3 main.py
# writes $MAKEFUN_OUTPUT_DIR/entry.png (default: /output/entry.png)
MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py
```

Output: a single 1024x1024 PNG, under 1 MiB.

## License

MIT — see `LICENSE`.
