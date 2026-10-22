# FollowCore-CAN v3.0.0-rc.100

Controller-only candidate for an operator-run online OTA test from the locally
installed v3.0.0-rc.32. This is not a stable or production-qualified release.

## Changes from the installed rc.32

- Advance the controller version to v3.0.0-rc.100 for update discovery.
- Show "网络已连接" when the existing network connectivity check succeeds;
  use shorter connection-check messages for pending and failed states.
- Add regression checks for the requested wording and numeric version ordering:
  rc.100 > rc.32, and v3.1.0-rc.1 > v3.0.0-rc.100.
- No motion, CAN/PDO, homing, current-limit, connectivity-check policy, partition,
  NVS format, signing trust or installation-safety change from rc.32.

Source: `3dfc48952ef323e3f4db2cc89f5d9d06dd5d8e9f`.
Compatible installed driver: v3.0.0-rc.5, source
`3b0090e6b9cc1bbf2483fd20931b4cdd5a89a75d`; unchanged and not included.
Do not update or downgrade the driver for this test.

## Included improvements since the last public rc.29

The locally validated rc.32 base includes the combined Upgrade page with Local
upload and Remote download, a bounded connectivity indicator, corrected pinned
SDK asynchronous HTTP-body polling, reduced UI callback/refresh stack frames,
a 256 KiB PSRAM LVGL pool and a 16 KiB internal UI task stack. The matching
browser bundle is included. These are controller changes, not driver changes.

## Test workflow and limits

Enable the testing channel, check for updates, and verify that the controller
offers v3.0.0-rc.100. Download and validate first; installation/restart requires
its separate explicit confirmation. After reboot, verify the controller version.
Do not erase NVS or guess Flash addresses. Updating never resumes motion.

This candidate has not been serial-flashed or hardware-tested in this publication
task; the operator will test complete online OTA. The rc.32 base completed one
real connection, catalog query and network-close replay without a reset, but
that does not qualify rc.100 online binary download, power-loss recovery,
mechanical operation or long-term reliability. A green connectivity indicator
does not guarantee reachability of GitHub's separate download hosts.

The v3.1.0 candidate series will start only after this OTA test is accepted.
Read release-manifest.json for the exact build and validation scope.

Support: sapphiresaiv@gmail.com; Douyin: dys5roelfesy.
Download the accompanying third-party notices. Upstream licenses remain valid.
