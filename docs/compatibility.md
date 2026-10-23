# Compatibility

| Control variant | Controller hardware | Controller firmware | Paired driver | Driver firmware | Status |
| --- | --- | --- | --- | --- | --- |
| FollowCore-CAN | ESP-V3.003 / ESP32-S3-WROOM-1-N16R8 | v3.0.0-rc.47 | Existing paired STM32F303 hardware / project IAP | Installed v3.0.0-rc.9, unchanged and not included | Controlled calibration-workflow candidate; operator OTA from rc.44 pending |
| FollowCore-Pulse | Not assigned | Not available | Not qualified | Not available | Planned |
| FollowCore-ECAT | Not assigned | Not available | Not qualified | Not available | Planned |

Controller and driver use independent source repositories and binary hashes.
Matching version strings alone do not establish compatibility. Read the
component, hardware, interface, and paired-version fields in the release
manifest. The public release tag is variant-qualified; MCU software versions
and the corresponding private source tags remain component-specific (`rc.47` S3,
`rc.9` unchanged F303). This does not require reflashing the unchanged driver.
The rc.47 manifest records the existing driver identity without claiming a
published driver download URL. Older public pairings are not automatically
qualified by this controller-only candidate. In particular, the public driver
rc.3 is not qualified for this package. The testing catalog's independent
driver entry still describes that older public release, not a new rc.9 download.
Historical rc.100/104 exercise assets remain unchanged; devices actually
running them will not consider rc.47 newer and must not force an online downgrade.

The current S3 UI reports its own actual application version. Its existing
paired-driver row reports the driver's build identifier, not a guessed semantic
version. The F303's standard read-only CANopen `100A:00` supplies its software
version/source identifier on request.

Do not interpret candidate availability as completed mechanical, loaded,
weak-signal, worst-case timing, or long-duration qualification. No third-party
servo backend is certified by this pairing.
