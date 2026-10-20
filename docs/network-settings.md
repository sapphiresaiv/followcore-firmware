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
