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

`v3.0.0-rc.100` (controller, paired installed F303 `v3.0.0-rc.5`) is a
**release candidate for controlled evaluation**, not a stable
or production-qualified release. Read the release's compatibility table and
known limitations before installation. Older test counts do not certify a new
firmware version.

rc.100 is an online OTA test target for the locally installed rc.32 controller,
with the requested simplified network-status wording and regression tests.
It is intended for that already paired rc.32/driver-rc.5 setup;
the unchanged driver is not rebuilt or included in this release. This does not
qualify an upgrade from every older public pairing. The source diff, build,
signature and test scope are recorded in the release manifest. No device was
flashed by this publication task; the operator performs the online update.

The rc.32 base adds the combined Upgrade interface, bounded connectivity
indicator, corrected asynchronous HTTP-body polling, reduced UI stack frames,
and extra LVGL/UI memory headroom. Refresh the matching browser bundle for the
updated wording. No motor/CAN/homing or network-validation policy changes are
made from rc.32. v3.1.0 candidates will follow only after the OTA test is accepted.

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
`rc.12` remembers the most recent successful Wi-Fi pair, adds a global connection
indicator and corrects maintenance-banner navigation. Local credentials are not
Flash-encrypted; see [network settings](docs/network-settings.md) before saving.
`rc.13` adds named DNS presets without IP typing and separate bounded DNS lookup
diagnostics. Explicit changes retain maintenance and require reconnecting Wi-Fi.
Changing plain DNS does not guarantee GitHub reachability.
`rc.14` corrects rc.13's empty DNS entry handling, which could make a saved-network
connection fail and leave network closing in a retry loop. The SDK contract is
now replayed in tests; rc.13 has been withdrawn from the testing catalog.
`rc.15` only advances the S3 version for an operator-run local OTA exercise.
It adds no functional fixes, does not resolve Internet reachability problems,
and leaves the F303 driver unchanged at rc.3.
`rc.16` adds signed online controller OTA, separate component version cards,
scrollable catalog notes, download progress and explicit install confirmation.
Older firmware needs this bootstrap once through local upload/qualified USB.
`rc.17` only advances VERSION to exercise rc.16's online OTA implementation.
`rc.18` fixes long signed GitHub Release download requests that exceed rc.16/17's
512-byte TX buffer, adds capacity checks and stage-specific download failures.
Install this corrected bootstrap by local upload/qualified USB before relying
on online download. Fixed signing trust and motor/driver control are unchanged.
`rc.19` is a VERSION-only target on the corrected rc.18 base for direct online
download/validation/install testing. Original rc.16/17 Release assets remain
immutable; their downloader has the documented request-size defect.
`rc.20` adds retained passive evidence to the actual query/download connections;
it does not change network policy or prove regional reachability. Explicit
NETTRACE export distinguishes TCP, TLS, request and response progress without
capturing signed URLs or credentials. `rc.21` is its exact VERSION-only OTA target.
[Read the update workflow and its limits](docs/firmware-update.md).
[Historical rc.18 hardware acceptance](docs/qualification/online-ota-rc18-2026-10-21.md).
[Current rc.20 connection captures and limitations](docs/qualification/connection-capture-rc20-2026-10-21.md).
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
