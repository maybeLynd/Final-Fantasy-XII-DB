"""restatus22.py - owner re-status batch 22: the shop-table page PARTIAL -> DOCUMENTED (OPUS, 2026-10-01).
Byte-preserving, idempotent. Prints PATCHED / ALREADY and FAILS n."""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "..", "..", "..", "12-Items-Equipment-Shops-License", "the-shop-table-and-its-stock-gates.md")
OLD = "status: PARTIAL — the three list-interface questions are answered 2026-09-30"
NEW = ("status: DOCUMENTED — every register row the page names is answered and its prose residue is closed (owner "
       "re-status 2026-10-01, OPUS, batch 22): the three list-interface questions are answered 2026-09-30")
fails = 0
b = open(P, "rb").read()
o, n = OLD.encode("utf-8"), NEW.encode("utf-8")
if n in b:
    print("ALREADY")
elif b.count(o) != 1:
    print("REFUSING (%d)" % b.count(o)); fails += 1
else:
    open(P, "wb").write(b.replace(o, n)); print("PATCHED")
print("FAILS", fails)
sys.exit(1 if fails else 0)
