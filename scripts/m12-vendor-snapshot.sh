#!/system/bin/sh
# Read-only stock-vendor inventory for Galaxy M12 SM-M127F.
# Run with Termux: sh scripts/m12-vendor-snapshot.sh
# For files inaccessible to the normal shell, you may run the same script with su.
# Never include IMEI, serial number, account data, modem/EFS/persist dumps.
set -eu
OUT="${1:-$HOME/m12-vendor-snapshot}"
mkdir -p "$OUT/vintf/vendor" "$OUT/vintf/odm"
{
  echo '# Galaxy M12 read-only stock vendor diagnostics'
  for key in \
    ro.product.model ro.product.device ro.product.vendor.device \
    ro.treble.enabled ro.vndk.version ro.product.cpu.abi \
    ro.boot.slot_suffix ro.boot.dynamic_partitions \
    ro.vendor.build.version.sdk ro.vendor.build.version.release \
    ro.build.version.release ro.build.version.sdk \
    ro.build.version.incremental ro.boot.verifiedbootstate \
    ro.boot.vbmeta.device_state; do
    printf '%s=' "$key"
    getprop "$key"
  done
  printf 'kernel_release='
  uname -r
  echo '# super symlink'
  ls -l /dev/block/by-name/super 2>&1 || true
  echo '# logical partition mapping'
  ls -l /dev/block/mapper 2>&1 || true
} > "$OUT/properties.txt"

for partition in vendor odm; do
  SRC="/$partition/etc/vintf"
  DEST="$OUT/vintf/$partition"
  if [ -d "$SRC" ]; then
    for file in "$SRC"/*.xml "$SRC"/manifest/*.xml "$SRC"/compatibility_matrix/*.xml; do
      [ -f "$file" ] || continue
      base=$(basename "$file")
      case "$file" in
        */manifest/*) name="manifest-$base" ;;
        */compatibility_matrix/*) name="matrix-$base" ;;
        *) name="$base" ;;
      esac
      if ! cp "$file" "$DEST/$name" 2>/dev/null; then
        echo "Cannot read $file; run with appropriate read permission" >&2
      fi
    done
  fi
done

echo "Collected diagnostic files in: $OUT"
echo "Review the contents before sharing. No partitions or system files were modified."
