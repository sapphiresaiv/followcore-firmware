# FollowCore-CAN v3.0.0-rc.19

Candidate for controlled online OTA evaluation, not production qualification.
Controller v3.0.0-rc.19, source `94bf56d99c058189b843f407ea273bff92728d9b`.
Compatible F303 v3.0.0-rc.3 remains unchanged at its original release.

VERSION-only exercise of the exact rc.18 functional base recorded in validation.

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
