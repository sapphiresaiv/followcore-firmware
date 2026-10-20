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
    p.add_argument("--button-feedback", action="store_true", help="This revision fixes query and shared button feedback")
    p.add_argument("--update-errors", action="store_true", help="This revision adds visible query failure categories and explicit RAM diagnostics")
    p.add_argument("--async-tls-fix", action="store_true", help="This revision corrects pinned SDK async connection polling and error forwarding")
    p.add_argument("--network-profile-ui", action="store_true", help="This revision adds remembered Wi-Fi and global connection/navigation feedback")
    p.add_argument("--dns-presets", action="store_true", help="This S3-only revision adds named DNS presets and asynchronous lookup diagnostics")
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
    if args.network_profile_ui and (not args.s3_only or any((args.commissioning_ui,
            args.button_feedback, args.update_errors, args.async_tls_fix))):
        raise ValueError("Network profile/UI update requires S3-only release notes")
    if args.dns_presets and (not args.s3_only or any((args.commissioning_ui,args.button_feedback,
            args.update_errors,args.async_tls_fix,args.network_profile_ui))):
        raise ValueError("DNS presets require separate S3-only release notes")
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
    if args.button_feedback:
        if not args.s3_only or args.commissioning_ui:
            raise ValueError("Button feedback is an S3-only release with its own notes")
        notes = f"""# FollowCore-CAN {version}

Pre-release for controlled evaluation, not stable or production qualified.
S3 {version}, source `{components['s3']['commit']}`.
Compatible unchanged F303: {driver_version}, source `{components['f303']['commit']}`.
Only S3 and its matching browser UI are updated.

Accepted update checks immediately display a querying label and disable both
the button and channel selector throughout queued/clock/fetching states.
Completion or failure restores the controls. UI and backend independently
reject repeat requests; explicit cancellation remains usable during a query.
Search, connection, hotspot and feedback controls reflect accepted service
states immediately. Shared buttons have consistent pressed and disabled
visuals, including directional controls. No motion button event semantics,
network admission, wire layout, PDO, homing or current-limit changes.

First-use network setup and opt-in testing-channel checks from rc.7 are retained.
Direct GitHub download/install and automatic F303 updating are NOT implemented.
Use the matching signed image and browser package; do not erase NVS or guess
flash addresses. Private keys, MCU source, ELF and raw captures are excluded.

Actual tests and limitations are recorded in release-manifest.json. Simulated
query/HTTP errors and UI tests are not proof of regional Internet access,
mechanical safety, loaded behavior or long-term reliability.

Support: sapphiresaiv@gmail.com; Douyin: dys5roelfesy.
Download the accompanying third-party notices. Upstream licenses remain valid.
"""
        (out / "RELEASE_NOTES.md").write_text(notes)
    if args.update_errors:
        if not args.s3_only or args.commissioning_ui or args.button_feedback:
            raise ValueError("Update diagnostics is an S3-only release with its own notes")
        notes = f"""# FollowCore-CAN {version}

Pre-release for controlled evaluation, not stable or production qualified.
S3 {version}, source `{components['s3']['commit']}`.
Compatible unchanged F303: {driver_version}, source `{components['f303']['commit']}`.
Only S3 and its matching browser UI are updated.

Show concrete query failures, suggested actions and the last confirmed stage:
DNS, unreachable/refused/interrupted connections, TLS/certificate validation,
HTTP 404/403/429/5xx, response size/redirect/catalog and local device failures.
An unknown connection timeout is not blamed on the user or regional network.
No HTTP response means unknown, not successful access or proof of a bad URL.

Retain the last attempt's stage, timing, byte count and SDK/HTTP/TLS/socket codes
in RAM. An explicit read-only UPDATE GET serial request returns one Q reply;
it never starts networking, a retry, motion, logging or Flash writes. Default
serial output stays quiet. The existing maintenance N layout is unchanged.

This is diagnostic reporting, NOT a repair or qualification of the SDK's 100 ms
asynchronous connection path. SNTP success does not establish GitHub access.
First-use admission, cancellation, certificate/hostname/signature checks and
rollback remain in force. No F303, PDO, homing or current-limit change.
Direct GitHub download/install and automatic F303 updating remain unavailable.

See release-manifest.json for actual evidence and limitations. Simulated network
errors do not prove physical MCU Internet access or regional reliability. Use
the matching signed image and browser package; do not erase NVS or guess flash
addresses. MCU source, private keys, ELF and raw captures are excluded.

Support: sapphiresaiv@gmail.com; Douyin: dys5roelfesy.
Download the accompanying third-party notices. Upstream licenses remain valid.
"""
        (out / "RELEASE_NOTES.md").write_text(notes)
    if args.async_tls_fix:
        if not args.s3_only or args.commissioning_ui or args.button_feedback or args.update_errors:
            raise ValueError("Async TLS correction is an S3-only release with its own notes")
        notes = f"""# FollowCore-CAN {version}

Pre-release for controlled evaluation, not stable or production qualified.
S3 {version}, source `{components['s3']['commit']}`.
Compatible unchanged F303: {driver_version}, source `{components['f303']['commit']}`.
Only S3 requires a firmware update. The unchanged browser UI is included.

Correct the pinned ESP-IDF 5.5 asynchronous TCP/TLS connection state machine:
rebuild descriptor sets before every select, resume after timeout/interruption,
and reject socket/select errors before starting the TLS handshake. Forward
async DNS/socket/TLS failures to the retained HTTP diagnostics.

The shared SDK installation is never modified. Reviewed, hash-pinned source
corrections are generated only in the build directory, with an input/output
hash manifest. Unknown SDK sources fail configuration. Tests compile the actual
SDK functions; the original fails delayed-readiness/error-forwarding replays,
while the corrected functions pass. These host tests are not MCU packet capture.

Keep the 100 ms polling slice, overall deadlines, certificate/hostname/time
validation, explicit cancellation and maintenance/upgrade safety gates. No HTTP
downgrade, verification bypass or alternate host. SNTP success alone does not
establish GitHub access. Actual MCU Internet reachability still requires retest.

No F303, CAN/PDO, motion, homing or current-limit changes. Direct GitHub device
download/install and automatic F303 updating remain unavailable. See
release-manifest.json for actual evidence and limitations. Use the signed S3 OTA
image; do not erase NVS or guess flash addresses. Private keys, MCU source, ELF
and raw captures are excluded from the public binary release.

Support: sapphiresaiv@gmail.com; Douyin: dys5roelfesy.
Download the accompanying third-party notices. Upstream licenses remain valid.
"""
        (out / "RELEASE_NOTES.md").write_text(notes)
    if args.network_profile_ui:
        notes = f"""# FollowCore-CAN {version}

Pre-release for controlled evaluation, not stable or production qualified.
S3 {version}, source `{components['s3']['commit']}`.
Compatible unchanged F303: {driver_version}, source `{components['f303']['commit']}`.
Only S3 requires an update. Refresh the matching browser bundle after installing.

Show a Wi-Fi icon before the top-bar clock when associated with an IP address;
show AP separately for the local hotspot. This is not an RSSI meter or a guarantee
of Internet access. Route the maintenance banner to maintenance; a fresh fault
still takes priority and opens fault history. Navigation retains the motion lock.

Remember the most recent successful SSID/password pair in a dedicated NVS key.
Enter the password once after upgrading; later select the exact saved SSID and
leave the password blank to reuse it. A new typed password overrides the saved
one. Failed/cancelled connections do not save; unchanged pairs do not rewrite.
Forget network removes only that logical key. No automatic boot-time networking.

Passwords are not sent through status mirrors or diagnostic feedback, but local
NVS is NOT encrypted. Physical Flash access can expose stored credentials;
logical deletion is not forensic secure erasure. Do not use a sensitive network
where this storage model is unacceptable. Storage errors are reported separately
from motor/CAN faults. Host tests do not certify real power-loss behavior.

The U mirror adds three read-only fields; old browser bundles may reject it.
S/N/Q, CAN/PDO, drive algorithms, homing and current limits remain unchanged.
Direct GitHub device download/install and automatic F303 updating remain
unavailable. See release-manifest.json for actual validation and limitations.
Use the signed S3 OTA image; do not erase NVS or guess flash addresses.

Support: sapphiresaiv@gmail.com; Douyin: dys5roelfesy.
Download the accompanying third-party notices. Upstream licenses remain valid.
"""
        (out / "RELEASE_NOTES.md").write_text(notes)
    if args.dns_presets:
        notes = f"""# FollowCore-CAN {version}

Pre-release for controlled evaluation, not stable or production qualified.
S3 {version}, source `{components['s3']['commit']}`.
Compatible unchanged F303: {driver_version}, source `{components['f303']['commit']}`.
Only S3 requires an update. Refresh the matching browser bundle after installing.

Choose Automatic (DHCP/router), AliDNS, Google Public DNS or Cloudflare in Wi-Fi.
No manual IP entry is required. An explicit choice is saved separately in NVS;
unchanged choices do not rewrite. Changing a choice closes idle Wi-Fi and keeps
the maintenance lock. Reconnect explicitly. No automatic boot-time networking.
Queries/feedback and RF transitions reject changes until idle.

Apply and read back the selected servers before outbound jobs. A bounded,
nonblocking DNS preflight retains the configured servers, lookup time/error and
resolved IPv4 separately from the later TCP/TLS connection. Detailed evidence
is available only on explicit serial UPDATE GET; ordinary status remains quiet.
Resolver cancellation is safe for late SDK callbacks. N and Q add read-only
tails; previous indices are unchanged and updated readers accept old frames.

Retain HTTPS hostname, time and CA verification. Do not pin a GitHub IP or
downgrade HTTP. Ordinary plaintext DNS is not encrypted DNS, an anti-poisoning
guarantee or proof that GitHub will be reachable on a given network.
The existing browser link diagnostics, unique granted-port selection, EOF
cleanup and content-hashed resource bundle are included.

No F303 rebuild, CAN/PDO, motion, homing or current-limit changes.
Direct device download/install and automatic F303 updating remain unavailable.
See release-manifest.json for actual tests, hardware scope and limitations.
Use the signed S3 OTA image; do not erase NVS or guess Flash addresses.

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
