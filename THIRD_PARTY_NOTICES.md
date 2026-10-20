# Third-party notices

FollowCore's own firmware is not published as open source. That does not change
the licenses, copyrights, or permissions of third-party components embedded in
the firmware or browser applications.

The accompanying `licenses/` directory preserves notices for ESP-IDF,
CANopenNode, STM32 HAL/USB, CMSIS, LVGL, LovyanGFX and its upstream notices,
FreeRTOS, lwIP, mbedTLS, newlib, cJSON, SPIFFS, wpa_supplicant, Montserrat, Font
Awesome, and the FollowCore UI font subsets. Components remain under their
respective terms; the publisher's personal-use notice does not override them.

The UI bitmap subsets `ui_font_chinese_16` and `ui_font_action_18` are renamed
derivatives of Adobe Source Han Sans SC Regular/Medium, release commit
`a4f7cf94edfb9d7ffbdfc4841de276358bd7e0f2`. They remain under the SIL Open Font
License 1.1, including Adobe's copyright notice in
[followcore-ui-font-ofl.txt](licenses/followcore-ui-font-ofl.txt).
These subsets replace the earlier PingFang-generated ones in this release.

Starting with S3 v3.0.0-rc.10, FollowCore modifies two ESP-IDF 5.5 compilation
units under their existing Apache-2.0 license: `components/esp-tls/esp_tls.c`
(asynchronous connection descriptor-set rearming and socket error checks) and
`components/tcp_transport/transport_ssl.c` (asynchronous error forwarding).
These are FollowCore changes, not an upstream release or endorsement. Original
Espressif copyright and license notices remain applicable.

Selected source locations:

- https://github.com/espressif/esp-idf
- https://github.com/CANopenNode/CANopenNode
- https://github.com/STMicroelectronics/stm32f3xx-hal-driver
- https://github.com/STMicroelectronics/stm32-mw-usb-device
- https://github.com/lvgl/lvgl
- https://github.com/lovyan03/LovyanGFX
- https://github.com/adobe-fonts/source-han-sans
- https://github.com/JulietaUla/Montserrat
- https://github.com/FortAwesome/Font-Awesome

License copies and notices accompany the release assets. This inventory is
distribution documentation, not a claim of legal certification or endorsement
by any upstream author.
