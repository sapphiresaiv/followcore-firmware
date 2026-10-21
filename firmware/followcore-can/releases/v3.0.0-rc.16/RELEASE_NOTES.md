# FollowCore-CAN v3.0.0-rc.16

Pre-release for controlled online OTA evaluation, not production qualification.
Controller v3.0.0-rc.16, source `799deb82e53b4479e55f59edb6e52328e4d3b33e`.
Compatible driver v3.0.0-rc.3, source `fb9b11db6b8e532aa1353cb746daf81ad48e7969`;
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

This is the functional bootstrap that introduces online controller OTA.

See release-manifest.json for the precise validation scope and hardware result.
Network availability in a VPN-enabled computer does not prove direct access by
the ESP32. DNS success does not prove TCP/TLS/HTTP success; an interrupted or
failed download must not be reported as installed or already latest.

Support: sapphiresaiv@gmail.com; Douyin: dys5roelfesy.
Download the accompanying third-party notices. Upstream licenses remain valid.
