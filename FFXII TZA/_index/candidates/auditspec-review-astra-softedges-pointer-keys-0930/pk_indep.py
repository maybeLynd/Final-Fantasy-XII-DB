"""SWE2-AUDIT-SPEC independent re-derivation for ASTRA pointer-key packet (a50f9dea4). Read-only on the EXE.
Dumps the exact windows the packet's claims rest on, straight from the image via tk.py (section-aware)."""
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), r"..\..\..\..\Tools\work\FABLE\takebacks"))
import tk
import hashlib
print("EXE sha256", hashlib.sha256(tk.d).hexdigest())
def win(owner_hint, lo, hi, tag):
    o = tk.owner(lo)
    e = o[0] if isinstance(o, tuple) else o
    print("== %s  window %08X..%08X  owner %s" % (tag, lo, hi, tk.fname(lo)))
    for x in tk.fdis(e if isinstance(e, int) else owner_hint):
        if lo <= x.address <= hi:
            print("  %08X %-6s %s" % (x.address, x.mnemonic, x.op_str))
# 1. getter bytes
o = tk.off(0x0016D680); print("16D680 bytes", tk.d[o:o + 4].hex())
# 2. 632A10 body: where arg7 ([rsp+0x38] at entry) goes
win(0x00632A10, 0x00632A10, 0x00632B40, "632A10 member-descriptor builder")
# 3. registration call sites passing kind
for a in (0x005E48C6, 0x005E4951, 0x005EED9A):
    win(None, a - 0x40, a + 5, "registration site %08X" % a)
# 4. child link in 59B430
win(0x0059B430, 0x0059B900, 0x0059B945, "59B430 child link")
# 5. guard 59EC40
win(0x0059EC40, 0x0059EC40, 0x0059ED20, "59EC40 guard")
# 6. 59BED0 return
win(0x0059BED0, 0x0059C0B0, 0x0059C0E8, "59BED0 return")
# 7. count read / prewrite / assignment call
win(None, 0x0059CCE0, 0x0059CD30, "59CD07 count / 59CD14 prewrite / 59CD25 call")
