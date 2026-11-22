# Exynos850 / Galaxy M12: newer LineageOS reference

Reviewed the following source files directly on GitHub:

- [M12 LineageOS 21 BoardConfig.mk](https://github.com/galaxym12development/android_device_samsung_m12/blob/lineage-21/BoardConfig.mk)
- [M12 LineageOS 21 device.mk](https://github.com/galaxym12development/android_device_samsung_m12/blob/lineage-21/device.mk)
- [Older M12 LineageOS 19.1 BoardConfig.mk](https://github.com/exynos850-dev/old_device_samsung_m12/blob/lineage-19.1/BoardConfig.mk)
- [Older Exynos850 common config](https://github.com/exynos850-dev/old_device_samsung_exynos850-common/blob/lineage-19.1/BoardConfigCommon.mk)

## Findings from the newer M12-specific tree

The LineageOS 21 M12 device tree inherits `device/samsung/m12-common/BoardConfigCommon.mk` and `vendor/samsung/m12/BoardConfigVendor.mk`, sets `TARGET_SCREEN_DENSITY := 300`, references `m12_defconfig`, dynamic partitions, and vendor SELinux policy.

Its device.mk references vendor mixer paths, an NFC configuration and device overlays, but the files are built as part of a full ROM, with vendor makefiles and boot/kernel context.

### Important difference

The older LineageOS 19.1 M12 tree used `TARGET_SCREEN_DENSITY := 280`, while the newer LineageOS 21 tree uses 300. **This is not evidence that either value should be patched into an existing AOSP Android 16 GSI.** It illustrates why patching blindly from an old tree is unsafe.

Likewise, the newer tree declares a super size and expects vendor components in a full device build, but this is NOT permission to overwrite the existing stock Android 13 vendor or super partition.

## Compatibility gates, in order

1. **Done:** ARM64, Treble and dynamic-partition properties from the M12 (stock Android 13).
2. **Done:** Base XZ integrity check and raw ext-family filesystem header on GitHub Actions.
3. **Next:** Extract and inspect the actual GSI filesystem; read system VINTF matrices and SDK.
4. **Pending device information:** exact stock firmware, kernel release, device VINTF, partition sizes, recoverable backup / download mode.
5. **Pending:** controlled, justified patches only where an actual discrepancy is demonstrated.
6. **Pending:** boot, radio, audio, Wi-Fi, camera and SELinux testing on the actual SM-M127F.

**No current claim of Android 16 LineageOS port or M12-compatible bootable GSI.**
