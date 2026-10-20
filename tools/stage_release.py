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
    p.add_argument("--driver-version", help="Previously published compatible driver version")
    p.add_argument("--s3-only", action="store_true", help="Reference, but do not republish, the unchanged driver")
    p.add_argument("--github-check", action="store_true", help="This S3 implements version checking, not online installation")
    p.add_argument("--commissioning-ui", action="store_true", help="This revision fixes first-use maintenance and simplifies the UI")
    p.add_argument("--s3-web", type=Path, required=True)
    p.add_argument("--validation", type=Path, required=True, help="Reviewed public validation JSON; never infer PASS from a build")
    args = p.parse_args()
    version = args.version
    driver_version = args.driver_version or version
    import re
    if not re.fullmatch(r"v\d+\.\d+\.\d+-rc\.\d+", version):
        raise ValueError("This tool publishes candidate versions only")
    if not re.fullmatch(r"v\d+\.\d+\.\d+-rc\.\d+", driver_version):
        raise ValueError("Invalid compatible driver candidate")
    if args.s3_only and not (ROOT / "firmware/followcore-can/releases" / driver_version / "release-manifest.json").is_file():
        raise ValueError("S3-only update requires an existing public driver release")
    validation = json.loads(args.validation.read_text())
    if validation.get("version") != version or validation.get("variant") != "FollowCore-CAN":
        raise ValueError("Validation record does not belong to this candidate")
    out = ROOT / ".build" / version
    out.mkdir(parents=True, exist_ok=False)
    tag = "followcore-can-" + version
    prefix = "https://github.com/" + REPO + "/releases/download/" + tag + "/"
    components = {}
    for component, project, component_version, image_name in (
        ("s3", args.s3, version, f"followcore-can-s3-{version}-ota.bin"),
        ("f303", args.driver, driver_version, f"followcore-can-f303-{driver_version}-app.bin"),
    ):
        release = project / "releases" / component_version
        record = json.loads((release / "manifest.json").read_text())
        image = release / image_name
        if record["component"] != component or record["version"] != component_version or record["dirty"] or \
                record["image_sha256"] != sha(image) or record["image_bytes"] != image.stat().st_size:
            raise ValueError("Unverified component image: " + component)
        data = image.read_bytes()
        if component == "s3":
            if data[:1] != b"\xe9" or data[32:36] != bytes.fromhex("3254cdab") or \
                    data[48:80].split(b"\0", 1)[0] != component_version.encode() or \
                    record["commit"].encode() + b"\0" not in data:
                raise ValueError("S3 image descriptor/source mismatch")
        else:
            import struct
            sp, reset = struct.unpack_from("<II", data)
            if not (0x20000000 <= sp <= 0x20008000 and 0x08006000 <= reset < 0x0801F000 and reset & 1) or \
                    (component_version + "+g" + record["commit"][:12]).encode() + b"\0" not in data:
                raise ValueError("Wrong F303 App address/version/source")
        included = component == "s3" or not args.s3_only
        if included:
            (out / image_name).write_bytes(data)
        components[component] = {key: record[key] for key in
            ("version", "commit", "image_bytes", "image_sha256")}
        component_prefix = prefix if included else "https://github.com/" + REPO + "/releases/download/followcore-can-" + component_version + "/"
        components[component].update(file=image_name, url=component_prefix + image_name,
                                     included_in_release=included, update_required=included)
    archive(out / f"followcore-can-s3-{version}-web.zip", [
        (args.s3_web / name, name) for name in
        ("index.html", "app.js", "ui_wasm.js", "ui_wasm.wasm")])
    if not args.s3_only:
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
        "github_device_check_available": args.github_check,
        "pulse_available": False, "ethercat_available": False,
        "validation": validation,
        "assets": [{"file": f.name, "bytes": f.stat().st_size, "sha256": sha(f),
                    "url": prefix + f.name} for f in sorted(out.iterdir())],
    }
    (out / "release-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    notes = f"""# FollowCore-CAN {version}

Pre-release for controlled evaluation, not a stable/production qualification.

S3: {version}, source `{components['s3']['commit']}`.
F303: {driver_version}, source `{components['f303']['commit']}`.

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
    if args.s3_only:
        notes = f"""# FollowCore-CAN {version}

Pre-release for controlled evaluation, not stable or production qualified.
S3 {version}, source `{components['s3']['commit']}`.
Compatible unchanged driver: {driver_version}, source `{components['f303']['commit']}`.
This package updates S3 only. F303 is referenced at its original immutable release,
not rebuilt, re-labelled, automatically downloaded or flashed.

Changes: MCU-side HTTPS version checking with opt-in testing channel, separate
S3/F303 comparisons and optional read-only standard 100A software metadata;
HTTP/DNS/TLS/timeout/catalog diagnostics; referenced MinPost safety gate for
ordinary networking; navigation retains maintenance and explicit cancellation
cleans up before lease release. No motor algorithm, PDO layout, homing threshold
or current limit is changed. Direct GitHub download/install is NOT implemented.

Use the matching signed OTA image and browser package. Private MCU source, ELF,
keys, calibration data and raw logs are not included. Do not guess flash addresses
or erase NVS. Updating never automatically resumes motion.

Host/simulated-error/UI/build evidence and real-device limitations are in the
reviewed validation record. Real regional Internet reachability, mechanical
homing/contact force, loaded/weak-signal behavior and long-term reliability are
not certified by these tests. See docs/update-check.md and compatibility docs.

Support: sapphiresaiv@gmail.com; Douyin: dys5roelfesy.
Download the accompanying third-party notices. Upstream licenses remain valid.
"""
        (out / "RELEASE_NOTES.md").write_text(notes)
    if args.commissioning_ui:
        if not args.s3_only:
            raise ValueError("Commissioning UI release must leave the driver unchanged")
        notes = f"""# FollowCore-CAN {version}

Pre-release for controlled evaluation, not stable or production qualified.
S3 {version}, source `{components['s3']['commit']}`.
Compatible unchanged F303: {driver_version}, source `{components['f303']['commit']}`.
Only S3 and its matching browser UI are updated.

Fix first-use networking before mechanical/laser calibration or homing. The CAN
owner must still confirm stationary feedback or local quiescence with no
unresolved motion. Referenced devices still require safe MinPost parking.
First-boot maintenance is adopted without releasing the motion lock.

Offline Version now opens Wi-Fi search. Upgrade offers a local upload hotspot,
including switching from STA without releasing maintenance; USB recovery is
identified separately. Normal diagnostics show four current status summaries;
engineering evidence remains available through explicit diagnostics. Navigation
still retains maintenance until explicit cancellation and cleanup.

No F303 rebuild, motor algorithm, PDO layout, homing threshold or current-limit
change. Signed OTA validation and rollback checks are retained. Direct GitHub
download/install and automatic F303 updating are NOT implemented.

See release-manifest.json for actual tests and limitations. Limited host/UI and
device network checks do not qualify mechanical, loaded, regional Internet or
long-term behavior. Use the matching signed image and browser package; do not
guess addresses or erase NVS. Private keys, sources and raw captures are absent.

Support: sapphiresaiv@gmail.com; Douyin: dys5roelfesy.
Download the accompanying third-party notices. Upstream licenses remain valid.
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
