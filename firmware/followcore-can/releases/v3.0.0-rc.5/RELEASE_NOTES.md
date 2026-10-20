# FollowCore-CAN v3.0.0-rc.5

Pre-release for controlled evaluation, not stable or production qualified.
S3 v3.0.0-rc.5, source `756817e8b63ff6ec8bddbbd12338fcd9cb538182`.
Compatible unchanged driver: v3.0.0-rc.3, source `fb9b11db6b8e532aa1353cb746daf81ad48e7969`.
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
