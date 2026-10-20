# Troubleshooting

- **No serial connection:** close other serial owners, verify the selected MCU
  and USB cable, and use the matching UI. Do not kill unrelated applications.
- **Maintenance after an update:** this is the upgrade motion lock. Follow the
  local exit/recovery procedure; re-home before motion.
- **Firmware rejected:** check hardware, component, signed-image type, size,
  version pairing, and download integrity. Do not disable verification.
- **Motion or homing fault:** stop further automatic retries. Preserve the
  original error, firmware versions, and available diagnostic records.
- **Communication timeout:** record the exact object/frame/error and context.
  A timeout alone does not establish whether the controller, driver, bus,
  physical power, or test tool caused it.

Fault windows from a low-rate computer logger are not equivalent to the
controller's high-rate internal recording. Report the capture method and gaps.
Remove credentials and identifying data before attaching logs to public Issues.
