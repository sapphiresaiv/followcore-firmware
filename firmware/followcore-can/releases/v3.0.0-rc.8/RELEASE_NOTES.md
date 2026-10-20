# FollowCore-CAN v3.0.0-rc.8

Pre-release for controlled evaluation, not stable or production qualified.
S3 v3.0.0-rc.8, source `27b66352508b6bb8f00ee1dc806916dd2bfe6f6e`.
Compatible unchanged F303: v3.0.0-rc.3, source `fb9b11db6b8e532aa1353cb746daf81ad48e7969`.
Only S3 and its matching browser UI are updated.

Accepted update checks immediately display a querying label and disable both
the button and channel selector throughout queued/clock/fetching states.
Completion or failure restores the controls. UI and backend independently
reject repeat requests; explicit cancellation remains usable during a query.
Search, connection, hotspot and feedback controls reflect accepted service
states immediately. Shared buttons have consistent pressed and disabled
visuals, including directional controls. No motion button event semantics,
network admission, wire layout, PDO, homing or current-limit changes.

First-use network setup and opt-in testing-channel checks from rc.7 are retained.
Direct GitHub download/install and automatic F303 updating are NOT implemented.
Use the matching signed image and browser package; do not erase NVS or guess
flash addresses. Private keys, MCU source, ELF and raw captures are excluded.

Actual tests and limitations are recorded in release-manifest.json. Simulated
query/HTTP errors and UI tests are not proof of regional Internet access,
mechanical safety, loaded behavior or long-term reliability.

Support: sapphiresaiv@gmail.com; Douyin: dys5roelfesy.
Download the accompanying third-party notices. Upstream licenses remain valid.
