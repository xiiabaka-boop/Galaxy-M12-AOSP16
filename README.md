# Galaxy M12 SM-M127F × AOSP Android 16 (experimental research)

**Current status: hardware study and read-only analysis, not a bootable custom ROM.**
This repository does not contain an Android 16 build that has been tested on the M12. No flashing instructions, boot image, AVB change, proprietary driver injection or kernel patch has been validated.

## Known target facts (from owner's Termux)

| Item | Observed |
| --- | --- |
| Model | Samsung Galaxy M12 SM-M127F |
| Stock Android & vendor API | Android 13 / SDK 33 |
| ABI | arm64-v8a |
| Project Treble | true |
| Dynamic partitions | true |
| Slot suffix | empty; actual layout still needs checking |
| Super block | /dev/block/mmcblk0p31 |
| Stock firmware, kernel & VINTF | **not yet inspected** |

## Base release

- [AOSP 16 GSI .img.xz in GitHub Releases](https://github.com/xiiabaka-boop/Galaxy-M12-AOSP16/releases/tag/aosp16-base)
- Filename: `aosp-arm64-ab-vanilla-16.0-20250625.img.xz`
- Expected SHA-256: `f3abc15e85fb3d8050881c0710259f8e12baf8fd5cf05598e672073b7816c831`
- Observed compressed size: 882,462,536 bytes; XZ reports ~2,346.8 MiB uncompressed.
- Preliminary workflow `Validate AOSP 16 GSI` **succeeded**: archive digest and decompression check passed; header identifies Linux ext-family filesystem.

## Workflows

1. [Validate AOSP 16 GSI](.github/workflows/validate-gsi.yml) — verify hash, XZ, filesystem header. Requires URL and SHA input.
2. [Analyze AOSP 16 GSI filesystem](.github/workflows/analyze-gsi.yml) — download and verify the fixed Release, extract the full image, mount it **read-only** on the disposable GitHub runner, inventory properties and system-side VINTF XML, publish a small report artifact. Runs on workflow creation and manually.

The second workflow intentionally does **not** upload the ~2.3 GiB image as an artifact or publish a purported ready-to-flash ROM. GitHub-hosted runners have limited temporary disk space.

## Device reference trees

- [LineageOS 21 M12 notes](docs/lineage-21-reference.md) — newer M12 device configuration reviewed from source.
- [Older LineageOS 19.1 Exynos850 notes](docs/lineage-reference.md) — historical reference only.
- [Stock facts](device/m12-stock-facts.json) — observed, not verified from stock firmware dump.

**A device tree used to compile a complete LineageOS ROM is not an Android 16 GSI vendor driver pack.** Hardware services usually depend on the existing firmware's `vendor`, `odm`, kernel, SELinux and VINTF compatibility.

## To continue toward real device compatibility

Gather the **exact firmware build** and *read-only* vendor VINTF XML and filesystem/partition metadata on the physical M12. Use `scripts/collect-device-info.sh` for a brief property report. Compare VINTF in the stock firmware with the GSI system matrix, then investigate any actual incompatibility. Before trying a device image, ensure recovery/download mode and verified backups are available.

Do **not** flash a system image from this repository yet: success of integrity or file inspection is not proof it will boot.
