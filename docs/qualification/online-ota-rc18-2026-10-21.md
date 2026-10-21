# Corrected online OTA request acceptance — 2026-10-21

Controller rc.18 is installed. rc.19 is its VERSION-only online exercise target.
F303 rc.3 remains unchanged. No F303 serial access, enable, motor target,
homing or parameter change was requested in this task.

## Correction and host evidence

- rc.18 original source: `35211229d65b7f8ecbedb93c0f00f7cd2934b842`.
- rc.19 original source: `94bf56d99c058189b843f407ea273bff92728d9b`.
- rc.18 signed BIN SHA256:
  `5730b53f938e4b71470187fdedf920a65c0bcd005da507378ba7fa8742fdfaf5`.
- rc.19 signed BIN SHA256:
  `937671ba3d3f2b78e1fddbce2ab8ac69991546716c8d65d27140ce7aece848e7`.
- Both signed files are 2,375,680 bytes. Exact app descriptor, frozen source
  identity and unchanged fixed RSA-3072/PSS trust were independently checked.
- Full functional-base regression passed: 113 C++ ASAN/UBSAN groups plus the
  runner's protocol/Python/signing/pinned-SDK/feedback adjuncts. rc.19 has only
  VERSION changed, not a separate claimed 113-group functional run.
- A new production test fails the old 512-byte TX setting for a captured-length
  957-byte GitHub URL / 928-byte request line. The unchanged installed SDK helper
  also reproduces it. Corrected 2,048-byte TX passes captured and maximum-allowed
  URL lengths; all URLs are checked before initialization. Async polling clears
  stale errno. Host allowlist, size bound, CA/hostname checks and signing remain.
- Errors identify connection, request, response or receive stage; logs include
  hop/host without signed queries. Per-hop/total/receive deadlines are bounded.
- Classified CAN source commits and rc.18/19 tags are pushed. All six assets per
  public prerelease were fetched and SHA256-checked before advancing the testing
  catalog to rc.19. A preliminary mispointed source-export tag was withdrawn
  before release; final source tags were checked against their VERSION content.

## Actual device evidence

Qualified wired bootstrap installed rc.18 into inactive ota_1 while preserving
the VALID rc.16 slot, partitions, NVS and reserved data. SDK first-boot confirmation
was observed; serial bad CRC count was zero. CAN remained off, drive disabled,
startup recovery/maintenance lock retained. The browser bundle is unchanged.

Saved Wi-Fi connected through native UI. The native version check succeeded:
current rc.18, available rc.19, Update controller enabled.

Three explicit native download attempts were bounded and failed before any image
body was received. None emitted `Out of buffer`:

| Attempt | Last confirmed stage | Evidence |
| --- | --- | --- |
| 1 | github.com, hop 0, response | Request sent; HTTP -1 / ESP 0x7004 / TLS 0x8008 (transport reports clean FIN) before complete response; 0 bytes |
| 2 | github.com, hop 0, connecting | 20-second deadline / ESP 0x107; HTTP/TLS/errno 0; 0 bytes |
| 3 | github.com, hop 0, connecting | ESP 0x7002 / TLS 0x8004 / errno 113, EHOSTUNREACH (no route to host); 0 bytes |

Certificate-validation text in attempt 2 does not prove the remaining handshake
completed. FIN and unreachable reports do not identify the remote cause, provider
or censorship mechanism. A PC replay using the same HTTP/1.1 headers/user-agent
downloaded rc.19 with matching SHA256, but that PC uses VPN and is not an equivalent
ESP32 network path.

The capacity correction is proven by actual SDK host replay, but these device
attempts never reached redirected-request transmission. Complete online transfer,
downloaded-image verification, activation and post-online-boot confirmation remain
**BLOCKED / NOT QUALIFIED**. Do not substitute wired bootstrap or PC download for
that result. No power-loss, mechanical or long-term qualification is claimed.

## Handoff

Running controller remains rc.18, native Version tab shows rc.19 and a connection
failure. Maintenance is retained, CAN off, drive disabled, no active drive error
or EMCY in the final snapshots. The observer stopped and released the serial port;
no install or boot selection was requested. rc.19 is published, not installed.

Use a network that directly reaches GitHub Release endpoints, then explicitly retry
Update controller → Download and validate. Only after Verified, confirm Install
and restart. Do not weaken TLS/signature checks, pin a temporary signed URL, or
automatically release maintenance/resume motion.
