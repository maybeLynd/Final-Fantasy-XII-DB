"""SWE2-AUDIT-SPEC independent re-derivation for SD-6 (2026-09-30). Read-only on the image.
Uses tk.py's whole-.text raw sweeps (not retool.py's extent-limited scan):
  R1 every rip-relative and image-base-relative reference to the two gate globals and to the table/count
  R2 stored pointers (DIR64 relocs + raw qwords) to the gate cells
  R3 raw callers of the loader 0079FB10, the handler 00797A20, the registrar 007A0180 (rawcalls.json + jcc rel32 sweep)
  R4 the gate cells lie past .data's raw bytes (zero-initialised)
  C  control: the same sweep finds the window-procedure byte store 02EA5213 (sensitivity to a real writer in the block)
"""
import sys, json, struct
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk
RAW = json.load(open(r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\pub140-scratch\tools\rawcalls.json"))

def show(lo, hi, label):
    hits, raw = tk.rip_refs(lo, hi)
    print("%s rip refs [%08X,%08X): %d (raw-only %d)" % (label, lo, hi, len(hits), len(raw)))
    for h in hits:
        x, k = h[0], h[1]
        print("   %08X %-6s %-40s owner=%s store=%s" % (x.address, x.mnemonic, x.op_str[:40],
              tk.fname(x.address), tk.is_store(x, k)))
    dh = tk.disp_refs(lo - tk.BASE, hi - tk.BASE)
    dh = dh[0]
    print("%s image-base-relative disp refs: %d" % (label, len(dh)))
    for x, k, v in dh[:10]:
        print("    %08X %s %s owner=%s" % (x.address, x.mnemonic, x.op_str[:40], tk.fname(x.address)))
    return hits

for lo, hi, lab in [(0x02EA5220, 0x02EA5228, "gate1"), (0x02EA5230, 0x02EA5238, "gate2"),
                    (0x02EA5480, 0x02EA5490, "count+table"), (0x02EA5213, 0x02EA5214, "C-byte")]:
    show(lo, hi, lab)

print("R2 relocs into 02EA5210..02EA5238:", len(tk.reloc_ptrs(0x02EA5210, 0x02EA5238)),
      " raw qwords:", len(tk.raw_q(0x02EA5210, 0x02EA5238)))

va, vs, rs, ro = tk.secs[".data"]
print("R4 .data va %08X raw end %08X virtual end %08X; gate1 past raw: %s gate2 past raw: %s" % (
    va, va + rs, va + vs, 0x02EA5220 >= va + rs, 0x02EA5230 >= va + rs))

# R3 raw callers + jcc rel32 sweep of .text
text = tk.d[tk.TRO:tk.TRO + tk.TRS]
def jcc_to(t):
    out = []
    for i in range(len(text) - 6):
        if text[i] == 0x0F and 0x80 <= text[i + 1] <= 0x8F:
            rel = struct.unpack_from("<i", text, i + 2)[0]
            if tk.TVA + i + 6 + rel == t: out.append(tk.TVA + i)
    return out
for t in (0x0079FB10, 0x00797A20, 0x007A0180, 0x00792760):
    sites = RAW.get("%X" % t, [])
    rr, _ = tk.rip_refs(t, t + 1)
    print("R3 %08X raw call/jmp sites: %s  owners: %s  rip refs(lea/ptr): %s  jcc: %s" % (
        t, sites, [tk.fname(int(s, 16)) for s in sites],
        ["%s@%08X" % (tk.fname(h[0].address), h[0].address) for h in rr], ["%08X" % j for j in jcc_to(t)]))
