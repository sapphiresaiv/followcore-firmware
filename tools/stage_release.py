#!/usr/bin/env python3
"""Stage only allowlisted public assets; never copy a private source tree."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
REPO = "sapphiresaiv/followcore-firmware"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def archive(path, entries):
    with zipfile.ZipFile(path, "x", zipfile.ZIP_DEFLATED) as out:
        for source, name in entries:
            if not source.is_file() or source.is_symlink():
                raise ValueError("Missing or unsafe asset: " + name)
            info = zipfile.ZipInfo(name, (2026, 10, 20, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            out.writestr(info, source.read_bytes())


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--version", required=True)
    p.add_argument("--s3", type=Path, required=True, help="Private S3 project directory")
    p.add_argument("--driver", type=Path, required=True, help="Private F303 project directory")
    p.add_argument("--s3-web", type=Path, required=True)
    p.add_argument("--validation", type=Path, required=True, help="Reviewed public validation JSON; never infer PASS from a build")
    args = p.parse_args()
    version = args.version
    import re
    if not re.fullmatch(r"v\d+\.\d+\.\d+-rc\.\d+", version):
        raise ValueError("This tool publishes candidate versions only")
    validation = json.loads(args.validation.read_text())
    if validation.get("version") != version or validation.get("variant") != "FollowCore-CAN":
        raise ValueError("Validation record does not belong to this candidate")
    out = ROOT / ".build" / version
    out.mkdir(parents=True, exist_ok=False)
    tag = "followcore-can-" + version
    prefix = "https://github.com/" + REPO + "/releases/download/" + tag + "/"
    components = {}
    for component, project, image_name in (
        ("s3", args.s3, f"followcore-can-s3-{version}-ota.bin"),
        ("f303", args.driver, f"followcore-can-f303-{version}-app.bin"),
    ):
        release = project / "releases" / version
        record = json.loads((release / "manifest.json").read_text())
        image = release / image_name
        if record["component"] != component or record["version"] != version or record["dirty"] or \
                record["image_sha256"] != sha(image) or record["image_bytes"] != image.stat().st_size:
            raise ValueError("Unverified component image: " + component)
        data = image.read_bytes()
        if component == "s3":
            if data[:1] != b"\xe9" or data[32:36] != bytes.fromhex("3254cdab") or \
                    data[48:80].split(b"\0", 1)[0] != version.encode() or \
                    record["commit"].encode() + b"\0" not in data:
                raise ValueError("S3 image descriptor/source mismatch")
        else:
            import struct
            sp, reset = struct.unpack_from("<II", data)
            if not (0x20000000 <= sp <= 0x20008000 and 0x08006000 <= reset < 0x0801F000 and reset & 1) or \
                    (version + "+g" + record["commit"][:12]).encode() + b"\0" not in data:
                raise ValueError("Wrong F303 App address/version/source")
        (out / image_name).write_bytes(data)
        components[component] = {key: record[key] for key in
            ("version", "commit", "image_bytes", "image_sha256")}
        components[component].update(file=image_name, url=prefix + image_name)
    archive(out / f"followcore-can-s3-{version}-web.zip", [
        (args.s3_web / name, name) for name in
        ("index.html", "app.js", "ui_wasm.js", "ui_wasm.wasm")])
    archive(out / f"followcore-can-f303-{version}-web.zip", [
        (args.driver / "web" / name, name) for name in
        ("index.html", "app.js", "console.js", "canopen.js", "canopen.html",
         "style.css", "overrides.css", "console.css")])
    archive(out / f"followcore-can-f303-{version}-update-tools.zip", [
        (args.driver / "tools/upload_usb.py", "upload_usb.py"),
        (ROOT / "docs/firmware-update.md", "README.md"),
        (ROOT / "NOTICE.md", "NOTICE.md")])
    archive(out / f"followcore-can-{version}-notices.zip", [
        (ROOT / "NOTICE.md", "NOTICE.md"),
        (ROOT / "THIRD_PARTY_NOTICES.md", "THIRD_PARTY_NOTICES.md"),
        *((f, "licenses/" + f.name) for f in sorted((ROOT / "licenses").iterdir()) if f.is_file())])
    manifest = {
        "schema": 1, "product": "FollowCore", "variant": "FollowCore-CAN",
        "control_type": "CAN", "version": version, "channel": "prerelease",
        "release_tag": tag, "repository": REPO,
        "controller_hardware": "ESP-V3.003 / ESP32-S3-WROOM-1-N16R8",
        "paired_driver": "supported STM32F303 project hardware with existing IAP",
        "components": components,
        "github_device_ota_available": False,
        "pulse_available": False, "ethercat_available": False,
        "validation": validation,
        "assets": [{"file": f.name, "bytes": f.stat().st_size, "sha256": sha(f),
                    "url": prefix + f.name} for f in sorted(out.iterdir())],
    }
    (out / "release-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    notes = f"""# FollowCore-CAN {version}

Pre-release for controlled evaluation, not a stable/production qualification.

S3: {version}, source `{components['s3']['commit']}`.
F303: {version}, source `{components['f303']['commit']}`.

Only CAN is supported by this package. Pulse/EtherCAT and direct GitHub device
updates remain planned. Use the signed S3 OTA image and separate F303 App image;
they are not interchangeable. Do not erase partitions/calibration or guess a
flash address. The F303 updater is a POSIX/macOS Python 3 host tool, not firmware
source. Browser packages contain client-side code only, not MCU control source.

Changes: FollowCore-CAN identity and support contacts on both interfaces;
product/control-type feedback metadata; OFL-derived renamed UI font subsets.
The S3 rc.2 manual direction fix is retained. No drive algorithm, PDO layout,
network identity, homing threshold, or current limit is changed in this release.

Validation: see the reviewed validation record in release-manifest.json.
Mechanical homing, contact force, loaded/weak-signal behavior, worst-case
communication timing and long-term reliability are NOT fully qualified. Read
the known limitations before testing. Build/host results do not replace actual
machine acceptance. Updating does not automatically resume motion.

Support: sapphiresaiv@gmail.com; Douyin: dys5roelfesy.

Download this release's third-party notices together with the firmware. Publisher
terms do not override upstream licenses. See the repository documentation for
compatibility, safe updating, and reporting sanitized diagnostics.
"""
    (out / "RELEASE_NOTES.md").write_text(notes)
    sums = "".join(sha(f) + "  " + f.name + "\n" for f in sorted(out.iterdir()))
    (out / "SHA256SUMS").write_text(sums)
    public = ROOT / "firmware/followcore-can/releases" / version
    public.mkdir(parents=True, exist_ok=False)
    for name in ("release-manifest.json", "SHA256SUMS", "RELEASE_NOTES.md"):
        (public / name).write_bytes((out / name).read_bytes())
    print("Staged " + str(out))
    print("Public metadata " + str(public))


if __name__ == "__main__":
    main()
