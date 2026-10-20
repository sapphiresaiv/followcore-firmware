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

S3 rc.5 adds explicit [controller-side version checks](update-check.md), after
homing and returning to MinPost. Navigation does not cancel the maintenance lock;
use the explicitly labelled cancellation action. First-boot local maintenance must
be explicitly cancelled before restoring control and homing. Physical isolation
recovery remains wired; it does not authorize wireless operation.

Direct GitHub download/install is not implemented. F303 is only compared and
reported, not automatically updated by S3. Keep the signed local upload method
and qualified wired recovery available. Internet failures must not be reported
as "already latest" or as CAN/motor faults.
