"""sd101_pass1.py - SD-101: which widgets carry flag bit 24 (+0x40 & 0x01000000), and so draw their background and
messages 3/4 in the second bracket pass (OPUS, 2026-09-30). Static, the certified image, via
Database/Tools/analysis-kit/gfz-scripts/retool.py and the `pe` module of _index/candidates/rc22-34-resource-readers-0930/.
"""
import collections, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
sys.path.insert(0, os.path.join(HERE, "..", "rc22-34-resource-readers-0930"))
import retool as T  # noqa: E402
import pe  # noqa: E402

R, SZ, c = T.R, T.sizes(), T.scan()
fails = 0


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def txt(a):
    i = next(R.md.disasm(R.at(a, 16), a, 1))
    return "%s %s" % (i.mnemonic, i.op_str)


# P1 - the gate: the draw walker tests node +0x40 bit 24 against the pass index 0208F564 (002461BB-002461C8,
#      0024623A-00246245); 00252990, the second bracket, walks the two UI roots [0208EA28] and [0208EA40] with pass 1
check("P1", txt(0x002461BB) == "mov eax, dword ptr [rbx + 0x40]" and txt(0x002461C2) == "shr eax, 0x18"
      and txt(0x002461C8).endswith("0x1e49396], eax") and txt(0x0024623A) == "mov ecx, dword ptr [rbx + 0x40]"
      and txt(0x002529BB).endswith("0x1e3c066]") and txt(0x002529C2) == "call 0x245110"
      and txt(0x002529C7).endswith("0x1e3c072]") and txt(0x002529CE) == "call 0x245110",
      "bit 24 of node +0x40 against 0208F564; pass 1 = 00252990 over roots [0208EA28], [0208EA40]")
# P2 - a new widget starts with bit 24 clear: the constructor 002465F0 merges only bit 17, ORs 0x80A and sets bit 14
#      from its pooled argument into +0x40 (CONTRACT-widget-object.md row +0x40)
check("P2", txt(0x0024664A) == "and ecx, 0x20000" and txt(0x00246653) == "or ecx, 0x80a" and txt(0x002466F2) == "or dword ptr [rdi + 0x40], eax",
      "the constructor's +0x40 writes touch bits 17, 11/3/1 and 14 only")
# P3 - the setters, image-wide: an immediate OR of bit 24 into a +0x40 dword (or bit 0 of a +0x43 byte), or a register
#      shifted left by 24 and ORed into +0x40
imm, shl = [], []
for f in pe.funcs:
    xs = pe.dis(f)
    for k, x in enumerate(xs):
        o = x.op_str
        m = re.match(r"(dword|byte) ptr \[(\w+) \+ (0x40|0x43)\], (0x[0-9a-f]+|\d+)$", o)
        if x.mnemonic in ("or", "bts") and m and m.group(2) not in ("rsp", "rbp"):
            v = int(m.group(4), 0)
            if (m.group(1) == "dword" and m.group(3) == "0x40" and (v >> 24) & 1) or (m.group(1) == "byte" and m.group(3) == "0x43" and v & 1):
                imm.append(x.address)
        m2 = re.match(r"dword ptr \[(\w+) \+ 0x40\], (e\w\w|r\d+d)$", o)
        if x.mnemonic == "or" and m2 and any(y.mnemonic == "shl" and y.op_str == "%s, 0x18" % m2.group(2) for y in xs[max(0, k - 4):k]):
            shl.append(x.address)
check("P3", sorted(imm) == [0x005728E6, 0x00573AF5] and sorted(shl) == [0x00247754, 0x0057390E, 0x00573952],
      "immediate setters %s; shifted setters %s" % (["%08X" % a for a in sorted(imm)], ["%08X" % a for a in sorted(shl)]))
# P4 - 00247730(widget, on): clears bit 24, ORs (on & 1) << 24, and recurses over the children list (+0x18, siblings
#      +0x20): it moves a whole subtree between the passes
check("P4", txt(0x0024773A) == "and dword ptr [rcx + 0x40], 0xfeffffff" and txt(0x00247751) == "shl eax, 0x18"
      and txt(0x0024774B) == "mov rbx, qword ptr [rcx + 0x18]" and txt(0x00247765) == "call 0x247730"
      and txt(0x0024776A) == "mov rbx, qword ptr [rbx + 0x20]",
      "00247730 = set the subtree's pass bit")
# P5 - its 32 outside call sites, by the edx they pass (1 / 0 / a variable) and the page the address index files the
#      caller under
idx = {}
for l in open(os.path.join(HERE, "..", "..", "ADDRESS-INDEX.md"), encoding="utf-8"):
    m = re.match(r"\| `([0-9A-F]{8})` \| (.*)", l)
    if m:
        p = re.findall(r"\[([^\]]+)\]", m.group(2))
        idx[int(m.group(1), 16)] = p[0] if p else "(no page)"
rows, kinds = [], collections.Counter()
for f, site in sorted(c["calls"].get(0x00247730, ())):
    if f == 0x00247730:
        continue
    ins = [i for i in R.md.disasm(R.at(f, SZ.get(f, 0x2000)), f) if i.address < site][-10:]
    e = next(("%s %s" % (i.mnemonic, i.op_str) for i in reversed(ins) if re.match(r"(edx|rdx|dl)\b", i.op_str)), "?")
    k = "1" if e == "mov edx, 1" else "0" if e == "xor edx, edx" else "var"
    kinds[k] += 1
    rows.append((f, site, k, idx.get(f, "(not indexed)")))
by = collections.defaultdict(list)
for f, site, k, page in rows:
    by[page].append("%08X:%s" % (site, k))
for page in sorted(by):
    print("      %-52s %s" % (page, " ".join(by[page])))
check("P5", len(rows) == 32 and kinds == {"1": 19, "0": 3, "var": 10},
      "32 call sites: on = 1 at 19, 0 at 3, a variable at 10 (%s)" % dict(kinds))
# P6 - the handbook toggles its panes as a set: 005738D0(on) stores on at [0209AC30]+0xDEA, calls 00247920(on), and sets
#      the pass bit on [02CA9718]+0x110 and [[02CA9718]+0xF8]+0xE0 directly and on the subtrees [02CA9718]+0xE8 and
#      0028F570(); 00572890 / 00573980 put the +0x110 pane (built from a template by 002CCCA0) in pass 1
check("P6", txt(0x005738E1) == "mov byte ptr [rax + 0xdea], bl" and txt(0x005738E7) == "call 0x247920"
      and txt(0x005738F3) == "mov rdx, qword ptr [rax + 0x110]" and txt(0x00573911) == "mov rcx, qword ptr [rax + 0xe8]"
      and txt(0x00573937) == "mov rcx, qword ptr [rcx + 0xe0]" and txt(0x00573955) == "call 0x28f570" and txt(0x00573969) == "jmp 0x247730"
      and txt(0x005728B6) == "call 0x2ccca0" and txt(0x005728E6) == "or dword ptr [rcx + 0x40], 0x1000000",
      "handbook: 005738D0 moves its panes between passes as one set")
print("FAILS %d" % fails)
