# FollowCore-CAN v3.0.0-rc.15

Version-only pre-release for an operator-run local OTA exercise, not a new
functional release or production qualification. S3 v3.0.0-rc.15, source
`557e0a11266b67db5bec0c8ae4a6fa206a7eea79`. The exact source diff against the reviewed
rc.14 base is VERSION only; generated build identity also changes.

Compatible unchanged F303: v3.0.0-rc.3, source `fb9b11db6b8e532aa1353cb746daf81ad48e7969`.
Do not update the driver for this test. Motor control, CAN/PDO, homing, current
limits, Wi-Fi/DNS/TLS behavior, storage, partition layout and trust anchor are
unchanged. Existing rc.14 issues and qualification limits remain applicable.

Download `followcore-can-s3-v3.0.0-rc.15-ota.bin` on the computer, then use the
controller's existing local-hotspot upload workflow. The Version tab can compare
the testing catalog, but direct GitHub device download/install is not implemented.
Keep HTTPS/signature checks enabled; an Internet failure is not a successful update.

This candidate has not been flashed or hardware-tested by the publisher in this
release task; the operator will perform the OTA exercise. Verify the displayed
v3.0.0-rc.15 after reboot. See release-manifest.json for build/signature evidence.
The browser bundle is unchanged from rc.14 and does not require replacing an
already matching rc.14 bundle. Do not erase NVS or guess Flash addresses.

Support: sapphiresaiv@gmail.com; Douyin: dys5roelfesy.
Download the accompanying third-party notices. Upstream licenses remain valid.
