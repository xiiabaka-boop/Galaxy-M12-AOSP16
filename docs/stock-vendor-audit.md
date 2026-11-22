# SM-M127F stock vendor: offline diagnostic audit (2026-11-22)

This page summarizes a **user-provided, read-only** vendor VINTF snapshot. Only normalized technical findings are published; **the original device archive and its raw property file were not uploaded**.

## Observed facts

| Item | Observation |
| --- | --- |
| Intended target | Samsung Galaxy M12 SM-M127F |
| Android/vendor SDK | 13 / API 33 |
| Vendor codename | `m12` |
| VNDK | 33 |
| Main device VINTF target FCM | **5** |
| Main device VINTF kernel target | 5 |
| Main device SELinux policy version | 33.0 |
| Reported kernel release | `4.19.111-physwizz+` |
| Android build ID | `M127FXXS9DXJ1` |
| Bootloader report | `orange` (unlocked / unverified boot state) |
| Dynamic partitions | enabled; mapper includes `system`, `vendor`, `product`, `odm` |
| Product identity | **the `ro.product.model` and `ro.product.device` properties do not match M12 while `ro.product.vendor.device` reports `m12`** |

The last item may be caused by Magisk property spoofing or another modification. It is **not evidence the physical device is a different model**; firmware ID and vendor codename are more consistent with M12. Confirm with owner before testing.

## VINTF inspection

- 37 XML files from `/vendor/etc/vintf` and `/odm/etc/vintf` parsed successfully (32 vendor, 5 ODM SKU variants).
- The vendor XML declarations include Samsung audio, camera, GNSS, graphics composer/allocator, keymaster, radio, sensors and Wi-Fi HALs.
- Important versions in the actual main vendor manifest include audio **HIDL 6.0**, graphics composer **HIDL 2.2**, graphics allocator **HIDL 4.0**, keymaster **HIDL 4.0**, and GNSS **HIDL 2.1**.
- Some additional services come from VINTF fragments; not all ODM SKU variants can be assumed to be active simultaneously.
- The device's vendor compatibility matrix includes `vendor-ndk` version 33 and `system-sdk` version 30.

## What this means for an Android 16 GSI

**Do not compare the Android 16 FCM 202504 requirements directly against this device as if it were a new Android 16 launch device.** The shipping vendor manifest declares target FCM 5. Android chooses the matching compatibility matrix for the device's target level, plus applicable optional HALs at later levels. See [Android VINTF matching rules](https://source.android.com/docs/core/architecture/vintf/match-rules) and [FCM lifecycle](https://source.android.com/docs/core/architecture/vintf/fcm).

The existing GSI structural report found `compatibility_matrix.5.xml`, `.6.xml`, `.7.xml`, `.8.xml`, `.202404.xml` and `.202504.xml`. Presence of those files is encouraging **but does not prove VINTF compatibility**. Need a complete check using actual XML, product/system_ext VINTF overlays, framework manifest and kernel configuration. Static HAL name overlap is not a valid replacement for `checkvintf`.

## Critical missing evidence before modification

1. Confirm why product-model properties appear spoofed and whether Magisk modules are changing props/HALs.
2. Confirm a tested recovery strategy, full firmware download availability and backup.
3. Verify Android 16 GSI's **FCM 5** requirements, the custom kernel's config and compatibility.
4. Decide on a specific, evidence-based patch. Do **not** transfer an old LineageOS vendor stack, disable SELinux/AVB, or resize super blindly.
5. Only after these checks attempt a recoverable hardware test.

**Status: diagnostic complete, static compatibility not established, no patched image or successful boot test.**
