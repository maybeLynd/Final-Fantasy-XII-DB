"""B-2/b (OPUS, 2026-09-26): can the 128 group-D funclets be told from atexit thunks without relying on "nothing takes
their address"? STATIC over the shipped image.

  S1 The image's POGO debug record (type 13, 'GCTL') names its linker section contributions. It states .text$x
     00896280-008A6970, where MSVC places EH funclets, and .text$yd 008A6970-008C1635, where it places dynamic atexit
     destructors.
  S2 Every FuncInfo reached from .pdata -> UNWIND_INFO (handler data leads with the FuncInfo RVA for both
     __CxxFrameHandler3 and __GSHandlerCheck_EH) passes its magic check: 4,518 records. Their unwind-map actions and
     catch handlers are the declared funclets. All but one lie in .text$x. The exception, 00861EAE, is not a body: it
     is the `jmp [__std_terminate]` import thunk, used directly as an unwind action.
  S3 Group D is rebuilt by the page's own rule: a declared funclet that does not use RDX as the establisher frame (A),
     does not tail-jump to _Init_thread_abort 0080926C (B), and does not reach __std_terminate (C). It is 128, all in
     .text$x, in three shapes.
  S4 atexit registrations are `lea rcx,[rip+F]` immediately before a call or jmp to 00808B90. There are 1,569
     registered functions. 1,567 are in .text$yd and none are in .text$x; the other two are the CRT's own. The
     page's two controls, 008A81D0 and 008A9240, are among them.
  S5 By body alone, the answer is no for 75 of the 128. 1,144 registered .text$yd thunks have exactly group D's
     `lea rcx,[rip+N]; jmp N` shape. The other 53 (`lea; add rcx,N; jmp`) have no registered twin in this image.
  S6 .text$x holds only funclets. Every .pdata entry starting in it is a declared funclet or an RDX-frame body.
Writes result.json; exit 1 on any FAIL."""
import os, struct, re, collections, json, sys
from pathlib import Path
import pefile, capstone
ROOT = Path(__file__).resolve().parents[5]
pe = pefile.PE(str(ROOT / "Database/Tools/work/exe/FFXII_TZA.exe")); img = pe.get_memory_mapped_image(); IB = pe.OPTIONAL_HEADER.ImageBase
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
u32 = lambda a: struct.unpack_from("<I", img, a - IB)[0]
imp = {i.address: i.name.decode() for e in pe.DIRECTORY_ENTRY_IMPORT for i in e.imports if i.name}
# ---- S1
pogo = {}
for d in pe.DIRECTORY_ENTRY_DEBUG:
    if d.struct.Type == 13:
        data = pe.get_data(d.struct.AddressOfRawData, d.struct.SizeOfData); o = 4
        while o + 8 < len(data):
            rva, size = struct.unpack_from("<II", data, o); o += 8
            e = data.index(b"\0", o); pogo[data[o:e].decode("latin-1")] = (rva + IB, rva + IB + size); o = (e + 4) & ~3
X, YD = pogo.get(".text$x"), pogo.get(".text$yd")
inr = lambda a, r: r[0] <= a < r[1]
# ---- S2
pd = [d for d in pe.OPTIONAL_HEADER.DATA_DIRECTORY if d.name == "IMAGE_DIRECTORY_ENTRY_EXCEPTION"][0]
rfs = [struct.unpack_from("<III", img, pd.VirtualAddress + 12 * k) for k in range(pd.Size // 12)]
starts = sorted(r[0] + IB for r in rfs)
funclets = set(); nfi = 0
for b, e, ui in rfs:
    ui += IB
    if ui & 1: continue
    flags = img[ui - IB] >> 3; cnt = img[ui - IB + 2]
    if not flags & 3 or flags & 4: continue
    h = ui + 4 + 2 * ((cnt + 1) & ~1)
    fi = u32(h + 4) + IB
    if not (IB <= fi < IB + len(img) - 4) or u32(fi) & 0xFFFFFFF0 != 0x19930520: continue
    nfi += 1
    maxst, pum, ntry, ptry = u32(fi + 4), u32(fi + 8), u32(fi + 12), u32(fi + 16)
    for k in range(maxst):
        act = u32(pum + IB + 8 * k + 4)
        if act: funclets.add(act + IB)
    for t in range(ntry):
        tb = ptry + IB + 20 * t
        for c in range(u32(tb + 12)): funclets.add(u32(u32(tb + 16) + IB + 20 * c + 12) + IB)
def thunk_of(a):
    o = a - IB
    return a + 6 + struct.unpack_from("<i", img, o + 2)[0] if img[o] == 0xFF and img[o + 1] == 0x25 else None
outside = sorted(f for f in funclets if not inr(f, X))
# ---- S3
def body(f, n=12):
    out = []
    for i in md.disasm(img[f - IB:f - IB + 0x80], f):
        out.append(i)
        if i.mnemonic in ("ret", "jmp") or len(out) >= n: break
    return out
def jtarget(i):
    if i.op_str.startswith("0x"): return ("rel", int(i.op_str, 16))
    m = re.match(r"qword ptr \[rip \+ (0x[0-9a-f]+)\]", i.op_str)
    return ("iat", i.address + i.size + int(m.group(1), 16)) if m else None
def is_A(f):
    for i in body(f):
        if i.op_str.startswith("rdx,"): return False
        if re.search(r"\brdx\b|\[rdx", i.op_str): return True
    return False
def is_B(f):
    b = body(f); return bool(b) and b[-1].mnemonic == "jmp" and b[-1].op_str == hex(0x80926C)
def is_C(f):
    b = body(f)
    if not b or b[-1].mnemonic not in ("jmp", "call"): return False
    jt = jtarget(b[-1])
    if not jt: return False
    return imp.get(jt[1] if jt[0] == "iat" else thunk_of(jt[1])) == "__std_terminate"
def sk(f): return " ; ".join(i.mnemonic + " " + re.sub(r"0x[0-9a-f]+", "N", i.op_str) for i in body(f))
D = sorted(f for f in funclets if not is_A(f) and not is_B(f) and not is_C(f))
dshape = collections.Counter(sk(f) for f in D)
# ---- S4
reg = set()
for m in re.finditer(rb"[\xE8\xE9]", img[0x1000:0x8C0000 - IB]):
    o = m.start() + 0x1000; a = o + IB
    if a + 5 + struct.unpack_from("<i", img, o + 1)[0] != 0x808B90: continue
    ins = list(md.disasm(img[a - 7 - IB:a - IB], a - 7))
    if len(ins) == 1:
        mm = re.match(r"rcx, \[rip \+ (0x[0-9a-f]+)\]", ins[0].op_str)
        if ins[0].mnemonic == "lea" and mm: reg.add(ins[0].address + ins[0].size + int(mm.group(1), 16))
reg_yd = sum(1 for r in reg if inr(r, YD)); reg_x = sum(1 for r in reg if inr(r, X))
reg_else = sorted("%08X" % r for r in reg if not inr(r, YD) and not inr(r, X))
# ---- S5
twin = collections.Counter(sk(r) for r in reg if sk(r) in dshape)
# ---- S6
xst = [s for s in starts if inr(s, X)]
odd = [s for s in xst if s not in funclets]
odd_rdx = all(any(i.op_str in ("rbp, rdx",) for i in body(s)) for s in odd)
res = {"pogo": {k: ["%08X" % v[0], "%08X" % v[1]] for k, v in pogo.items() if k.startswith(".text")},
       "funcinfo_records": nfi, "declared_funclets": len(funclets), "declared_outside_text_x": ["%08X" % f for f in outside],
       "outside_is": {"%08X" % f: imp.get(thunk_of(f)) for f in outside},
       "group_D": len(D), "group_D_in_text_x": sum(1 for f in D if inr(f, X)), "group_D_shapes": dict(dshape),
       "group_D_members": ["%08X" % f for f in D],
       "atexit_registered": len(reg), "registered_in_text_yd": reg_yd, "registered_in_text_x": reg_x, "registered_elsewhere": reg_else,
       "registered_with_a_group_D_shape": dict(twin), "pdata_starts_in_text_x": len(xst), "undeclared_pdata_starts_in_text_x": ["%08X" % s for s in odd]}
cases = {
    "S1_pogo_states_text_x_and_text_yd": X == (0x896280, 0x8A6970) and YD == (0x8A6970, 0x8C1635),
    "S2_4518_funcinfo_all_declared_funclets_in_text_x_but_the_terminate_thunk": nfi == 4518 and len(outside) == 1 and imp.get(thunk_of(outside[0])) == "__std_terminate",
    "S3_group_D_is_128_and_all_in_text_x": len(D) == 128 and all(inr(f, X) for f in D),
    "S4_registered_atexit_thunks_in_text_yd_none_in_text_x_controls_found": reg_x == 0 and reg_yd == len(reg) - len(reg_else) and len(reg_else) <= 2
        and all(x.startswith("0080") for x in reg_else) and {0x8A81D0, 0x8A9240} <= reg,
    "S5_body_alone_cannot_separate_the_lea_jmp_shape": sum(twin.values()) > 1000 and set(twin) == {"lea rcx, [rip + N] ; jmp N"},
    "S6_text_x_holds_only_funclets": not (set(xst) & reg) and odd_rdx,
}
out = {"evidence": ["STATIC"], "live_game": False, "results": res, "cases": cases, "ok": all(cases.values())}
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "result.json"), "w"), indent=1, sort_keys=True)
print(json.dumps({k: v for k, v in res.items() if k != "group_D_members"}, indent=1, sort_keys=True))
for k, v in cases.items(): print("%-84s %s" % (k, "PASS" if v else "FAIL"))
print("ALL PASS" if out["ok"] else "FAILED")
sys.exit(0 if out["ok"] else 1)
