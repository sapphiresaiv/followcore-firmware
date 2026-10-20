# Getting started

1. Identify the hardware and control variant. The current product is
   FollowCore-CAN with ESP-V3.003 controller hardware.
2. Read [safety](safety.md) and the release's compatibility metadata.
3. Obtain the matching S3 controller and F303 driver packages from Releases.
4. Check the SHA256 values and follow the component-specific update procedure.
5. After an update, complete the required local recovery and homing procedure
   before testing motion. Firmware updates do not automatically resume motion.

The controller's USB mirror and the F303 commissioning console are separate
applications. They connect to different serial devices. Do not open a serial
device from two tools simultaneously.

Serial browser applications require a compatible Web Serial browser. Serve the
S3 controller UI from localhost; do not open its WASM page directly as a file.
An example for an extracted controller UI directory is:

```sh
python3 -m http.server 8765 --bind 127.0.0.1
```

Open `http://127.0.0.1:8765/`, then explicitly select the S3 serial device.
Connecting a commissioning tool is not authorization for unattended motion.
