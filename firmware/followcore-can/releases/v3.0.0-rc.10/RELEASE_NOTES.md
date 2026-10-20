# FollowCore-CAN v3.0.0-rc.10

Pre-release for controlled evaluation, not stable or production qualified.
S3 v3.0.0-rc.10, source `2b53ea26e001ab86b9a70db6353b94ed5ee092ba`.
Compatible unchanged F303: v3.0.0-rc.3, source `fb9b11db6b8e532aa1353cb746daf81ad48e7969`.
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
