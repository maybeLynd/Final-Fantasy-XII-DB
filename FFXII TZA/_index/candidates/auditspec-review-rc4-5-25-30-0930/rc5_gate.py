"""SWE2-AUDIT-SPEC independent check for RC-5 item 2 (rc5b-event-slot-residue-0930), 2026-09-30. Image only.
G1 raw callers (call/jmp, from the raw call index) of 00306BD0 and 00309230 - is 0030CF0D the only route in?
G2 the branch structure between the bit-30 test 0030CE93 and the call 0030CF0D (every jcc and its target).
"""
import sys, json
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk
RAW = json.load(open(r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\pub140-scratch\tools\rawcalls.json"))
for e in (0x306BD0, 0x309230):
    cs = RAW.get("%X" % e, [])
    print("G1 raw callers of %08X: %d -> %s" % (e, len(cs), " ".join("%s(in %s)" % (c, tk.fname(int(c, 16))) for c in cs)))
    rr, _ = tk.rip_refs(e, e + 1)
    rel = tk.reloc_ptrs(e, e + 1)
    print("   rip refs (lea / pointer loads): %d; relocated pointers: %d" % (len(rr), len(rel)))
print("G2 0030CE80..0030CF12:")
for x in tk.dis(0x30CE80, 0x30CF12):
    if x.mnemonic.startswith("j") or x.mnemonic in ("test", "cmp", "call", "ret") or x.address in (0x30CE93,):
        print("  %08X %s %s" % (x.address, x.mnemonic, x.op_str))
