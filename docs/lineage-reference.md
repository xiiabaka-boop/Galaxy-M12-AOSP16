# LineageOS references for Galaxy M12 (research only)

Target: SM-M127F, Android 13 vendor (SDK 33), Treble enabled, ARM64, dynamic partitions, no reported slot suffix. These are user-observed values, not independently verified.

## Reviewed sources
- https://github.com/exynos850-dev/old_device_samsung_m12/tree/lineage-19.1
- https://github.com/exynos850-dev/old_device_samsung_exynos850-common/tree/lineage-19.1
- https://github.com/exynos850-dev/old_vendor_samsung_exynos850-common
- https://github.com/LineageOS/android_kernel_samsung_exynos850

Old M12 BoardConfig.mk includes common Exynos850 config, density 280, resolution 720x1600, and lineage_m12_defconfig.
Old M12 device.mk inherits common.mk, includes fingerprint keylayout and OTA assert for f12,m12.
Old common BoardConfigCommon.mk specifies arm64, Exynos850/universal3830, Samsung dynamic partitions (odm/product/system/system_ext/vendor), and vendor-specific Bluetooth, Wi-Fi, RIL, keymaster, SELinux and VINTF settings.

**Caution:** These are older LineageOS 19.1-era trees; they are NOT validated Android 16 GSI patches. Their static super partition size and security settings MUST NOT be copied into an Android 13 stock device without examining its real partition table and firmware. Never transplant vendor blobs, SELinux policy, AVB flags, or kernel blindly.

## Work plan
1. Inspect actual Android 13 vendor and partition metadata (read-only).
2. Compare stock VINTF HAL versions and kernel against Android 16 framework requirements.
3. Collect sanitized boot logs from a recoverable test environment.
4. Only then implement targeted, reversible changes, with explicit evidence and tests.

No compatibility modifications are currently applied. No boot success claimed.
