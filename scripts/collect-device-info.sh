#!/system/bin/sh
# Read-only diagnostic output; inspect before sharing.
echo "Galaxy M12 compatibility diagnostics"
for key in ro.product.model ro.product.device ro.product.vendor.device ro.treble.enabled ro.vndk.version ro.product.cpu.abi ro.boot.slot_suffix ro.boot.dynamic_partitions ro.vendor.build.version.sdk ro.boot.verifiedbootstate; do
  printf '%s=' "$key"; getprop "$key"
done
echo "Mapped partitions:"
ls -l /dev/block/mapper 2>/dev/null | grep -E 'system|vendor|product|odm|super' || true
echo "Physical super:"
ls -l /dev/block/by-name/super 2>/dev/null || true
echo "NOTE: Do not share serial numbers, IMEI, or personal identifiers."
