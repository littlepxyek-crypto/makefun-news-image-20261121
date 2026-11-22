#!/usr/bin/env python3
"""Copy the finished news poster into the bounty output folder.

The poster itself is prepared beforehand as ``poster.png`` next to this
file.  This program does not draw anything: it only checks that the
poster is a genuine PNG of an allowed size, copies it byte for byte to
``entry.png`` in the output folder, and then reads the copy back to
prove the two files match exactly.
"""

import hashlib
import os
import sys
from pathlib import Path

# The eight bytes every PNG file starts with.
PNG_MARK = b"\x89PNG\r\n\x1a\n"

# Bounty limits for the submitted image.
MAX_BYTES = 1024 * 1024
MAX_SIDE = 1024

SOURCE_NAME = "poster.png"
TARGET_NAME = "entry.png"
DEFAULT_OUTPUT = "/output"


def poster_next_to_program() -> Path:
    """Return the path of the poster sitting beside this program."""
    here = Path(__file__).resolve().parent
    return here / SOURCE_NAME


def read_header_size(png_bytes: bytes) -> tuple[int, int]:
    """Pull the pixel width and height out of a PNG header.

    Layout of the first bytes of a PNG: 8 signature bytes, then a
    4-byte chunk length, then the 4 letters ``IHDR``, then the width
    (4 bytes, big-endian) and the height (4 bytes, big-endian).
    """
    if len(png_bytes) < 24:
        raise ValueError("file is too short to hold a PNG header")
    width = int.from_bytes(png_bytes[16:20], "big")
    height = int.from_bytes(png_bytes[20:24], "big")
    return width, height


def check_poster(png_bytes: bytes) -> tuple[int, int]:
    """Refuse anything that is not a small, valid PNG poster."""
    if not png_bytes.startswith(PNG_MARK):
        raise ValueError("poster.png does not start with the PNG signature")
    width, height = read_header_size(png_bytes)
    if len(png_bytes) > MAX_BYTES:
        raise ValueError(
            f"poster is {len(png_bytes)} bytes, over the {MAX_BYTES} byte limit"
        )
    if width > MAX_SIDE or height > MAX_SIDE:
        raise ValueError(
            f"poster is {width}x{height}, over the {MAX_SIDE}x{MAX_SIDE} limit"
        )
    if width == 0 or height == 0:
        raise ValueError("poster has a zero width or height")
    return width, height


def choose_output_folder() -> Path:
    """Use MAKEFUN_OUTPUT_DIR when set, otherwise the default folder."""
    chosen = os.environ.get("MAKEFUN_OUTPUT_DIR") or DEFAULT_OUTPUT
    folder = Path(chosen)
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def main() -> int:
    try:
        source = poster_next_to_program()
        png_bytes = source.read_bytes()
        width, height = check_poster(png_bytes)
        folder = choose_output_folder()
        target = folder / TARGET_NAME
        target.write_bytes(png_bytes)
        written_back = target.read_bytes()
        if written_back != png_bytes:
            raise ValueError("written entry.png does not match poster.png")
    except (OSError, ValueError) as problem:
        print(f"failed: {problem}", file=sys.stderr)
        return 1
    digest = hashlib.sha256(written_back).hexdigest()
    print(f"wrote {target}")
    print(f"size: {len(written_back)} bytes")
    print(f"sha256: {digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
