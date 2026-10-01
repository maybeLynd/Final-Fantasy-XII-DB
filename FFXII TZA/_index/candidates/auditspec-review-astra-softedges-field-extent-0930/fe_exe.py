"""SWE2-AUDIT-SPEC independent EXE re-derivation for phyretext-softedges-field-extent (ASTRA 5bbbe5528).
Reads the shipping EXE directly through tk.py (not the packet's retained JSON captures)."""
import sys, os, json, struct, hashlib
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk
print("exe sha256", hashlib.sha256(tk.d).hexdigest())
def cstr(a, n=96):
    o = tk.off(a); b = tk.d[o:o + n]; return b[:b.find(b"\0")].decode("latin1")
def show(lo, hi, owner=None):
    e = owner if owner else tk.owner(lo)
    e = e[0] if isinstance(e, tuple) else e
    for x in tk.fdis(e):
        if lo <= x.address < hi: print("  %08X %-6s %s" % (x.address, x.mnemonic, x.op_str))
print("owner 001D03C6:", tk.fname(0x1D03C6), " owner 001EA609:", tk.fname(0x1EA609))
print("[caller 001D03B0..001D03D0]"); show(0x1D03B0, 0x1D03D0)
# raw callers of 001EA3C0 (E8/E9 + jcc) straight from the bytes
T = 0x1EA3C0; TVA, TVS, TRS, TRO = tk.TVA, tk.TVS, tk.TRS, tk.TRO
t = tk.d[TRO:TRO + TRS]; callers = []
for i in range(len(t) - 5):
    op = t[i]
    if op in (0xE8, 0xE9) and TVA + i + 5 + struct.unpack_from("<i", t, i + 1)[0] == T: callers.append((TVA + i, "E8" if op == 0xE8 else "E9"))
    if op == 0x0F and 0x80 <= t[i + 1] <= 0x8F and i + 6 <= len(t) and TVA + i + 6 + struct.unpack_from("<i", t, i + 2)[0] == T: callers.append((TVA + i, "jcc"))
print("raw branches to 001EA3C0:", ["%08X %s in %s" % (a, k, tk.fname(a)) for a, k in callers])
print("rip refs to 001EA3C0:", len(tk.rip_refs(T, T + 1)[0]), " relocs:", len(tk.reloc_ptrs(T, T + 1)))
# the callee body: RSI writes between 001EA3DC and 001EA5C1, plus the copy block
body = list(tk.fdis(0x1EA3C0))
print("001EA3C0 listed size", tk.fsize(0x1EA3C0), "insns", len(body))
rsi_w = [x for x in body if x.op_str.startswith(("rsi,", "esi,", "si,", "sil,")) and x.mnemonic not in ("cmp", "test", "push")]
print("instructions writing rsi/esi in body:", ["%08X %s %s" % (x.address, x.mnemonic, x.op_str) for x in rsi_w])
xchg = [x for x in body if x.mnemonic in ("xchg", "pop") and "rsi" in x.op_str]
print("xchg/pop rsi:", ["%08X %s %s" % (x.address, x.mnemonic, x.op_str) for x in xchg])
calls = [x for x in body if x.mnemonic == "call" and 0x1EA3DC <= x.address < 0x1EA5C1]
print("calls between 001EA3DC and 001EA5C1 (rsi is callee-saved in the Win64 ABI):", len(calls))
print("[001EA5A8..001EA612]"); show(0x1EA5A8, 0x1EA612, 0x1EA3C0)
lea = next(x for x in body if x.address == 0x1EA5AD)
tgt = lea.address + lea.size + lea.disp if hasattr(lea, "disp") else None
tgt = lea.address + lea.size + lea.operands[1].mem.disp
print("lea at 001EA5AD ->", "%08X" % tgt, repr(cstr(tgt)))
# memcpy thunk and IAT
print("[thunk 00861EBA]"); [print("  %08X %s %s" % (x.address, x.mnemonic, x.op_str)) for x in tk.dis(0x861EBA, 0x861EC0)]
th = list(tk.dis(0x861EBA, 0x861EC0))[0]; iat = th.address + th.size + th.operands[0].mem.disp
import pefile
pe = pefile.PE(tk.EXE, fast_load=True); pe.parse_data_directories(directories=[pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_IMPORT"]])
ib = pe.OPTIONAL_HEADER.ImageBase
nm = [(e.dll.decode(), i.name.decode()) for e in pe.DIRECTORY_ENTRY_IMPORT for i in e.imports if i.address - ib + tk.BASE == iat]
print("IAT %08X ->" % iat, nm, " image base in header 0x%X" % ib)
# resource-name slots 01DFDE00 / 01DFDE08 (absolute pointers, relocated)
for s in (0x1DFDE00, 0x1DFDE08):
    q = tk.u64(s); va = q - ib + tk.BASE
    print("slot %08X qword %X -> %08X %r" % (s, q, va, cstr(va)))
print("[lookup 0018D240]"); show(0x18D240, 0x18D2C0)
print("[0059C4D0..0059C4E0, 0059C5A0..0059C5B0 in 0059C250]"); show(0x59C4D0, 0x59C4E0, 0x59C250); show(0x59C5A0, 0x59C5B0, 0x59C250)
print("[0059BF50..0059BF72 in 0059BED0]"); show(0x59BF50, 0x59BF72, 0x59BED0)
print("arith: outer+8+0x118 = 0x%X ; first AE0 byte needs len > 0x%X (%d) ; whole AE0 needs len >= 0x%X (%d)" % (8 + 0x118, 0xAE0 - 0x120, 0xAE0 - 0x120, 0xAE4 - 0x120, 0xAE4 - 0x120))
