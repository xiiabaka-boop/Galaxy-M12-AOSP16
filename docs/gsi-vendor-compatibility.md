# Comparison: AOSP 16 GSI system VINTF vs SM-M127F stock Android 13 vendor

**Status: significant static kernel/FCM incompatibility detected. No patch or boot success is claimed.**

Sources inspected:
- User-provided local VINTF snapshot (`vendor`/`odm` XML; **not published**)
- [GSI read-only GitHub Actions full-XML report](https://github.com/xiiabaka-boop/Galaxy-M12-AOSP16/actions/runs/45082254316)
- [Earlier source analysis](stock-vendor-audit.md)
- [Android VINTF kernel matching rules](https://source.android.com/docs/core/architecture/vintf/match-rules)

## Verified static comparison

| Value | User's SM-M127F | GSI system image |
| --- | --- | --- |
| Vendor image API | Android 13 / 33 | system image labelled Android 16 |
| Main device manifest target FCM | **5** | `compatibility_matrix.5.xml` exists |
| Device manifest kernel FCM | **5** | FCM 5 kernel section(s) present |
| Reported running Linux kernel | **4.19.111-physwizz+** | FCM 5 declares **5.4.61** kernel section(s) |
| FCM 5 HAL list | historical Samsung HIDL/vendor services | FCM 5 XML has **zero HAL entries**, but does specify kernel constraints |
| Framework system matrix levels | N/A | 5, 6, 7, 8, 202404, 202504 |

**Red flag:** For the selected FCM 5 matrix, the shipped GSI lists only kernel `5.4.61` requirements, while the M12 reports Linux `4.19.111`. Android's documented kernel-VINTF rule requires a kernel section with the same major.minor Linux version as the device (and a sufficient patch version). The observed **4.19 vs 5.4** pair has no match in the *system-side FCM 5 XML*. This is a likely VINTF compatibility blocker for the unmodified image/firmware pairing. This does **not** prove every possible boot path fails: full device VINTF merging, runtime config and boot tests have not been evaluated.

Do **not** "fix" this by falsifying kernel version/FCM, forcing permissive SELinux, disabling checks or blindly flashing a kernel that does not match SM-M127F hardware. Kernel/driver changes are substantially beyond an ordinary system-only GSI patch.

## Other observations

- The M12 vendor main manifest declares audio HIDL `6.0`, Exynos graphics composer HIDL `2.2`, graphics allocator HIDL `4.0`, keymaster HIDL `4.0` and GNSS HIDL `2.1`. The GSI's new-launch FCM matrices (202404/202504) mention many AIDL HALs, but **a direct comparison against those newer levels is not an appropriate pass/fail test for this older FCM 5 device**.
- Vendor audio, Wi-Fi, modem and Samsung camera services need runtime tests on the actual phone; they are not transplanted into `system.img` just by copying LineageOS makefiles.
- Vendor system SDK declarations and the GSI's system manifest need full libvintf integration testing, not just HAL-name overlap.
- Product-model properties differ from the intended M12 target, perhaps due to Magisk spoofing. Verify before flashing.
- The kernel release string includes `physwizz+`; confirm which custom kernel/boot image is actually in use and whether the owner can restore a compatible boot image.

## Required next action

1. Obtain a *read-only* kernel configuration (e.g. `/proc/config.gz` if available) plus the exact installed kernel/boot image provenance.
2. Verify a full restorable backup, Samsung Download Mode and matching official firmware.
3. Evaluate a well-documented device-specific Android 16 kernel/vendor port separately from the GSI. This is not an automatic GSI-only fix.
4. Only after a supported kernel and HAL combination is demonstrated, construct a test image or device-targeted ROM and trial it under recoverable conditions.

**Release status: no ready-to-flash ROM.**
