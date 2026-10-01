"""b12_struct.py - DD prose-residue closure, batch 12 (SWE2-STRUCT for OPUS, 2026-09-30).

Run: python -B b12_struct.py        (FAILS 0)      archive: $FF12_VBF, else the Steam install path below

Static, the certified shipping image (73461d08...) through retool.py / structflow.py, plus the installed FFXII_TZA.vbf
(the 1,066 .cm @FCP blocks, the nine battle_pack.bin and the licd board files), read by census_format_magics.load_index.

  SB1-SB9   the three model-declared special bones 0x104 / 0x105 / 0x106 (render-record page, section 13)
  F1-F5     CharacterRenderRecord +0x414 (render-record page, section 12)
  C1-C3     the FCP page: 0041F010 read whole, the three computed-id sites, the section-8 copy readers (a lead)
  R1-R4     the registry page: header +0x0A, the board-request slots, the binder's slot arguments, the motion-index setters

Every census check carries a positive control on a field whose readers are already known.
"""
import collections, io, os, re, struct, sys, zlib

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
KIT = os.path.join(DB, "..", "Tools", "analysis-kit", "gfz-scripts")
sys.path.insert(0, KIT)
import retool as T  # noqa: E402
import structflow as S  # noqa: E402
from census_format_magics import load_index  # noqa: E402

VBF = os.environ.get("FF12_VBF", r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\FFXII_TZA.vbf")
R, SZ, SC = T.R, T.sizes(), T.scan()
FAILS = 0


def check(name, ok, detail=""):
    global FAILS
    print(("PASS " if ok else "FAIL ") + name + (" - " + detail if detail else ""))
    if not ok:
        FAILS += 1


def ins(a):
    return next(R.md.disasm(R.at(a, 15), a))


def txt(a):
    i = ins(a)
    return "%s %s" % (i.mnemonic, i.op_str)


def pin(cid, a, rx, why):
    t = txt(a)
    check("%s %s" % (cid, why), re.search(rx, t) is not None, "%08X  %s" % (a, t))


def sites(callee):
    return sorted(SC["calls"].get(callee, ()), key=lambda cs: cs[1])      # [(caller, site)]


def body(f):
    return list(R.md.disasm(R.at(f, SZ[f]), f))


def back_write(f, site, reg, n=12):
    """the last instruction before `site` in f that writes `reg` (by text), within n instructions"""
    prev = [x for x in body(f) if x.address < site][-n:]
    fam = S.FAM
    for x in reversed(prev):
        try:
            w = {fam.get(x.reg_name(r), x.reg_name(r)) for r in x.regs_access()[1]}
        except Exception:
            w = set()
        if reg in w:
            return x
    return None


def rip_target(x):
    for op in x.operands:
        if op.type == 3 and op.mem.base and x.reg_name(op.mem.base) == "rip":
            return x.address + x.size + op.mem.disp
    return None


def rip_load_seeds(glob, mnems=("mov", "add")):
    out = set()
    for f, a, k in SC["refs"].get(glob, ()):
        x = ins(a)
        if x.mnemonic in mnems and "qword ptr [rip" in x.op_str and not x.op_str.startswith("qword"):
            out.add((f, glob - (a + x.size), a))
    return out


def base_tagcount(g, h):
    """how many element offsets the access's base/index register carries at the hit (a loop-induction alias carries the
    whole stride residue, 232 or more; a real field access carries one or two)"""
    x = ins(h[1])
    regs = set()
    for op in x.operands:
        if op.type == 3:
            for r in (op.mem.base, op.mem.index):
                if r:
                    regs.add(S.FAM.get(x.reg_name(r), x.reg_name(r)))
    return max([len(g.probe[h[1]].get(r, ())) for r in regs] or [0])


def real_hits(g, limit=16):
    return sorted({(h[0], h[1], h[2], h[4], h[5]) for h in g.hits if base_tagcount(g, h) <= limit})


# ---------------------------------------------------------------------------------------------- the VBF reader
BLOCK = 0x10000
_vf = io.open(VBF, "rb")
NAMES, BLOCKS = load_index(_vf)


def read_all(p):
    sb, size, off = NAMES[p]
    n = (size + BLOCK - 1) // BLOCK
    out = b""
    _vf.seek(off)
    for i in range(n):
        cs = BLOCKS[sb + i] or BLOCK
        exp = BLOCK if i < n - 1 else size - BLOCK * (n - 1)
        c = _vf.read(cs)
        if cs != exp:
            c = zlib.decompress(c)
        out += c
    return out


import hashlib  # noqa: E402
img = hashlib.sha256(open(R.b.EXE, "rb").read()).hexdigest()
print("image", img)
check("image identity", img == "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8")

# ============================================================================================ SB: the special bones
print("\n== SB: the three model-declared special bones (render-record page, section 13)")
# SB1 the selector
pin("SB1", 0x003E5AD0, r"^mov r8, qword ptr \[rcx \+ 0x400\]$", "003E5AD0 reads the record's @FCP payload pointer +0x400")
pin("SB1", 0x003E5AE7, r"^cmp edx, 0x20$", "ids below 0x20 ...")
pin("SB1", 0x003E5AEF, r"^movzx eax, word ptr \[rcx \+ rax\*2 \+ 0x14c\]$", "... index section 1's u16 bone table at +0x14C")
for a_cmp, a_ld, idv, off in ((0x003E5AF8, 0x003E5B00, 0x104, 0x3A), (0x003E5B06, 0x003E5B0E, 0x105, 0x3C),
                              (0x003E5B14, 0x003E5B1C, 0x106, 0x3E)):
    pin("SB1", a_cmp, r"^cmp edx, %s$" % hex(idv), "id %s ..." % hex(idv))
    pin("SB1", a_ld, r"^movzx eax, word ptr \[r8 \+ %s\]$" % hex(off), "... returns payload word +%s" % hex(off).upper().replace("0X", "0x"))
pin("SB1", 0x003E5B22, r"^mov eax, 0xffff$", "every other id returns 0xFFFF")

# SB2 every caller of the selector, and the id each passes
cs = sites(0x003E5AD0)
check("SB2 003E5AD0 has exactly 8 direct call sites and no rip reference",
      len(cs) == 8 and not SC["refs"].get(0x003E5AD0), " ".join("%08X@%08X" % c for c in cs))
want = {0x003B57FF: r"^mov edx, 0x104$", 0x003B5834: r"^mov edx, 0x106$", 0x0047124D: r"^mov edx, 0x104$",
        0x0047180B: r"^mov edx, 0x104$", 0x0041EE7E: r"^movzx edx, word ptr \[r15 \+ 0x36\]$",
        0x0041F0B9: r"^movzx edx, word ptr \[r15 \+ 0x36\]$", 0x0042173E: r"^movsx edx, bp$",
        0x00421F51: r"^movsx edx, bx$"}
for f, s in cs:
    w = back_write(f, s, "rdx")
    t = "%s %s" % (w.mnemonic, w.op_str) if w else "?"
    check("SB2 the id at %08X (in %08X)" % (s, f), s in want and re.search(want[s], t) is not None, "%08X  %s" % (w.address if w else 0, t))
pin("SB2", 0x00421733, r"^cmp bp, ax$", "004215A0: a variable id reaches 003E5AD0 only below 0x100 ...")
pin("SB2", 0x0042172E, r"^mov eax, 0x100$", "... (the bound)")
pin("SB2", 0x00421736, r"^jge 0x42176a$", "... ids at or above it go to 00422380 instead")
pin("SB2", 0x00421EAE, r"^mov ecx, 0xff$", "00421E20: the bound is 0xFF ...")
pin("SB2", 0x00421F46, r"^cmp bx, cx$", "... and the id is tested against it ...")
pin("SB2", 0x00421F49, r"^jge 0x421f9b$", "... before the call, so no call passes 0x105")

# SB3 census: every read of payload +0x3A / +0x3C / +0x3E through an FCP payload pointer
loads = set()
for f, n in SZ.items():
    d = R.at(f, n)
    if not d:
        continue
    for x in R.md.disasm(d, f):
        if x.mnemonic == "mov" and x.op_str.endswith(" + 0x400]") and ", qword ptr [r" in x.op_str \
                and "[rsp" not in x.op_str and "[rbp" not in x.op_str:
            loads.add((f, 0x400))
            break
gcalls = {(c, 0x003E55F0) for c, s in sites(0x003E55F0)}
g = S.Flow([0x3A, 0x3C, 0x3E], 1, stride=0x1000, slot=0, seed_loads=loads, seed_calls=gcalls)
g.run(sorted({f for f, _ in loads} | {c for c, _ in gcalls}))
hits = real_hits(g)
got = sorted((f, a, off) for f, a, k, off, w in hits)
expect = [(0x003E4CB0, 0x003E4CE6, 0x3A), (0x003E4CB0, 0x003E4CF4, 0x3C), (0x003E4CB0, 0x003E4CFD, 0x3E),
          (0x003E5AD0, 0x003E5B00, 0x3A), (0x003E5AD0, 0x003E5B0E, 0x3C), (0x003E5AD0, 0x003E5B1C, 0x3E),
          (0x003E5FA0, 0x003E5FD2, 0x3A), (0x003E5FA0, 0x003E5FE0, 0x3C), (0x003E5FA0, 0x003E5FE9, 0x3E),
          (0x00421CD0, 0x00421CE7, 0x3A), (0x00421CD0, 0x00421CF5, 0x3C), (0x00421CD0, 0x00421D07, 0x3E),
          (0x004221F0, 0x0042225D, 0x3A)]
check("SB3 census (%d payload-pointer functions, %d getter callers): the readers of +0x3A/+0x3C/+0x3E are exactly five "
      "functions, all reads" % (len(loads), len(gcalls)), got == expect and all(k == "r" for f, a, k, off, w in hits),
      " ".join("%08X:+%X" % (a, o) for f, a, o in got))
check("SB3 control: the census finds the selector's own three reads (known before it ran)",
      {(0x003E5AD0, 0x003E5B00, 0x3A), (0x003E5AD0, 0x003E5B0E, 0x3C), (0x003E5AD0, 0x003E5B1C, 0x3E)} <= set(got))

# SB4 the chain: first non-0xFFFF of the three
for a, rx, why in ((0x00421CE2, r"^cmp byte ptr \[rax\], 3$", "00421CD0 gates on payload byte 0 >= 3"),
                   (0x00421CE7, r"word ptr \[rax \+ 0x3a\]", "then takes +0x3A ..."),
                   (0x00421CF5, r"word ptr \[rax \+ 0x3c\]", "... else +0x3C ..."),
                   (0x00421D07, r"word ptr \[rax \+ 0x3e\]", "... else +0x3E ..."),
                   (0x00421D0E, r"^cmovne bx, ax$", "... and returns 0 when all three are 0xFFFF"),
                   (0x003E4CB0 + 0x36, r"word ptr \[rax \+ 0x3a\]", "003E4CB0 runs the same chain"),
                   (0x003E5FD2, r"word ptr \[rax \+ 0x3a\]", "003E5FA0 (the focus-point frame) runs the same chain")):
    pin("SB4", a, rx, why)
for f, s, st in ((0x0041F340, 0x0041F6B8, 0x0041F6C1), (0x0042F4C0, 0x0042F5D0, 0x0042F5D5),
                 (0x0042F880, 0x0042FA5F, 0x0042FA64)):
    check("SB4 %08X calls the chain at %08X ..." % (f, s), (f, s) in sites(0x00421CD0))
    pin("SB4", st, r"^mov word ptr \[r\w+ \+ 0xb6\], ax$", "... and stores it at the model object's +0xB6")
check("SB4 the chain 00421CD0 has exactly these three callers", len(sites(0x00421CD0)) == 3)

# SB5 the +0xB6 bone's one reader: the draw setup's reference point
b6 = []
for f, n in SZ.items():
    d = R.at(f, n)
    if not d:
        continue
    for x in R.md.disasm(d, f):
        if "+ 0xb6]" in x.op_str and "[rsp" not in x.op_str and "ptr [r" in x.op_str:
            b6.append((f, x.address, "%s %s" % (x.mnemonic, x.op_str)))
reads = [r for r in b6 if not re.match(r"^mov (word|dword) ptr \[", r[2])]
check("SB5 image-wide, +0xB6 is written by the three chain callers and the initialiser 005049E0, and read once",
      len(b6) == 5 and [r[1] for r in reads] == [0x0053D952], "; ".join("%08X %s" % (r[1], r[2]) for r in b6))
pin("SB5", 0x0053D965, r"^imul rdx, rax, 0x290$", "0053D780 scales the bone by the 0x290-byte pose record ...")
pin("SB5", 0x0053D96C, r"^sub rdx, -0x80$", "... + 0x80, the bone's matrix ...")
pin("SB5", 0x0053D973, r"^call 0x4fd4b0$", "... and hands it to the draw setup 004FD4B0 as rdx")
pin("SB5", 0x004FD4E3, r"^mov r15, rdx$", "004FD4B0 keeps that matrix in r15")
for a, o in ((0x004FDA6F, 0x30), (0x004FDA79, 0x34), (0x004FDA83, 0x38)):
    pin("SB5", a, r"^mov eax, dword ptr \[r15 \+ %s\]$" % hex(o), "its translation row +%s is copied into the draw packet" % hex(o))
rf = sorted((k, "%08X" % fn) for gl in (0x02EBA4A0, 0x02EBA4A4, 0x02EBA4A8) for fn, a, k in SC["refs"].get(gl, ()))
check("SB5 the published point 02EBA4A0..A8 is written only by 004FD4B0 and read only by 0053AB50 (the FTE/FCT packet builder)",
      {x for x in rf if x[0] == "W"} == {("W", "004FD4B0")} and {x for x in rf if x[0] == "R"} == {("R", "0053AB50")}, repr(rf))

# SB6 the shadow's two anchors
pin("SB6", 0x003B5804, r"^mov word ptr \[rbx \+ 0x3c\], ax$", "003B56D0 stores bone 0x104 at the shadow entry's +0x3C")
pin("SB6", 0x003B5839, r"^mov word ptr \[rbx \+ 0x3e\], ax$", "... and bone 0x106 at +0x3E")
pin("SB6", 0x003B5841, r"^mov word ptr \[rbx \+ 0x38\], ax$", "... and starts the current anchor +0x38 on bone 0x104")
pin("SB6", 0x003B5D0D, r"^mov word ptr \[r9 \+ 0x3a\], ax$", "003B5CE0 saves the current anchor as the previous one ...")
pin("SB6", 0x003B5D22, r"^movzx eax, word ptr \[r9 \+ 0x3c\]$", "... and picks bone 0x104 when its edx is 0 ...")
pin("SB6", 0x003B5D2D, r"^movzx eax, word ptr \[r9 \+ 0x3e\]$", "... or bone 0x106 otherwise")
check("SB6 003B5CE0's only caller is the class-0x09 authored presentation command 00417F40",
      [c for c, s in sites(0x003B5CE0)] == [0x00417F40])
pin("SB6", 0x004183D7, r"^mov edx, dword ptr \[r14 \+ 0xa8\]$", "the command passes its own +0xA8 as the choice")
pin("SB6", 0x003B59D9, r"^movzx edx, word ptr \[rbx \+ 0x3c\]$", "the shadow LOD 003B5980 measures height from bone 0x104")
pin("SB6", 0x003B6343, r"^movzx edx, word ptr \[rbx \+ 0x3c\]$", "the shadow draw 003B62D0 resolves bone 0x104 ...")
pin("SB6", 0x003B6360, r"^movzx edx, word ptr \[rbx \+ 0x3e\]$", "... and bone 0x106, and blends between them")

# SB7 the rig applies that displace bone 0x104
for f, sel, add in ((0x00471230, 0x0047126B, 0x004712DA), (0x004717E0, 0x0047184D, 0x004718BC)):
    pin("SB7", f + (0x15 if f == 0x00471230 else 0x23), r"^mov edx, 0x104$", "%08X asks for bone 0x104 ..." % f)
    pin("SB7", sel, r"^movups xmm1, xmmword ptr \[rax \+ rbx \+ 0x260\]$", "... loads that bone's pose translation (+0x260) ...")
    pin("SB7", add, r"^movups xmmword ptr \[rax \+ rbx \+ 0x260\], xmm0$", "... and writes it back moved by the controller's +0x20 vector")

# SB8 lights evaluated at the body bone
pin("SB8", 0x0042E82C, r"^call 0x4221f0$", "0042E7F0 resolves bone +0x3A through 004221F0 ...")
pin("SB8", 0x0042E831, r"^mov qword ptr \[rbx \+ 0xf0\], rax$", "... into the model instance's +0xF0 (record matrix +0x180 at +0xE8)")
pin("SB8", 0x004FD57C, r"^mov r8, qword ptr \[rdi \+ 0xe8\]$", "004FD4B0 passes +0xE8 as the gather's r8 ...")
pin("SB8", 0x004FD56E, r"^mov r9, qword ptr \[rdi \+ 0xf0\]$", "... and +0xF0 as its r9")
pin("SB8", 0x003ABE80, r"^test byte ptr \[rax \+ 5\], 0xe$", "003ABD50 tests each light's +5 bits 1-3 ...")
pin("SB8", 0x003ABE86, r"^mov rax, qword ptr \[rsp \+ 0xc0\]$", "... clear: install the record's matrix (the spilled r8) ...")
pin("SB8", 0x003ABEB4, r"^movups xmm0, xmmword ptr \[r13\]$", "... set: install the bone's matrix (r13 = r9)")
pin("SB8", 0x0042225D, r"^movzx ecx, word ptr \[rdi \+ 0x3a\]$", "004221F0 uses +0x3A alone ...")
pin("SB8", 0x004222A9, r"^mov edx, 0x100$", "... and without it falls back to 00421E20(0x100) ...")
pin("SB8", 0x004222C3, r"^mov edx, 0x101$", "... then 00421E20(0x101)")

# SB9 the shipped values
cms = sorted(p for p in NAMES if p.lower().endswith(".cm"))
by = collections.defaultdict(collections.Counter)
tot_a, tot_b, tot_c, b0 = collections.Counter(), collections.Counter(), collections.Counter(), collections.Counter()
for p in cms:
    d = read_all(p)
    i = d.find(b"@FCP")
    pl = d[i + 0x30:i + struct.unpack_from("<I", d, i + 8)[0]]
    a, b, c = struct.unpack_from("<3H", pl, 0x3A)
    kind = next((x for x in p.split("/") if x in ("chara", "monster", "npc", "summon", "high", "weapon", "gadget",
                                                  "treasure", "bg_obj")), "?")
    by[kind]["A" if a != 0xFFFF else ("B" if b != 0xFFFF else "none")] += 1
    tot_a["1" if a == 1 else ("ffff" if a == 0xFFFF else "other")] += 1
    tot_b["1" if b == 1 else ("ffff" if b == 0xFFFF else "other")] += 1
    tot_c[c] += 1
    b0[pl[0]] += 1
check("SB9 1,066 .cm read", len(cms) == 1066, str(len(cms)))
check("SB9 control: +0x3A is 1 / 0xFFFF / other in 628 / 426 / 12 and +0x3C 0xFFFF / 1 / other in 762 / 301 / 3, the FCP "
      "page's falsification-pass figures", (tot_a["1"], tot_a["ffff"], tot_a["other"], tot_b["ffff"], tot_b["1"], tot_b["other"])
      == (628, 426, 12, 762, 301, 3), "%s %s" % (dict(tot_a), dict(tot_b)))
check("SB9 +0x3E (bone 0x106) is 0, the root, in all 1,066; payload byte 0 is 4 in all 1,066, so the >= 3 gate always passes",
      tot_c == collections.Counter({0: 1066}) and b0 == collections.Counter({4: 1066}), "%s %s" % (dict(tot_c), dict(b0)))
exp9 = {"chara": {"A": 17}, "monster": {"A": 253, "B": 1}, "npc": {"A": 173, "none": 1}, "summon": {"A": 26},
        "treasure": {"A": 17}, "weapon": {"B": 284, "A": 41, "none": 1}, "gadget": {"A": 87, "B": 16},
        "high": {"none": 121, "A": 11}, "bg_obj": {"A": 15, "none": 2}}
check("SB9 by directory (A = +0x3A declared, B = only +0x3C declared, none = the chain falls to +0x3E): characters "
      "declare 0x104, weapons 0x105", {k: dict(v) for k, v in by.items()} == exp9, repr({k: dict(v) for k, v in sorted(by.items())}))

# ============================================================================================ F: +0x414
print("\n== F: CharacterRenderRecord +0x414 (render-record page, section 12)")
pin("F1", 0x0041FA68, r"^mov dword ptr \[rbx \+ 0x414\], 0x3e2aaaab$", "the reset writes 1/6")
pin("F1", 0x0042876A, r"^mov eax, dword ptr \[rdi \+ 0x48828\]$", "the promoter reads tail +0x28 ...")
pin("F1", 0x00428773, r"^mov dword ptr \[rsi \+ 0x414\], eax$", "... and copies it into +0x414")
t28 = []
for f, n in SZ.items():
    d = R.at(f, n)
    for x in R.md.disasm(d or b"", f):
        if "+ 0x48828]" in x.op_str:
            t28.append((f, x.address, "%s %s" % (x.mnemonic, x.op_str)))
check("F1 tail +0x28 is written with the constant 1/6 by 004269A0 and 0042ED30 and read only by the promoter",
      sorted(a for f, a, t in t28) == [0x00426C75, 0x0042876A, 0x0042ED53]
      and all(t.endswith("0x3e2aaaab") for f, a, t in t28 if a != 0x0042876A), "; ".join("%08X %s" % (a, t) for f, a, t in t28))

ARR = 0x022C6F28
seeds = rip_load_seeds(ARR) | rip_load_seeds(0x02EBB740, ("mov",)) | rip_load_seeds(0x02EBB750, ("mov",))


def closure(root, depth):
    seen, fr = {root}, [root]
    for _ in range(depth):
        nx = []
        for f in fr:
            for x in body(f):
                if x.mnemonic in ("call", "jmp") and x.op_str.startswith("0x"):
                    t = int(x.op_str, 16)
                    if t in SZ and t not in seen and not (f <= t < f + SZ[f]):
                        seen.add(t)
                        nx.append(t)
        fr = nx
    return seen


wide = set()
for f, n in SZ.items():
    d = R.at(f, n)
    for x in R.md.disasm(d or b"", f):
        if x.mnemonic == "mov" and "qword ptr [r" in x.op_str and not x.op_str.startswith("qword") \
                and ("+ 0xf8]" in x.op_str or "+ 0x2e0]" in x.op_str) and "[rsp" not in x.op_str and "[rbp" not in x.op_str:
            wide.add((f, 0xF8 if x.op_str.endswith("+ 0xf8]") else 0x2E0))
wide |= {(f, 0x28) for f in closure(0x0046FD00, 2)} | {(f, 0x8) for f in closure(0x0051E3A0, 2)}
OUT = {0x003A459F: 0x40, 0x003A596E: 0x40, 0x003A4C45: 0x50, 0x003A5F4F: 0x60, 0x003A6E2C: 0x20}


class OutFlow(S.Flow):
    """structflow plus the five out-parameters through which 003A40F0 and 00426650 return a record pointer"""
    def step(self, f, x, st, depth):
        S.Flow.step(self, f, x, st, depth)
        if x.address in OUT:
            st[("rsp", OUT[x.address])] = {("E", 0)}


def run414(fields, with_escapes):
    g = (OutFlow if with_escapes else S.Flow)(fields, 3, stride=0x740, slot=0, seed_loads=seeds | (wide if with_escapes else set()))
    roots = {s[0] for s in seeds} | ({s[0] for s in wide} | {0x003A4290, 0x003A56F0, 0x003A6DF0} if with_escapes else set())
    g.run(sorted(roots))
    return g


g1 = run414([0x414], False)
h1 = real_hits(g1)
alias = sorted({h[1] for h in g1.hits} - {h[1] for h in h1})
check("F2 from the array global (%d seed sites in %d functions, call depth 3, %d functions walked): the only accesses to "
      "+0x414 are the two writes" % (len(seeds), len({s[0] for s in seeds}), len(g1.entry)),
      [(a, k) for f, a, k, off, w in h1] == [(0x0041FA68, "w"), (0x00428773, "w")], repr(["%08X%s" % (a, k) for f, a, k, o, w in h1]))
check("F2 every other hit is a loop-induction alias (the base register carries >= 232 offsets)",
      all(base_tagcount(g1, h) >= 232 for h in g1.hits if h[1] in alias), "%d alias sites" % len(alias))
esc = sorted({(e[0], e[1]) for e in g1.esc})
check("F3 the record pointer escapes at 12 sites (the published array, the model instance +0xF8 / +0xE8, the +0x2E0 "
      "holders, the status-push blocks, two out-parameters)", len(esc) == 12, " ".join("%08X" % a for f, a in esc))
g2 = run414([0x414], True)
h2 = real_hits(g2)
check("F3 with those routes seeded as well (%d more seeds, %d functions walked): still only the two writes"
      % (len(wide), len(g2.entry)), [(a, k) for f, a, k, off, w in h2] == [(0x0041FA68, "w"), (0x00428773, "w")],
      repr(["%08X%s" % (a, k) for f, a, k, o, w in h2]))
gc = run414([0x408, 0x5EC], True)
hc = {(a, off) for f, a, k, off, w in real_hits(gc)}
check("F4 control: the same census finds the known +0x408 read 002EDC14 (array route) and the light gather's +0x5EC read "
      "003ABDF3, reached only through the model instance's +0xF8 back-pointer",
      (0x002EDC14, 0x408) in hc and (0x003ABDF3, 0x5EC) in hc, "%d hits" % len(hc))
wider = [h for h in g2.hits if h[5] >= 16 and base_tagcount(g2, h) <= 16]
check("F5 no 16-byte or wider access covers +0x414 on any followed route", not wider, repr(wider[:3]))

# ============================================================================================ C: the FCP page
print("\n== C: the FCP page")
pin("C1", 0x0041F035, r"^call 0x3e5cf0$", "0041F010 takes the slot from the child (003E5CF0) ...")
pin("C1", 0x003E5CF0, r"^movzx eax, byte ptr \[rcx \+ 0x6a0\]$", "... which is the child's @FOR byte +0x6A0")
pin("C1", 0x0041F042, r"^mov byte ptr \[rdi \+ 0x40c\], bpl$", "a slot below 0x16 is recorded at the parent's +0x40C")
pin("C1", 0x0041F04C, r"^test dword ptr \[rdi \+ 0x284\], 0x8000000$", "bit 27 of the parent's +0x284 forces mode 0 ...")
pin("C1", 0x0041F05D, r"^movzx eax, byte ptr \[rdi \+ 0x40b\]$", "... otherwise the mode is the parent's default (+0x40B bits 0-1), no requested mode")
pin("C1", 0x0041F07B, r"^call 0x3e5cd0$", "the parent's section 3 (003E5CD0) ...")
pin("C1", 0x0041F0B1, r"^movzx edx, word ptr \[r15 \+ 0x36\]$", "mode 1: the child's own header word +0x36 as the bone")
pin("C1", 0x0041F10B, r"^movss xmm0, dword ptr \[r14 \+ rbp\*4 \+ 0x1c0\]$", "the slot's scale from section 3 +0x1C0")
pin("C1", 0x0041F158, r"^movzx eax, word ptr \[rax \+ rbp\*2\]$", "mode 0: the slot's bone word from section 3 +0")
pin("C1", 0x0041F19F, r"^mov ecx, dword ptr \[r14 \+ rax\*4 \+ 0x240\]$", "mode 0: the rotation from +0x240")
pin("C1", 0x0041F1CF, r"^mulss xmm0, dword ptr \[r14 \+ rdx\*4 \+ 0x40\]$", "mode 0: the offset from +0x40, scaled as in 0041EDE0")
pin("C1", 0x0041F143, r"^mov word ptr \[rdi \+ 0x2c8\], ax$", "the child's index is kept at the parent's +0x2C8 (slot below 0x16) ...")
pin("C1", 0x0041F246, r"^mov word ptr \[rdi \+ 0x2ca\], ax$", "... or +0x2CA (slot 0x16): the two children 00429760 re-attaches")
check("C1 0041F010's callers are 004215A0 (the dirty-bit-19 handler) and 00424D80 (twice)",
      sorted(c for c, s in sites(0x0041F010)) == [0x004215A0, 0x00424D80, 0x00424D80])
pin("C2", 0x002E9688, r"^mov edx, 0x1002143$", "002E9698: the id is 0x1002143 ...")
pin("C2", 0x002E968D, r"^cmovne edx, ecx$", "... or 0x1002D4F when the field bit holds - two constants")
pin("C2", 0x002E9698, r"^jmp 0x3e6150$", "... handed to the scaling wrapper")
for s, why in ((0x002ECE69, "002ECE50 passes its caller's edx through"), (0x003E6332, "003E6310 passes its caller's edx through")):
    f = 0x002ECE50 if s == 0x002ECE69 else 0x003E6310
    w = back_write(f, s, "rdx", 40)
    ok = (w is None) if f == 0x002ECE50 else (w is not None and "%s %s" % (w.mnemonic, w.op_str) == "mov edx, ebx")
    check("C2 %s (%08X)" % (why, s), ok, "%s" % ("no write to rdx" if w is None else "%08X %s %s" % (w.address, w.mnemonic, w.op_str)))
for a, rx in ((0x003E6694, r"dword ptr \[rbx \+ 0x300\]"), (0x003E66B0, r"dword ptr \[rbx \+ 0x300\]")):
    pin("C3", a, rx, "lead: 003E6680 reads the record's section-8 copy offset +0x300")
check("C3 lead: the four +0x300 accessors and their callers", sorted(c for c, s in sites(0x003E6680)) == [0x00425DC0]
      and sorted(c for c, s in sites(0x003E66D0)) == [0x00425E10]
      and sorted(c for c, s in sites(0x003E6710)) == [0x0041FCF0, 0x00520140]
      and sorted(c for c, s in sites(0x003E6D40)) == [0x00421280, 0x004213E0, 0x0042CBF0, 0x0042D050])

# ============================================================================================ R: the registry page
print("\n== R: the registry page")
# R1 header +0x0A
packs = sorted(p for p in NAMES if p.endswith("/battle_pack.bin"))
hw, nsec = collections.Counter(), 0
for p in packs:
    pk = read_all(p)
    starts = {struct.unpack_from("<I", pk, o)[0] for o in range(4, 0x120, 4)}
    for st in sorted(s for s in starts if 0 < s < len(pk) - 0x20):
        if pk[st:st + 4] == b"st2e":
            nsec += 1
            hw[struct.unpack_from("<H", pk, st + 0x0A)[0]] += 1
check("R1 nine battle_pack.bin, every st2e section header: the word at +0x0A (the high half of the u32 recordSize) is 0",
      len(packs) == 9 and nsec > 0 and hw == collections.Counter({0: nsec}), "%d sections, %s" % (nsec, dict(hw)))
rs = set()
for slot in [s for s in range(0x02EBF008, 0x02EBF208, 8) if s not in (0x02EBF188, 0x02EBF190)]:
    rs |= rip_load_seeds(slot, ("mov",))
g = S.Flow([0x0A], 1, stride=0x40, slot=0, seed_loads=rs)
g.run(sorted({s[0] for s in rs}))
hh = real_hits(g)
check("R1 census from %d slot loads in %d functions: no access covers +0x0A except the dword +8 of slot 02EBF158, whose "
      "header is {u16 +4 stride, u16 +6 count, u32 +8 rows} (not st2e)" % (len(rs), len({s[0] for s in rs})),
      {f for f, a, k, off, w in hh} == {0x00238660, 0x002FA920, 0x002FAE40} and all(off == 8 and w == 4 for f, a, k, off, w in hh),
      " ".join("%08X:+%X/%d" % (a, o, w) for f, a, k, o, w in hh))
check("R1 control: every one of those three functions loads its descriptor from 02EBF158",
      all(any(fn == f for fn, a, k in SC["refs"].get(0x02EBF158, ())) for f in (0x00238660, 0x002FA920, 0x002FAE40)))
pin("R1", 0x002FF110, r"^movzx r13d, word ptr \[rcx \+ 8\]$", "a stride reader (002FF110, the .ard slot 02EBF120 block) takes the low word only")

# R2 the board-request slots hold the board buffer's address
pin("R2", 0x00238364, r"^mov r9d, 3$", "00238260 passes 3 as 00384420's fourth argument ...")
pin("R2", 0x00384448, r"^mov ebx, r9d$", "... 00384420 keeps it in ebx ...")
pin("R2", 0x00384464, r"^mov ecx, ebx$", "... and spends it on 0036C1D0 ...")
pin("R2", 0x00384479, r"^call 0x36a190$", "... before allocating the buffer ...")
pin("R2", 0x0038447E, r"^mov rbx, rax$", "... which replaces rbx")
pin("R2", 0x003844B4, r"^lea rax, \[rsp \+ 0x30\]$", "the request descriptor is rsp+0x30 ...")
pin("R2", 0x003844B9, r"^mov dword ptr \[rsp \+ 0x38\], ebx$", "... and its +8 word is the buffer's low dword, not 3 ...")
pin("R2", 0x003844A0, r"^mov qword ptr \[rsp \+ 0x40\], r14$", "... its +0x10 the callback (the setter) ...")
pin("R2", 0x003844B1, r"^mov r8, rbx$", "... and the buffer is also the load's destination")
pin("R2", 0x0032E678, r"^movups xmm0, xmmword ptr \[rax\]$", "0032E620 copies the descriptor whole")
pin("R2", 0x0032E8E5, r"^mov r11d, dword ptr \[rcx \+ 8\]$", "0032E870 takes the descriptor's +8 word ...")
pin("R2", 0x0032E961, r"^mov dword ptr \[r10 \+ 0x60\], r11d$", "... into the request's +0x60")
pin("R2", 0x0032E34C, r"^mov ecx, dword ptr \[rcx \+ 0x60\]$", "the delivery call passes +0x60 as ecx")
pin("R2", 0x0032E38F, r"^mov ecx, dword ptr \[rcx \+ 0x60\]$", "the failure call passes +0x60 as ecx")
pin("R2", 0x00238396, r"^movsxd rbx, ecx$", "the setter sign-extends that word ...")
pin("R2", 0x002383A5, r"^call 0x3844f0$", "... after releasing the previous value through 003844F0 ...")
pin("R2", 0x002383AA, r"^mov qword ptr \[rip \+ 0x2c86def\], rbx$", "... and stores it at 02EBF1A0")
pin("R2", 0x003844F0, r"^jmp 0x3697f0$", "003844F0 is the free 003697F0")
pin("R2", 0x0055C0A8, r"^mov rdx, qword ptr \[rdx \+ rax\*8 \+ 0x2d9f1a0\]$", "0055BFF0 loads a slot of the 02EBF1A0 array ...")
pin("R2", 0x0055C0B0, r"^movzx ecx, word ptr \[rdx \+ 4\]$", "... and dereferences it: word +4 (licd width) ...")
pin("R2", 0x0055C0B9, r"^movzx eax, word ptr \[rdx \+ 6\]$", "... word +6 (licd height) ...")
pin("R2", 0x0055C0CC, r"^movzx ecx, word ptr \[rdx \+ rax\*2 \+ 8\]$", "... and the u16 cell grid at +8")
boards = sorted(p for p in NAMES if re.search(r"/board_\d+\.bin$", p))
okb = [p for p in boards if (lambda d: d[:4] == b"licd" and struct.unpack_from("<HH", d, 4) == (24, 24) and len(d) == 1160)(read_all(p))]
check("R2 control: every shipped board_N.bin is 'licd' with width and height 24 at +4 / +6 - the two words 0055BFF0 reads "
      "as bounds through the slot", len(boards) == 48 and len(okb) == 48, "%d of %d" % (len(okb), len(boards)))

# R3 the binder writes only the slot it is handed
pin("R3", 0x003845F4, r"^mov qword ptr \[rcx\], rdx$", "003845F0 stores the descriptor into [rcx] only")
bad, n3, slots3 = [], 0, set()
for f, s in sites(0x003845F0):
    n3 += 1
    w = back_write(f, s, "rcx", 16)
    tg = rip_target(w) if w is not None and w.mnemonic == "lea" else None
    if f == 0x00238640:
        ok = w is not None and w.op_str == "rcx, [rcx + rax*8]"
    else:
        ok = tg is not None and 0x02EBF008 <= tg <= 0x02EBF200 and tg != 0x02EBF198
        slots3.add(tg)
    if not ok:
        bad.append("%08X@%08X %s" % (f, s, "%s %s" % (w.mnemonic, w.op_str) if w else "?"))
check("R3 all %d calls of 003845F0 hand it one slot's own address (a rip lea), never 02EBF198; 00238640 indexes "
      "02F973C0, outside the registry" % n3, n3 == 42 and not bad, "; ".join(bad) or "%d distinct slots" % len(slots3))
pin("R3", 0x00237010, r"^lea rcx, \[rip \+ 0x2c87ff1\]$", "the 'array base' lea at 00237010 is slot 0 (02EBF008) itself ...")
pin("R3", 0x00237017, r"^movsxd rdx, dword ptr \[rax \+ 0x118\]$", "... and the data-driven value beside it is the descriptor")
pin("R3", 0x00238643, r"^lea rcx, \[rip \+ 0x2d5ed76\]$", "00238640's base is 02F973C0")

# R4 the motion-index setters' callers
check("R4 003DC330 (sets 02B58188) is referenced once, as a load-completion callback the binder 003DCBC0 registers",
      not sites(0x003DC330) and [fn for fn, a, k in SC["refs"].get(0x003DC330, ())] == [0x003DCBC0])
pin("R4", 0x003DC332, r"^mov qword ptr \[rip \+ 0x277be4f\], rax$", "003DC330 stores 02B58188")
check("R4 003DCF00 (02B58178) is called from 003EA6B0, 003EA710 and 003EA820; 003DCF10 (02B58180) from 003EA6B0 and 003EAA00",
      sorted({c for c, s in sites(0x003DCF00)}) == [0x003EA6B0, 0x003EA710, 0x003EA820]
      and sorted({c for c, s in sites(0x003DCF10)}) == [0x003EA6B0, 0x003EAA00])

print("\nFAILS %d" % FAILS)
