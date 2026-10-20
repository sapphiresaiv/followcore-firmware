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

Direct GitHub checking/downloads from the controller are planned, not enabled
by this public release manifest. Keep the local upload method available.
