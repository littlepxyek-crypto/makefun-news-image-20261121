[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/littlepxyek-crypto/makefun-news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/littlepxyek-crypto/makefun-news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

# The World in One Image — Saturday, November 21, 2026

An entry for the make.fun bounty
[news-image-20261121](https://make.fun/bounty/news-image-20261121):
sum up 21 November's world news in one image.

`poster.png` is an original newspaper-style front page for **Saturday,
November 21, 2026**. It carries 51 stories — 3 lead stories, 12 illustrated
cards and a 36-story index — each checked against reporting dated that day,
plus a numbered world map, a UTC timeline, the day in numbers, and a
DATE CHECK box listing the big stories deliberately left out because they
belong to other days.

The three lead stories:

1. **Climate** — COP31 talks in Antalya deadlocked over fossil fuels:
   nearly 200 nations failed to agree a final deal after the draft dropped
   fossil-fuel phase-out language, and the talks ran into overtime.
2. **Middle East** — Bahrain said an Iranian attack set an industrial
   facility ablaze; Iran's IRGC said it targeted US positions at two bases.
3. **Ukraine** — A Russian ballistic strike on Kryvyi Rih, President
   Zelenskyy's hometown, killed two people and wounded 60.

## Run it

`main.py` is a small Python program using only the standard library. Run it
and it validates `poster.png` (whole PNG, ≤ 1 MiB, ≤ 1024×1024) and copies it
byte for byte to the output directory as `entry.png`:

```sh
python3 main.py
# writes /output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png)
```

The poster was drawn by a Python/Pillow rendering program from a verified
story file; every drawing on it is original program output, and every story
on it happened or was first reported on Saturday 21 November 2026.

## License

MIT — see `LICENSE`.
