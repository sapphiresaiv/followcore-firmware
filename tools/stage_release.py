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
    p.add_argument("--reference-only-driver", action="store_true", help="Record an installed driver identity without advertising an unpublished download")
    p.add_argument("--release-notes", type=Path, help="Reviewed candidate-specific public release notes")
    p.add_argument("--github-check", action="store_true", help="This S3 implements version checking, not online installation")
    p.add_argument("--commissioning-ui", action="store_true", help="This revision fixes first-use maintenance and simplifies the UI")
    p.add_argument("--button-feedback", action="store_true", help="This revision fixes query and shared button feedback")
    p.add_argument("--update-errors", action="store_true", help="This revision adds visible query failure categories and explicit RAM diagnostics")
    p.add_argument("--async-tls-fix", action="store_true", help="This revision corrects pinned SDK async connection polling and error forwarding")
    p.add_argument("--network-profile-ui", action="store_true", help="This revision adds remembered Wi-Fi and global connection/navigation feedback")
    p.add_argument("--dns-presets", action="store_true", help="This S3-only revision adds named DNS presets and asynchronous lookup diagnostics")
    p.add_argument("--dns-empty-fix", action="store_true", help="This revision corrects rc.13 empty DNS set/restore and close failure")
    p.add_argument("--version-only", action="store_true", help="S3 OTA exercise: only VERSION differs from the reviewed base commit")
    p.add_argument("--online-ota-ui", action="store_true", help="Signed controller online OTA and independent version cards; driver unchanged")
    p.add_argument("--download-request-fix", action="store_true", help="Online OTA long signed-URL request fix and stage-specific failures")
    p.add_argument("--connection-capture", action="store_true", help="Retain passive query/download connection evidence on explicit NETTRACE GET")
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
    if args.reference_only_driver and not args.s3_only:
        raise ValueError("A reference-only driver requires an S3-only release")
    if args.s3_only and not args.reference_only_driver and not (ROOT / "firmware/followcore-can/releases" / driver_version / "release-manifest.json").is_file():
        raise ValueError("S3-only update requires an existing public driver release")
    if args.network_profile_ui and (not args.s3_only or any((args.commissioning_ui,
            args.button_feedback, args.update_errors, args.async_tls_fix))):
        raise ValueError("Network profile/UI update requires S3-only release notes")
    if args.dns_presets and (not args.s3_only or any((args.commissioning_ui,args.button_feedback,
            args.update_errors,args.async_tls_fix,args.network_profile_ui))):
        raise ValueError("DNS presets require separate S3-only release notes")
    if args.dns_empty_fix and not args.dns_presets:
        raise ValueError("DNS empty-entry correction requires the DNS preset notes")
    if args.online_ota_ui and (not args.s3_only or not args.github_check or any((args.commissioning_ui,
            args.button_feedback,args.update_errors,args.async_tls_fix,args.network_profile_ui,args.dns_presets))):
        raise ValueError("Online OTA requires separate S3-only notes and version checking")
    if args.download_request_fix and not args.online_ota_ui:
        raise ValueError("Download request correction requires online OTA release notes")
    if args.connection_capture and not args.online_ota_ui:
        raise ValueError("Connection capture requires online OTA release notes")
    if args.version_only and (not args.s3_only or any((args.commissioning_ui,
            args.button_feedback,args.update_errors,args.async_tls_fix,args.network_profile_ui,
            args.dns_presets,args.dns_empty_fix))):
        raise ValueError("Version-only requires separate S3-only release notes")
    validation = json.loads(args.validation.read_text())
    if validation.get("version") != version or validation.get("variant") != "FollowCore-CAN":
        raise ValueError("Validation record does not belong to this candidate")
    if args.version_only:
        import subprocess
        base=validation.get("version_only_base_commit","")
        if not re.fullmatch(r"[0-9a-f]{40}",base):
            raise ValueError("Version-only requires an exact reviewed base commit")
        record=json.loads((args.s3/"releases"/version/"manifest.json").read_text())
        changed=subprocess.check_output(["git","-C",str(args.s3),"diff","--name-only",
            base,record["commit"]],text=True).splitlines()
        if changed != ["VERSION"]:
            raise ValueError("Version-only source contains other changes")
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
        if component == "f303" and args.reference_only_driver:
            components[component].update(url=None, reference_only=True,
                distribution_note="Installed compatible driver identity only; no driver download is published by this release.")
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
        "github_device_ota_available": args.online_ota_ui,
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
        repair = """Correct rc.13's deterministic preset/close failure (0x5001): IDF rejects
empty DNS addresses. Set nonempty entries through ESP-NETIF and clear empty
entries on the TCP/IP thread through lwIP's supported clear operation. Restore
the DHCP baseline, including empty backup/fallback entries, without ignoring
errors or leaving a preset in Automatic mode. Scan-first is not required for
a saved network. Actual SDK function replays and a 100-cycle transport test
cover the contract previously omitted by the host stub.
""" if args.dns_empty_fix else ""
        notes = f"""# FollowCore-CAN {version}

Pre-release for controlled evaluation, not stable or production qualified.
S3 {version}, source `{components['s3']['commit']}`.
Compatible unchanged F303: {driver_version}, source `{components['f303']['commit']}`.
Only S3 requires an update. Refresh the matching browser bundle after installing.

{repair}
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
    if args.version_only:
        notes=f"""# FollowCore-CAN {version}

Version-only pre-release for an operator-run local OTA exercise, not a new
functional release or production qualification. S3 {version}, source
`{components['s3']['commit']}`. The exact source diff against the reviewed
rc.14 base is VERSION only; generated build identity also changes.

Compatible unchanged F303: {driver_version}, source `{components['f303']['commit']}`.
Do not update the driver for this test. Motor control, CAN/PDO, homing, current
limits, Wi-Fi/DNS/TLS behavior, storage, partition layout and trust anchor are
unchanged. Existing rc.14 issues and qualification limits remain applicable.

Download `followcore-can-s3-{version}-ota.bin` on the computer, then use the
controller's existing local-hotspot upload workflow. The Version tab can compare
the testing catalog, but direct GitHub device download/install is not implemented.
Keep HTTPS/signature checks enabled; an Internet failure is not a successful update.

This candidate has not been flashed or hardware-tested by the publisher in this
release task; the operator will perform the OTA exercise. Verify the displayed
{version} after reboot. See release-manifest.json for build/signature evidence.
The browser bundle is unchanged from rc.14 and does not require replacing an
already matching rc.14 bundle. Do not erase NVS or guess Flash addresses.

Support: sapphiresaiv@gmail.com; Douyin: dys5roelfesy.
Download the accompanying third-party notices. Upstream licenses remain valid.
"""
        (out/"RELEASE_NOTES.md").write_text(notes)
    if args.online_ota_ui:
        notes=f"""# FollowCore-CAN {version}

Pre-release for controlled online OTA evaluation, not production qualification.
Controller {version}, source `{components['s3']['commit']}`.
Compatible driver {driver_version}, source `{components['f303']['commit']}`;
unchanged, not rebuilt, republished, downloaded or automatically flashed.

Controller/driver versions now have independent cards and status badges. The
complete bounded catalog summaries open in a scrollable release-notes window.
An available controller image offers Download and validate, visible progress,
then a separate Install and restart confirmation. This is controller-only OTA;
motor/CAN/PDO/homing/current limits and the fixed signing trust are unchanged.

Older controllers need the signed rc.16-or-newer bootstrap through the existing
local-hotspot/qualified USB workflow before they gain online installation.
The device streams a fixed-repository HTTPS release asset to the inactive slot,
checking target version/project/chip, exact size, SHA256 and the fixed public
RSA-3072/PSS signature. No automatic slot selection; first-boot verification and
rollback remain enabled. Do not erase NVS or bypass HTTPS/signature checks.
Page navigation keeps the maintenance lock; End maintenance explicitly cancels.

{"This target differs from its exact reviewed base recorded in validation only in VERSION and generated identity; it exercises that base's online OTA." if args.version_only else "This is the functional bootstrap that introduces online controller OTA."}

See release-manifest.json for the precise validation scope and hardware result.
Network availability in a VPN-enabled computer does not prove direct access by
the ESP32. DNS success does not prove TCP/TLS/HTTP success; an interrupted or
failed download must not be reported as installed or already latest.

Support: sapphiresaiv@gmail.com; Douyin: dys5roelfesy.
Download the accompanying third-party notices. Upstream licenses remain valid.
"""
        (out/"RELEASE_NOTES.md").write_text(notes)
    if args.download_request_fix:
        notes=f"""# FollowCore-CAN {version}

Candidate for controlled online OTA evaluation, not production qualification.
Controller {version}, source `{components['s3']['commit']}`.
Compatible F303 {driver_version} remains unchanged at its original release.

{"VERSION-only exercise of the exact rc.18 functional base recorded in validation." if args.version_only else "Fix the rc.16/17 controller online-download request path."}

GitHub Release signed redirect requests can exceed the old 512-byte TX buffer.
The downloader uses 2,048-byte TX, checks the URL/request budget before opening
the client and clears stale errno before async polling. Each trusted hop has a
bounded first-byte budget within the existing total deadline. Failures distinguish
connection, request send, response wait and receive. Diagnostic logs retain only
host/hop/stage, never signed query strings. Actual installed SDK request-builder
replays reproduce the old failure and test captured and maximum accepted lengths.

The original rc.16 second-attempt device log contained 1,257 Out of buffer errors
before a generic timeout. Do not automatically attribute this failure to network
reachability. Real regional TCP/TLS access still depends on the device's network;
a VPN-enabled PC download does not certify the ESP32 connection.

Only the controller is updated. Motor/CAN/PDO/homing/current limits are unchanged.
Keep HTTPS CA/hostname checks, fixed RSA-3072/PSS trust, exact size/hash/version
validation, inactive-slot writes, separate install confirmation and boot rollback.
Older controllers require this corrected bootstrap through local upload/qualified
USB once before the corrected online downloader can run. rc.16/17 themselves
cannot be relied on to download this correction through long Release redirects.
The matching browser bundle is byte-identical to rc.16.

See release-manifest.json for exact host/build and hardware qualification scope.
No mechanical, power-interruption or long-term reliability qualification is claimed.
Do not erase NVS, overwrite an immutable release, or bypass signature checks.

Support: sapphiresaiv@gmail.com; Douyin: dys5roelfesy.
Download the accompanying third-party notices. Upstream licenses remain valid.
"""
        (out/"RELEASE_NOTES.md").write_text(notes)
    if args.connection_capture:
        notes=f"""# FollowCore-CAN {version}

Candidate for controlled connection diagnosis, not production qualification.
Controller {version}, source `{components['s3']['commit']}`.
Compatible F303 {driver_version} is unchanged at its original release.

{"VERSION-only OTA target of the exact functional base recorded in validation." if args.version_only else "Add retained passive evidence to the existing query and download connections."}
The explicit NETTRACE GET diagnostic exports separate bounded records for the
latest catalog query and firmware download. Observe the actual connect target,
TCP readiness, TLS result, request-line/Host comparison, positive transport write
count and response header progress. Keep only a short HTTP status-line prefix;
do not retain passwords, signed redirect queries, cookies or firmware payload.

The observer follows the actual job, without additional requests or probes.
Ordinary status mirrors remain unchanged; no continuous diagnostic printing.
This is not packet capture: local transport acceptance does not prove remote
receipt, and a connection timeout alone does not identify censorship or a server
refusal. Query and download use different endpoints and must be assessed apart.
Evidence persists in RAM until the next same-channel job or controller reset.

Retain rc.18's long-request correction and all existing DNS, deadlines, retry,
HTTPS CA/hostname, fixed RSA-3072/PSS, image size/hash/version and rollback gates.
There is no new network workaround or claim of repaired regional reachability.
No driver, motor/CAN/PDO, homing, current-limit or partition changes.
The matching browser bundle is byte-identical to rc.16.

See release-manifest.json for the exact host/build and hardware scope. Mechanical,
power-loss and long-term reliability are not qualified by these diagnostics.
Use the signed controller OTA image; do not erase NVS or bypass verification.

Support: sapphiresaiv@gmail.com; Douyin: dys5roelfesy.
Download the accompanying third-party notices. Upstream licenses remain valid.
"""
        (out/"RELEASE_NOTES.md").write_text(notes)
    if args.release_notes:
        notes = args.release_notes.read_text()
        if not notes.startswith("# FollowCore-CAN " + version + "\n"):
            raise ValueError("Reviewed release notes do not identify this candidate")
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
