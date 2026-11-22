# Android 16-labelled M12-common tree: additional research

A newer community source was reviewed directly:

- [varifocal / android_device_samsung_m12-common (branch a16-lts)](https://github.com/varifocal/android_device_samsung_m12-common/tree/a16-lts)
- [BoardConfigCommon.mk](https://github.com/varifocal/android_device_samsung_m12-common/blob/a16-lts/BoardConfigCommon.mk)
- [common.mk](https://github.com/varifocal/android_device_samsung_m12-common/blob/a16-lts/common.mk)
- [Exynos850 kernel source, a16-ci](https://github.com/varifocal/android_kernel_samsung_exynos850/tree/a16-ci)
- [Vendor source repository (lineage-23.2)](https://github.com/varifocal/android_vendor_samsung_m12-common/tree/lineage-23.2)

## Relevant observations

- Branch names suggest Android 16 work, but **this is not independent proof of a successful Galaxy M12 SM-M127F Android 16 boot**.
- The shared tree includes Exynos850 boot-header and kernel configurations, Samsung keymaster, Bluetooth, Wi-Fi, camera, proprietary-vendor dependencies and display services.
- It sets `AB_OTA_UPDATER := false`; the user's blank slot suffix and stock dynamic-partition property are consistent with researching A-only layout, but require actual partition inspection.
- `common.mk` references Samsung audio HAL behavior (stock Samsung server) and a newer HWC3/SLSI display stack: both are relevant to incompatibility investigations.
- Crucially, some bring-up settings include `androidboot.selinux=permissive`, `ro.adb.secure=0` and USB debugging enabled at boot. **These weaken device security and MUST NOT be copied into a general-purpose user image.**
- These makefiles are for compiling a *device-specific ROM and vendor stack*. They cannot be directly overlaid as text into an arbitrary GSI `system.img` to solve missing firmware services.

## Decision for this project

Keep this tree as a **reference**, use its HAL/service definitions to guide comparison, and preserve Android secure defaults until an actual, device-tested compatible build is available. Do not inject or publish vendor binaries without confirming redistribution permission. Do not change AVB, recovery or super partition automatically.

Next hard evidence required: the SM-M127F stock Android 13 vendor manifest/matrix, exact firmware and recovery path, and GSI Android 16 system-side VINTF from the new read-only analysis.
