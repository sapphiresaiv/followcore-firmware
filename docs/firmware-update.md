# Firmware updates

## Choose the correct artifact

- `followcore-can-s3-<version>-ota.bin`: signed S3 application for the already
  qualified 16 MiB dual-slot controller layout. Not a factory/full-flash image.
- `followcore-can-f303-<version>-app.bin`: F303 application for the existing
  project IAP bootloader. Not an S3 image or a replacement bootloader.
- Component-specific `*-web.zip`: browser UI, not MCU firmware.
- `release-manifest.json` and `SHA256SUMS`: compatibility and integrity records.

Never flash an application BIN at a guessed address. First installation or
recovery from a different partition/bootloader layout requires publisher
instructions for the exact hardware. Do not erase NVS/calibration storage as a
normal update step.

## S3 local update

Make the mechanism safe, stop motion, and use the controller's existing
maintenance/update workflow. Connect to its local update hotspot and upload
only the matching signed S3 OTA BIN. Follow its on-screen validation and reboot
prompts. An interrupted upload must not be treated as a completed update.

The qualified implementation writes the inactive application slot, validates
the image, and performs first-boot checks before confirming it. Rollback needs
a compatible bootloader and a valid previous slot; it does not guarantee
recovery from every hardware, power, or storage failure.

## F303 driver update

Use the matching IAP uploader supplied in the driver update-tools package.
Its application/bootloader handshake and CRC checks must complete successfully.
Do not run a browser serial console concurrently with the uploader. An S3
hotspot update does not update this MCU.

## Afterwards

Verify reported versions. Exit maintenance and explicitly restore control as
instructed locally; repeat homing before ordinary motion. Do not resume an old
movement automatically.

S3 rc.7 supports initial setup networking before calibration/homing, using
owner-confirmed stationary feedback or local quiescence. Once referenced,
ordinary networking still requires returning to MinPost. [Read the admission rules](update-check.md).
The Version tab routes an offline user to Wi-Fi. The Upgrade tab can start or
switch to the local upload hotspot; fault recovery uses USB and a computer.
Navigation does not cancel the maintenance lock: use Cancel upgrade or End
maintenance. Explicitly end first-boot maintenance before restoring control and
homing. Physical isolation alone does not authorize wireless operation.

## Controller online OTA (rc.16 and newer)

Older firmware only checks versions. Install the signed rc.16-or-newer bootstrap
once through local upload or the qualified USB workflow to gain online OTA.
Connect Wi-Fi, open Version, select Include testing for prereleases, then Check
updates. Controller and driver have separate current/available versions and
status badges. Release notes opens the complete bounded catalog summaries with
scrolling and page buttons, not the full GitHub Markdown page.

An available controller image with installation metadata enables Update
controller. Confirm Download and validate; progress is shown while the inactive
slot is written. Exact size, SHA256, project/chip/version and the fixed signing
key must pass before Install and restart becomes available. Confirm restart
separately; maintain stable power. First-boot verification/rollback still apply.
Navigation does not release the maintenance lock. End maintenance cancels.

F303 is compared and reported, not automatically installed. Keep the signed
local upload method and qualified wired recovery available. Internet failures
are not "already latest" or CAN/motor faults. DNS success alone does not prove
direct GitHub access; a computer's VPN does not extend to the controller.
