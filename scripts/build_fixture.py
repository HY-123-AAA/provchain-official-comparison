"""Build deterministic per-record archives for GitHub provenance attestation."""

from __future__ import annotations

import hashlib
import json
import shutil
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
METADATA = ROOT / "metadata"
DIST = ROOT / "dist"
FIXED_TIMESTAMP = (1980, 1, 1, 0, 0, 0)


def add_bytes(archive, name, content):
    info = zipfile.ZipInfo(name, FIXED_TIMESTAMP)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o100644 << 16
    archive.writestr(info, content)


def main():
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)
    rows = []
    for source in sorted(SRC.glob("*.txt")):
        metadata = METADATA / (source.stem + ".json")
        if not metadata.is_file():
            raise FileNotFoundError("missing metadata for %s" % source.name)
        output = DIST / (source.stem + ".zip")
        with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            add_bytes(archive, "qwen_output.txt", source.read_bytes())
            add_bytes(archive, "record.json", metadata.read_bytes())
        rows.append({
            "artifact": output.name,
            "sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
            "bytes": output.stat().st_size,
        })
    (DIST / "build_summary.json").write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(rows, indent=2))


if __name__ == "__main__":
    main()
