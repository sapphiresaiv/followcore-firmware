# Controller online OTA acceptance — 2026-10-21

Scope: FollowCore-CAN controller ESP-V3.003, rc.16 bootstrap and rc.17 target.
Driver rc.3 is unchanged. No driver serial access, enable, homing, CAN target,
motor tuning or mechanical test was performed in this acceptance task.

## Published artifacts and source

- rc.16 original frozen source: `799deb82e53b4479e55f59edb6e52328e4d3b33e`.
- rc.17 original frozen source: `616fd5f75c2773e5638f7eba536c77f14900e312`.
- Commit-to-commit source difference: `VERSION` only.
- Both signed files are 2,375,680 bytes. Fixed RSA-3072/PSS trust, application
  descriptor/project/chip/source identity and release provenance checks passed.
- All six assets for each prerelease were fetched publicly and SHA256-verified
  before advancing the testing catalog. The catalog has exact signed-file size
  and SHA256. Source and binary repositories have matching component tags.
- One incremental rc.17 output had a stale rc.16 SDK application descriptor;
  the independent manifest guard rejected it before any upload or flash. The
  clean rc.17 rebuild passed. This is not a successfully installed artifact.

## Passed

- Full functional-base C++ suite: 113 groups with ASAN/UBSAN, plus the runner's
  protocol/Python/signing/pinned-SDK and feedback adjuncts.
- New transport/writer checks cover HTTPS host/redirect restrictions, bounded
  polling, wrong/truncated/oversize input, real SHA256, header rejection before
  first erase, SDK signature failure, cancellation/lease revocation and no
  automatic candidate activation.
- Native UI and normal/fixed-192KiB WASM previews cover independent component
  cards, full bounded catalog summaries, scrolling/page buttons, confirmation,
  progress, disabled repeat clicks, authoritative mirror and legacy clearing.
- Qualified wired rc.14-to-rc.16 bootstrap completed into the inactive slot;
  current slot, NVS, partitions and reserved data preservation checks passed.
  SDK first-boot confirmation was observed. CAN remained off, driver disabled,
  startup recovery/maintenance lock retained. Serial observer reported zero bad CRCs.
- Actual rc.16 device/browser displayed independent controller/driver cards and
  the complete paged catalog notes. It later queried rc.17 successfully and
  enabled Update controller. Driver version remained unknown while the deliberate
  first-boot local maintenance lease kept CAN off; no latest-version claim was made.
- Both explicit native download attempts passed running-image fixed-key signature
  verification and reported a valid existing rollback candidate. Failure remained
  visible and the update could be explicitly requested again without clearing faults.

## Blocked / not passed

Real rc.16-to-rc.17 online installation **did not complete**. Each of two native
download attempts ended in about 20 seconds with `ESP_ERR_TIMEOUT (0x107)`, HTTP 0,
TLS/mbedTLS/flags/errno 0 and received/written bytes 0. No install confirmation or
boot selection was requested. The running controller is still rc.16.

These codes do not distinguish TCP connection from TLS handshake, and cannot
independently prove censorship, a server problem or a firmware defect. A
VPN-enabled computer's successful release download is not an equivalent direct
ESP32 network test. Re-test on a network that can directly reach the GitHub release
download hosts. Do not weaken HTTPS/signature validation or replace this with a
computer-assisted upload and call it online OTA acceptance.

The first catalog response was the old rc.15 listing; the device correctly showed
Local newer and disabled installation. Public branch-URL headers showed a 300s
cache lifetime; the exact committed catalog already contained rc.17. Once the
branch cache refreshed, one query timed out before HTTP, then an explicit retry
received the correct rc.17 metadata. No old cached response was fabricated as new.

Real online transfer, downloaded-image verification, online activation and SDK
confirmation after that activation remain **not qualified**. Host tests and wired
bootstrap success are not substitutes. Power-interruption, loaded motion and
long-term reliability are also outside this result. Packaging-time manifests
correctly say that this later online hardware acceptance had not yet run.

## Handoff

Controller rc.16 stays in maintenance with its successful rc.17 catalog result and
visible download failure. No automatic motion recovery is attempted. The normal
workflow is: connect suitable Wi-Fi, Include testing, Check updates, Update
controller, Download and validate, then only after Verified, Install and restart.
Navigation keeps the lock; End maintenance explicitly cancels. Local signed upload
and qualified wired recovery remain available.
