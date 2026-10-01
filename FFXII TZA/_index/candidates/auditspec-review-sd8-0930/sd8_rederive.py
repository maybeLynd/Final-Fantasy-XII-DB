"""SWE2-AUDIT-SPEC independent re-derivation for SD-8 (2026-09-30). Read-only on the image.
  R1 every access (whole-.text rip sweep + image-base-relative disp sweep) touching the mode byte 02064AD3, including
     wider stores anchored at 02064AD0..02064AD2 whose width covers it (alias writes)
  R2 raw callers of the outside setter 00229F00 (rawcalls.json + jcc rel32 + rip refs / stored pointers)
  R3 listing of the mode-1 exit (0022B830..0022B860), the mode-5 exit (0022BDA8..0022BDCC) and the poll gate
     (0022A600..0022A660) for reading
"""
import sys, json, struct
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk
RAW = json.load(open(r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\pub140-scratch\tools\rawcalls.json"))
MODE = 0x02064AD3

hits, raw = tk.rip_refs(0x02064AC8, 0x02064AD4)
cover = []
for x, k, t in hits:
    sz = tk.memsize(x, k)
    if t <= MODE < t + sz:
        cover.append((x, k, t, sz))
print("R1 rip accesses covering 02064AD3: %d (raw-only in window %d)" % (len(cover), len(raw)))
for x, k, t, sz in cover:
    print("   %08X %-5s %-42s tgt=%08X w=%d store=%s  %s" % (x.address, x.mnemonic, x.op_str[:42], t, sz,
          tk.is_store(x, k), tk.fname(x.address)))
dh, draw = tk.disp_refs(0x02064AC8 - tk.BASE, 0x02064AD4 - tk.BASE)
print("R1 image-base-relative accesses in 02064AC8..02064AD3: %d (raw-only %d)" % (len(dh), len(draw)))
for x, k, v in dh:
    print("   %08X %s %s %s" % (x.address, x.mnemonic, x.op_str[:40], tk.fname(x.address)))

text = tk.d[tk.TRO:tk.TRO + tk.TRS]
def jcc_to(t):
    out = []
    for i in range(len(text) - 6):
        if text[i] == 0x0F and 0x80 <= text[i + 1] <= 0x8F:
            if tk.TVA + i + 6 + struct.unpack_from("<i", text, i + 2)[0] == t: out.append(tk.TVA + i)
    return out
T = 0x00229F00
sites = RAW.get("%X" % T, [])
rr, _ = tk.rip_refs(T, T + 1)
print("R2 00229F00 raw call/jmp sites: %s" % ["%s@%s" % (tk.fname(int(s, 16)), s) for s in sites])
print("R2 jcc: %s  rip refs: %s  relocs: %d" % (jcc_to(T), ["%08X" % h[0].address for h in rr], len(tk.reloc_ptrs(T, T + 1))))
for s in sites:
    a = int(s, 16)
    prev = [x for x in tk.dis(a - 12, a + 5)]
    print("   before %s: %s" % (s, " | ".join("%08X %s %s" % (x.address, x.mnemonic, x.op_str) for x in prev if x.address < a + 5)[-160:]))

for lo, hi in ((0x00229F00, 0x00229F10), (0x0022B830, 0x0022B862), (0x0022BDA8, 0x0022BDCC), (0x0022A600, 0x0022A660)):
    print("R3 listing %08X..%08X" % (lo, hi))
    for x in tk.dis(lo, hi):
        print("   %08X %s %s" % (x.address, x.mnemonic, x.op_str))
