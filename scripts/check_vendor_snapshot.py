#!/usr/bin/env python3
"""Read-only audit of a user-provided M12 vendor snapshot.

Input archive stays local. Does not unpack to disk or upload personal data.
Optionally accepts analysis.json from a GitHub Actions GSI report.
Does not replace Android's checkvintf / VTS or prove boot compatibility.
"""
import argparse
import io
import json
import tarfile
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import PurePosixPath

MAX_XML_BYTES = 1024 * 1024
EXPECTED = "SM-M127F"

def read_snapshot(path):
    props = {}
    files, hal_items, parse_issues = [], [], []
    with tarfile.open(path, "r:gz") as archive:
        for entry in archive:
            if not entry.isfile():
                continue
            if entry.size > MAX_XML_BYTES:
                parse_issues.append("Skipped oversized file: " + PurePosixPath(entry.name).name)
                continue
            if entry.name.endswith("/properties.txt"):
                text = archive.extractfile(entry).read().decode("utf-8", "replace")
                for line in text.splitlines():
                    if line.startswith("ro.") and "=" in line:
                        key, value = line.split("=", 1)
                        if key in (
                            "ro.product.model", "ro.product.device", "ro.product.vendor.device",
                            "ro.treble.enabled", "ro.vndk.version",
                            "ro.vendor.build.version.sdk", "ro.boot.slot_suffix",
                            "ro.boot.dynamic_partitions", "ro.build.version.incremental",
                        ):
                            props[key] = value
                    elif line.startswith("kernel_release="):
                        props["kernel_release"] = line.partition("=")[2]
                continue
            if not (entry.name.endswith(".xml") and "/vintf/" in entry.name):
                continue
            relative = entry.name.split("/vintf/", 1)[-1]
            try:
                root = ET.fromstring(archive.extractfile(entry).read())
            except ET.ParseError as error:
                parse_issues.append(relative + ": " + str(error))
                continue
            files.append((relative, root.tag, root.attrib))
            if root.tag != "manifest":
                continue
            for h in root.findall("hal"):
                name = h.findtext("name")
                if name:
                    hal_items.append((relative, name, h.get("format") or "hidl",
                                      tuple(v.text or "" for v in h.findall("version"))))
    return props, files, hal_items, parse_issues

def inspect(props, files, hal_items, errors, gsi=None):
    vendor_base = [(path, attrs) for path, tag, attrs in files
                   if path == "vendor/manifest.xml" and tag == "manifest"]
    targets = [x[1].get("target-level") for x in vendor_base]
    names = {name for _, name, _, _ in hal_items}
    system_matrices = []
    if gsi is not None:
        system_matrices = [(v["file"], v.get("level"), v.get("hal_count"))
                           for v in gsi.get("vintf", [])
                           if v.get("root_tag") == "compatibility-matrix"]
    output = [
        "# Galaxy M12: stock-vendor XML snapshot (offline check)",
        "",
        "**Important:** This is a static XML inventory. It does NOT run checkvintf,",
        "does not test the kernel, and cannot validate booting an Android 16 image.",
        "",
        "## Stock identifiers",
        "- Intended target: " + EXPECTED,
        "- Vendor device: " + props.get("ro.product.vendor.device", "<missing>"),
        "- Vendor SDK: " + props.get("ro.vendor.build.version.sdk", "<missing>"),
        "- VNDK: " + props.get("ro.vndk.version", "<missing>"),
        "- Vendor main manifest target FCM: " + ", ".join(x or "<not set>" for x in targets),
        "- Kernel: " + props.get("kernel_release", "<missing>"),
        "- Product-model property consistent with target: " +
          ("yes" if props.get("ro.product.model") == EXPECTED else "NO (may be spoofed)"),
        "",
        "## XML overview",
        "- XML files parsed: " + str(len(files)),
        "- Manifest HAL entries across all fragments and ODM alternatives: " + str(len(hal_items)),
        "- Unique HAL names (including inactive SKU alternatives): " + str(len(names)),
        "- XML parse issues: " + str(len(errors)),
        "",
        "## Representative device HAL declarations",
    ]
    for name in (
        "android.hardware.audio", "android.hardware.camera.provider",
        "android.hardware.graphics.composer", "android.hardware.graphics.allocator",
        "android.hardware.keymaster", "android.hardware.radio", "android.hardware.gnss",
        "android.hardware.wifi", "android.hardware.sensors",
    ):
        relevant = [x for x in hal_items if x[1] == name]
        versions = sorted({v for x in relevant for v in x[3]})
        if relevant:
            output.append("- " + name + ": " + (", ".join(versions) or "versions in fqname"))
    if system_matrices:
        output += ["", "## GSI framework matrices observed"]
        for path, level, count in system_matrices:
            output.append("- " + str(level) + ": " + str(count) + " HAL names in " + path)
        if targets and "5" in targets and not any(level == "5" for _, level, _ in system_matrices):
            output += ["", "**Warning:** No FCM 5 system matrix observed; investigate."]
    output += ["", "## Interpretation and next checks",
               "- The main vendor manifest targets FCM 5, regardless of the Android 13 vendor API level.",
               "- Android VINTF compatibility is determined by exact versions, interfaces, requiredness and kernel requirements; names alone cannot prove success or failure.",
               "- Vendor XML fragments and ODM manifest SKU alternatives are NOT necessarily all active concurrently.",
               "- Next: compare full Android 16 framework FCM 5 XML and stock vendor XML using checkvintf in a controlled build environment.",
               "- Check kernel 4.19 build against framework kernel requirements, and verify a tested recovery route before any flash."]
    if errors:
        output += ["", "## Parse issues"] + ["- " + x for x in errors]
    return "\n".join(output) + "\n"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("vendor_snapshot", help="Local m12-vendor-snapshot.tar.gz")
    ap.add_argument("--gsi-analysis-json", help="analysis.json extracted from GitHub Actions artifact")
    args = ap.parse_args()
    props, files, hals, errors = read_snapshot(args.vendor_snapshot)
    gsi = json.load(open(args.gsi_analysis_json, encoding="utf-8")) if args.gsi_analysis_json else None
    print(inspect(props, files, hals, errors, gsi))

if __name__ == "__main__":
    main()
