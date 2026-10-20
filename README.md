# FollowCore

Precision gap-following controllers. This is the official public **firmware
distribution, documentation, and support repository**, not the firmware source
repository. Private development code and history are not published here.

## Product variants

| Variant | Control interface | Availability |
| --- | --- | --- |
| FollowCore-CAN | CAN bus; CANopen-based integration | Current candidate builds |
| FollowCore-Pulse | Pulse/direction | Planned; no firmware available |
| FollowCore-ECAT | EtherCAT | Planned; requires suitable hardware |

The current controller is `ESP-V3.003`, using an ESP32-S3-WROOM-1-N16R8.
Its supported paired driver is the STM32F303-based FollowCore-CAN driver.
Do not install CAN firmware on a future Pulse or EtherCAT product.

## Downloads

Use [GitHub Releases](https://github.com/sapphiresaiv/followcore-firmware/releases).
Download the component-specific BIN and matching documentation/checksums.
Controller and motor-driver BIN files are **not interchangeable**.

`v3.0.0-rc.9` (S3, compatible unchanged F303 `v3.0.0-rc.3`) is a
**release candidate for controlled evaluation**, not a stable
or production-qualified release. Read the release's compatibility table and
known limitations before installation. Older test counts do not certify a new
firmware version.

## Current project scope

- Distance-feedback-based gap following and touchscreen operation.
- Manual up/down control with latest-direction handoff.
- Homing coordination for the supported drive and mechanical setup.
- CAN communication supervision, fault/event reporting, and diagnostic export.
- S3 local Wi-Fi hotspot upload with signed image verification and dual-slot
  boot validation/rollback support on the qualified partition layout.

S3 implements explicit MCU-side version checking, separate controller/driver
comparison, and network failure diagnostics. `rc.7` fixes first-use network
admission and simplifies the maintenance interface. [Read the checks and safety gates](docs/update-check.md).
`rc.8` adds immediate querying/busy feedback, repeat-click prevention and shared
pressed/disabled button visuals on the device and matching browser UI.
`rc.9` distinguishes visible update-query errors and adds explicit read-only
query diagnostics; unknown timeouts are not automatically blamed on the network.
Direct GitHub firmware download/install is **not implemented**.
S3 OTA does not update the F303 driver. Universal servo compatibility and
CANopen/EtherCAT safety or conformance certification are not claimed.

## Documentation

- [Getting started](docs/getting-started.md)
- [Firmware updates](docs/firmware-update.md)
- [Compatibility](docs/compatibility.md)
- [Troubleshooting](docs/troubleshooting.md)
- [Release policy](docs/release-policy.md)
- [Safety](docs/safety.md)
- [Support](SUPPORT.md) and [security reports](SECURITY.md)
- [Distribution notice](NOTICE.md) and [third-party notices](THIRD_PARTY_NOTICES.md)

## Contact

- Email: [sapphiresaiv@gmail.com](mailto:sapphiresaiv@gmail.com)
- Douyin: `dys5roelfesy`
- Issues: https://github.com/sapphiresaiv/followcore-firmware/issues

Product names and account handles do not identify a legal entity or grant an
open-source license. Existing publisher terms and third-party licenses apply.
