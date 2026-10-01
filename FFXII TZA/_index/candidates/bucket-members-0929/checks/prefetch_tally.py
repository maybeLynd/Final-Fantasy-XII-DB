"""prefetch_tally.py - DATA cross-check: which bucket files any shipped prefetch list names (9,351 lists under
prefetchdata/). it/events/338.txt is the one list carrying the boot-time kind-9/kind-7 set. Positive controls:
files the code requests at boot (map_ref, test_area_ref, Item_Clut, summoneffectdata, battle_pack) must appear.
license_chip is requested by code (00561663) but only in the license menu, so its absence shows the list is NOT
exhaustive: absence here corroborates, it does not prove."""
import os, glob
from common import check, finish
root = "D:/FFXII_TZA_extract/prefetchdata"
lists = [p for p in glob.glob(root + "/**/*", recursive=True) if os.path.isfile(p)]
print("lists:", len(lists))
text = {p: open(p, "rb").read().lower() for p in lists}
names = ["fhmusicdata", "test_map_ref", "test_area_ref", "menu_version", "license_chip", "item_clut", "shop_data.bin",
         "wepjob_matrix", "commandpack", "battle_pack", "map_ref.bin", "mapjumpgroupflagrom", "summoneffectdata"]
hits = {n: [p for p, t in text.items() if n.encode() in t] for n in names}
for n in names: print(f"  {n:22s} {len(hits[n])} list(s) {[os.path.relpath(p, root) for p in hits[n]][:3]}")
for n in ("map_ref.bin", "test_area_ref", "item_clut", "summoneffectdata", "battle_pack", "mapjumpgroupflagrom"):
    check(f"control: {n} named by a prefetch list", len(hits[n]) >= 1)
for n in ("fhmusicdata", "test_map_ref", "menu_version", "shop_data.bin", "wepjob_matrix"):
    check(f"{n} named by no prefetch list", not hits[n])
check("negative control: license_chip (code-requested in the license menu) is also absent -> lists are not exhaustive", not hits["license_chip"])
finish()
