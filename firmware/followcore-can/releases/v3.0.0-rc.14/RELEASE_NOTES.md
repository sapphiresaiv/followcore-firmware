# FollowCore-CAN v3.0.0-rc.14

Pre-release for controlled evaluation, not stable or production qualified.
S3 v3.0.0-rc.14, source `44537748fd119afee4899a2cdbdee2f88ddddc9a`.
Compatible unchanged F303: v3.0.0-rc.3, source `fb9b11db6b8e532aa1353cb746daf81ad48e7969`.
Only S3 requires an update. Refresh the matching browser bundle after installing.

Correct rc.13's deterministic preset/close failure (0x5001): IDF rejects
empty DNS addresses. Set nonempty entries through ESP-NETIF and clear empty
entries on the TCP/IP thread through lwIP's supported clear operation. Restore
the DHCP baseline, including empty backup/fallback entries, without ignoring
errors or leaving a preset in Automatic mode. Scan-first is not required for
a saved network. Actual SDK function replays and a 100-cycle transport test
cover the contract previously omitted by the host stub.

Choose Automatic (DHCP/router), AliDNS, Google Public DNS or Cloudflare in Wi-Fi.
No manual IP entry is required. An explicit choice is saved separately in NVS;
unchanged choices do not rewrite. Changing a choice closes idle Wi-Fi and keeps
the maintenance lock. Reconnect explicitly. No automatic boot-time networking.
Queries/feedback and RF transitions reject changes until idle.

Apply and read back the selected servers before outbound jobs. A bounded,
nonblocking DNS preflight retains the configured servers, lookup time/error and
resolved IPv4 separately from the later TCP/TLS connection. Detailed evidence
is available only on explicit serial UPDATE GET; ordinary status remains quiet.
Resolver cancellation is safe for late SDK callbacks. N and Q add read-only
tails; previous indices are unchanged and updated readers accept old frames.

Retain HTTPS hostname, time and CA verification. Do not pin a GitHub IP or
downgrade HTTP. Ordinary plaintext DNS is not encrypted DNS, an anti-poisoning
guarantee or proof that GitHub will be reachable on a given network.
The existing browser link diagnostics, unique granted-port selection, EOF
cleanup and content-hashed resource bundle are included.

No F303 rebuild, CAN/PDO, motion, homing or current-limit changes.
Direct device download/install and automatic F303 updating remain unavailable.
See release-manifest.json for actual tests, hardware scope and limitations.
Use the signed S3 OTA image; do not erase NVS or guess Flash addresses.

Support: sapphiresaiv@gmail.com; Douyin: dys5roelfesy.
Download the accompanying third-party notices. Upstream licenses remain valid.
