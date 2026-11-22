# Galaxy M12 SM-M127F × AOSP Android 16 (experimental research)

**Current status: hardware study and read-only analysis, not a bootable custom ROM.**

**Updated after owner feedback:** an **Android 16 GSI already booted on this Galaxy M12 via DSU Sideloader**; the exact filename and source are not yet known. Our static review found a 4.19 vs 5.4 FCM kernel-section discrepancy for the **current** GSI, but that alone must not be claimed to prove Android 16 cannot boot. See [revised comparison](docs/gsi-vendor-compatibility.md). The current uploaded image remains untested on-device.
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
| Stock firmware, kernel & VINTF | **stock vendor XML and reported kernel examined**, runtime boot configuration not independently checked |

## Base release

- [AOSP 16 GSI .img.xz in GitHub Releases](https://github.com/xiiabaka-boop/Galaxy-M12-AOSP16/releases/tag/aosp16-base)
- Filename: `aosp-arm64-ab-vanilla-16.0-20250625.img.xz`
- Expected SHA-256: `f3abc15e85fb3d8050881c0710259f8e12baf8fd5cf05598e672073b7816c831`
- Observed compressed size: 882,462,536 bytes; XZ reports ~2,346.8 MiB uncompressed.
- Preliminary workflow `Validate AOSP 16 GSI` **succeeded**: archive digest and decompression check passed; header identifies Linux ext-family filesystem.
- **Origin not authenticated:** matching a SHA-256 calculated on the phone only proves that the GitHub copy matches the phone copy. We have NOT verified the original publisher's checksum or signature. This filename alone does not prove this image is an official Google GSI.

## Workflows

1. [Validate AOSP 16 GSI](.github/workflows/validate-gsi.yml) — verify hash, XZ, filesystem header. Requires URL and SHA input.
2. [Analyze AOSP 16 GSI filesystem](.github/workflows/analyze-gsi.yml) — download and verify the fixed Release, extract the full image, mount it **read-only** on the disposable GitHub runner, inventory properties and system-side VINTF XML, publish a small report artifact. Runs on workflow creation and manually.

The [first full inspection run](https://github.com/xiiabaka-boop/Galaxy-M12-AOSP16/actions/runs/45081368520) **succeeded**: ext filesystem mounted read-only, system-side VINTF matrices and APEX/init/SELinux directories were observed. A second [full inspection run](https://github.com/xiiabaka-boop/Galaxy-M12-AOSP16/actions/runs/45081601287) also succeeded. The selected SDK property remains undetected in parsed property files, so Android 16 identification currently relies on the release filename and presence of newer VINTF framework matrices; actual build provenance/version still needs independent confirmation.

The second workflow intentionally does **not** upload the ~2.3 GiB image as an artifact or publish a purported ready-to-flash ROM. GitHub-hosted runners have limited temporary disk space.

## Device reference trees

- [LineageOS 21 M12 notes](docs/lineage-21-reference.md) — newer M12 device configuration reviewed from source.
- [Android 16-labelled M12 common notes](docs/a16-port-reference.md) — newer community source; contains insecure debug settings that are NOT used.
- [Local stock vendor audit](docs/stock-vendor-audit.md) — redacted diagnostics from the owner's VINTF XML snapshot.
- [Static GSI↔vendor comparison](docs/gsi-vendor-compatibility.md) — kernel FCM 5 mismatch and follow-up checks.
- [Older LineageOS 19.1 Exynos850 notes](docs/lineage-reference.md) — historical reference only.
- [Stock facts](device/m12-stock-facts.json) — observed, not verified from stock firmware dump.

**A device tree used to compile a complete LineageOS ROM is not an Android 16 GSI vendor driver pack.** Hardware services usually depend on the existing firmware's `vendor`, `odm`, kernel, SELinux and VINTF compatibility.

## To continue toward real device compatibility

Stock vendor VINTF XML and firmware build have been examined from the user's snapshot. **First identify the Android 16 GSI already booted on the device** and compare its source and matrix with our image. Use `scripts/collect-device-info.sh` for a brief property report. Compare VINTF in the stock firmware with the GSI system matrix, then investigate any actual incompatibility. Before trying a device image, ensure recovery/download mode and verified backups are available.

Do **not** flash a system image from this repository yet: success of integrity or file inspection is not proof it will boot.
