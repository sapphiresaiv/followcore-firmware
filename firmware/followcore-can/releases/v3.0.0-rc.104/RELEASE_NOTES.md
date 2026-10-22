# FollowCore-CAN v3.0.0-rc.104

Controller OTA test target for the locally installed v3.0.0-rc.34.
The frozen MCU source differs from rc.34 only in VERSION. This candidate
includes the same fixes; it is not the older rc.100 functional snapshot.

- Keep the network indicator green while accepted HTTPS data is arriving.
  Background checks do not erase recent connectivity evidence. Waiting/checking
  without fresh evidence is amber; disconnect or a failed check is red.
- Expire old receive evidence; DNS queries, outgoing traffic and TLS handshake
  bytes do not prove a working HTTP data path. No extra concurrent OTA probe.
- Preserve an observed startup communication EMCY in the fault history before
  local maintenance suspends confirmation. No automatic drive fault clearing.
- During maintenance, the home action opens Network maintenance instead of
  offering Recover control and then refusing it. Exit maintenance explicitly
  before recovery; interrupted motion is not resumed.
- Retain compact KB/MB progress and passive, on-demand TLS diagnostics. Keep
  TLS certificates, fixed signing trust, exact size/hash/version checks,
  inactive-slot writes, explicit install confirmation and boot rollback.

Controller only. Installed F303 v3.0.0-rc.5 is unchanged; this release does not
include a driver download. CAN is the supported control type; no Pulse/EtherCAT
support or conformance certification is claimed. No motor parameter, homing
threshold, current-limit, partition or signing-key change.

Validation: rc.34's functional candidate passed 116 ASan/UBSan host groups and
adjuncts, followed by affected final-review tests, native LVGL/WASM UI tests and
a qualified wired rc.34 startup. This rc.104 version-only image has its own
frozen build, signature and artifact checks. A PC download does not certify
regional ESP32 connectivity. rc.34-to-rc.104 online installation remains for
operator acceptance; mechanical, power-loss and long-term reliability are not
qualified by this release. See release-manifest.json for exact evidence.

Support: sapphiresaiv@gmail.com; Douyin: dys5roelfesy.
Accompanying notices contain applicable upstream licenses.
