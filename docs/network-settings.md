# Network settings

From S3 v3.0.0-rc.12, a successful Wi-Fi connection remembers the most recent
SSID/password pair in local NVS. Enter the password once after upgrading. The
SSID is prefilled on later use; leave the password empty to reuse the saved
password for that exact SSID. A typed password overrides it. This is one saved
network, not a multi-network manager. Failed/cancelled connections do not save,
and an unchanged pair is not rewritten. There is no automatic boot connection.

To forget the saved pair, disconnect/end network work and use **Forget network**
on the Wi-Fi tab. This removes only the application's network key, not mechanical
calibration or other settings. The maintenance lock remains until explicitly
ended. Networking/Flash actions still require the existing safety admission.

The top-bar Wi-Fi icon indicates an associated connection with an IP address,
not signal strength or verified Internet access. **AP** means the local hotspot,
not a connection to an external access point. Actual faults still open fault
history; the maintenance banner opens maintenance without releasing its lock.

Passwords are not included in status mirrors or diagnostic feedback. However,
this product configuration does **not** enable NVS/Flash encryption. Physical
Flash access can reveal stored credentials. Forgetting is logical deletion, not
guaranteed forensic erasure of wear-levelled Flash. Do not save credentials for
a sensitive network if this model is unacceptable. A storage error can leave
physical persistence uncertain; it is not reported as a motor/CAN fault.

Install the matching S3 browser bundle and refresh the page after updating;
older browser bundles can reject the extended read-only U mirror.

From S3 v3.0.0-rc.13 the Wi-Fi tab also offers named DNS presets:
Automatic (the router/DHCP default), AliDNS, Google Public DNS, and Cloudflare.
Select a name; no IP typing is needed. The explicit choice is saved separately
from credentials. Changing it closes idle Wi-Fi and keeps maintenance locked;
reconnect, then retry Check updates. Active queries/feedback and RF transitions
temporarily disable selection. Automatic restores the next connection's router
DNS; no Wi-Fi connection is started automatically on boot.

The update check separately identifies DNS lookup failure/timeout and later
connection/TLS/HTTP failures. Engineering lookup evidence is retained for an
explicit serial diagnostic read, not a continual serial stream. A resolved IP
is not proof that HTTPS or GitHub works. These presets use ordinary plaintext
DNS, not encrypted DNS or a guarantee against interception. A provider's name
does not select a country endpoint. HTTPS certificate/hostname checks stay on.

Use rc.14 or later for DNS presets. In rc.13, attempting to clear an empty DNS
slot through ESP-NETIF returned `0x5001`; the same mistake during restoration
could leave closing in a retry loop. rc.14 clears empty slots using lwIP's
documented operation on its TCP/IP thread and verifies the result. Nonempty
addresses still use ESP-NETIF. Connecting to the saved network does not require
a preliminary scan. rc.13 is withdrawn from the testing catalog; its original
release assets remain immutable for diagnosis.

The rc.34 functional base (also included in the rc.104 OTA target) separates the
Wi-Fi-page connectivity lamp from association and from OTA validation. Recent
successful connectivity probes or accepted HTTPS response data keep it green.
Background rechecks preserve recent success; waiting/checking without fresh
evidence is amber. Disconnect clears the evidence immediately. A failed probe
without recent success is red, labelled as a failed check rather than proof that
every Internet endpoint is inaccessible. A long job without new receive data
does not keep a stale green forever. No standalone probe competes with OTA.

No GitHub/Microsoft-specific public DNS accelerator is configured. GitHub states
that its [IP addresses change](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/about-githubs-ip-addresses);
hard-coding them is not a supported reliability fix. Microsoft's Azure resolver
168.63.129.16 is [VNet-scoped](https://learn.microsoft.com/en-us/azure/dns/dns-troubleshoot),
not a public device resolver. Existing DNS presets may help name resolution;
they do not guarantee that a later TCP/TLS connection will succeed.
