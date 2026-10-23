# FollowCore-CAN v3.0.0-rc.47

Controller-only candidate for controlled evaluation, not a stable release.
Controller source: `8505a64d601fd577fe616abef2e09e2a3c07b7de`.
Requires the existing paired F303 v3.0.0-rc.9,
source `097229879d01770e2f155a7f151164d0baaff05c`.
The driver is unchanged and is not included or automatically updated.
Compatibility with the older public rc.3 driver is not qualified.

## Changes

- Require referenced mechanical travel before load/electrical calibration;
  laser calibration is not a prerequisite. Keep existing safety and mutual
  exclusion gates and electrical-calibration endpoint clearance.
- Show load and electrical qualifications independently. A changed electrical
  fingerprint invalidates the old PID qualification, not the verified new
  electrical result itself.
- Add explicit Confirm use and return to mechanical zero. Verify/apply saved
  parameters, then use the existing native enable/return route to the already
  referenced MinPost. This is not another contact-homing cycle.
- Do not restore stale PID parameters when explicitly using verified new
  electrical parameters. Retain the old record for rollback/reference.
- Reject duplicate confirmation and stale-owner return/stop requests; manual
  intervention, cancellation, timeout and faults do not resume motion.
- Include the matching browser UI with append-only read-only status fields.
  Refresh/replace the browser bundle only after the controller upgrade.

## Updating

Use `followcore-can-s3-v3.0.0-rc.47-ota.bin` for either the controller's local
hotspot uploader or explicit online Download/validate followed by Install/restart.
It is a signed application image, not a full first-flash/USB recovery image.
Keep maintenance admission, HTTPS/signature checks, exact size/hash checks,
inactive-slot installation and SDK first-boot/rollback protections enabled.
If the currently installed firmware refuses maintenance admission, stop there;
this package does not bypass that refusal. Do not erase calibration/NVS or guess
flash addresses. Updating itself does not resume motion.

The testing catalog now points to rc.47 instead of the historical rc.104 OTA
exercise target. Existing immutable rc.100/104 assets are retained. A device
actually running rc.100/104 will not treat rc.47 as a newer version; do not force
an online downgrade. This test is intended for the currently installed rc.44.

## Validation and limitations

122 C++ ASan/UBSan groups plus ancillary checks, four trace-enabled groups,
native UI and two WASM configurations passed. Clean ON/OFF builds, fixed-key
signature/provenance and selected local stack-frame gates passed; these are not
complete worst-case timing/stack or machine-safety proofs.

The published image has optional calibration diagnostics compiled in for this
controlled test. It is 2453504 bytes with SHA256
`b1b668224fe897210c644ff41eb6499a1ee6b6e5dac506b7153d250f3ffce45c`.
F303 loops, motion profile/current limits, partitions, eFuses and signing trust
are unchanged. No driver binary, private source/keys, ELF or raw logs are included.

rc.47 has not yet been flashed or mechanically accepted. The old controller's
normal wired upgrade refused maintenance standstill before reset/write; the
operator will test OTA. Regional Internet reachability, loaded behavior,
power-loss and long-term reliability remain unqualified. See release-manifest.json
for exact evidence. Download the accompanying notices; upstream licenses apply.

Support: sapphiresaiv@gmail.com; Douyin: dys5roelfesy.
