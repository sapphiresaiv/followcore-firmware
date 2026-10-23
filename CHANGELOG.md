# Changelog

## v3.0.0-rc.47 — Calibration qualification and explicit use

- Require calibrated mechanical travel, but not laser calibration, for load/electrical calibration.
- Keep independent trusted-used indicators and invalidate only records with a changed fingerprint.
- Explicitly verify/use saved parameters, then return to the existing mechanical zero through the native control route.
- Permit verified new electrical parameters without restoring a stale PID record; reject late-owner requests.
- Include the matching browser UI and optional calibration diagnostics for controlled testing.
- Existing paired F303 rc.9 is required, unchanged and not included; older public driver pairing is not qualified.
- Build/host/UI/signature checks passed. rc.47 installation, mechanical use/return and online OTA remain pending operator acceptance.
- Supersede the historical rc.104 catalog target without deleting or overwriting its immutable assets.

## v3.0.0-rc.104 — Synchronized OTA target for local rc.34

- VERSION-only target of the final rc.34 controller source; retain rc.100 unchanged.
- Keep green on fresh accepted HTTPS data; background checks retain recent evidence,
  waiting/checking is amber, and true disconnect clears stale session evidence.
- Record pending observed startup communication EMCY before local maintenance
  suspends confirmation; do not automatically clear faults or enable the drive.
- Correct the home maintenance/recovery action and visibly disable jog in maintenance.
- Retain compact KB/MB progress, passive TLS diagnostics and all OTA trust gates.
- Installed F303 rc.5 is unchanged and not included. No homing/current/partition changes.
- rc.34 host/UI/wired startup evidence is recorded; rc.34-to-rc.104 online installation
  is pending operator acceptance, not claimed passed by PC asset verification.

## v3.0.0-rc.100 — Controller online OTA test target

- Advance from the locally installed rc.32 to rc.100; simplify the network success label to "网络已连接".
- Add numeric rc.100/rc.32 and future v3.1.0 ordering plus native wording regressions.
- Retain rc.32's unified Upgrade page, bounded connectivity indicator, SDK body-poll correction and UI memory/stack fixes.
- No motion, CAN/PDO, homing, current-limit, network-check policy, partition or signing-trust changes from rc.32.
- Paired installed F303 rc.5 remains unchanged and is not included; no new driver download is advertised.
- Not serial-flashed by this publication task; complete online OTA is for operator acceptance, not claimed passed.

## v3.0.0-rc.29 — Version-only target for the installed rc.28 controller

- Exact frozen source difference from rc.28 is VERSION only; generated build identity changes.
- No new motor, CAN/PDO, calibration, Wi-Fi, TLS, storage or protection changes.
- Reuse the byte-identical rc.28 browser bundle; paired installed F303 rc.5 is unchanged and not included.
- Intended for operator-run online OTA from rc.28, not a new mechanical or network qualification.

## v3.0.0-rc.21 — Connection-capture OTA exercise target

- Exact VERSION-only target of rc.20; no additional network/control changes.
- Published separately so rc.20 can exercise its native query/download workflow.
- Download validation and installation remain separate explicit actions.

## v3.0.0-rc.20 — Passive query/download connection evidence

- Retain separate bounded evidence for the latest query and firmware download.
- Observe actual connect address, TCP/TLS progress, request write and header parsing.
- One-shot NETTRACE export; no passwords, signed links, cookies or payload capture.
- No new network workaround, diagnostic probe, retry or ordinary status output.
- Preserve rc.18's request correction, TLS/signature checks and all motion gates.
- Driver rc.3, motor/CAN/PDO, homing, current limits and partition layout unchanged.

## v3.0.0-rc.19 — Corrected online OTA exercise target

- VERSION-only target on the corrected rc.18 base; exact source difference verified.
- Use rc.18 or newer for the direct GitHub download test; driver stays at rc.3.
- Download verification and installation remain separate explicit steps.

## v3.0.0-rc.18 — FollowCore-CAN online download request correction

- Correct the 512-byte TX buffer that rejects long GitHub signed redirect requests.
- Check URL/request capacity before opening a client; use 2048-byte TX and clear stale errno.
- Distinguish secure connection, request send, response wait and receive failures; retain bounded per-hop/total/idle deadlines.
- Replay the actual installed SDK builder with captured/max-size URLs; old configuration must fail.
- Controller only; unchanged driver rc.3, motor/CAN/PDO/homing/current control and fixed signing trust.
- See corrected rc.16 incident evidence in the qualification report; real rc.18/19 online acceptance is separate.

## v3.0.0-rc.17 — FollowCore-CAN online OTA exercise

- VERSION-only target based on the rc.16 implementation; motor/CAN/driver unchanged.
- Requires the rc.16 bootstrap before the controller can download it online.
- Candidate, not a production or long-term reliability qualification; see release validation.

## v3.0.0-rc.16 — FollowCore-CAN controller online OTA

- Independent controller/driver version cards, highlighted updates and scrollable catalog notes.
- Explicit signed HTTPS download into the inactive slot; exact size/SHA/project/chip/version checks.
- Separate install/restart confirmation; preserve maintenance gates, fixed trust and rollback.
- Driver rc.3 remains unchanged; no automatic driver installation or motor-control changes.

## v3.0.0-rc.15 — FollowCore-CAN S3 OTA exercise

- Version-only candidate based on rc.14; the firmware source diff is VERSION only.
- No functional fix: network reachability, TCP/TLS uncertainty and other rc.14
  limitations remain. F303 stays at rc.3 and does not require updating.
- Prepared for operator-run local-hotspot OTA; not pre-flashed or claimed as
  hardware-accepted by this release task. See the signed BIN and validation record.

## v3.0.0-rc.14 — FollowCore-CAN S3 only

- Fix rc.13 preset setup and closing stuck at `0x5001`: ESP-NETIF does not
  accept empty DNS addresses; empty entries now use a verified lwIP clear in
  the TCP/IP context, not the rejecting setter.
- Restore empty DHCP backup/fallback entries correctly; do not hide errors or
  leak a selected preset into later Automatic sessions.
- Correct the host stub and add actual SDK function replays plus 100 direct
  connect/preset/restore/close cycles. See the release's actual hardware scope.
- Keep presets/UI/wire layout, mechanical maintenance gates and F303 unchanged.

## v3.0.0-rc.13 — FollowCore-CAN S3 only

Withdrawn from the testing catalog: selecting a preset can fail setup with
`0x5001` and leave network closing stuck. IDF 5.5 rejects empty DNS entries;
the rc.13 host stub missed this SDK restriction. Use the corrected rc.14
candidate. Existing signed assets remain immutable.

- Add named Automatic, AliDNS, Google and Cloudflare presets; no IP keyboard.
- Persist the explicit choice independently; reconnect after a change, retaining
  maintenance. Reject changes during queries/feedback or RF transitions.
- Apply/read back selected servers before jobs; distinguish bounded asynchronous
  DNS lookup from later TCP/TLS/HTTP progress and retain explicit diagnostic evidence.
- Append validated N/Q tails and include the matching content-hashed web bundle
  with connection diagnostics, granted-port reuse and correct EOF cleanup.
- Preserve HTTPS verification. Plain DNS does not guarantee regional GitHub access.
- No F303, CAN/PDO, motion, homing or current-limit changes.

## v3.0.0-rc.12 — FollowCore-CAN S3 only

- Remember the last successfully connected SSID/password as one NVS record;
  prefill SSID and reuse the saved password only for that exact SSID.
- Add explicit Forget network. Keep credentials out of status/feedback mirrors,
  avoid unchanged Flash writes and do not start Wi-Fi automatically at boot.
- Show a global Wi-Fi connection icon before uptime; distinguish hotspot AP.
- Route maintenance banners to maintenance, with fresh faults taking priority.
- Add three read-only U mirror fields; refresh the matching browser bundle.
- Local NVS is unencrypted; logical forgetting is not secure physical erasure.
- Retain rc.10 async TLS correction. No driver, CAN/PDO or motion changes.
- Internal rc.11 was superseded before publication after correcting the new
  host-side screenshot fixture; immutable source snapshots were not moved.

## v3.0.0-rc.10 — FollowCore-CAN S3 only

- Correct pinned ESP-IDF async connection polling: rebuild select descriptor
  sets on every poll and resume correctly after a timeout or interruption.
- Reject actual socket/select failures before TLS and forward async connection
  error evidence to the existing HTTP diagnostics.
- Apply the hash-pinned correction only in the build directory; leave the shared
  SDK untouched and fail configuration for unreviewed SDK source changes.
- Retain polling intervals, deadlines, certificate validation, cancellation and
  maintenance safety gates. No driver, CAN/PDO, motion or homing changes.
- Host replays exercise actual SDK functions; physical MCU Internet reachability
  and regional reliability remain subject to retesting.

## v3.0.0-rc.9 — FollowCore-CAN S3 only

- Show the observed failure category, action hint and last confirmed stage for
  update queries; distinguish DNS, connection, TLS/certificate, HTTP and local errors.
- Do not blame unknown timeouts on the user's network or infer GitHub access
  from a successful time synchronization.
- Retain per-attempt timing, received bytes and SDK/error evidence in RAM, read
  once on explicit UPDATE GET without starting networking or motion.
- Keep normal serial output quiet, N-mirror layout and network/motion admission
  unchanged. No driver update, motor, PDO, homing or current-limit changes.
- This improves diagnostics; it does not repair/qualify the prior SDK asynchronous
  connection path or establish regional Internet/long-term reliability.

## v3.0.0-rc.8 — FollowCore-CAN S3 only

- Show an immediate querying label and disabled state during queued, clock and
  fetching phases; restore controls on completion/failure and reject repeat clicks.
- Keep explicit cancellation usable during queries and connection/search work.
- Reflect accepted search, connection, hotspot and feedback states immediately.
- Add consistent pressed/disabled visuals to shared buttons, including arrows,
  without changing motion-control press/release semantics.
- Retain rc.7 initial-setup networking and existing backend duplicate admission.
- No F303 rebuild, protocol layout, homing, current-limit or motor changes.
- This remains a candidate, not regional Internet or long-term qualification.

## v3.0.0-rc.7 — FollowCore-CAN S3 only

- Permit first-use networking before lead/laser calibration or homing, using
  owner-confirmed stationary feedback or proven local CAN quiescence. Unresolved
  motion still blocks networking; referenced devices still require MinPost.
- Adopt the first-boot maintenance lease without unlocking motion.
- Show Connect network on the offline Version tab and route to Wi-Fi search.
- Add direct STA/selection-to-hotspot switching under the same maintenance lease;
  identify USB recovery separately from local hotspot upload.
- Reduce normal diagnostics to initialization, hardware, communication and
  control summaries. Keep detailed engineering evidence in explicit diagnostics.
- Remove engineering-oriented user prompts. Preserve navigation locks and
  explicit cancellation, signed image validation and rollback checks.
- No F303 update, motor algorithm, PDO layout, homing or current-limit changes.
- This remains a candidate, not mechanical or long-term qualification.

## v3.0.0-rc.5 — FollowCore-CAN S3 only

- Add explicit MCU-side HTTPS version checks, optional testing releases and
  independent S3/F303 version comparisons. Direct download/install is not included.
- Report HTTP 404/403/429/50x, DNS, timeout, TLS/certificate and catalog failures
  on the update page and explicit serial diagnostics, not as CAN/motor faults.
- Require a safe, homed and stationary MinPost before ordinary networking;
  page navigation retains the motion lock until explicit cancellation.
- Keep wired recovery separate; no wireless isolation bypass. Defer ordinary
  parameter saves while maintenance owns the system.
- Read optional standard 100A driver software metadata once per peer session;
  missing metadata does not revoke motor/homing eligibility.
- Keep the compatible F303 at rc.3 without algorithm/PDO/current-limit changes.
- Host/UI/build and safe boot observations passed; MCU Internet connectivity,
  TLS peak runtime stacks, mechanical and long-term behavior are not qualified.

## v3.0.0-rc.3 — FollowCore-CAN

- Identify both controller and driver software as FollowCore-CAN.
- Add public support email, Douyin account, and repository information.
- Add explicit product/variant/control-type fields to controller feedback;
  retain receiver compatibility with older reports.
- Retain the S3 rc.2 manual latest-direction handoff fix.
- Replace the controller's previously generated PingFang subsets with renamed
  bitmap subsets derived from OFL-licensed Source Han Sans.
- Identify the driver through its existing standard read-only `100A:00`
  software-version object, without changing PDO mappings or drive identity.
- Publish matching controller/driver artifacts with checksums and compatibility
  metadata. Motion algorithms and safety thresholds are not changed here.

Status: release candidate. See each release for actual validation and deployment
evidence; do not infer mechanical or long-term acceptance from build success.
