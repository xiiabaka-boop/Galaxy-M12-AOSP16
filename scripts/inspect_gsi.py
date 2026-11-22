#!/usr/bin/env python3
"""Generate a read-only report from an already mounted GSI filesystem.

No vendor blobs, identifiers or system files are copied to artifacts.
This is a structural report, NOT a runtime VINTF compatibility test.
"""
import argparse
import json
from pathlib import Path
import xml.etree.ElementTree as ET

KEYS = (
    "ro.build.version.release", "ro.build.version.sdk",
    "ro.build.version.codename", "ro.build.version.security_patch",
    "ro.system.build.version.release", "ro.system.build.version.sdk",
    "ro.product.cpu.abi", "ro.product.system.cpu.abi",
    "ro.build.type", "ro.zygote", "ro.sf.lcd_density",
    "ro.treble.enabled", "ro.vndk.version"
)

def properties(path):
    result = {}
    try:
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            if "=" in line and not line.lstrip().startswith("#"):
                key, value = line.split("=", 1)
                key = key.strip()
                if key in KEYS:
                    result[key] = value.strip()
    except (OSError, UnicodeError):
        pass
    return result

def read_vintf(path):
    try:
        root = ET.parse(path).getroot()
        halnames = sorted({n.text.strip() for n in root.findall(".//hal/name")
                           if n.text and n.text.strip()})
        return {
            "file": str(path),
            "root_tag": root.tag,
            "type": root.get("type"),
            "level": root.get("level"),
            "hal_count": len(halnames),
            "hal_names": halnames[:80]
        }
    except (OSError, ET.ParseError) as exc:
        return {"file": str(path), "error": str(exc)}

def report_image(root, out):
    facts = json.loads((Path(__file__).resolve().parent.parent / "device/m12-stock-facts.json").read_text())
    # Some system-as-root GSIs put build.prop under system/; others do not.
    build_candidates = [
        root / "build.prop",
        root / "system/build.prop",
        root / "system/etc/build.prop",
        root / "system_ext/etc/build.prop",
        root / "product/etc/build.prop",
    ]
    found_props = {}
    for p in build_candidates:
        if p.is_file():
            found_props[str(p.relative_to(root))] = properties(p)
    # Android releases move generated properties between partitions.
    # If fixed locations don't expose an SDK, scan other small *.prop
    # files and prop.default, without copying any proprietary content.
    if not any(found_props.values()):
        candidates = list(root.rglob("*.prop")) + list(root.rglob("prop.default"))
        for p in sorted(set(candidates)):
            try:
                if p.is_file() and p.stat().st_size <= 1024 * 1024:
                    matched = properties(p)
                    if matched:
                        found_props[str(p.relative_to(root))] = matched
            except OSError:
                pass
    vintf = []
    for prefix in ("etc/vintf", "system/etc/vintf", "system_ext/etc/vintf", "product/etc/vintf"):
        folder = root / prefix
        if folder.is_dir():
            for f in sorted(folder.glob("*.xml")):
                info = read_vintf(f)
                info["file"] = str(f.relative_to(root))
                vintf.append(info)
    features = {}
    for name in ("system/apex", "apex", "system/etc/selinux", "etc/selinux",
                 "system/etc/init", "etc/init", "system/etc/permissions"):
        p = root / name
        features[name] = {"exists": p.exists(),
                          "entries": len(list(p.iterdir())) if p.is_dir() else 0}
    sdk = next((v.get("ro.build.version.sdk") or v.get("ro.system.build.version.sdk")
               for v in found_props.values() if v.get("ro.build.version.sdk") or v.get("ro.system.build.version.sdk")), None)
    warnings = [
        "Treble / VNDK / ARM64 alone does not establish Android 16 boot compatibility.",
        "Stock vendor Android 13 VINTF and the kernel remain uninspected.",
        "LineageOS device trees are reference material, not drop-in GSI driver packages.",
        "No image patch, flash command, vendor extraction or boot test was performed."
    ]
    if not found_props:
        warnings.append("No build.prop found in the expected paths; inspect filesystem layout.")
    if not vintf:
        warnings.append("No VINTF XML located inside the system image.")
    if sdk and sdk != "36":
        warnings.append("Observed GSI SDK is not 36, expected for Android 16: " + sdk)
    result = {
        "image_type": "GSI system filesystem, mounted read-only",
        "target": facts, "detected_gsi_sdk": sdk,
        "build_properties": found_props, "vintf": vintf,
        "directories": features, "warnings": warnings
    }
    out.mkdir(parents=True, exist_ok=True)
    (out / "analysis.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    lines = [
        "# AOSP Android 16 GSI: structural inspection",
        "",
        "**Device:** Samsung Galaxy M12 SM-M127F",
        "**Stock vendor:** Android 13 / SDK 33 (user-observed)",
        "**GSI SDK (if present):** " + str(sdk or "not found"),
        "",
        "## Build properties"
    ]
    for path, props in found_props.items():
        lines.append("### `" + path + "`")
        lines += ["- `" + k + "`: `" + v + "`" for k,v in sorted(props.items())]
    lines.append("")
    lines.append("## System-side VINTF documents")
    for item in vintf:
        lines.append("- `" + item["file"] + "`: " +
                     ("parse error: " + item["error"] if "error" in item else
                      "type=" + str(item["type"]) + ", level=" + str(item["level"]) +
                      ", HAL names=" + str(item["hal_count"])))
    lines += ["", "## Directory presence"]
    lines += ["- `" + k + "`: " + ("yes" if v["exists"] else "no") +
              " (" + str(v["entries"]) + " entries)" for k,v in features.items()]
    lines += ["", "## Limitations"] + ["- " + w for w in warnings]
    (out / "analysis.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    if not args.root.is_dir():
        parser.error("--root must be a mounted directory")
    report_image(args.root.resolve(), args.out.resolve())
