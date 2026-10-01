"""sd127_keys.py - SD-127: which battle-HUD layout keys are also read through a base pointer rather than a rip-relative
load (OPUS, 2026-09-30). Static, the certified image, via Database/Tools/analysis-kit/gfz-scripts/retool.py and the `pe`
module of _index/candidates/rc22-34-resource-readers-0930/ (38,161 bodies).

The battle-HUD key set: every key in 16-UI/Layout-Parameter-System/members/layout-key-readers.tsv whose rip-relative
reader is one of the functions the battle-HUD page (16-UI/Battle-Hud/the-battle-hud-layout-readers.md) cites.
Routes by which a key can be read without a rip-relative operand, each swept image-wide:
  R1 an image-base-relative operand: a memory operand with a base or index register and displacement key - 0x00120000
     (the form 0036E3B0 uses on 022D97B0);
  R2 a lea of a layout-block address (01E0C000..01E0D100) outside the console installer 001AF470, i.e. the block's
     address in a register, followed by [reg + d] in the same function with address + d on the key;
  R3 a stored qword whose value is the key's address (a pointer table);
  R4 the tuning console's slot-pointer array: 001AF470 lea-installs keys into [01F811E8] + 0x3B00 (development console
     route, not a HUD reader).
"""
import collections, csv, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
sys.path.insert(0, os.path.join(HERE, "..", "rc22-34-resource-readers-0930"))
import retool as T  # noqa: E402
import pe  # noqa: E402

R, c, SZ = T.R, T.scan(), T.sizes()
DB = os.path.join(HERE, "..", "..", "..")
fails = 0


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


page = open(os.path.join(DB, "16-UI", "Battle-Hud", "the-battle-hud-layout-readers.md"), encoding="utf-8").read()
cited = set(int(x, 16) for x in re.findall(r"`(00[0-9A-F]{6})`", page))
rows = list(csv.DictReader(open(os.path.join(DB, "16-UI", "Layout-Parameter-System", "members", "layout-key-readers.tsv"),
                                encoding="utf-8"), delimiter="\t"))
hud = {}
for r in rows:
    if int(r["reader"], 16) in cited:
        hud[int(r["global"], 16)] = r["key"]
LO, HI = 0x01E0C000, 0x01E0D100
print("battle-HUD keys (reader cited on the page): %d; readers %d" % (len(hud), len(set(r["reader"] for r in rows if int(r["reader"], 16) in cited))))

# R1 / R2 over every body
r1 = collections.defaultdict(list)
leas = []                    # (fn, site, register, block address)
reads_via = collections.defaultdict(list)
dispset = {k - 0x00120000: k for k in hud}
for f in pe.funcs:
    xs = pe.dis(f)
    regs = {}
    for x in xs:
        for m in re.finditer(r"\[(\w+)(?: \+ (\w+)\*\d)? \+ (0x[0-9a-f]+)\]", x.op_str):
            if m.group(1) != "rip":
                d = int(m.group(3), 16)
                for k in (d, d - 1, d - 2, d - 3):
                    if k in dispset:
                        r1[dispset[k]].append((f, x.address, "%s %s" % (x.mnemonic, x.op_str)))
        m = re.match(r"(r\w+), \[rip \+ (0x[0-9a-f]+)\]$", x.op_str)
        if x.mnemonic == "lea" and m:
            t = x.address + x.size + int(m.group(2), 16)
            if LO <= t < HI and f != 0x001AF470:
                leas.append((f, x.address, m.group(1), t))
                regs[m.group(1)] = t
                continue
        if regs:
            for reg, t in list(regs.items()):
                for mm in re.finditer(r"\[%s(?: \+ (0x[0-9a-f]+|\d+))?\]" % reg, x.op_str):
                    a = t + (int(mm.group(1), 0) if mm.group(1) else 0)
                    reads_via[a].append((f, x.address))
                if x.op_str.startswith(reg + ",") and x.mnemonic not in ("cmp", "test"):
                    regs.pop(reg, None)
r2 = {k: reads_via[k] for k in hud if reads_via.get(k)}
# R3 - stored qword pointers to a key
r3 = {k: [q for q in T.qword_sites(k)] for k in hud}
r3 = {k: v for k, v in r3.items() if v}
# R4 - console installs
inst = set(k for k in hud for fn, a, kind in c["refs"].get(k, ()) if kind == "lea" and fn == 0x001AF470)
inst2 = set(k for k in hud for fn, a, kind in c["refs"].get(k, ()) if kind == "lea" and fn == 0x001B44A0)
print("R1 image-base-relative operands on a HUD key: %d" % sum(len(v) for v in r1.values()))
for k, v in sorted(r1.items()):
    print("   %08X %-36s %s" % (k, hud[k], ["%08X@%08X %s" % x for x in v]))
print("R2 lea of a block address outside 001AF470: %d sites %s" % (len(leas), ["%08X@%08X %s=%08X" % x for x in leas]))
print("R2 reads through such a register landing on a HUD key: %d" % sum(len(v) for v in r2.values()))
for k, v in sorted(r2.items()):
    print("   %08X %-36s %s" % (k, hud[k], ["%08X@%08X" % x for x in v]))
print("R3 stored qword pointers to a HUD key: %d %s" % (len(r3), {"%08X" % k: v for k, v in r3.items()}))
print("R4 installed into the console slot array by 001AF470: %d of %d HUD keys" % (len(inst), len(hud)))
# controls: the sweep sees SD-121's image-base-relative stores on 022D97B0 (R1 form) and 004001D0's lea of 01E0C590 (R2)
ctl1 = any("0x21b97b0]" in "%s %s" % (x.mnemonic, x.op_str) for x in pe.dis(0x0036E3B0))
ctl2 = any(l[0] == 0x004001D0 and l[3] == 0x01E0C590 for l in leas)
check("C1", ctl1 and ctl2, "controls: the R1 form is decoded (0036E3B0 on 022D97B0) and the R2 sweep finds 004001D0's lea of 01E0C590")
check("K1", len(hud) > 0 and not r1 and not r2 and not r3,
      "no battle-HUD key is read through an image-base-relative operand, a block lea or a stored pointer")
check("K2", len(inst) == len(hud) - 1 and inst2 == {0x01E0CF94} and not (inst & inst2),
      "85 HUD keys are installed into the console slot array by 001AF470; FontItalicScale (01E0CF94) into 001B44A0's "
      "object at +0x300 (beside 01E0CF90 at +0x2F8 and FontShadowAlphaMuti 01DF6DE0 at +0x308)")
# K3 - the two block addresses a HUD function takes that sit next to HUD keys are not key reads:
#      004001D0 passes the 0x20-byte record at 01E0C590 (read at +0, +2, +4, +8, +0x10, +0x18 by 004006A0 / 004017D0 /
#      00401D40) - the BossGaugeExColor keys at 01E0C5B0.. (+0x20) are never reached through it; 002679F0 walks the
#      8-entry table 01E0C328..01E0C347 (byte, byte, word) whose end is exactly mScrollListHeight (01E0C348)
def t_(a):
    i = next(R.md.disasm(R.at(a, 16), a, 1))
    return "%s %s" % (i.mnemonic, i.op_str)
tab = R.at(0x01E0C328, 0x20)
check("K3", t_(0x004006DB) == "mov rbp, qword ptr [r14 + 0x18]" and t_(0x0040070A) == "movsx eax, word ptr [r14 + 4]"
      and t_(0x00401884) == "movsx eax, word ptr [r10 + 2]" and t_(0x0040190A) == "mov rdx, qword ptr [r10 + 8]"
      and t_(0x00401D8C) == "mov rdi, qword ptr [r14 + 0x10]" and t_(0x00401E33) == "cmp bp, word ptr [r14]"
      and t_(0x00267A44) == "lea rdx, [rdx + 4]" and t_(0x00267A25) == "movzx r13d, word ptr [rax + r12]"
      and [tab[4 * i] for i in range(8)] == [0, 1, 1, 2, 2, 3, 3, 3] and hud.get(0x01E0C348) == "mScrollListHeight",
      "the 01E0C590 record's readers stop at +0x18; the 01E0C328 table is 8 entries ending at the first HUD key")
print("FAILS %d" % fails)
