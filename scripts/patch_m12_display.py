#!/usr/bin/env python3
"""Apply narrowly scoped SM-M127F display tuning to an already writable GSI mount.

In-place update preserves build.prop inode ownership, permissions and SELinux xattrs.
The value 300 comes from the M12 LineageOS 21 BoardConfig.mk; it may differ from
the owner's preferred stock density. No vendor, kernel, SELinux or AVB changes.
"""
import argparse
import re
from pathlib import Path

PROPERTY = "ro.sf.lcd_density"
VALUE = "300"

def patch_file(path: Path):
    if not path.is_file():
        raise RuntimeError(f"Missing build.prop: {path}")
    data = path.read_bytes()
    lines = data.decode("utf-8").splitlines(keepends=True)
    indices = [i for i, line in enumerate(lines)
               if re.match(r"^\s*ro\.sf\.lcd_density\s*=", line)]
    if len(indices) > 1:
        raise RuntimeError("Multiple density declarations; refusing ambiguous update")
    old_value = None
    if indices:
        index = indices[0]
        old_value = lines[index].strip()
        lines[index] = f"{PROPERTY}={VALUE}\n"
    else:
        if lines and not lines[-1].endswith("\n"):
            lines[-1] += "\n"
        lines += [f"\n# Galaxy M12 SM-M127F DSU display test (LineageOS 21 density)\n",
                  f"{PROPERTY}={VALUE}\n"]
    new_data = "".join(lines).encode("utf-8")
    if new_data == data:
        raise RuntimeError("Image already has exact requested density; no changed-image build")
    # Write same inode so original file labels/mode remain intact.
    with path.open("r+b") as out:
        out.seek(0)
        out.write(new_data)
        out.truncate()
        out.flush()
    print(f"{PROPERTY}={VALUE}; previous: {old_value or '(absent)'}")
    if path.read_bytes() != new_data:
        raise RuntimeError("Failed to verify updated build.prop")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    path = root / "system/build.prop"
    patch_file(path)

if __name__ == "__main__":
    main()
