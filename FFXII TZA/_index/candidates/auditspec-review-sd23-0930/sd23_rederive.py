"""sd23_rederive.py - SWE2-AUDIT-SPEC independent re-derivation for SD-23 (2026-09-30), not through retool.
(1) Walk .rdata for every vtable whose [vt-8] is an MSVC x64 complete-object locator naming a class that ends in
    "Sound@Driver@Sd@SQEX" (all Sound-family classes, primary and secondary vtables), and print slots 38 / 39.
(2) Raw census of `call qword ptr [reg + 0x130]` / `[reg + 0x138]` in the audio range 007A0000..00800000 (linear
    decode of listed functions) - site count against the record's 16 / 2.
(3) The instructions after the two sites whose table row names a zeroed register (007BDBD6, 007BED8E)."""
import sys, re, struct
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk
FALSE, TRUE = 0x007E57B0, 0x007E5800
def rtti(vt):
    col = tk.u64(vt - 8)
    if not col or tk.off(col) is None or tk.u32(col) != 1: return None
    td = tk.BASE + tk.u32(col + 0x0C)
    o = tk.off(td + 0x10)
    if o is None: return None
    n = tk.d[o:o + 160].split(b"\0")[0].decode("latin1")
    return n if n.startswith(".?A") else None
va, vs, rs, ro = tk.secs[".rdata"]
fam = []
for off in range(0, rs - 8, 8):
    vt = va + off + 8
    q = struct.unpack_from("<Q", tk.d, ro + off)[0]
    if not (va <= q < va + vs): continue
    n = rtti(vt)
    if n and n.endswith("Sound@Driver@Sd@SQEX@@"):
        fam.append((vt, n))
def nm(a): return {FALSE: "false", TRUE: "true"}.get(a, "%08X" % a if a else "none")
print("Sound-family vtables found: %d" % len(fam))
for vt, n in fam:
    print("  %08X %-45s slot38 %s slot39 %s" % (vt, n, nm(tk.u64(vt + 38 * 8)), nm(tk.u64(vt + 39 * 8))))
print("stub bodies:", " | ".join("%08X: %s" % (a, "; ".join("%s %s" % (x.mnemonic, x.op_str) for x in tk.dis(a, a + 4))) for a in (FALSE, TRUE)))
sites = {0x130: [], 0x138: []}
for e, sz in tk.flist:
    if not (0x007A0000 <= e < 0x00800000): continue
    try: body = tk.fdis(e)
    except Exception: continue
    for x in body:
        if x.mnemonic == "call":
            m = re.match(r"qword ptr \[r\w+ \+ (0x130|0x138)\]$", x.op_str)
            if m: sites[int(m.group(1), 16)].append((x.address, e))
for k, v in sites.items():
    print("call [reg + %#x]: %d sites: %s" % (k, len(v), " ".join("%08X/%08X" % s for s in v)))
for a in (0x007BDBD6, 0x007BED8E):
    print("--- after %08X" % a)
    for x in tk.dis(a - 8, a + 0x30)[:14]:
        print("  %08X %s %s" % (x.address, x.mnemonic, x.op_str))
# raw byte sweep, all of .text: FF /2 mod=10 (call [reg+disp32]) with disp 0x130 / 0x138, incl. REX.B (41 FF) and SIB forms
import re as _re
t = tk.d[tk.TRO:tk.TRO + tk.TRS]
for disp in (0x130, 0x138):
    pat = _re.compile(b"\xff[\x90-\x97]" + struct.pack("<I", disp) + b"|\xff\x94[\x00-\xff]" + struct.pack("<I", disp), _re.S)
    hits = [tk.TVA + m.start() for m in pat.finditer(t)]
    ins = [h for h in hits if tk.dis(h, h + 7) and tk.dis(h, h + 7)[0].mnemonic == "call"]
    aud = [h for h in ins if 0x007A0000 <= h < 0x00800000]
    print("raw FF-call disp %#x in 007A0000..00800000: %d: %s" % (disp, len(aud), " ".join("%08X" % h for h in aud)))
    print("raw FF-call disp %#x: %d byte hits, %d decode as call, owners %s" % (disp, len(hits), len(ins), sorted(set("%08X" % (tk.owner(h)[0] or 0) for h in ins))))
print("--- after 007BED8E")
for x in tk.dis(0x007BED8E, 0x007BEDB0): print("  %08X %s %s" % (x.address, x.mnemonic, x.op_str))
