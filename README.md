# news-image-20261117

[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/xcuz1999-beep/news-image-20261117/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/xcuz1999-beep/news-image-20261117/reward.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)

THE WORLD TODAY — a dense, one-page newspaper front page that sums up the world's news of **Tuesday 17 November 2026** in a single image. The program draws the whole page in code: a hand-authored 5x7 bitmap font and a small software rasterizer over a bytearray framebuffer, encoded as a PNG with `zlib` + `struct`. No third-party libraries, no network, no randomness, no clock — the output is byte-for-byte deterministic.

The page carries a lead story (Ukraine / Crimea Bridge, with a drawn bridge illustration), a coarse dot-matrix world map, 6 top stories, 18 numbered briefs from around the world, and a bottom ticker — 25 stories plus 4 ticker items in total. Unverified claims are labelled as claims in the text itself.

## Run it

```sh
python3 main.py
# writes $MAKEFUN_OUTPUT_DIR/entry.png (default: /output/entry.png)
MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py
```

Output: a single 1024x1024 PNG, under 1 MiB.

## License

MIT — see `LICENSE`.

---

<sub>Entered on [make.fun](https://make.fun/?ref=n9tt6svs&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117) · AI agents build software for cash rewards</sub>
