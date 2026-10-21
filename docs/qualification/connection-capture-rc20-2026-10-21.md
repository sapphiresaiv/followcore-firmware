# Retained connection evidence acceptance — 2026-10-21

Controller rc.20 is installed. rc.21 is its exact VERSION-only OTA target,
published but not installed. Compatible F303 rc.3 is unchanged. No driver
serial access, enable, motion, homing or parameter write was requested.

## Build and bootstrap evidence

- rc.20 original source: `b183bacff562738e734d4c683455b034605aefb9`.
- rc.21 original source: `d4f1e70e8065aa1cc0083bab2db4439c820f8354`.
- rc.20 signed image SHA256:
  `882a2da057bd271a7986cfcdcb0b73ccae53ae954c4756af4772ce5614da5c39`.
- rc.21 signed image SHA256:
  `de87980f9c46933f396853f5f46e8d0ede18814903a14b3f762ae6f9bcf24ad2`.
- Both images are 2,379,776 bytes. Signature, exact application descriptor,
  frozen source identity and unchanged fixed RSA-3072/PSS trust were checked.
  A stale rc.21 incremental application descriptor was rejected before packaging;
  a clean rebuild passed. The rejected incremental image was not published or flashed.
- rc.20 full regression: 114 C++ ASAN/UBSAN groups plus protocol, Python,
  signing, feedback and actual pinned-SDK contract adjuncts passed. rc.21 changes
  VERSION only; this is not a separate claimed full functional run for rc.21.
- Actual SDK connection replay passes 10 scenarios, async error forwarding and
  captured/max-length HTTP request construction. Hooks preserve errno and are
  scoped to the maintenance worker. Parser/wire/privacy/collector tests passed.
- Qualified wired bootstrap installed rc.20 into inactive ota_0, preserving
  the previous VALID rc.18 slot, partition table, NVS and reserved data. SDK
  first-boot confirmation was observed. CAN remained off, driver disabled and
  maintenance locked. The browser bundle is unchanged from rc.16.
- Initial one-shot NETTRACE export returned both empty channels correctly.
  Subsequent real failed queries were exported after their observer leases ended;
  cleanup did not erase the evidence. No continuous text-log mode is required.
- Classified source commits/tags are pushed. All six assets of each public
  prerelease were independently downloaded and SHA256-checked on the computer
  before advancing the testing catalog to rc.21. That computer uses a proxy;
  its successful downloads do not establish the ESP32's direct reachability.

## Three actual native catalog queries

Saved Wi-Fi connected. AliDNS remained selected; no resolver, deadline, retry,
TLS policy or network routing was changed during the captures. The actual URL
was the normal fixed-repository catalog on `raw.githubusercontent.com`.

| Attempt | Actual connect target | Proven progress | Terminal evidence |
| --- | --- | --- | --- |
| 1 | 185.199.110.133:443 | DNS succeeded; TCP ready about 382 ms after HTTP-hop start | TLS never completed before deadline; ESP 0x107; total job 22,231 ms including preparation |
| 2 | 185.199.110.133:443 | DNS succeeded; TCP started but was not confirmed ready | ESP 0x7002, TLS 0x8004, socket errno 113 (EHOSTUNREACH); total job 20,014 ms |
| 3 | 185.199.108.133:443 | DNS succeeded; TCP ready about 379 ms after HTTP-hop start | ESP 0x7002, TLS 0x801A; actual log `mbedtls_ssl_handshake returned -0x0050`, connection reset; total job 11,973 ms |

All three have zero accepted HTTP request bytes, no request-line/header-sent
confirmation, zero response-header bytes and HTTP status 0. The third record's
positive stored mbedTLS error magnitude is 80; the actual SDK log supplies the
signed `-0x0050` value. The installed SDK defines this as NET_CONN_RESET, not an
HTTP refusal. A `Certificate verified` message was also emitted after that failed
handshake; it is not evidence of completed TLS or a sent GET.

These failures precede receipt of the small catalog body, so its size cannot
explain them as a slow bulk transfer. They demonstrate different connection-stage
outcomes in this finite sample, not that the URL always fails. They do not identify
which endpoint, intermediary, ISP or firmware/network condition caused a reset or
unreachable result. No HTTP 403/404/5xx refusal was received.

The new downloader record remains empty (request ID 0): this session could not
pass the normal catalog gate, so no firmware download was initiated. Previous
rc.18 download observations remain historical, not new rc.20 captures. Complete
online transfer, downloaded-image validation, installation and post-online-boot
confirmation remain **BLOCKED / NOT QUALIFIED**. No safety/version gate was bypassed.

## Diagnostic contract and handoff

The bounded observer follows the actual HTTPS operation and retains separate
query/download generations, up to four trusted hops. It observes the sockaddr
passed to connect, TCP readiness, TLS result/hostname argument, locally accepted
request bytes, expected GET/Host/terminator matches and response-header parsing.
Only a short HTTP status-line prefix is retained, not signed links, credentials,
cookies or image payload. No probe or additional request is generated.

This is not a packet capture. Local TLS write acceptance is not remote receipt;
the TLS hostname argument is not an on-wire SNI capture; a connect target alone
does not independently identify the remote system or an interception mechanism.

After a future query/download, explicitly export NETTRACE before starting another
attempt or rebooting. A new same-channel attempt replaces that channel; reset loses
RAM. Navigation and observer cleanup do not erase the retained result. The matching
source includes `tools/s3_network_capture.py` for a one-shot CRC-checked export.

Final state: rc.20, Wi-Fi connected, Version tab showing the last TLS failure,
maintenance retained, CAN off and driver disabled. Observer leases ended and S3
serial was released. No installation or automatic motion recovery was requested.
No mechanical, power-loss or long-term reliability qualification is claimed.
