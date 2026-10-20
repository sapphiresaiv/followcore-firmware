# Controller-side version checking

The S3 adds an explicit **Check updates** operation on the S3 itself. The browser
mirror only displays the S3 result. In `v3.0.0-rc.7`, an offline Version tab
offers **Connect network**, opening Wi-Fi search/selection. Local hotspot upload
is separate from Internet version checking.

From `v3.0.0-rc.8`, an accepted check immediately displays **正在查询** and
disables the query button and channel selector until completion or failure.
Repeated clicks do not submit more requests. Explicit cancellation is still
available; navigation alone does not cancel a query or release maintenance.
Search, network switching and feedback controls also show their accepted busy
states, with shared pressed/disabled button visuals in both interfaces.

The public catalog is
`firmware/followcore-can/update-catalog.json`. It is ASCII JSON, at most 4096
bytes, with schema/product/variant/control/hardware identity and two channels.
`stable: null` means there is no stable release, not that the installed version
has been certified. Testing is opt-in. Component versions are independent.
Only advertise versions with already published, verified release assets.

Checks use HTTPS with certificate, hostname and date verification. No GitHub
credential is embedded. A fixed raw.githubusercontent.com URL avoids API login
and REST API quota dependencies, but does not guarantee regional connectivity.
There is no automatic mirror, certificate bypass or unbounded retry loop.
An alternative distribution host requires a separately reviewed official endpoint.

## Safety and cancellation

Before a mechanical reference exists, initial networking does not require
lead/laser calibration or motion permission. The existing CAN owner must prove
fresh stationary feedback or local CAN quiescence with no unresolved motion.
First-boot local maintenance is adopted without releasing the motion lock.
Local silence is not a measurement of mechanical position or motor health.

After a reference is established, networking still requires confirmed travel
limits, a safe main state and a stopped axis within 0.1 mm of MinPost. The
program does not move the axis to obtain this qualification. Wired isolation
recovery is separate and does not grant wireless permission by itself.

Navigation away from the page does not cancel maintenance or allow motion.
Use the explicitly labelled cancellation action. Cleanup precedes lease release;
failure, lost permission and disconnection never resume old motion.

## Failure diagnostics

| Kind | Meaning |
| --- | --- |
| 1 | Clock synchronization failed or timed out |
| 2 | HTTP 404: requested public resource was not found |
| 3 | HTTP 403/429: access restricted or requests limited |
| 4 | HTTP 500-599: remote service error |
| 5 | Other unsuccessful HTTP status |
| 6 | Connection/query timeout |
| 7 | Other connection failure |
| 8 | DNS resolution failure |
| 9 | TLS handshake or certificate failure |
| 10 | Invalid catalog or incompatible product/hardware |
| 11 | Oversized response or refused redirect |
| 12 | Allocation/client initialization failure |
| 13 | Explicit cancellation or lost local authorization |
| 14 | Local firmware version is not qualified for comparison |

The update page shows a concise failure reason and HTTP status where available.
Explicit serial diagnostics retain the SDK error, TLS/mbedTLS error, certificate
flags and socket errno; normal diagnostics show four current status summaries.
HTTP 0 means no HTTP response was obtained. Codes identify the observed failure,
not proof of a particular ISP, country, hardware fault or motor-driver refusal.
Network-check errors are not CAN EMCY/motion faults and do not write a motor
fault snapshot to Flash. Default serial operation remains quiet.

In rc.9, failure details include a suggested action and the last confirmed
stage. The public HTTP SDK confirms a completed secure connection, request sent,
headers and body; it does not expose separate successful DNS/TCP/TLS stages
before connection completion. Unknown connection timeout remains explicitly
unattributed. The previous 100 ms asynchronous connection path is not changed or
qualified by this diagnostic revision.

The private source includes `tools/s3_update_diagnostics.py` for an explicit
read-only query of the retained RAM result. Its CRC-protected UPDATE GET request
within a SYNC lease receives one numeric Q reply: boot-local attempt ID, stage,
elapsed times, bytes and SDK/HTTP/TLS/socket codes. It neither starts a query nor
retries or enables motion. A later query, maintenance session or reboot may
replace/clear the RAM evidence. No raw response, credentials or SSIDs are exported.

Any failed check clears the previous comparison result. It must never say
"already latest" on failure. Both components are reported as latest only if
both current versions are known and exactly match their selected public entries.
The supported F303 version is read once per peer session through read-only
standard 100A:00; missing metadata is not a new motor/homing qualification.

This stage checks versions and displays notices. Direct GitHub download/install
and automatic F303 updating are **not implemented**. Keep the signed local
hotspot/qualified wired update workflows available.
