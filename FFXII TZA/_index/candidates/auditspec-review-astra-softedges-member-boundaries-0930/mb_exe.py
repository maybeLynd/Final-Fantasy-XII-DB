"""SWE2-AUDIT-SPEC independent EXE re-derivation for phyretext-member-boundaries (ASTRA 7a524fda9).
Reads the shipping EXE through tk.py and pefile (.pdata / UNWIND_INFO), not the packet's captures."""
import sys, struct
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk
def cstr(a, n=64):
    o = tk.off(a)
    if o is None: return "(zero-init .data tail, %s)" % tk.sec_of(a)
    b = tk.d[o:o + n]; return b[:b.find(b"\0")].decode("latin1")
def lin(lo, hi):
    return list(tk.dis(lo, hi))
def pr(xs):
    for x in xs: print("  %08X %-7s %s" % (x.address, x.mnemonic, x.op_str))
def ripdst(x, k=1):
    return x.address + x.size + x.operands[k].mem.disp
print("[registration 005EEDA0..005EEE00, owner %s]" % tk.fname(0x5EEDAF))
xs = [x for x in tk.fdis(tk.owner(0x5EEDAF) if isinstance(tk.owner(0x5EEDAF), int) else 0x5EEB20) if 0x5EEDA0 <= x.address < 0x5EEE00]
pr(xs)
for x in xs:
    if x.mnemonic == "mov" and x.op_str.startswith("qword ptr [rip"):
        print("   store %08X -> [%08X] (%s)" % (x.address, x.address + x.size + x.operands[0].mem.disp, tk.sec_of(x.address + x.size + x.operands[0].mem.disp)))
    if x.mnemonic == "lea" and "rip" in x.op_str:
        t = ripdst(x); print("   lea %08X -> %08X %r" % (x.address, t, cstr(t) if tk.sec_of(t) != ".text" else "(code)"))
print("qword D4BD30+0x40 = %X" % tk.u64(0xD4BD30 + 0x40), " sec", tk.sec_of(0xD4BD30))
print("D4BD30 qwords 0..0x48:", ["%X" % tk.u64(0xD4BD30 + 8 * i) for i in range(10)])
print("[dispatcher 0060F3D0..0060F3F1] listed size", tk.fsize(0x60F3D0)); pr(lin(0x60F3D0, 0x60F3F2))
print("[callback 0060F280..0060F290] listed size", tk.fsize(0x60F280)); pr(lin(0x60F280, 0x60F290))
print("[0060EFE0 head] listed size", tk.fsize(0x60EFE0)); ys = list(tk.fdis(0x60EFE0)); pr(ys[:40])
# first memory write / array read in 0060EFE0 vs the negative-count exit
print("[resolver 0059EC40 continuation 0059ED20..0059ED61]")
zs = list(tk.dis(0x59EC40, 0x59ED61)); pr([x for x in zs if 0x59ED20 <= x.address < 0x59ED61])
# .pdata entries covering 0059EC40..0059ED61 and their chaining
import pefile
pe = pefile.PE(tk.EXE, fast_load=True); pe.parse_data_directories(directories=[pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_EXCEPTION"]])
ib = pe.OPTIONAL_HEADER.ImageBase
ents = []
for e in pe.DIRECTORY_ENTRY_EXCEPTION:
    b = e.struct.BeginAddress + tk.BASE; en = e.struct.EndAddress + tk.BASE
    if 0x59EC40 <= b < 0x59ED80: ents.append((b, en, e.struct.UnwindData + tk.BASE))
for b, en, u in sorted(ents):
    o = tk.off(u); ver_fl = tk.d[o]; flags = ver_fl >> 3; ncodes = tk.d[o + 2]
    chain = None
    if flags & 4:
        co = o + 4 + 2 * ((ncodes + 1) & ~1); cb, ce, cu = struct.unpack_from("<III", tk.d, co); chain = (cb + tk.BASE, ce + tk.BASE)
    print("  pdata %08X..%08X unwind %08X flags=%d chained_to=%s" % (b, en, u, flags, ("%08X..%08X" % chain) if chain else "-"))
