# Controller-side version checking

The S3 `v3.0.0-rc.5` candidate adds an explicit **Check updates** operation on
the S3 itself. The browser mirror only displays the S3 result. The installed
`v3.0.0-rc.3` did not have this operation; do not mistake local hotspot upload
for Internet version checking.

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

Ordinary Wi-Fi, hotspot and version checks require a valid homing reference,
confirmed travel limits, a safe main state and a stopped axis within 0.1 mm of
MinPost. The existing CAN owner's fresh stationary evidence is still required.
The program does not move the axis to acquire this qualification. Wired
isolation recovery is separate and does not grant wireless permission.

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

The update page and explicit serial mirror retain the latest result, HTTP
status, SDK error, TLS/mbedTLS error, certificate flags and socket errno.
HTTP 0 means no HTTP response was obtained. Codes identify the observed failure,
not proof of a particular ISP, country, hardware fault or motor-driver refusal.
Network-check errors are not CAN EMCY/motion faults and do not write a motor
fault snapshot to Flash. Default serial operation remains quiet.

Any failed check clears the previous comparison result. It must never say
"already latest" on failure. Both components are reported as latest only if
both current versions are known and exactly match their selected public entries.
The supported F303 version is read once per peer session through read-only
standard 100A:00; missing metadata is not a new motor/homing qualification.

This stage checks versions and displays notices. Direct GitHub download/install
and automatic F303 updating are **not implemented**. Keep the signed local
hotspot/qualified wired update workflows available.
