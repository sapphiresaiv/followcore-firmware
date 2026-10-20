# FollowCore-CAN v3.0.0-rc.9

Pre-release for controlled evaluation, not stable or production qualified.
S3 v3.0.0-rc.9, source `137b225014688f69308058cae84469599be63044`.
Compatible unchanged F303: v3.0.0-rc.3, source `fb9b11db6b8e532aa1353cb746daf81ad48e7969`.
Only S3 and its matching browser UI are updated.

Show concrete query failures, suggested actions and the last confirmed stage:
DNS, unreachable/refused/interrupted connections, TLS/certificate validation,
HTTP 404/403/429/5xx, response size/redirect/catalog and local device failures.
An unknown connection timeout is not blamed on the user or regional network.
No HTTP response means unknown, not successful access or proof of a bad URL.

Retain the last attempt's stage, timing, byte count and SDK/HTTP/TLS/socket codes
in RAM. An explicit read-only UPDATE GET serial request returns one Q reply;
it never starts networking, a retry, motion, logging or Flash writes. Default
serial output stays quiet. The existing maintenance N layout is unchanged.

This is diagnostic reporting, NOT a repair or qualification of the SDK's 100 ms
asynchronous connection path. SNTP success does not establish GitHub access.
First-use admission, cancellation, certificate/hostname/signature checks and
rollback remain in force. No F303, PDO, homing or current-limit change.
Direct GitHub download/install and automatic F303 updating remain unavailable.

See release-manifest.json for actual evidence and limitations. Simulated network
errors do not prove physical MCU Internet access or regional reliability. Use
the matching signed image and browser package; do not erase NVS or guess flash
addresses. MCU source, private keys, ELF and raw captures are excluded.

Support: sapphiresaiv@gmail.com; Douyin: dys5roelfesy.
Download the accompanying third-party notices. Upstream licenses remain valid.
