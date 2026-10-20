# FollowCore-CAN v3.0.0-rc.7

Pre-release for controlled evaluation, not stable or production qualified.
S3 v3.0.0-rc.7, source `7cadaf2f8eca76e5b7d7ca29efc35abaa3c19b3a`.
Compatible unchanged F303: v3.0.0-rc.3, source `fb9b11db6b8e532aa1353cb746daf81ad48e7969`.
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
