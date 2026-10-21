#!/usr/bin/env python3
"""Validate the public metadata without credentials, network or device access."""
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
VERSION = re.compile(r"v(?:0|[1-9][0-9]{0,5})\.(?:0|[1-9][0-9]{0,5})\.(?:0|[1-9][0-9]{0,5})(?:-(?:alpha|beta|rc)\.[1-9][0-9]{0,5})?\Z")


def unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate key: " + key)
        result[key] = value
    return result


def main():
    data = (ROOT / "firmware/followcore-can/update-catalog.json").read_bytes()
    if not 0 < len(data) <= 4096 or any(b > 126 or b < 32 and b not in (9, 10, 13) for b in data):
        raise ValueError("Catalog must be bounded ASCII JSON")
    catalog = json.loads(data, object_pairs_hook=unique)
    for key, value in {"schema": 1, "product": "FollowCore", "variant": "FollowCore-CAN",
                       "control_type": "CAN", "controller_hardware": "ESP-V3.003"}.items():
        if catalog.get(key) != value:
            raise ValueError("Wrong catalog identity: " + key)
    for channel in ("stable", "testing"):
        entries = catalog[channel]
        if entries is None:
            continue
        for component in ("s3", "f303"):
            entry = entries[component]
            if entry is None:
                continue
            version, notes = entry["version"], entry["notes"]
            if not VERSION.fullmatch(version) or len(version) > 25 or not isinstance(notes, str) or \
                    len(notes) > 96 or any(ord(c) < 32 or ord(c) > 126 for c in notes):
                raise ValueError("Invalid component metadata")
            if channel == "stable" and "-" in version:
                raise ValueError("A prerelease is not a stable release")
            manifest = json.loads((ROOT / "firmware/followcore-can/releases" / version / "release-manifest.json").read_text())
            if manifest["components"][component]["version"] != version:
                raise ValueError("Component release does not match catalog")
            if "image_bytes" in entry or "sha256" in entry:
                size, digest = entry.get("image_bytes"), entry.get("sha256")
                if type(size) is not int or not 8192 <= size <= 4194304 or size % 4096 or \
                        not isinstance(digest,str) or not re.fullmatch(r"[0-9a-f]{64}",digest):
                    raise ValueError("Invalid signed artifact metadata")
                actual=manifest["components"][component]
                if size!=actual["image_bytes"] or digest!=actual["image_sha256"]:
                    raise ValueError("Catalog artifact differs from immutable release")
    print("Catalog identity, bounds, channels and local release references validated")


if __name__ == "__main__":
    main()
