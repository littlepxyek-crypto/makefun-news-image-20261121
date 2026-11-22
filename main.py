#!/usr/bin/env python3
"""Deliver the finished news poster as this entry's output image.

The artwork is prepared ahead of time and stored beside this program as
``poster.png``.  Running the program validates that the poster is a
whole, well-formed PNG inside the bounty limits, then copies it byte
for byte to ``entry.png`` in the output folder and reads the copy back
to prove the bytes survived the trip unchanged.

Only the Python standard library is used, and nothing here touches the
network, so two runs always produce exactly the same output bytes.
"""

import hashlib
import os
import struct
import sys
import zlib
from pathlib import Path

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_FILE_BYTES = 1024 * 1024  # bounty cap: 1 MiB
MAX_SIDE_PIXELS = 1024        # bounty cap: 1024 x 1024

POSTER_NAME = "poster.png"
ENTRY_NAME = "entry.png"
FALLBACK_OUTPUT_DIR = "/output"


def iter_chunks(data: bytes):
    """Yield (kind, payload) for each PNG chunk after the signature.

    A chunk is a 4-byte length, a 4-byte kind, ``length`` payload bytes
    and a 4-byte CRC.  The CRC is checked here so a truncated or corrupt
    poster is refused instead of delivered.
    """
    pos = len(PNG_SIGNATURE)
    while pos < len(data):
        if pos + 8 > len(data):
            raise ValueError("chunk header runs past the end of the file")
        (length,) = struct.unpack(">I", data[pos:pos + 4])
        kind = data[pos + 4:pos + 8]
        end = pos + 8 + length
        if end + 4 > len(data):
            raise ValueError(f"chunk {kind!r} runs past the end of the file")
        payload = data[pos + 8:end]
        (stored_crc,) = struct.unpack(">I", data[end:end + 4])
        if zlib.crc32(kind + payload) & 0xFFFFFFFF != stored_crc:
            raise ValueError(f"chunk {kind!r} has a bad checksum")
        yield kind, payload
        pos = end + 4


def validate_poster(data: bytes) -> tuple[int, int]:
    """Check the poster against every bounty rule; return (width, height)."""
    if len(data) > MAX_FILE_BYTES:
        raise ValueError(f"poster is {len(data)} bytes; the limit is {MAX_FILE_BYTES}")
    if not data.startswith(PNG_SIGNATURE):
        raise ValueError("poster does not start with the PNG signature")
    kinds = []
    width = height = 0
    for kind, payload in iter_chunks(data):
        kinds.append(kind)
        if kind == b"IHDR":
            width, height = struct.unpack(">II", payload[:8])
    if not kinds or kinds[0] != b"IHDR":
        raise ValueError("the first chunk is not the IHDR header")
    if kinds[-1] != b"IEND":
        raise ValueError("the last chunk is not IEND; the PNG is incomplete")
    if width == 0 or height == 0:
        raise ValueError("poster reports a zero width or height")
    if width > MAX_SIDE_PIXELS or height > MAX_SIDE_PIXELS:
        raise ValueError(
            f"poster is {width}x{height}; the limit is {MAX_SIDE_PIXELS}x{MAX_SIDE_PIXELS}"
        )
    return width, height


def output_folder() -> Path:
    """MAKEFUN_OUTPUT_DIR wins; otherwise the bounty default /output."""
    folder = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or FALLBACK_OUTPUT_DIR)
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def deliver() -> tuple[Path, int, int]:
    """Validate the poster beside this program and copy it to the output.

    Returns the written path and the poster's (width, height).
    """
    poster_path = Path(__file__).resolve().parent / POSTER_NAME
    data = poster_path.read_bytes()
    width, height = validate_poster(data)
    target = output_folder() / ENTRY_NAME
    target.write_bytes(data)
    if target.read_bytes() != data:
        raise ValueError("the written entry.png differs from poster.png")
    return target, width, height


def main() -> int:
    try:
        target, width, height = deliver()
    except (OSError, ValueError) as problem:
        print(f"failed: {problem}", file=sys.stderr)
        return 1
    data = target.read_bytes()
    print(f"wrote {target}")
    print(f"image: {width}x{height} pixels")
    print(f"size: {len(data)} bytes")
    print(f"sha256: {hashlib.sha256(data).hexdigest()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
