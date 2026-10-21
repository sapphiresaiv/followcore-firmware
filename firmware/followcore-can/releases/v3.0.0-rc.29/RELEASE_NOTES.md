# FollowCore-CAN v3.0.0-rc.29

VERSION-only pre-release for an operator-run online OTA test from the installed
rc.28 controller, not a new functional release or production qualification.
Controller v3.0.0-rc.29, source `50da2720e0728008f36a6dea48537afc53dd8e0c`.
Compatible driver v3.0.0-rc.5, source `3b0090e6b9cc1bbf2483fd20931b4cdd5a89a75d`;
unchanged, not rebuilt, republished, downloaded or automatically flashed.

The exact frozen source diff against rc.28
(`8fe2b88c0360fc1eaa3b49a5fc0755cd6f99163c`) is VERSION only. Generated
application/source identity changes, but motor/CAN/PDO, calibration, protection,
Wi-Fi/DNS/TLS, storage, partition and fixed signing trust do not change.
The paired installed driver rc.5 is a reference only; no driver download URL is
claimed and no driver update is required. Older public pairings are not
automatically qualified by this operator's rc.28/rc.5 OTA exercise.

Enable Include testing, Check for updates, then Download and validate. Installation
and restart require a separate explicit confirmation. The device streams this
fixed-repository HTTPS release asset to the inactive slot,
checking target version/project/chip, exact size, SHA256 and the fixed public
RSA-3072/PSS signature. No automatic slot selection; first-boot verification and
rollback remain enabled. Do not erase NVS or bypass HTTPS/signature checks.
Page navigation keeps the maintenance lock; End maintenance explicitly cancels.

The included browser bundle is byte-identical to rc.28. The publisher has not
flashed rc.29 or run a new hardware OTA/motion test; the operator will test it.
After restart, verify controller v3.0.0-rc.29 and the unchanged driver version.

See release-manifest.json for the precise validation scope and hardware result.
Network availability in a VPN-enabled computer does not prove direct access by
the ESP32. DNS success does not prove TCP/TLS/HTTP success; an interrupted or
failed download must not be reported as installed or already latest.

Support: sapphiresaiv@gmail.com; Douyin: dys5roelfesy.
Download the accompanying third-party notices. Upstream licenses remain valid.
