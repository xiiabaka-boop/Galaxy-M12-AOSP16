# Galaxy M12 AOSP 16 GSI — experimental

Target: Samsung Galaxy M12 SM-M127F. Base image: `aosp-arm64-ab-vanilla-16.0-20250625.img.xz`.

**This is not a tested or device-adapted ROM. Do not flash the output without verifying Treble support, partition layout, firmware/vendor compatibility and recovery options.** Unlocking a bootloader and flashing can erase data or brick a device.

## Workflow

1. Publish the original XZ file as a GitHub Release asset, ideally with tag `aosp16-base`.
2. Open Actions → Validate AOSP 16 GSI → Run workflow.
3. Enter the HTTPS download URL of the release asset and its SHA-256 checksum.
4. Workflow downloads, verifies, extracts, checks Android sparse/raw ext4/EROFS signatures, and uploads a small report. It does **not** flash or patch the image.

GitHub-hosted runners have limited disk space; the workflow deliberately avoids repacking or publishing a huge image as an artifact.

## Device checks

Before adapting, collect `getprop ro.product.device`, `getprop ro.treble.enabled`, `getprop ro.boot.slot_suffix`, `getprop ro.vndk.version`, `getprop ro.product.cpu.abi`, and partition information. Never share identifiers such as IMEI or serial numbers.
