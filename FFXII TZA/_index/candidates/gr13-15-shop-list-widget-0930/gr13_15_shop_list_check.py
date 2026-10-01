"""gr13_15_shop_list_check.py - GR-13 / GR-14 / GR-15: the shop list rows, the list widget's message-26 layout write, and
the list kind each widget family is built with (SWE2-STRUCT for OPUS, 2026-09-30). Static, the certified image, via
Database/Tools/analysis-kit/gfz-scripts/retool.py, regval.py and structflow.py (structflow gained seed_calls and per-site
(func, disp, address) seed_loads for this row; with neither passed every earlier result is unchanged).

GR-13  A1  0057DAD0 is a layout-A filler: its cursor is entry + 8 (0057DAFF lea rbx, [rcx + 8]) and entry + 0 is rbx - 8
           (0057DB55), so its stores land at +0 (name qword), +8 (id), +0xA, +0xC, +0xE and +0x10 (price) - the offsets
           0057DED0 / 0057DD60 / 0057DC30 write. "Layout B" (id +0, price +8) does not exist.
       A2  structflow from 0057CF20 (the allocator returns seeded): the four fillers receive the list at 11 sites, 0057CF20 returns it,
           and it escapes only to widget +0xE0 (005656AE, 00565785) and to the driver's +0xC8 (0056E55A); the driver keeps
           a row pointer at +0xD0 (0056D56F). 0057D620 hands every filler rcx = 0 (count only): it builds no list.
       A3  the holder-field census (every qword load of +0xC8 / +0xD0 / +0xE0 in the direct-call closure of the shop,
           driver and list-widget procedures and their row callbacks) is at its fixpoint; the typed seed sites below are
           every one of those loads whose base is the shop widget, the driver or a list widget.
       A4  every reader of a row's +0x10 dword, from any holder: the driver 0056D370, its selection test 0056E700, the four
           row callbacks 0056CBC0 / 0056CD50 / 0056CF10 / 0056D1B0 and their helpers 0056D870 / 0056DA80. Each either
           compares the whole dword with 0x80000000 or clears bit 31 (btr ..., 0x1f) before using the value. Every +0x08
           read is a word (the id). Family A bodies write +0x10 only as layout state (005651E0 message 26, 00564650)
           or move whole rows (00565BD0); one family-A row pointer goes into a constructor message (005665B0, not followed).
       A5  the sentinel's consumer: in sale mode (driver+0xD8 bit 0) 0056E700 returns 8 when dword[row+0x10] >= 0x80000000
           (0056E715-0056E72B) and the driver refuses the selection (0056D576-0056D57D); 0056CF10 greys the row the same way.
           The sell tab runs the driver in sale mode: shop +0x194 bit 0 for ids 0x597-0x59D / 0x59F-0x5A2 (0056DE3D) goes
           to the driver as its create bit (0056D71D-0056D736); the sell tab's id is 0x5A2.
       A6  which shop rows 0057DAD0 fills: tail arms 1 (0x0C, 0x18; class 5) and 3 (0x06, 0x0F, 0x1B; class 7), and 4
           (0x07; class 0xD); the zero-price flag 0x20 is set only for selector 0x0F (0057D3ED cmp esi, 0xf / cmovne).
       A7  category 7 = loot: 002FABD0's nibble table 00D0F990 maps id nibble 2 to 7; 0057CF20's category is selector - 0x14,
           so 0x1B is category 7, and tail arm 3 resolves its ids with class 7 (0057D3FF); 00D113B8[7] = class 7.
GR-14  B1  005651E0 (the message-26 arm) is entered only by tail jumps from the four list procedures 005636F0 / 00563930 /
           00563B10 / 00563D20; no rip reference or data qword names it.
       B2  those four procedures are named only by the four leas in 00564B90 and by no data qword; 00564AC0 -> 00244F50 ->
           002465F0 stores the procedure into the new widget's +0 (00246641).
       B3  00564B90 creates them only for ids 0x405..0x40F: ids 0x405-0x408 -> 005636F0, 0x409 and 0x40E -> 00563930,
           0x40D -> 00563B10, 0x40F -> 00563D20, 0x40A-0x40C -> none; the id table 00D233A0 gives them kinds 0..7.
       B4  the shop widget is created by 0056DD50 with procedure 0056E140 (0056DD66); 0056E140 dispatches messages 1..20
           through its table (0056E3B8) and sends 26 to 005C5230 (xor eax, eax / ret); the driver 0056D370 handles 1, 2, 12,
           18 and sends 26 to the same stub (0056D3B8).
       B5  the shop widget's +0xE0 is written only by 005655F0 (0056563E, 005656AE), 0056E410 (0056E561) and 0056E140's
           message-18 arm (0056E398); on a shop widget 005655F0 runs only from 0056E410 (0056E535), which moves the list
           at 0056E55A.
       B6  message-26 senders (immediate 0x1A stored as a message id): the list-control draw bodies 002D2600 (002D2680) and
           002D28E0 (002D2924), both called only from 002D1420; they call the target's procedure qword [target] with it.
GR-15  C1  the create message: 00564AC0 puts the id-table slot at create data + 8 (00564B01, 00564B0C); 002465F0 copies data
           + 8 to message + 8 (00246726-0024672A); each list procedure copies message + 8 to its own message's + 0xC
           (0056372F, 0056395F, 00563B4D, 00563D4F), which 00564010 passes to 00564780 (005640ED). So family A's kind is the
           slot of its widget id: 0..7. 00565E00 binds exactly the eight ids 0x405-0x409 and 0x40D-0x40F.
       C2  family B: 0057C070 takes the id from 00D23920[tab] (0x5AF, 0x5A2, 0x5AE; then 0), tab bounded by the 3-entry loop
           in 0057BD40 (0057BEA0); 0056E140's create arm stores message + 8 at +0x192 (0056E16D-0056E173); 0056DD50 passes
           it to 00564780 (0056DD8B). Kinds 32, 19, 31 (buy, sell, bazaar); 005655F0 remaps 0x20 / 0x13 through 0057D5E0
           (00D23D60: 0x14-0x1B, 0x1D; 00D23D6C: 0x08-0x0C, 0x0F).
       C3  family C: 003FDFE0's create arm tests message + 8 against 1: kind 1 -> 003FD860 -> 003FD360 with edx = 1 (the
           constant; selector 0x41); any other -> 003FD6B0 -> 003FD360 with edx = message + 8. 003FDA20 (sole caller
           003FF040, only when +0x178 == 0x400) puts its ecx there; 003FF040's sole caller is the equip menu 003FF360,
           message 12 sub 0x8001, ecx = message + 0x10 (the chosen row). 003FDFE0 handles kinds 0..4, 01F2CC98 holds five
           row tables, and 003FF360 allocates five rows: selectors 0x40..0x44.
       C4  only two instructions in the image store a byte at +0x17F (005647B4, 003FD371); inside the three families'
           closure no store of any width covers it.
       C5  kind -> selector -> filler, for every kind the three families can hold (tables read from the image).
       C6  structflow is unchanged for earlier callers (the new seeds are opt-in) and the result is stable at depth 5.
PAGE   D1  the band tables 00D23960 / 00D23988 have five rip-relative reference sites outside 0057CF20 / 0057D620, three of
           them reading each record's second word (the page says nine sites, all in the two builders, +2 never read).
Prints PASS/FAIL per step and FAILS n last.
"""
import os, struct, sys, collections

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import retool as T  # noqa: E402
import regval as V  # noqa: E402
import structflow as S  # noqa: E402

R, SZ, SC = T.R, T.sizes(), T.scan()
fails = 0


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def ins(a):
    return next(R.md.disasm(R.at(a, 16), a, 1))


def txt(a):
    i = ins(a)
    return ("%s %s" % (i.mnemonic, i.op_str)).strip()


def has(a, s):
    return s in txt(a)


def body(f):
    return list(R.md.disasm(R.at(f, SZ[f]), f))


def u16(a):
    return struct.unpack("<H", R.at(a, 2))[0]


def u32(a):
    return struct.unpack("<I", R.at(a, 4))[0]


def i32(a):
    return struct.unpack("<i", R.at(a, 4))[0]


def u64(a):
    return struct.unpack("<Q", R.at(a, 8))[0]


def rip_refs(t):
    return sorted(SC["refs"].get(t, ()))


def calls_to(t):
    return sorted(SC["calls"].get(t, ()))


def calls_of(f):
    out = set()
    for i in body(f):
        if i.mnemonic in ("call", "jmp") and i.operands and i.operands[0].type == 2:
            t = i.operands[0].imm
            if t in SZ and not (f <= t < f + SZ[f]):
                out.add(t)
    return out


def closure(roots, depth, keep):
    seen, fr = set(roots), list(roots)
    for _ in range(depth):
        nf = []
        for f in fr:
            for c in calls_of(f):
                if c not in seen:
                    seen.add(c)
                    nf.append(c)
        fr = nf
    return {f for f in seen if keep(f)}


_QW = None


def qword_holders(vals):
    """every aligned qword in any section whose value is in vals"""
    global _QW
    import pefile
    if _QW is None:
        pe = pefile.PE(R.b.EXE, fast_load=True)
        base = pe.OPTIONAL_HEADER.ImageBase
        _QW = [(base + s.VirtualAddress, s.get_data()) for s in pe.sections]
    out = []
    for va, d in _QW:
        for v in vals:
            p = struct.pack("<Q", v)
            k = d.find(p)
            while k >= 0:
                if k % 8 == 0:
                    out.append((va + k, v))
                k = d.find(p, k + 1)
    return out


# ---------------------------------------------------------------- GR-13
print("== GR-13: who reads a 0057DAD0 row's price, and does such a list reach the driver")
DAD0, DED0, DD60, DC30 = 0x0057DAD0, 0x0057DED0, 0x0057DD60, 0x0057DC30
check("A1a", has(0x0057DAFF, "lea rbx, [rcx + 8]") and has(0x0057DB55, "lea r14, [rbx - 8]")
      and has(0x0057DEF1, "lea rbx, [rcx + 0x10]") and has(0x0057DD86, "lea rdi, [rcx + 0x10]"),
      "cursors: 0057DAD0 rbx = entry + 8, r14 = rbx - 8 = entry; 0057DED0 rbx / 0057DD60 rdi = entry + 0x10")

CALLSEEDS = {(0x0057CF20, 0x002497E0), (0x0057CF20, 0x0057CDD0)}
fb = S.Flow(fields=tuple(range(0x20)), depth=3, stride=0x20, seed_calls=CALLSEEDS)
fb.run([0x0057CF20])
wr = collections.defaultdict(set)
for (f, a, k, form, off, w, t) in fb.hits:
    if k == "w":
        wr[f].add(off)
check("A1b", wr[DAD0] == {0x00, 0x08, 0x0A, 0x0C, 0x0E, 0x10} and wr[DD60] == {0x00, 0x08, 0x0A, 0x0C, 0x0E, 0x10}
      and wr[DED0] == {0x00, 0x08, 0x0A, 0x0B, 0x0C, 0x0E, 0x10} and wr[DC30] == {0x00, 0x08, 0x0A, 0x0C, 0x0E, 0x10},
      "entry offsets written (structflow, stride 0x20): 0057DAD0 %s; 0057DD60 %s; 0057DC30 %s; 0057DED0 %s"
      % tuple(" ".join("+%02X" % o for o in sorted(wr[x])) for x in (DAD0, DD60, DC30, DED0)))
pricew = sorted((f, a) for (f, a, k, form, off, w, t) in fb.hits if k == "w" and off == 0x10 and w == 4 and f == DAD0)
check("A1c", pricew == [(DAD0, 0x0057DB9F), (DAD0, 0x0057DBCC), (DAD0, 0x0057DBE0)]
      and has(0x0057DBCC, "mov dword ptr [rbx + 8], eax") and has(0x0057DBDC, "bts eax, 0x1f")
      and has(0x0057DB98, "mov qword ptr [r14], rax") and has(0x0057DB7E, "mov word ptr [rbx], ax"),
      "0057DAD0's price dword and zero-price bit land at entry +0x10 (0057DB9F, 0057DBCC, 0057DBE0; bts at 0057DBDC); "
      "its id at +8 (0057DB7E), its name pointer at +0 (0057DB98)")

handed = {(c, s, t) for (c, s, t, a) in fb.handoffs if t in (DAD0, DED0, DD60, DC30)}
fsites = sorted(s for (c, s, t) in handed)
check("A2a", len(handed) == 11 and {t for (_, _, t) in handed} == {DAD0, DED0, DD60, DC30}
      and all(c == 0x0057CF20 for (c, _, _) in handed)
      and fb.retsum.get(0x0057CF20) == {"B"},
      "0057CF20 hands its list to all four fillers at %d sites (%s) and returns it (ret 0057D513)"
      % (len(fsites), ", ".join("%08X" % s for s in fsites)))
esc = sorted((f, a) for (f, a, t, x) in fb.esc)
check("A2b", esc == [(0x005655F0, 0x005656AE), (0x00565720, 0x00565785)] and not fb.copies and not fb.indirect,
      "the returned list escapes only at 005655F0 005656AE and 00565720 00565785 (mov [rdi + 0xe0], rax); no copy, "
      "no indirect call")
D620 = [0x0057D783, 0x0057D7F7, 0x0057D896, 0x0057D8D5, 0x0057D908, 0x0057D974, 0x0057D9B3, 0x0057DA2B, 0x0057DA56]
d620ok = []
for s in D620:
    b = [i for i in body(0x0057D620) if i.address < s]
    last = next(i for i in reversed(b) if "rcx" in i.op_str.split(",")[0] or "ecx" in i.op_str.split(",")[0])
    d620ok.append(("%s %s" % (last.mnemonic, last.op_str)) == "xor ecx, ecx")
check("A2c", all(d620ok) and sorted(s for (c, s) in [(c, s) for (c, s) in calls_to(DAD0) + calls_to(DED0) + calls_to(DD60)
                                                     if c == 0x0057D620]) == D620,
      "0057D620 calls the fillers at 9 sites, each with rcx = 0 (xor ecx, ecx) - it counts, it builds no list; "
      "0057D610 is its only caller (a jmp)")

# A3: holder census over the procedures' direct-call closure
ROOTS_D = [0x0056E140, 0x0056D370, 0x0056CF10, 0x0056D1B0, 0x0056CD50, 0x0056CBC0, 0x0056DD50, 0x0056C950]
ROOTS_A = [0x005636F0, 0x00563930, 0x00563B10, 0x00563D20, 0x003FDFE0, 0x00563560, 0x005637D0, 0x005639D0, 0x00563C00,
           0x00564010, 0x00564B90, 0x003FDA20, 0x003FD6B0, 0x003FD860]
UI = lambda f: 0x00560000 <= f < 0x00580000
UIC = lambda f: 0x00560000 <= f < 0x00580000 or 0x003FC000 <= f < 0x00400000


def census(roots, depth, keep, disps):
    out = set()
    for f in closure(roots, depth, keep):
        for i in body(f):
            if i.mnemonic == "lea":
                continue
            for op in i.operands:
                if op.type == 3 and op.mem.disp in disps and op.size == 8 and \
                        i.reg_name(op.mem.base) not in ("rip", "rsp", "rbp"):
                    out.add((f, i.address))
    return out


cD = {d: census(ROOTS_D, d, UI, (0xC8, 0xD0, 0xE0)) for d in (3, 12)}
cA = {d: census(ROOTS_A, d, UIC, (0xE0,)) for d in (5, 12)}
check("A3a", cD[3] == cD[12] and cA[5] == cA[12] and len(cD[3]) == 37 and len(cA[5]) == 39,
      "holder-field census at its fixpoint: shop/driver closure %d sites (depth 3 = depth 12), list-widget closure "
      "%d +0xE0 sites (depth 5 = depth 12); closure limited to 00560000-0057FFFF and 003FC000-003FFFFF" % (len(cD[3]), len(cA[5])))
# typed seeds: the loads (mov / add) of a list pointer or row pointer, base = shop widget, driver or list widget
SHOP_E0 = [(0x0056E140, 0xE0, 0x0056E387), (0x0056E410, 0xE0, 0x0056E550), (0x005655F0, 0xE0, 0x0056562D),
           (0x00565A00, 0xE0, 0x00565AA1)]
DRV_C8 = [(0x0056D370, 0xC8, 0x0056D3C2), (0x0056D370, 0xC8, 0x0056D568), (0x0056C850, 0xC8, 0x0056C8C8),
          (0x0056CBC0, 0xC8, 0x0056CBC8), (0x0056CD50, 0xC8, 0x0056CD5B), (0x0056CF10, 0xC8, 0x0056CF18),
          (0x0056D1B0, 0xC8, 0x0056D1BB), (0x0056E410, 0xC8, 0x0056E43F), (0x0056E410, 0xC8, 0x0056E4EF),
          (0x0056E410, 0xC8, 0x0056E53A), (0x0056E5D0, 0xC8, 0x0056E648), (0x0056DED0, 0xC8, 0x0056DFDF)]
DRV_D0 = [(0x0056D370, 0xD0, a) for a in (0x0056D450, 0x0056D4B3, 0x0056D4C5, 0x0056D5E1)] + \
         [(0x0056C490, 0xD0, 0x0056C796), (0x0056CA60, 0xD0, 0x0056CB19), (0x0056D9D0, 0xD0, 0x0056D9ED)]
LIST_E0 = [(0x00563560, 0xE0, 0x00563575), (0x005637D0, 0xE0, 0x005637E5), (0x005639D0, 0xE0, 0x005639E5),
           (0x00563C00, 0xE0, 0x00563C0F), (0x00563DC0, 0xE0, 0x00563DC9), (0x00563F10, 0xE0, 0x00563F39),
           (0x00564650, 0xE0, 0x00564680), (0x005651E0, 0xE0, 0x00565285), (0x005651E0, 0xE0, 0x005653C2),
           (0x005651E0, 0xE0, 0x005655A1), (0x00565720, 0xE0, 0x00565730), (0x00565720, 0xE0, 0x0056588B),
           (0x003FDAD0, 0xE0, 0x003FDC70), (0x003FDFE0, 0xE0, 0x003FE053), (0x003FDFE0, 0xE0, 0x003FE07E),
           (0x00564E10, 0xE0, 0x00564F62), (0x00565BD0, 0xE0, 0x00565BEE), (0x005665B0, 0xE0, 0x00566628)]
# census loads NOT seeded, each with the reason (its base is not a list holder, or it only tests / stores)
NOT_LIST = {0x0056C815: "r15 = [driver + 0x10] = the shop widget; its +0xC8 is the child from 00567190",
            0x0056DE13: "the shop widget's +0xC8 child (00567190 at 0056DDE4)",
            0x0056E0D0: "the shop widget's +0xC8 child", 0x0056DDEC: "store of the child"}
seeds = SHOP_E0 + DRV_C8 + DRV_D0 + LIST_E0
seedaddr = {a for (_, _, a) in seeds}
allc = cD[3] | cA[5]
unseeded = sorted(a for (f, a) in allc if a not in seedaddr)
reason = {}
for a in unseeded:
    i = ins(a)
    m = i.mnemonic
    if a in NOT_LIST:
        reason[a] = NOT_LIST[a]
    elif m == "cmp":
        reason[a] = "a null test"
    elif m == "mov" and i.operands[0].type == 3:
        reason[a] = "a store"
    elif m == "call":
        reason[a] = "a call"
    else:
        reason[a] = None
check("A3b", seedaddr <= {a for (_, a) in allc} and all(reason[a] for a in unseeded),
      "%d typed seed loads, all inside the census; the %d other census sites are null tests, stores or the shop widget's "
      "child pointer (%s)" % (len(seedaddr), len(unseeded), ", ".join("%08X" % a for a in unseeded if a in NOT_LIST)))

fr = S.Flow(fields=tuple(range(0x20)), depth=3, stride=0x20, seed_calls=CALLSEEDS, seed_loads=set(seeds))
fr.run([0x0057CF20] + sorted({s[0] for s in seeds}))
H = sorted(fr.hits)
p10 = sorted({(f, a) for (f, a, k, form, off, w, t) in H if k == "r" and off in (0x10, 0x11, 0x12, 0x13) and w == 4})
EXP10 = [(0x0056CBC0, 0x0056CC7E), (0x0056CBC0, 0x0056CCA2), (0x0056CD50, 0x0056CE07), (0x0056CD50, 0x0056CE31),
         (0x0056CF10, 0x0056CFF3), (0x0056CF10, 0x0056D023), (0x0056CF10, 0x0056D0C8), (0x0056D1B0, 0x0056D267),
         (0x0056D1B0, 0x0056D291), (0x0056D370, 0x0056D461), (0x0056D870, 0x0056D8F1), (0x0056DA80, 0x0056DBCA),
         (0x0056E700, 0x0056E71A), (0x0056E700, 0x0056E797)]
check("A4a", [x for x in p10 if x[0] not in (DAD0, DED0, DD60, DC30)] == EXP10,
      "every dword read of a row's +0x10 outside the fillers (%d): %s"
      % (len(EXP10), ", ".join("%08X" % a for (_, a) in EXP10)))


def price_use_ok(a):
    """the read at a is `cmp dword [r + 0x10], 0x80000000`, or its destination register gets `btr reg, 0x1f` within the
    next eight instructions before any other write to it"""
    i = ins(a)
    if i.mnemonic == "cmp":
        return "0x80000000" in i.op_str
    dst = i.op_str.split(",")[0]
    f = T.func_of(a, SZ)
    seq = [x for x in body(f) if x.address > a][:8]
    for x in seq:
        if x.mnemonic == "btr" and x.op_str == "%s, 0x1f" % dst:
            return True
        if x.op_str.split(",")[0] == dst and x.mnemonic not in ("cmp", "test"):
            return False
    return False


bad = [a for (_, a) in EXP10 if not price_use_ok(a)]
cmps = [a for (_, a) in EXP10 if ins(a).mnemonic == "cmp"]
check("A4b", not bad and has(0x0056D468, "btr ebx, 0x1f") and has(0x0056D02B, "btr eax, 0x1f"),
      "each of them either compares the whole dword with 0x80000000 (%d sites: %s) or clears bit 31 of the loaded value "
      "within the next eight instructions before any other use (%d sites)"
      % (len(cmps), ", ".join("%08X" % a for a in cmps), len(EXP10) - len(cmps)))
r08 = sorted({(f, a, w) for (f, a, k, form, off, w, t) in H if k == "r" and off == 0x08 and f not in (DAD0, DED0, DD60, DC30)})
check("A4c", r08 and all(w == 2 for (_, _, w) in r08) and (0x0056D370, 0x0056D464, 2) in r08,
      "every +0x08 read outside the fillers is a word, the id (%d sites, the driver's 0056D464 among them); none reads "
      "a price there" % len(r08))
w10 = sorted({(f, a) for (f, a, k, form, off, w, t) in H if k == "w" and 0x10 <= off <= 0x15
              and f not in (DAD0, DED0, DD60, DC30)})
check("A4d", {f for (f, _) in w10} == {0x005651E0, 0x00564650, 0x00565BD0},
      "the only non-filler writers of +0x10..+0x15 are 005651E0 (message 26, %d stores), 00564650 (the reset, "
      "0056468E / 00564692) and 00565BD0 (whole-row moves, 00565C7B / 00565C92) - all list-widget (family A) bodies"
      % sum(1 for (f, _) in w10 if f == 0x005651E0))
check("A4e", sorted((f, a) for (f, a, t, x) in fr.esc) == [(0x005655F0, 0x005656AE), (0x00565720, 0x00565785),
                                                          (0x005665B0, 0x00566631), (0x0056D370, 0x0056D56F),
                                                          (0x0056E410, 0x0056E55A)]
      and {(c, s) for (c, s, t, a) in fr.handoffs if t == 0x0056E700} ==
      {(0x0056C490, 0x0056C7AF), (0x0056CA60, 0x0056CB2C), (0x0056D370, 0x0056D576), (0x0056D9D0, 0x0056D9F7)},
      "with the holders seeded the list escapes at the same two widget stores, the driver's +0xC8 (0056E55A), its row "
      "pointer +0xD0 (0056D56F) and one family-A row pointer handed to a constructor message (005665B0 00566631, not "
      "followed); the driver's row reaches 0056E700 from 0056C7AF, 0056CB2C, 0056D576 and 0056D9F7")
check("A5", has(0x0056E715, "test byte ptr [rdx], 1") and has(0x0056E71A, "cmp dword ptr [rcx + 0x10], 0x80000000")
      and has(0x0056E721, "mov edx, 8") and has(0x0056E72B, "cmovb edx, eax") and has(0x0056D576, "call 0x56e700")
      and has(0x0056D57B, "test eax, eax") and has(0x0056D598, "mov eax, ebp")
      and has(0x0056CFF3, "cmp dword ptr [r14 + 0x10], 0x80000000") and has(0x0056D46F, "test r8b, 1")
      and has(0x0056DE3D, "lea ecx, [rsi - 0x597]") and has(0x0056DE4E, "lea ecx, [rsi - 0x59f]")
      and has(0x0056DE65, "or dword ptr [rdi + 0x194], ebx") and has(0x0056DE72, "and r8d, ebp")
      and has(0x0056D71D, "mov eax, dword ptr [r9 + 4]") and has(0x0056D736, "mov dword ptr [rdi + 0xe4], eax")
      and u32(0x00D23924) == 0x5A2,
      "sale mode (driver +0xD8 bit 0, the commit's 0056D46F bit): a row whose +0x10 dword is >= 0x80000000 scores 8 in "
      "0056E700 and the driver declines it (0056D57B); the sell tab id 0x5A2 sets the sale bit (0056DE3D-0056DE72 -> "
      "0056C950 -> 0056D71D)")
# A6 / C5: selector -> head / tail arm -> filler
hmap, tmap = R.at(0x0057D528, 61), R.at(0x0057D594, 0x45)
htab = [0x120000 + u32(0x0057D514 + 4 * k) for k in range(5)]
ttab = [0x120000 + u32(0x0057D568 + 4 * k) for k in range(11)]
ARMFILL = {0x0057D168: "0057DED0", 0x0057D1A1: "0057DED0", 0x0057D1A6: "0057DED0 x2", 0x0057D26A: "0057DD60",
           0x0057D35C: "0057DD60", 0x0057D494: "0057DD60", 0x0057D330: "0057DAD0 class 5", 0x0057D3E3: "0057DAD0 class 7",
           0x0057D41B: "0057DAD0 class 0xD", 0x0057D4BD: "0057DC30", 0x0057D4DF: "none (freed, returns 0)"}


def route(sel):
    h = htab[hmap[sel - 5]] if 0 <= sel - 5 <= 0x3C else 0x0057D08B
    t = ttab[tmap[sel]] if sel <= 0x44 else 0x0057D4DF
    return h, t


dad = sorted(s for s in range(0x45) if ARMFILL[route(s)[1]].startswith("0057DAD0"))
check("A6", dad == [0x04, 0x06, 0x07, 0x0C, 0x0F, 0x18, 0x1B] and has(0x0057D3EA, "or ebx, 0x20")
      and has(0x0057D3ED, "cmp esi, 0xf") and has(0x0057D3F0, "cmovne ebx, r14d") and has(0x0057D3FF, "mov r9d, 7")
      and has(0x0057D33F, "mov r9d, 5") and has(0x0057D47F, "mov r9d, 0xd"),
      "selectors routed to 0057DAD0: %s; the zero-price flag 0x20 only for 0x0F (0057D3EA-0057D3F0)"
      % ", ".join("0x%02X" % s for s in dad))
nib = [i32(0x00D0F990 + 4 * k) for k in range(8)]
check("A7", nib == [4, -1, 7, 6, 5, 8, 9, 10] and has(0x0057CFB9, "lea r8d, [rsi - 0x14]") and R.at(0x00D113B8, 12)[7] == 7
      and has(0x002FAD20, "mov eax, dword ptr [rsp + rax*4 + 0x38]") and has(0x002FABE3, "movdqa xmm0, xmmword ptr [rip"),
      "002FABD0 nibble table 00D0F990 = %s: id nibble 2 (0x2xxx) -> category 7; shop category = selector - 0x14 "
      "(0057CFB9), so 0x1B is category 7 = loot; category->class 00D113B8[7] = 7 = 0057DAD0's class on tail arm 3" % nib)

# ---------------------------------------------------------------- GR-14
print("== GR-14: can message 26's layout write land on a shop list")
PROCS = [0x005636F0, 0x00563930, 0x00563B10, 0x00563D20]
c51 = calls_to(0x005651E0)
check("B1", sorted(c for (c, s) in c51) == PROCS and all(txt(s).startswith("jmp") for (c, s) in c51)
      and not rip_refs(0x005651E0) and not qword_holders([0x005651E0]),
      "005651E0 is entered only by tail jumps from %s; no rip reference, no data qword"
      % ", ".join("%08X@%08X" % x for x in c51))
pr = {p: rip_refs(p) for p in PROCS}
check("B2", all(len(v) == 1 and v[0][0] == 0x00564B90 and v[0][2] == "lea" for v in pr.values())
      and not any(calls_to(p) for p in PROCS) and not qword_holders(PROCS)
      and has(0x00564B4B, "call 0x244f50") and has(0x00244FCD, "call 0x2465f0") and has(0x00246641, "mov qword ptr [rdi], rbx"),
      "the four procedures are named only by leas in 00564B90 (%s) and by no data qword; 00564AC0 -> 00244F50 -> "
      "002465F0 stores the procedure at widget +0 (00246641)" % ", ".join("%08X" % v[0][1] for v in pr.values()))
jt = [0x120000 + u32(0x00564C4C + 4 * k) for k in range(11)]
TGT = {0x00564C0A: 0x005636F0, 0x00564C13: 0x00563930, 0x00564C1C: 0x00563B10, 0x00564C25: 0x00563D20, 0x00564C2C: None}
idproc = {0x405 + k: TGT[jt[k]] for k in range(11)}
tbl = {u16(0x00D233A0 + 4 * k): u16(0x00D233A2 + 4 * k) for k in range(33)}
famA = {i: (tbl.get(i), p) for i, p in idproc.items() if p}
check("B3", has(0x00564BE9, "lea eax, [r10 - 0x405]") and has(0x00564BF0, "cmp eax, 0xa") and has(0x00564B1D, "test r9, r9")
      and famA == {0x405: (0, 0x005636F0), 0x406: (1, 0x005636F0), 0x407: (2, 0x005636F0), 0x408: (3, 0x005636F0),
                   0x409: (4, 0x00563930), 0x40D: (5, 0x00563B10), 0x40E: (6, 0x00563930), 0x40F: (7, 0x00563D20)},
      "00564B90 creates a list-procedure widget only for ids 0x405..0x40F (jump table 00564C4C): %s; 0x40A-0x40C get no "
      "procedure and 00564AC0 then creates nothing (00564B1D)"
      % ", ".join("%X->kind %d/%08X" % (i, k, p) for i, (k, p) in sorted(famA.items())))
jt2 = [0x120000 + u32(0x0056E3B8 + 4 * k) for k in range(20)]
handled = sorted(k + 1 for k, t in enumerate(jt2) if t != 0x0056E3AB)
check("B4", has(0x0056DD66, "lea r9, [rip + 0x3d3]") and rip_refs(0x0056E140) == [(0x0056DD50, 0x0056DD66, "lea")]
      and has(0x0056E14B, "dec eax") and has(0x0056E14D, "cmp eax, 0x13") and has(0x0056E150, "ja 0x56e3ab")
      and has(0x0056E3B3, "jmp 0x5c5230") and txt(0x005C5230) == "xor eax, eax" and txt(0x005C5232) == "ret"
      and handled == [1, 8, 9, 10, 12, 14, 15, 18, 19, 20] and has(0x0056D3B8, "call 0x5c5230")
      and rip_refs(0x0056D370) == [(0x0056C950, 0x0056C9BC, "lea")],
      "the shop widget's procedure 0056E140 (installed only at 0056DD66) handles messages %s and sends 26 to 005C5230 "
      "(xor eax, eax / ret); the driver 0056D370 (installed only at 0056C9BC) sends it there too (0056D3B8)" % handled)
shopE0w = sorted(a for (f, a) in cD[3] if ins(a).mnemonic == "mov" and ins(a).operands[0].type == 3 and ins(a).operands[0].mem.disp == 0xE0)
check("B5", shopE0w == [0x0056563E, 0x005656AE, 0x0056E398, 0x0056E561]
      and sorted(c for (c, s) in calls_to(0x005655F0)) == [0x003FD6B0, 0x003FD860, 0x003FDAD0, 0x00564010, 0x00564E10, 0x0056E410]
      and has(0x0056E535, "call 0x5655f0") and has(0x0056E55A, "mov qword ptr [rsi + 0xc8], rcx"),
      "in the shop/driver closure +0xE0 is stored only at %s; 005655F0's callers are the list families' creators "
      "(003FD6B0, 003FD860, 003FDAD0, 00564010, 00564E10) and 0056E410, which moves the list at 0056E55A"
      % ", ".join("%08X" % a for a in shopE0w))
check("B6", has(0x002D2680, "mov dword ptr [rsp + 0x60], 0x1a") and has(0x002D2924, "mov dword ptr [rsp + 0x78], 0x1a")
      and has(0x002D2796, "lea rdx, [rsp + 0x60]") and has(0x002D279E, "call rax") and has(0x002D2B54, "lea rdx, [rsp + 0x78]")
      and has(0x002D2B5C, "call rax") and calls_to(0x002D2600) == [(0x002D1420, 0x002D14AE)]
      and calls_to(0x002D28E0) == [(0x002D1420, 0x002D14C1)],
      "message 26 is sent by the list-control draw bodies 002D2600 / 002D28E0 (only from 002D1420) through the target's "
      "own procedure (call rax = qword [target]); the shop list control forwards it to the driver, which routes it to the stub")

# ---------------------------------------------------------------- GR-15
print("== GR-15: which kinds each widget family is built with")
v1 = V.value_at(0x00564010, 0x005640F0, "rdx", 1)
check("C1a", v1 == {("M", "005640ED dword ptr [rsi + 0xc]")}
      and all(has(a, "mov eax, dword ptr [rdx + 8]") for a in (0x0056372F, 0x0056395F, 0x00563B4D, 0x00563D4F))
      and all(has(a, "mov dword ptr [rsp + 0x2c], eax") for a in (0x00563737, 0x00563967, 0x00563B55, 0x00563D57))
      and has(0x00246726, "mov rax, qword ptr [rsi + 8]") and has(0x0024672A, "mov qword ptr [rsp + 0x28], rax")
      and has(0x00564B01, "movzx eax, word ptr [r11 + rax*4 + 2]") and has(0x00564B0C, "mov qword ptr [rsp + 0x28], rax"),
      "source 1 (00564780 edx at 005640F0) = %s = the procedure's create message + 8 = 002465F0's copy of create data "
      "+ 8 = 00564AC0's id-table slot: family A's kind is the slot of its widget id, 0..7 (B3)" % sorted(v1))
ids565 = sorted(ins(a).operands[1].imm if ins(a).operands[0].type == 1 else None
                for a in (0x00565E81, 0x00565EA9, 0x00565EBD, 0x00565EE7, 0x00565EFB, 0x00565F23, 0x00565F40, 0x00565F5B))
b2 = [x.address for x in body(0x00565E00) if x.mnemonic == "call" and x.op_str == "0x2cd3c0"]
check("C1b", ids565 == [0x405, 0x406, 0x407, 0x408, 0x409, 0x40D, 0x40E, 0x40F] and len(b2) == 8
      and has(0x005663DB, "call 0x564b90"),
      "the menu 00565E00 binds exactly these eight ids (8 calls to 002CD3C0, %s) and creates the chosen one through "
      "00564B90 (005663DB)" % ", ".join("0x%X" % i for i in ids565))
v2 = V.value_at(0x0056DD50, 0x0056DD98, "rdx", 1)
tabs = [u32(0x00D23920 + 4 * k) for k in range(4)]
check("C2a", v2 == {("M", "0056DD8B byte ptr [rax + 0x192]")} and has(0x0056E16D, "movzx eax, byte ptr [rdx + 8]")
      and has(0x0056E173, "mov byte ptr [rbx + 0x192], al") and has(0x0056DD79, "call 0x564ac0")
      and tabs == [0x5AF, 0x5A2, 0x5AE, 0] and [tbl[t] for t in tabs[:3]] == [32, 19, 31]
      and has(0x0057C0FE, "mov edx, dword ptr [rax + rsi*4]") and has(0x0057BEA0, "cmp esi, 3")
      and has(0x0057C087, "cmp dword ptr [rcx + rdi*4 + 0x138], 0") and calls_to(0x0056DD50) == [(0x0057C070, 0x0057C101)],
      "source 2 (00564780 edx at 0056DD98) = %s = the shop widget's create message + 8 (0056E16D-0056E173) = the slot "
      "of id 00D23920[tab] = 0x5AF / 0x5A2 / 0x5AE -> kinds 32 / 19 / 31; tab passes only if its +0x138 dword, "
      "filled by the 3-tab loop (0057BEA0), is set" % sorted(v2))
rem1 = list(R.at(0x00D23D60, 9))
rem0 = list(R.at(0x00D23D6C, 6))
rows = {k: i32(u64(0x01F2CB90 + 8 * k)) for k in (19, 31, 32)}
check("C2b", rem1 == [0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x1B, 0x1D] and rem0 == [0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0F]
      and rows == {19: 6, 31: 1, 32: 9} and has(0x00565666, "cmp al, 0x20") and has(0x00565679, "cmp al, 0x13")
      and route(0x20)[1] == 0x0057D4DF and route(0x13)[1] == 0x0057D4DF and route(0x1F)[1] == 0x0057D4BD,
      "005655F0 remaps kind 0x20 by row through 00D23D60 (%s) and 0x13 through 00D23D6C (%s); the kinds' row tables "
      "(01F2CB90[k]) hold 9 / 6 / 1 rows; unremapped, 0x20 and 0x13 would take the empty default arm 0057D4DF, and "
      "0x1F is the bazaar arm" % (" ".join("%02X" % x for x in rem1), " ".join("%02X" % x for x in rem0)))
v3a = V.value_at(0x003FD6B0, 0x003FD76F, "rdx", 3)
v3b = V.value_at(0x003FD860, 0x003FD8E1, "rdx", 3)
check("C3a", v3a == {("M", "003FE30B qword ptr [rdx + 8]")} and v3b == {("C", 1)}
      and has(0x003FE30F, "cmp rax, 1") and has(0x003FE313, "je 0x3fe31e") and has(0x003FDA35, "movsxd rbx, ecx")
      and has(0x003FDA4B, "mov qword ptr [rsp + 0x28], rbx") and has(0x003FDA44, "lea rdx, [rip + 0x595]")
      and calls_to(0x003FDA20) == [(0x003FF040, 0x003FF0A2)] and has(0x003FF058, "movsxd rdi, edx")
      and has(0x003FF084, "cmp dword ptr [rbx + 0x178], 0x400") and has(0x003FF099, "mov ecx, edi")
      and calls_to(0x003FF040) == [(0x003FF360, 0x003FF765)] and has(0x003FF75F, "mov edx, dword ptr [rdx + 0x10]")
      and has(0x003FF6FA, "je 0x3ff75f"),
      "sources 3 and 4: 003FD6B0's edx = %s (003FDFE0's create message + 8, when it is not 1), 003FD860's edx = %s; "
      "create + 8 = 003FDA20's ecx = 003FF040's edx = the equip menu 003FF360's message-12 / 0x8001 + 0x10, the row the "
      "player picked, only when +0x178 == 0x400" % (sorted(v3a), sorted(v3b)))
kcases = [a for a in (0x003FE20C, 0x003FE225, 0x003FE23F, 0x003FE260, 0x003FE27A)]
tabC = [u64(0x01F2CC98 + 8 * k) for k in range(6)]
check("C3b", has(0x003FE20C, "test dl, dl") and has(0x003FE225, "cmp dl, 2") and has(0x003FE23F, "cmp dl, 4")
      and has(0x003FE260, "cmp dl, 1") and has(0x003FE27A, "cmp dl, 3") and all(0x00D23A00 <= t < 0x00D23C00 for t in tabC[:5])
      and tabC[5] == 0x00D23EE8 and has(0x003FF656, "mov r8d, 5") and has(0x003FF678, "call 0x2cd4d0")
      and [u16(0x00D23988 + 2 * k) for k in range(10)] == [1, 1, 2, 3, 2, 4, 2, 4, 3, 5],
      "003FDFE0 cases kinds 0..4 (003FE20C-003FE27A), 01F2CC98 holds five row tables (then 00D23EE8, not a row table), "
      "003FF360 allocates five rows (003FF656 -> 002CD4D0): kinds 0..4, selectors 0x40..0x44, high-band records "
      "{1,1} {2,3} {2,4} {2,4} {3,5}")
# C4: stores to the selector byte +0x17F: byte stores image-wide, and stores of any width inside the families' closure
def covers17f(i, bytes_only):
    if len(i.operands) < 1 or i.operands[0].type != 3 or i.mnemonic in ("cmp", "test", "bt", "push", "lea", "nop")             or i.mnemonic.startswith("prefetch"):
        return False
    if len(i.operands) == 1 and i.mnemonic not in ("inc", "dec", "not", "neg") and not i.mnemonic.startswith("set"):
        return False
    op = i.operands[0]
    if i.reg_name(op.mem.base) in ("rip", "rsp", "rbp") or op.mem.index:
        return False
    if bytes_only:
        return op.size == 1 and op.mem.disp == 0x17F
    return op.mem.disp <= 0x17F < op.mem.disp + op.size


b17f = []
for f, n in sorted(SZ.items()):
    d = R.at(f, n)
    if d:
        b17f += [(f, i.address) for i in R.md.disasm(d, f) if covers17f(i, True)]
fam = closure(ROOTS_A + ROOTS_D, 12, UIC)
w17f = sorted((f, i.address) for f in fam for i in body(f) if covers17f(i, False))
check("C4", b17f == [(0x003FD360, 0x003FD371), (0x00564780, 0x005647B4)] and w17f == b17f,
      "image-wide byte stores to +0x17F: %s; inside the three families' closure (%d functions) no store of any width "
      "covers +0x17F except those two" % (", ".join("%08X@%08X" % x for x in b17f), len(fam)))
famC = {k: 0x40 + k for k in range(5)}
rt = {}
for fam, kinds in (("A", {k: k for k in range(8)}), ("B", {32: None, 19: None, 31: 0x1F}), ("C", famC)):
    for k, sel in kinds.items():
        sels = [sel] if sel is not None else (rem1 if k == 32 else rem0)
        rt[(fam, k)] = [(s, ARMFILL[route(s)[1]]) for s in sels]
shopsel = {s for (fam, k), v in rt.items() if fam == "B" for (s, _) in v}
otherse = {s for (fam, k), v in rt.items() if fam != "B" for (s, _) in v}
check("C5", not (shopsel & otherse) and all(f != "none (freed, returns 0)" for v in rt.values() for (_, f) in v),
      "kind -> selector -> filler, and no selector is shared between the shop family and the others: " +
      "; ".join("%s kind %d: %s" % (fam, k, ", ".join("%02X %s" % (s, f) for s, f in v)) for (fam, k), v in sorted(rt.items())))
# C6: stability and opt-in
fr5 = S.Flow(fields=tuple(range(0x20)), depth=5, stride=0x20, seed_calls=CALLSEEDS, seed_loads=set(seeds))
fr5.run([0x0057CF20] + sorted({s[0] for s in seeds}))
f0 = S.Flow(fields=tuple(range(0x20)), depth=3, stride=0x20)
f0.run([0x0057CF20])
check("C6", fr5.hits == fr.hits and fr5.esc == fr.esc and not f0.hits and not f0.esc and not f0.handoffs,
      "the census is the same at depth 5 (%d accesses); without seed_calls the same run from 0057CF20 finds nothing "
      "(the new seeds are opt-in)" % len(fr.hits))
# D1: a page statement this lane contradicts - the band tables' reference sites
bt = sorted((g, f, a) for g in SC["refs"] if 0x00D23960 <= g < 0x00D239A0 for (f, a, k) in SC["refs"][g])
second = [a for (g, f, a) in bt if g in (0x00D23962, 0x00D2398A)]
check("D1", bt == [(0x00D23960, 0x00565BD0, 0x00565C25), (0x00D23960, 0x00565CD0, 0x00565D06),
                   (0x00D23962, 0x00563DC0, 0x00563E37), (0x00D23962, 0x00563F10, 0x00563F5B),
                   (0x00D2398A, 0x003FDFE0, 0x003FE2C5)]
      and has(0x00563E3E, "movzx ecx, word ptr [rax + rcx*4]") and has(0x00563F62, "movzx ecx, word ptr [rax + rcx*4]")
      and has(0x003FE2CC, "movzx esi, word ptr [rax + rbp*4]"),
      "beyond the builders' nine image-base-relative sites, the low / high band tables have %d rip-relative references "
      "(%s); the three at 00D23962 / 00D2398A read each record's SECOND word (00563E3E, 00563F62, 003FE2CC)"
      % (len(bt), ", ".join("%08X" % a for (_, _, a) in bt)))
print("FAILS %d" % fails)
