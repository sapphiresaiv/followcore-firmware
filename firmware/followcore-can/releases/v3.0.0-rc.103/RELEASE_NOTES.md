# FollowCore-CAN v3.0.0-rc.103

Controller-only prerelease for controlled online OTA diagnosis, not production qualification.
Controller source `4545de5f1b7f07ce80cdcebad3acf79e0df36ac7`. Compatible installed F303 rc.5 remains unchanged and is not included.

## Changes since public rc.100

- Download progress shows percentage, received amount and catalog size in compact decimal KB/MB.
- Size is visible before the connection; failure retains the received amount and red styling.
- Owner status distinguishes resolving, connecting, TLS handshake, request, receiving and validation.
- One-shot NETTRACE adds passive handshake states/results and encrypted BIO I/O counts, without packet contents, keys or credentials.

This target differs from the locally installed diagnostic rc.102 only in VERSION and build identity.
The trace is not a new network workaround. Local socket acceptance is not proof of server receipt.
No timeout/retry/route, TLS certificate/hostname or fixed signing trust is relaxed. Motion, driver,
CAN/PDO, homing, current limits and partition layout remain unchanged. No raw logs or MCU source are public.

Choose the testing channel, download and validate first; installation/restart is a separate confirmation.
The publisher will capture one rc.102 download attempt without automatically installing this target.
See release-manifest.json for actual tests and limitations. Regional Internet access, mechanical safety,
power-loss behavior and long-term reliability are not qualified. Do not erase NVS or guess addresses.

Support: sapphiresaiv@gmail.com; Douyin: dys5roelfesy.
Download the accompanying third-party notices. Upstream licenses remain valid.
