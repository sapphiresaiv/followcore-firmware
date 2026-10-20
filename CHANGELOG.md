# Changelog

## v3.0.0-rc.13 — FollowCore-CAN S3 only

Withdrawn from the testing catalog: selecting a preset can fail setup with
`0x5001` and leave network closing stuck. IDF 5.5 rejects empty DNS entries;
the rc.13 host stub missed this SDK restriction. Use automatic-DNS rc.12 until
the corrected candidate is verified. Existing signed assets remain immutable.

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
