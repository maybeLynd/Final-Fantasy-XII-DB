"""SWE2-AUDIT-SPEC independent re-derivation of the 24A680 local retirement guards from the shipping EXE
(the packet's checker reads only the retained listing; this reads the image). Read-only.
python rg_indep.py > rg_indep.out
"""
import sys, json, hashlib
ROOT = r"C:\Users\Kristian\source\repos\XIIOnline"
sys.path.insert(0, ROOT + r"\Database\Tools\work\FABLE\takebacks")
import tk
RAW = json.load(open(ROOT + r"\Database\Tools\work\FABLE\pub140-scratch\tools\rawcalls.json"))
print("EXE sha256", hashlib.sha256(tk.d).hexdigest())
def A(v): return v if isinstance(v, int) else v.address
def ripdst(x):
    for op in x.operands:
        if op.type == 3 and op.mem.base == 41: return x.address + x.size + op.mem.disp
    return None
def dump(e, lo=None, hi=None):
    out = []
    for x in tk.fdis(e):
        if lo is not None and not (lo <= x.address < hi): continue
        t = ripdst(x)
        out.append("   %08X %-10s %-22s %s%s" % (x.address, x.bytes.hex(), x.mnemonic, x.op_str, (" -> %08X" % t) if t else ""))
    return out

print("== R1 24A680 full body (owner %s, fsize %s)" % (tk.fname(0x24A680), tk.fsize(0x24A680)))
body = list(tk.fdis(0x24A680)); raw = b"".join(bytes(x.bytes) for x in body)
print("   decoded bytes %d, sha256 %s" % (len(raw), hashlib.sha256(raw).hexdigest()))
print("\n".join(dump(0x24A680)))
print("   reads/writes of [reg+0x38] in body:", [("%08X" % x.address, x.mnemonic, x.op_str) for x in body if "+ 0x38]" in x.op_str])
print("   stores in body:", [("%08X" % x.address, x.mnemonic, x.op_str) for x in body if x.operands and x.operands[0].type == 3 and x.mnemonic not in ("cmp", "test")])

print("== R2 pool arithmetic")
base, cnt = 0x208F580, 0x2090780
print("   base + 64*0x48 = %08X (counter %08X) equal=%s" % (base + 64 * 0x48, cnt, base + 64 * 0x48 == cnt))
print("   ticket pool 02090790 - counter = %d bytes; 12*0x20 = %d -> ticket pool ends %08X" % (0x2090790 - cnt, 12 * 0x20, 0x2090790 + 12 * 0x20))

print("== R3 249580 ticket allocator (fsize %s)" % tk.fsize(0x249580))
print("\n".join(dump(0x249580)))

print("== R4 394070 caller: mode argument and pointer source")
print("\n".join(dump(0x394070, 0x394080, 0x3940B0)))
print("   raw callers of 24A680:", RAW.get("24A680"))

print("== R5 who touches the counter 02090780 and the pool base 0208F580..02090780 (rip + image-base forms)")
for lo, hi, nm in ((cnt, cnt + 4, "counter"), (base - 8, base + 8, "pool head/base")):
    rr, rawonly = tk.rip_refs(lo, hi)
    print("   %s rip refs %d:" % (nm, len(rr)))
    for r in rr:
        a = A(r[0]); x = r[1] if not isinstance(r[1], int) else None
        print("      %08X %-18s %s  [%s]" % (a, x.mnemonic if x else "", x.op_str if x else "", tk.fname(a)))
    dr = tk.disp_refs(lo - 0x120000, hi - 0x120000)
    print("   %s image-base-relative refs %d; raw-only rip %d" % (nm, len(dr[0]) if isinstance(dr, tuple) else len(dr), len(rawonly)))

print("== R6 helpers: 3697F0 entry (NULL handling), 1B1C00, 1B1440 span, 181610 head")
print("\n".join(dump(0x3697F0)[:6]))
print("   1B1C00 fsize", tk.fsize(0x1B1C00)); print("\n".join(dump(0x1B1C00)))
b14 = list(tk.fdis(0x1B1440)); print("   1B1440 fsize %s, decoded %d bytes, last %08X %s" % (tk.fsize(0x1B1440), sum(x.size for x in b14), b14[-1].address, b14[-1].mnemonic))
print("   181610 calls:", [("%08X" % x.address, x.op_str) for x in tk.fdis(0x181610) if x.mnemonic == "call"])

print("== R7 249210 member source (cross-check with the member-notification route)")
print("\n".join(l for l in dump(0x249210, 0x249228, 0x249260)))

print("== R8 the other counter reference, and stores to +0xC8 in 394070")
for x in tk.fdis(0x24A4E0):
    if 0x24A580 <= x.address <= 0x24A590: print("   %08X %-8s %s" % (x.address, x.mnemonic, x.op_str))
st = [("%08X" % x.address, x.mnemonic, x.op_str) for x in tk.fdis(0x394070) if "0xc8]" in x.op_str]
print("   394070 fsize %s; operands naming +0xC8: %s" % (tk.fsize(0x394070), st))

print("== R9 retained manifest body hashes vs the shipping EXE bytes (the retirement checker reads no image)")
man = json.load(open(ROOT + r"\Database\FFXII TZA\_experiments\evidence\title-retirement-local-guards\section04-title-member-source\original_body_manifest.json"))
for b in man["bodies"]:
    e = int(b["entry"], 16); o = tk.off(e); z = tk.d[o:o + b["bytes"]]
    print("   %s %4dB exe-sha==manifest %s" % (b["entry"], b["bytes"], hashlib.sha256(z).hexdigest() == b["sha256"]))
