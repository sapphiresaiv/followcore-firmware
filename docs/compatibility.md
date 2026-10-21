# Compatibility

| Control variant | Controller hardware | Controller firmware | Paired driver | Driver firmware | Status |
| --- | --- | --- | --- | --- | --- |
| FollowCore-CAN | ESP-V3.003 / ESP32-S3-WROOM-1-N16R8 | v3.0.0-rc.29 | Existing paired STM32F303 hardware / project IAP | Installed v3.0.0-rc.5, unchanged and not included | Operator-run VERSION-only OTA from rc.28; see release validation |
| FollowCore-Pulse | Not assigned | Not available | Not qualified | Not available | Planned |
| FollowCore-ECAT | Not assigned | Not available | Not qualified | Not available | Planned |

Controller and driver use independent source repositories and binary hashes.
Matching version strings alone do not establish compatibility. Read the
component, hardware, interface, and paired-version fields in the release
manifest. The public release tag is variant-qualified; MCU software versions
and the corresponding private source tags remain component-specific (`rc.29` S3,
`rc.5` unchanged F303). This does not require reflashing the unchanged driver.
The rc.29 manifest records the existing driver identity without claiming a
published driver download URL. Older public pairings are not automatically
qualified by this controller-only OTA exercise.

The current S3 UI reports its own actual application version. Its existing
paired-driver row reports the driver's build identifier, not a guessed semantic
version. The F303's standard read-only CANopen `100A:00` supplies its software
version/source identifier on request.

Do not interpret candidate availability as completed mechanical, loaded,
weak-signal, worst-case timing, or long-duration qualification. No third-party
servo backend is certified by this pairing.
