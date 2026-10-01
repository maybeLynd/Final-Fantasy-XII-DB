"""gr4_gr5_row_readers_check.py - GR-4 / GR-5: who reads action row +0x28, and who reads +0x0B? (OPUS lane SWE2-STRUCT,
2026-09-30). Static, the certified image, via Database/Tools/analysis-kit/gfz-scripts retool.py, regval.py, ptrtaint.py
and this record's rowflow.py; the shipped rows via the UQ-80 record's pack.py.

S0  the table is reached only through its slot: every reference to 02EBF138 is a qword load by rip (722 in 129
    functions) except the binder's one `lea` (00237FC0 -> 003845F0); every access through the loaded header is +4, +8
    or +0xC.
S1  rowflow from the 129 functions (depth 3): no header, reference, base or row pointer is stored to non-stack memory,
    no row is block-copied (16-byte access, rep movs, memcpy), no tagged argument reaches an indirect call except the
    header in r9 at rand() (IAT 008C3098, no arguments).
S2  positive control, all 60 offsets: every one of the 232 sites of the hop census (members/action-row-reader-hops.tsv)
    and the page's later-found readers reappear.
S3  the census for +0x0A / +0x0B / +0x28 (width-covering): the five MP-cost BYTE reads at +0x0A (the controls) and one
    WORD read at +0x28, 0030A209 in 0030A190 (BattleAction_GetPresentationParameter). Nothing covers +0x0B. The only
    access at an unknown row offset is 00320DE9 `[row + r9 + 2]`, and regval gives r9 in {0, 1} (+0x02 / +0x03).
S4  depth 5 adds no access covering the three fields.
S5  the kit instrument: ptrtaint MONOTONE from every row-pointer formation rowflow found (and every call-return of a
    row-returning function), disps [0x28, 0x0B], width-cover, depth 3. Every hit is typed: 0030A209 is the S3 reader; the
    rest have a base regval types as a constant, a non-stack load or another call's return, or sit where rowflow shows no
    row pointer (the function is never handed one, or the base register holds none at that site). Control: with disp
    0x0A the same run lists the five MP-cost reads.
S6  0030A190 read whole: id = (row - base) / stride; for 0xD0 <= id <= 0xF1 while the special-sequence state 022C2160 is
    5 or 6 it returns the word at +0x28; otherwise the +0x24 word unless 0xFFFF, +0x0C bit 30, or bit 15; else -1.
S7  its two callers hand the result on as an effect id: 0030C890 -> 0031A230 -> 002FCAC0 (the effect budget test, the
    02EC19C0 per-id cost summed over the active list, <= 0x18) and 0030CBE0 -> 00328360 -> 0042FCE0 -> 002FCBF0 (an
    effect request node, id at +0x20, submitted by 002FC860 as resource kind 0xB), the handle stored at record +0x24.
S8  data (543 us rows): +0x28 is non-zero on exactly 26 rows, all with 0xD0 <= id <= 0xF1, value = 120 + (id - 0xD0);
    +0x29 is 0 on every row, so the word read is the byte. +0x0B is non-zero on rows 182-207 only, where +0x0A is 0, and
    rows 182+2k / 183+2k carry the +0x0A (Mist charges) of summon row 0x106+k.
N1  negative control: without following calls (depth 0) the +0x28 reader vanishes - the row reaches 0030A190 as an
    argument (from 0030CBE0 directly, and through 0030C890), which is what the two earlier censuses did not follow.
"""
import os, re, sys, struct, threading

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "uq80-table-field-coverage")))
sys.setrecursionlimit(200000)
threading.stack_size(256 * 1024 * 1024 - 4096)   # regval's backward walk recurses deeply

fails = 0
MP_READS = {0x002F962B, 0x00309054, 0x00309178, 0x00309D7E, 0x0031DBD2}
READER = 0x0030A209
FIELDS = [0x0A, 0x0B, 0x28]


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def main():
    import rowflow as RF
    import ptrtaint as P
    import regval as V
    import pack
    R, SZ, SC = RF.R, RF.SZ, RF.SC

    def txt(a):
        i = next(R.md.disasm(R.at(a, 16), a, 1))
        return ("%s %s" % (i.mnemonic, i.op_str)).strip()

    # S0 - the slot's references
    refs = SC["refs"].get(RF.SLOT, set())
    loads = [r for r in refs if r[2] == "R"]
    other = sorted((f, a, k) for f, a, k in refs if k != "R")
    fns = RF.slot_functions()
    ok = len(fns) == 129 and len(loads) == 722 and other == [(0x00237FC0, 0x00237FD5, "lea")] \
        and all(re.match(r"mov r\w+, qword ptr \[rip \+ 0x[0-9a-f]+\]$", txt(a)) for f, a, k in loads) \
        and txt(0x00237FDE) == "call 0x3845f0"
    F3 = RF.Flow(FIELDS, 3)
    F3.run(fns)
    hdisp = sorted({d for f, a, d, t in F3.hdr})
    ok &= hdisp == [4, 8, 0xC]
    check("S0", ok, "%d qword loads of 02EBF138 in %d functions; other references %s; header accessed at %s"
          % (len(loads), len(fns), ["%08X %08X %s" % o for o in other], [hex(d) for d in hdisp]))

    # S1 - escapes, copies, indirect hand-offs
    ind = sorted(F3.indirect)
    ok = F3.esc == set() and F3.copies == set() and len(ind) == 1 and ind[0][:2] == (0x00384B10, 0x00384BA6) \
        and "'r9': ['H']" in ind[0][3] and R.at(0x008C3098, 8) is not None
    check("S1", ok, "%d functions walked, %d row-pointer formations, %d hand-offs into %d callees, %d stack-argument hand-offs; "
          "escapes %d, copies %d, tagged indirect calls %s (rand, IAT 008C3098)"
          % (len(F3.entry), len(F3.forms), len(F3.handoffs), len({h[2] for h in F3.handoffs}), len(F3.stackargs),
             len(F3.esc), len(F3.copies), ["%08X %s" % (i[1], i[3]) for i in ind]))

    # S2 - positive control over all 60 offsets
    FA = RF.Flow(list(range(60)), 3)
    FA.run(fns)
    got = {h[1]: h[4] for h in FA.hits}
    unk = {u[1] for u in FA.unk}
    tsv = os.path.join(HERE, "..", "..", "..", "07-Combat-Action", "Action-Definition-Row", "members", "action-row-reader-hops.tsv")
    rows = [l.rstrip("\r\n").split("\t") for l in open(tsv, encoding="utf-8")][1:]
    miss = [r for r in rows if int(r[4], 16) not in got]
    offmiss = [r for r in rows if int(r[4], 16) in got and got[int(r[4], 16)] != int(r[0], 16)]
    LATER = {0x00238033: 0x38, 0x00238043: 0x39, 0x00388BE6: 0x04, 0x0038503B: 0x05, 0x00321716: 0x1D,
             0x00321733: 0x1F, 0x00321744: 0x20, 0x0030AD10: 0x24, 0x003121F5: 0x3A, 0x0030A457: 0x30, 0x0030A46A: 0x30}
    later_bad = {"%08X" % a: got.get(a) for a, o in LATER.items() if got.get(a) != o}
    ok = len(rows) == 232 and not miss and not offmiss and not later_bad and 0x00320DE9 in unk
    check("S2", ok, "hop-census sites re-found %d/%d at their offsets (misplaced %d); later readers %d/%d%s"
          % (len(rows) - len(miss), len(rows), len(offmiss), len(LATER) - len(later_bad), len(LATER),
             "" if not later_bad else " BAD %s" % later_bad))

    # S3 - the three fields
    hits = sorted(F3.hits, key=lambda h: h[1])
    mp = {h[1] for h in hits if h[4] == 0x0A and h[5] == 1}
    others = [h for h in hits if h[1] not in MP_READS]
    comp = V.value_at(0x00320D70, 0x00320DE6, "r9", 3)
    ok = mp == MP_READS and [(h[1], h[4], h[5]) for h in others] == [(READER, 0x28, 2)] \
        and not any(RF.covers(h[4], h[5], 0x0B) for h in hits) \
        and {u[1] for u in F3.unk} == {0x00320DE9} and txt(0x00320DE9) == "movzx ecx, byte ptr [rax + rdx + 2]" \
        and txt(0x00320DE6) == "mov eax, r9d" and comp == {("C", 0), ("C", 1)}
    check("S3", ok, "+0x0A byte reads %s; other covering accesses %s; covering +0x0B: %d; unknown-offset %s with r9 %s"
          % (" ".join("%08X" % a for a in sorted(mp)), ["%08X %s w%d %s" % (h[1], hex(h[4]), h[5], h[6]) for h in others],
             sum(1 for h in hits if RF.covers(h[4], h[5], 0x0B)), ["%08X" % u[1] for u in F3.unk], sorted(comp)))

    # S4 - depth 5
    F5 = RF.Flow(FIELDS, 5)
    F5.run(fns)
    ok = {h[1] for h in F5.hits} == {h[1] for h in F3.hits} and {u[1] for u in F5.unk} == {u[1] for u in F3.unk} \
        and not F5.esc and not F5.copies
    check("S4", ok, "depth 5 walks %d functions (depth 3: %d); covering accesses %d = %d; escapes %d, copies %d"
          % (len(F5.entry), len(F3.entry), len(F5.hits), len(F3.hits), len(F5.esc), len(F5.copies)))

    # S5 - the kit instrument, ptrtaint monotone, every hit typed
    seeds = sorted(F3.forms)
    rowret = sorted(f for f, t in F3.retsum.items() if any(isinstance(x, tuple) for x in t))
    for f in rowret:
        seeds += [(cf, cs, "rax") for cf, cs in SC["calls"].get(f, ()) if cf in SZ]
    P.MONOTONE = True
    ph, pseen = P.run_typed(seeds, [0x28, 0x0B], True, 3)
    walked = set(F3.entry)
    buckets, residue, rowhits = {}, [], set()

    def notrow(v):
        k, x = v
        if k == "C":
            return True
        if k == "M":
            return not re.search(r"\[(rsp|rbp)", x)
        if k == "R":
            return int(x, 16) not in set(rowret) | set(F3.retsum) and int(x, 16) != RF.RESOLVE
        return False
    for h in sorted(set(ph), key=lambda h: h[1]):
        if h[2] == "ret":
            continue
        t = h[4].split(" ", 1)[1]
        reg = t.split(",")[1].strip() if h[2] == "e" else re.findall(r"\[(\w+)", t)[0]
        reg = RF.FAM.get(reg, reg)
        if h[1] in {x[1] for x in F3.hits}:
            rowhits.add(h[1])
            continue
        vs = V.value_at(h[0], h[1], reg, 3)
        if vs and all(notrow(v) for v in vs):
            key = "regval " + "/".join(sorted({v[0] for v in vs}))
        elif h[0] not in walked:
            key = "no row pointer reaches the function"
        elif not {x for x in F3.probe.get(h[1], {}).get(reg, set()) if x not in ("H", "F")}:
            key = "no row pointer in the base at the site"
        else:
            residue.append(h)
            continue
        buckets[key] = buckets.get(key, 0) + 1
    ph0, _ = P.run_typed(seeds, [0x0A], True, 3)
    mp_pt = {h[1] for h in ph0 if h[1] in MP_READS}
    ok = rowhits == {READER} and residue == [] and mp_pt == MP_READS
    check("S5", ok, "%d seeds (%d formations + returns of %s), %d functions; %d accesses/escapes: row reader %s; excluded %s; "
          "residue %d; control disp 0x0A re-finds %d/5 MP reads"
          % (len(seeds), len(F3.forms), " ".join("%08X" % f for f in rowret), len({k[0] for k in pseen}),
             sum(1 for h in set(ph) if h[2] != "ret"), " ".join("%08X" % a for a in sorted(rowhits)),
             dict(sorted(buckets.items())), len(residue), len(mp_pt)))

    # S6 - what 0030A190 does with +0x28
    want = {0x0030A1BD: "sub r9d, eax", 0x0030A1C8: "div r8d", 0x0030A1CB: "cmp eax, 0xd0", 0x0030A1D0: "jb 0x30a213",
            0x0030A1F4: "cmp eax, 0xf1", 0x0030A1F9: "ja 0x30a213", 0x0030A201: "add eax, -5", 0x0030A204: "cmp eax, 1",
            0x0030A207: "ja 0x30a213", 0x0030A209: "movzx eax, word ptr [rbx + 0x28]", 0x0030A20D: "add rsp, 0x20",
            0x0030A212: "ret", 0x0030A213: "movzx eax, word ptr [rbx + 0x24]", 0x0030A221: "test dword ptr [rbx + 0xc], 0x40000000",
            0x0030A22D: "js 0x30a238", 0x0030A238: "or eax, 0xffffffff"}
    bad = {"%08X" % a: txt(a) for a, w in want.items() if txt(a) != w}
    gate = R.at(0x0030A1FB, 6)
    gtarget = 0x0030A1FB + 6 + struct.unpack_from("<i", gate, 2)[0]
    ok = not bad and gtarget == 0x022C2160 and txt(0x0030A196) == "mov rbx, rcx"
    check("S6", ok, "0030A190: row -> id by (row - base) / stride; 0xD0 <= id <= 0xF1 and [%08X] - 5 <= 1 -> word +0x28; "
          "else +0x24 (not 0xFFFF, +0x0C bit 30 clear, bit 15 clear) or -1%s" % (gtarget, "" if not bad else " BAD %s" % bad))

    # S7 - where the value goes
    callers = sorted(SC["calls"].get(0x0030A190, ()))
    want = {0x0030C8EB: "mov rcx, rdi", 0x0030C8F1: "call 0x30a190", 0x0030C8F6: "mov ecx, eax", 0x0030C8F8: "call 0x31a230",
            0x0030CCC0: "mov rcx, rsi", 0x0030CCC3: "call 0x30a190", 0x0030CCC8: "mov ecx, eax", 0x0030CCCA: "call 0x328360",
            0x0030CCCF: "mov dword ptr [rbx + 0x24], eax", 0x0031A241: "call 0x2fcac0", 0x00328368: "jmp 0x42fce0",
            0x0042FCE6: "jmp 0x2fcbf0", 0x002FCC7F: "mov word ptr [rbx + 0x20], di", 0x002FCC83: "call 0x2fc860",
            0x002FC891: "mov esi, 0xb", 0x002FCB1C: "movzx edx, word ptr [r11 + r10*8 + 4]", 0x002FCB28: "cmp edx, 0x18"}
    bad = {"%08X" % a: txt(a) for a, w in want.items() if txt(a) != w}
    ok = callers == [(0x0030C890, 0x0030C8F1), (0x0030CBE0, 0x0030CCC3)] and not bad \
        and F3.probe[0x0030CCC3]["rcx"] >= {("E", 0)} and F3.probe[0x0030C8F1]["rcx"] >= {("E", 0)}
    check("S7", ok, "callers %s (rcx a row at both); result -> 0031A230 -> 002FCAC0 effect budget (<= 0x18) and -> 00328360 -> "
          "002FCBF0 effect request (id at node +0x20, 002FC860 resource kind 0xB), handle at record +0x24%s"
          % (["%08X@%08X" % c for c in callers], "" if not bad else " BAD %s" % bad))

    # S8 - the shipped rows
    recs, _h = pack.records(0x3C)
    nz28 = [i for i, r in enumerate(recs) if r[0x28]]
    nz0B = [i for i, r in enumerate(recs) if r[0x0B]]
    ok = len(recs) == 543 and len(nz28) == 26 and all(0xD0 <= i <= 0xF1 and recs[i][0x28] == 120 + i - 0xD0 for i in nz28) \
        and not any(r[0x29] for r in recs) and nz0B == list(range(182, 208)) and all(recs[i][0x0A] == 0 for i in nz0B) \
        and all(recs[182 + 2 * k][0x0B] == recs[183 + 2 * k][0x0B] == recs[0x106 + k][0x0A] for k in range(13))
    gaps = [hex(i) for i in range(0xD0, 0xF2) if i not in nz28]
    check("S8", ok, "+0x28 non-zero on %d rows, all in 0xD0..0xF1, value 120 + (id - 0xD0); zero inside the span on %s; "
          "+0x29 zero on all; +0x0B non-zero on rows %d..%d (+0x0A 0 there), pairs = summon rows 0x106..0x112 +0x0A %s"
          % (len(nz28), gaps, nz0B[0], nz0B[-1], [recs[0x106 + k][0x0A] for k in range(13)]))

    # N1 - the reader needs a call hop
    F0 = RF.Flow(FIELDS, 0)
    F0.run(fns)
    ok = READER not in {h[1] for h in F0.hits} and {h[1] for h in F0.hits} <= MP_READS
    check("N1", ok, "without following calls: covering accesses %s - 0030A209 absent (the row arrives as an argument)"
          % " ".join("%08X" % h[1] for h in sorted(F0.hits, key=lambda h: h[1])))
    print("FAILS %d" % fails)


th = threading.Thread(target=main)
th.start()
th.join()
