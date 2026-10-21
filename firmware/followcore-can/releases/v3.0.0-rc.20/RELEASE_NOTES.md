# FollowCore-CAN v3.0.0-rc.20

Candidate for controlled connection diagnosis, not production qualification.
Controller v3.0.0-rc.20, source `b183bacff562738e734d4c683455b034605aefb9`.
Compatible F303 v3.0.0-rc.3 is unchanged at its original release.

Add retained passive evidence to the existing query and download connections.
The explicit NETTRACE GET diagnostic exports separate bounded records for the
latest catalog query and firmware download. Observe the actual connect target,
TCP readiness, TLS result, request-line/Host comparison, positive transport write
count and response header progress. Keep only a short HTTP status-line prefix;
do not retain passwords, signed redirect queries, cookies or firmware payload.

The observer follows the actual job, without additional requests or probes.
Ordinary status mirrors remain unchanged; no continuous diagnostic printing.
This is not packet capture: local transport acceptance does not prove remote
receipt, and a connection timeout alone does not identify censorship or a server
refusal. Query and download use different endpoints and must be assessed apart.
Evidence persists in RAM until the next same-channel job or controller reset.

Retain rc.18's long-request correction and all existing DNS, deadlines, retry,
HTTPS CA/hostname, fixed RSA-3072/PSS, image size/hash/version and rollback gates.
There is no new network workaround or claim of repaired regional reachability.
No driver, motor/CAN/PDO, homing, current-limit or partition changes.
The matching browser bundle is byte-identical to rc.16.

See release-manifest.json for the exact host/build and hardware scope. Mechanical,
power-loss and long-term reliability are not qualified by these diagnostics.
Use the signed controller OTA image; do not erase NVS or bypass verification.

Support: sapphiresaiv@gmail.com; Douyin: dys5roelfesy.
Download the accompanying third-party notices. Upstream licenses remain valid.
