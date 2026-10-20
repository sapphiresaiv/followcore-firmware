# FollowCore-CAN v3.0.0-rc.3

Pre-release for controlled evaluation, not a stable/production qualification.

S3: v3.0.0-rc.3, source `3710c128849a33bf040085c45029238038c6dbbd`.
F303: v3.0.0-rc.3, source `fb9b11db6b8e532aa1353cb746daf81ad48e7969`.

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
