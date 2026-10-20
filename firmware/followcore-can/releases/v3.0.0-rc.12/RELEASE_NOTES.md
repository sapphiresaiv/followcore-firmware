# FollowCore-CAN v3.0.0-rc.12

Pre-release for controlled evaluation, not stable or production qualified.
S3 v3.0.0-rc.12, source `bb61576b79308c877c1e5e210bcb92a1014ae3af`.
Compatible unchanged F303: v3.0.0-rc.3, source `fb9b11db6b8e532aa1353cb746daf81ad48e7969`.
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
