"""SWE2-AUDIT-SPEC independent re-derivation for SD-9 (2026-09-30). Read-only on the image.
  R1 every access into 022CA5C0..022CA5E0 over ALL .text (rip sweep with access width + image-base-relative disp sweep)
  R2 stored pointers into the block (relocs + unaligned raw qwords)
  R3 the block lies past .data's raw bytes (zero-initialised)
  R4 00290180's body and its callers; raw callers of 0035E7A0 (+ jcc) and what each does with eax after the call
"""
import sys, json, struct
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk
RAW = json.load(open(r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\pub140-scratch\tools\rawcalls.json"))
LO, HI = 0x022CA5C0, 0x022CA5E0
hits, raw = tk.rip_refs(LO - 8, HI)
print("R1 rip accesses touching 022CA5C0..022CA5DF:")
for x, k, t in hits:
    sz = tk.memsize(x, k) or 1
    if t + sz > LO and t < HI:
        print("   %08X %-5s %-44s tgt=%08X w=%d store=%s  %s" % (x.address, x.mnemonic, x.op_str[:44], t, sz,
              tk.is_store(x, k), tk.fname(x.address)))
print("   raw-only candidates: %s" % [("%08X" % p, "%08X" % t) for p, t in raw])
dh, draw = tk.disp_refs(LO - 8 - tk.BASE, HI - tk.BASE)
print("R1 image-base-relative: %d (raw-only %d)" % (len(dh), len(draw)))
print("R2 relocs: %d raw qwords: %d" % (len(tk.reloc_ptrs(LO, HI)), len(tk.raw_q(LO, HI))))
va, vs, rs, ro = tk.secs[".data"]
print("R3 .data raw end %08X; block past raw: %s" % (va + rs, LO >= va + rs))
print("R4 00290180 body: %s" % " | ".join("%s %s" % (x.mnemonic, x.op_str) for x in tk.dis(0x00290180, 0x00290188)))
text = tk.d[tk.TRO:tk.TRO + tk.TRS]
def jcc_to(t):
    return [tk.TVA + i for i in range(len(text) - 6) if text[i] == 0x0F and 0x80 <= text[i + 1] <= 0x8F
            and tk.TVA + i + 6 + struct.unpack_from("<i", text, i + 2)[0] == t]
for T in (0x00290180, 0x0035E7A0):
    sites = RAW.get("%X" % T, [])
    rr, _ = tk.rip_refs(T, T + 1)
    print("R4 %08X callers: %d %s  jcc %s  rip %s  relocs %d" % (T, len(sites),
          ["%s@%s" % (tk.fname(int(s, 16)).split()[0], s) for s in sites][:12], jcc_to(T),
          ["%08X" % h[0].address for h in rr], len(tk.reloc_ptrs(T, T + 1))))
for s in RAW.get("%X" % 0x0035E7A0, []):
    a = int(s, 16)
    print("   after %s: %s" % (s, " | ".join("%s %s" % (x.mnemonic, x.op_str) for x in tk.dis(a, a + 24))))
