"""SWE2-AUDIT-SPEC independent re-derivation for SD-62 (2026-09-30). Read-only on the image.
  R1 raw callers of the descriptor constructor 00632D80 (rawcalls.json + jcc + stored pointers), and for each the value
     reaching rdx: walk back on the caller's instruction boundaries to the last write of rdx/edx; if it is `mov rdx, rax`
     name the preceding call. Prints the tally and every site that is NOT 006373D0().
  R2 the two objects' leading qwords, whether each self pointer is a DIR64 relocation, and the qword at +0x40/+0x48
  R3 RTTI of the vtable at 00D56D10 (complete object locator -> type descriptor name)
  R4 00632D80: every use of rdx (the passed object) in its body
  R5 is 01F2E780's shape unique: stored pointers to the "getInstanceCount" string and to 01F2E780 itself
"""
import sys, json, struct, collections
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk
RAW = json.load(open(r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\pub140-scratch\tools\rawcalls.json"))
T = 0x00632D80
sites = sorted(int(s, 16) for s in RAW.get("%X" % T, []))
text = tk.d[tk.TRO:tk.TRO + tk.TRS]
jcc = [tk.TVA + i for i in range(len(text) - 6) if text[i] == 0x0F and 0x80 <= text[i + 1] <= 0x8F
       and tk.TVA + i + 6 + struct.unpack_from("<i", text, i + 2)[0] == T]
print("R1 00632D80 raw call/jmp sites: %d  jcc: %d  relocs: %d" % (len(sites), len(jcc), len(tk.reloc_ptrs(T, T + 1))))
tally = collections.Counter(); odd = []
for a in sites:
    b = sorted(x for x in tk.boundaries(a) if a - 0x100 <= x < a)
    src = None
    for s in reversed(b):
        x = tk.dis(s, s + 15)[0]
        if x.op_str.startswith(("rdx,", "edx,", "dx,")) and x.mnemonic not in ("cmp", "test"):
            if x.op_str == "rdx, rax":
                prev = [tk.dis(p, p + 15)[0] for p in b if p < s]
                c = next((y for y in reversed(prev) if y.mnemonic == "call"), None)
                src = "call %s" % (c.op_str if c else "?")
            else:
                src = "%s %s" % (x.mnemonic, x.op_str)
            break
        if x.mnemonic == "call": src = "rdx clobbered by call %s" % x.op_str; break
    tally[src] += 1
    if src != "call 0x6373d0": odd.append((a, src))
print("R1 rdx source tally: %s" % dict(tally))
for a, s in odd: print("   odd site %08X in %s: %s" % (a, tk.fname(a), s))
for base, n in ((0x01F2E330, 8), (0x01F2E780, 10)):
    qs = [tk.u64(base + 8 * i) for i in range(n)]
    rel = [base + 8 * i for i in range(n) if tk.reloc_ptrs(base + 8 * i, base + 8 * i + 1)]
    print("R2 %08X qwords: %s" % (base, ["%08X" % q for q in qs]))
    print("   relocated slots in the object: %s" % ["+0x%X" % (r - base) for r in set(r for r in tk.relocs() if base <= r < base + 8 * n)])
s48 = tk.u64(0x01F2E780 + 0x48)
o = tk.off(s48); print("R2 +0x48 string: %r" % tk.d[o:o + 24].split(b"\0")[0])
vt = 0x00D56D10; col = tk.u64(vt - 8)
td = tk.BASE + tk.u32(col + 0x0C); o = tk.off(td + 0x10)
print("R3 vtable 00D56D10 COL sig %d type %r" % (tk.u32(col), tk.d[o:o + 90].split(b"\0")[0]))
print("R4 00632D80 uses of rdx:")
for x in tk.fdis(T):
    if "rdx" in x.op_str or "edx" in x.op_str: print("   %08X %s %s" % (x.address, x.mnemonic, x.op_str))
print("R5 stored pointers to the name string: %d; to 01F2E780: relocs %d (in-object %d)" % (
    len(tk.reloc_ptrs(s48, s48 + 1)), len(tk.reloc_ptrs(0x01F2E780, 0x01F2E781)),
    len([r for r in tk.relocs() if 0x01F2E780 <= r < 0x01F2E7D0 and tk.u64(r) == 0x01F2E780])))
hits, _ = tk.rip_refs(s48, s48 + 1)
print("R5 rip refs to the name string: %s" % ["%08X %s" % (h[0].address, tk.fname(h[0].address)) for h in hits])
