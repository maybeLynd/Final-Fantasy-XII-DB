"""sd107_register_stores.py - can a store set a text element's kind byte (+0xA3) to 1? The widget setters 002475D0 /
00247680 and the register-sourced +0xA3 stores regval cannot bound (SWE2-ORACLE, 2026-09-30; register SD-107, follow-up
to OPUS's sd107-kind1-writers-0930 and OPUS's census Tools/work/OPUS/sd107_regstores.py). Static, certified image,
through Database/Tools/analysis-kit/gfz-scripts/retool.py and regval.py. Nothing is executed.

  S1  002475D0 stores (dl == 0xFF ? 1 : dl) at [rcx+0xA3]; 00247680 stores dl there
  S2  a widget base is not a text-element base: the widget constructor puts a code pointer at +0 and a qword pointer at
      +0x48; the text-element builder writes floats at +0x04, +0x0C and +0x48
  S3  the setter call census: 12 sites of 002475D0, 6 of 00247680, 2 of the wrapper 00247590; value set per site;
      the sites that can store 1 are exactly the nine listed in S4
  S4  each of those nine passes a widget base: the self pointer of a registered widget message procedure, a widget
      returned by the allocator 00244F50, or a slot of a container that 00559860 fills from 00244F50
  S5  widgets that carry text carry the element after their 0xC0 header (+0xC0 / +0xE0 / +0xD0), so the element's kind
      byte is widget +0x163 / +0x183 / +0x173, never widget +0xA3
  S6  every dispatcher / emit call site that reads a kind byte passes an element pointer (widget + 0xC0/0xD0/0xE0, a stack
      element, or a builder's own element), never a widget base
  S7  the 93 register-sourced +0xA3 stores regval leaves unresolved: 1 is the widget setter (S3/S4), 11 copy the same
      field of another object, 7 store through the `this` of a virtual method (vtable at +0), the rest are listed
  C1  control: the census reproduces OPUS's 180 = 86 resolved + 1 has-1 + 93 unresolved
"""
import collections, os, re, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import retool as T  # noqa: E402
import regval as V  # noqa: E402

sys.setrecursionlimit(20000)
R, SZ, SC = T.R, V.SZ, T.scan()
fails = 0


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def txt(a):
    i = next(R.md.disasm(R.at(a, 16), a, 1))
    return ("%s %s" % (i.mnemonic, " ".join(i.op_str.split()))).strip()


def has(pairs):
    bad = [("%08X" % a, txt(a)) for a, s in pairs if txt(a) != s]
    return not bad, bad


def vals(f, site, reg):
    try:
        return V.value_at(f, site, reg, 3)
    except RecursionError:
        return {("U", "walk too deep")}


# S1
ok, bad = has([(0x002475D9, "cmp edx, 0xff"), (0x002475DF, "movzx eax, dl"), (0x002475E2, "mov r8d, 1"),
               (0x002475E8, "cmove eax, r8d"), (0x002475EC, "mov byte ptr [rcx + 0xa3], al"),
               (0x0024768D, "mov byte ptr [rcx + 0xa3], dl"), (0x0024759D, "call 0x2475d0"),
               (0x005C5230, "xor eax, eax"), (0x005C5232, "ret")])
check("S1", ok, "002475D0 maps 0xFF to 1 before the +0xA3 store; 00247680 stores dl; 005C5230 returns 0 %s" % (bad or ""))

# S2
ok, bad = has([(0x00246641, "mov qword ptr [rdi], rbx"), (0x0024662E, "lea rax, [rip + 0x37ebfb]"),
               (0x00246677, "lea rax, [rip + 0x6ceb1a]"), (0x00246687, "mov qword ptr [rdi + 0x48], rax"),
               (0x00247583, "mov qword ptr [rcx + 0x48], rax"), (0x00246748, "call rax"),
               (0x002B3CF3, "movss dword ptr [rbx + 0x48], xmm1"), (0x002B3D35, "mov dword ptr [rbx + 4], 0x41b80000"),
               (0x002B3D41, "mov dword ptr [rbx + 0xc], 0x3f800000"), (0x002B3C40, "mov byte ptr [rcx + 0xa3], 0")])
check("S2", ok, "widget: +0 message procedure (default 005C5230), +0x48 qword pointer (00915198 / 00247570); text element: "
      "float 23.0 at +0x04, 1.0 at +0x0C, float at +0x48 - one base cannot be both %s" % (bad or ""))

# S3 - setter call census and per-site values
calls = {t: sorted(SC["calls"].get(t, ())) for t in (0x002475D0, 0x00247680, 0x00247590)}
may1, never1 = [], []
for t, lst in calls.items():
    for f, s in [x[:2] for x in lst]:
        vs = vals(f, s, "rdx")
        if t == 0x00247590:          # the wrapper forwards rdx to 002475D0
            vs = vs
        cs = {v[1] for v in vs if v[0] == "C"}
        rets = {v[1] for v in vs if v[0] == "R"}
        unk = [v for v in vs if v[0] in ("M", "U") or (v[0] == "R" and v[1] != "0x5c5230")]
        one = (0xFF in cs or 1 in cs) if t != 0x00247680 else (1 in cs)
        (may1 if one or unk else never1).append((t, f, s, sorted(map(str, vs))[:3]))
print("      setter sites: 002475D0 %d, 00247680 %d, 00247590 %d" % tuple(len(calls[t]) for t in (0x002475D0, 0x00247680, 0x00247590)))
for t, f, s, v in never1:
    print("      never-1 %08X in %08X  rdx %s" % (s, f, v))
for t, f, s, v in may1:
    print("      may-1   %08X in %08X  rdx %s" % (s, f, v))
MAY1 = {0x00228070, 0x00242060, 0x003F4649, 0x002A7164, 0x0057C802, 0x00559B64, 0x0055A2E3, 0x0056B79B, 0x0056B9BE}
check("S3", [len(calls[t]) for t in (0x002475D0, 0x00247680, 0x00247590)] == [12, 6, 2] and {s for _, _, s, _ in may1} == MAY1,
      "20 setter sites; the nine that can store 1 (0xFF, 1 or an unbounded value) are %s" % " ".join("%08X" % s for s in sorted(MAY1)))


# S4 - each may-1 site passes a widget base
END = {0x005599D0: 0x00559DD4}   # 005599D0's jump table (0x120000 + 0x439DD4, read at 005599F5) follows its last jmp


def self_reg(f, reg, setup):
    """reg is set from the incoming rcx at entry and only restored from the frame afterwards; rcx = reg at the site."""
    ins = [i for i in R.md.disasm(R.at(f, SZ[f]), f) if i.address < END.get(f, f + SZ[f])]
    entry = [i for i in ins[:16] if i.mnemonic == "mov" and i.op_str == "%s, rcx" % reg]
    other = [i for i in ins if V.canon(reg) in V.writes(i) and i not in entry
             and not (i.mnemonic == "pop" or re.match(r"%s, qword ptr \[(rsp|r11) \+ 0x[0-9a-f]+\]$" % reg, i.op_str))]
    return bool(entry) and not other and txt(setup) == "mov rcx, %s" % reg


HANDLERS = [  # site, function, self register, rcx setup, registration (lea of the function, allocator call)
    (0x00228070, 0x00227EE0, "rsi", 0x0022806D, 0x00227EB8, 0x00227EBF, "call 0x244f50"),
    (0x00242060, 0x00241D40, "rsi", 0x0024205D, 0x00241C6C, 0x00241C73, "call 0x2465f0"),
    (0x003F4649, 0x003F4330, "rdi", 0x003F4636, 0x003F4761, 0x003F47A4, "call 0x244f50"),
    (0x0057C802, 0x0057C480, "rsi", 0x0057C7EB, 0x0057C39F, 0x0057C3B8, "call 0x244f50"),
    (0x00559B64, 0x005599D0, "rbx", 0x00559B5E, 0x005598A8, 0x005598D6, "call 0x244f50"),
    (0x0056B79B, 0x0056B4D0, "rsi", 0x0056B78A, 0x0056B3BE, 0x0056B3C5, "call 0x244f50"),
    (0x0056B9BE, 0x0056B4D0, "rsi", 0x0056B9B5, 0x0056B3BE, 0x0056B3C5, "call 0x244f50"),
]
res4 = []
for site, f, reg, setup, lea, alloc, alloc_txt in HANDLERS:
    li = next(R.md.disasm(R.at(lea, 16), lea, 1))
    lt = li.address + li.size + li.operands[1].mem.disp
    ok = self_reg(f, reg, setup) and lt == f and txt(alloc) == alloc_txt
    res4.append(ok)
    print("      S4 %08X: self %s of widget procedure %08X, registered at %08X (%s) %s" % (site, reg, f, lea, alloc_txt, "ok" if ok else "FAIL"))
v70 = vals(0x002A70B0, 0x002A7164, "rcx")
ok70 = v70 == {("R", "0x244f50")} and txt(0x002A715C) == "mov rcx, rbx"
print("      S4 002A7164: rcx = %s (the widget 002A2C00 gets from the allocator 00244F50) %s" % (sorted(v70), "ok" if ok70 else "FAIL"))
v5a = vals(0x0055A1F0, 0x0055A2E3, "rcx")
ok5a = (v5a == {("M", "0055A230 qword ptr [rsi]")} and has([(0x0055A214, "lea rsi, [rcx + 0x140]"), (0x0055A229, "lea ebp, [rdi + 4]"),
        (0x00559884, "lea rbx, [rcx + 0x140]"), (0x005598D6, "call 0x244f50"), (0x005598DB, "mov qword ptr [rbx], rax"),
        (0x005598E0, "add rbx, 8"), (0x005598E4, "cmp edi, 4")])[0])
print("      S4 0055A2E3: rcx = [container+0x140+8i], i < 4, the slots 00559860 fills from 00244F50 %s" % ("ok" if ok5a else "FAIL"))
ok, bad = has([(0x005599F5, "mov r8d, dword ptr [rcx + rax*4 + 0x439dd4]"), (0x00559DCC, "jmp 0x5c5230"), (0x00244FCD, "call 0x2465f0"), (0x00245011, "call 0x2465f0"), (0x00244F70, "mov edi, 0xc0")])
check("S4", all(res4) and ok70 and ok5a and ok, "all nine may-store-1 sites act on widget bases (00244F50 / 00245000 both "
      "construct through 002465F0; default size 0xC0) %s" % (bad or ""))

# S5 - embedded element offsets
ok, bad = has([(0x00227EB3, "mov ecx, 0x190"), (0x00227FC5, "lea rcx, [rsi + 0xc0]"), (0x00227FE3, "call 0x2b3280"),
               (0x00227F95, "lea rcx, [rsi + 0xc0]"), (0x00227F9C, "call 0x2abec0"),
               (0x00241DD2, "lea rcx, [rsi + 0xe0]"), (0x00241DEB, "call 0x2b3280"),
               (0x0057C50D, "lea rcx, [rsi + 0xe0]"), (0x0057C520, "call 0x2b3400"), (0x0057C5D4, "lea rcx, [rsi + 0xe0]"),
               (0x002A5CD2, "lea rdi, [rcx + 0xd0]"), (0x002A4457, "lea rbx, [rcx + 0xd0]")])
check("S5", ok, "0x190-byte widget 00227EE0 = 0xC0 header + 0xD0 element at +0xC0; 00241D40 / 0057C480 build at +0xE0; the "
      "message window's element is at +0xD0 - kind bytes at widget +0x163 / +0x183 / +0x173 %s" % (bad or ""))

# S6 - readers' element pointers
READ = [(0x002A5CED, 0x002A5CEA, "mov rcx, rdi"), (0x0057C9B7, 0x0057C9B0, "lea rcx, [rsi + 0xe0]"),
        (0x002A3492, 0x002A348A, "lea rcx, [rsp + 0x130]"), (0x002A56A7, 0x002A569F, "lea rcx, [rbp - 0x40]"),
        (0x002A6D48, 0x002A6D43, "lea rcx, [rsp + 0x60]"), (0x00227F9C, 0x00227F95, "lea rcx, [rsi + 0xc0]"),
        (0x002421A5, 0x0024219E, "lea rcx, [rsi + 0xe0]"), (0x002A37BB, 0x002A37AC, "lea rcx, [rdi + 0xd0]"),
        (0x002A37D5, 0x002A37CE, "lea rcx, [rdi + 0xd0]"), (0x002A77F2, 0x002A77E8, "lea rdi, [rbx + 0xd0]"),
        (0x0057C8E7, 0x0057C8E0, "lea rcx, [rsi + 0xe0]"), (0x002A4541, 0x002A4457, "lea rbx, [rcx + 0xd0]"),
        (0x002A4B3E, 0x002A4899, "lea rbx, [rsp + 0x40]"), (0x002A4E2E, 0x002A4E29, "lea rcx, [rsp + 0x40]"),
        (0x00227F39, 0x00227F26, "lea r9, [rsi + 0xc0]"), (0x00242373, 0x00242366, "lea r9, [rsi + 0xe0]"),
        (0x0057C92A, 0x0057C916, "lea r9, [rsi + 0xe0]")]
disp = {t: len(SC["calls"].get(t, ())) for t in (0x002B3930, 0x002ABF20, 0x002ABEC0, 0x002AF960, 0x002D8550)}
ok, bad = has([(b, s) for _, b, s in READ])
check("S6", ok and disp == {0x002B3930: 2, 0x002ABF20: 3, 0x002ABEC0: 6, 0x002AF960: 4, 0x002D8550: 3},
      "kind readers 002B3930 x2, 002ABF20 x3, 002ABEC0 x6, 002AF960 x4 (002D8550's element is its r9: x3) take widget+0xC0/0xD0/0xE0, "
      "stack or builder elements; no reader is passed a widget base %s" % (bad or ""))

# S7 + C1 - OPUS's register-store census, then the unresolved 93
W = {"byte": 1, "word": 2, "dword": 4, "qword": 8}
rows = []
for f in SZ:
    for i in V.body(f)[0]:
        if i.mnemonic != "mov":
            continue
        m = re.match(r"(byte|word|dword|qword) ptr \[(\w+)(?: \+ (0x[0-9a-f]+))?\], (\w+)$", i.op_str)
        if not m or m.group(2) in ("rsp", "rbp", "rip") or not V.canon(m.group(4)):
            continue
        w, d = W[m.group(1)], int(m.group(3), 16) if m.group(3) else 0
        if d <= 0xA3 < d + w:
            rows.append((f, i.address, m.group(1), m.group(2), d, m.group(4)))
cnt, unres = collections.Counter(), []
for f, a, wd, base, d, src in rows:
    vs = vals(f, a, src)
    cs = [x[1] for x in vs if x[0] == "C"]
    oth = [x for x in vs if x[0] != "C"]
    bv = {(c >> ((0xA3 - d) * 8)) & 0xFF for c in cs}
    k = "resolved-no-1" if not oth and 1 not in bv else ("has-1" if 1 in bv else "unresolved")
    cnt[k] += 1
    if k == "unresolved":
        unres.append((f, a, wd, base, d, src, oth))
check("C1", len(rows) == 180 and cnt == {"resolved-no-1": 86, "has-1": 1, "unresolved": 93},
      "register-sourced +0xA3 stores: %d, %s (OPUS: 180 / 86 / 1 / 93)" % (len(rows), dict(cnt)))

import pefile  # noqa: E402
pe = pefile.PE(R.b.EXE, fast_load=True)
Q = collections.defaultdict(list)
for sec in pe.sections:
    data = sec.get_data()
    for off in range(0, len(data) - 7, 8):
        v = struct.unpack_from("<Q", data, off)[0]
        if v in SZ:
            Q[v].append(pe.OPTIONAL_HEADER.ImageBase + sec.VirtualAddress + off)


def classes(fn):
    return sorted({c for s in Q.get(fn, ()) for _, c in [T.vtable_start(s)] if c})


cls7 = collections.Counter()
for f, a, wd, base, d, src, oth in unres:
    if a == 0x0024768D:
        cls7["setter"] += 1
        continue
    if all(x[0] == "M" and re.search(r"%s ptr \[\w+ \+ %s\]$" % (wd, hex(d)), x[1]) for x in oth):
        cls7["same-field copy"] += 1
        print("      S7 copy  %08X %08X %s [%s+%#x] <- %s" % (f, a, wd, base, d, "; ".join(x[1] for x in oth)[:120]))
        continue
    bt, cl = vals(f, a, base), []
    for b in bt:
        m = re.match(r"argument rcx of (\w+)", str(b[1]))
        c = classes(int(m.group(1), 16)) if b[0] == "U" and m else []
        if not c:
            cl = None
            break
        cl.append(c[0])
    if cl:
        cls7["polymorphic base"] += 1
        print("      S7 this  %08X %08X [%s+%#x]: this of %s" % (f, a, base, d, cl[0]))
        continue
    cls7["open"] += 1
    print("      S7 open  %08X %08X %s [%s+%#x] <- %s" % (f, a, wd, base, d, "; ".join(sorted(str(x) for x in oth))[:110]))
check("S7", sum(cls7.values()) == 93 and cls7["setter"] == 1,
      "the 93: %s" % dict(sorted(cls7.items())))
print("FAILS %d" % fails)
