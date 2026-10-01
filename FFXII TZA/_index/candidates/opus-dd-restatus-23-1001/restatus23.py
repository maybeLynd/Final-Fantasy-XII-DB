"""restatus23.py - owner re-status batch 23 (OPUS, 2026-10-01): adjudicate ORACLE's two RC-17 corrections for FABLE (both
hold at the bytes), carry the adjudication into the native-command-lifecycle page and the map-ctrl page, and move the
native-command-lifecycle page REOPENED -> DOCUMENTED. Byte-preserving, idempotent; PATCHED / ALREADY, FAILS n."""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..", "..")
NCL = os.path.join(ROOT, "01-Script-VM-Native-Bridge", "Native-Command-Lifecycle", "native-command-lifecycle.md")
MAP = os.path.join(ROOT, "03-World-Area-Field", "Map-Pack", "the-map-ctrl-pack.md")
ADJ = ("adjudicated 2026-10-01 by OPUS for FABLE: both corrections hold at the bytes - `00360880` runs managers 1 to 3 "
       "(`ebx`), scans bits 0-7 of each mask from `022CB9C4` (`bt` loop `003608A0`-`003608AA`) and calls `00360710` once, at "
       "the first set bit (`003608B0`); `003604A0` returns dword `[022CB738 + (n + 8m)*16]`, the begun word "
       "([record](../../_index/candidates/opus-dd-restatus-23-1001/README.md))")
EDITS = [
    (NCL, "the entry's begun word, not the player's skip; `00228130`'s trigger is bit 13 of `[[0209AC30] + 0x400]`. **FABLE adjudication pending** on the corrections.",
     "the entry's begun word, not the player's skip; `00228130`'s trigger is bit 13 of `[[0209AC30] + 0x400]`. ~~**FABLE adjudication pending** on the corrections.~~ "
     "*(Corrections " + ADJ + ".)*"),
    (NCL, 'status: "REOPENED — SECTION-11 trigger resolved (accepted by a non-author review 2026-09-29) and the page returns through the owner read;',
     'status: "DOCUMENTED — every register row the page names is answered; owner read and re-status 2026-10-01 (OPUS, batch 23): the SECTION-11 trigger is resolved (accepted by a non-author review 2026-09-29);'),
    (NCL, "(RC-17, answered by FABLE; ORACLE's corrections pending FABLE's adjudication)",
     "(RC-17, answered by FABLE; ORACLE's two corrections adjudicated by OPUS 2026-10-01, both hold)"),
    (MAP, "`00360880` (bit-scans `dword[02CB9C4]`, dispatches `00360710(member=bitIdx, group=arg)`);",
     "`00360880` (~~bit-scans `dword[02CB9C4]`, dispatches `00360710(member=bitIdx, group=arg)`~~ for managers 1 to 3, finds "
     "the lowest set bit of `dword[022CB9C4 + 4*(m-1)]` and calls `00360710(member=bit, group=m)` once per manager - "
     "*corrected 2026-10-01, OPUS, on ORACLE's RC-17 correction, read at `003608A0`-`003608B0`*);"),
]
fails = 0
cache = {}
for path, old, new in EDITS:
    b = cache.get(path) or open(path, "rb").read()
    o, n = old.encode("utf-8"), new.encode("utf-8")
    if n in b:
        print("ALREADY", os.path.basename(path), old[:40]); cache[path] = b; continue
    if b.count(o) != 1:
        print("REFUSING (%d) %s: %s" % (b.count(o), os.path.basename(path), old[:60])); fails += 1; cache[path] = b; continue
    cache[path] = b.replace(o, n); print("PATCHED", os.path.basename(path), old[:40])
if not fails:
    for path, b in cache.items():
        open(path, "wb").write(b)
print("FAILS", fails)
sys.exit(1 if fails else 0)
