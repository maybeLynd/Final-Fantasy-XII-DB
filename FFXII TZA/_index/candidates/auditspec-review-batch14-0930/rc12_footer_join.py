"""rc12_footer_join.py - SWE2-AUDIT-SPEC (2026-09-30), independent of rc12_slots.py.

Question: which BYTE offset of an actor's footer holds the index of the function the decompiler calls `main`,
`parameter`, `mapjump`? The offset->name join is the whole RC-12 dispute (0-based special[k] at +2+2k, ORACLE; or
1-based special[t] at +2t, the page/FABLE reading). Names come from the DECOMPILED TEXT, not the raw name pool:
function w of actor a = the w-th `function` declaration under the a-th `actor` line of the .txt. That route shares
no code or layout assumption with rc12_slots.py Part B beyond the header's actor-table pointer (+0x18) and the
entry's function-list (+0x10) and footer (+0x18) offsets, which the alignment check below tests: the raw function
count of every actor must equal the number of declarations the text shows for it.

Sensitivity: if the 1-based reading were right, `main` would sit at +0x02 and `mapjump` at +0x18; the tallies print
every offset a name occurs at, so either reading shows up. Extra control independent of names: actors named
__MJ_CTRLnnn (map-jump controllers) must hold their non-init function at the offset the reading assigns to mapjump.
"""
import collections, os, re, struct, sys
CORPUS = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\pub140-scratch\corpus\us"
act_re = re.compile(r"^actor\s+(\S+?)\(")
fn_re = re.compile(r"^\s+function\s+([^\s(]+)\((\d*)\)")
tally = collections.defaultdict(collections.Counter)   # name -> Counter(byte offset)
printed = collections.defaultdict(collections.Counter)  # name -> Counter(printed number)
mj = collections.Counter()
aligned = misaligned = images = 0
for fn in sorted(os.listdir(CORPUS)):
    if not fn.endswith(".s000"):
        continue
    txt = os.path.join(CORPUS, fn[:-5] + ".txt")
    if not os.path.exists(txt):
        continue
    b = open(os.path.join(CORPUS, fn), "rb").read()
    if struct.unpack_from("<I", b, 0)[0] != 0x8000000B:
        continue
    actors = []
    for line in open(txt, encoding="utf-8", errors="replace"):
        m = act_re.match(line)
        if m:
            actors.append((m.group(1), []))
            continue
        m = fn_re.match(line)
        if m and actors:
            actors[-1][1].append((m.group(1), m.group(2)))
    tab = struct.unpack_from("<I", b, 0x18)[0]
    n = struct.unpack_from("<I", b, tab)[0]
    if n != len(actors):
        misaligned += 1
        continue
    images += 1
    for a in range(n):
        e = tab + 4 + a * 0x30
        flist = struct.unpack_from("<I", b, e + 0x10)[0]
        foot = struct.unpack_from("<I", b, e + 0x18)[0]
        nf = struct.unpack_from("<I", b, flist)[0]
        aname, decls = actors[a]
        if nf != len(decls):
            misaligned += 1
            continue
        aligned += 1
        cnt = struct.unpack_from("<H", b, foot)[0]
        for byte in range(2, 2 + 2 * cnt, 2):
            w = struct.unpack_from("<H", b, foot + byte)[0]
            if w < nf:
                nm, num = decls[w]
                tally[nm][byte] += 1
                printed[nm][num] += 1
                if aname.startswith("__MJ_CTRL") and nm != "init":
                    mj["+0x%02X %s" % (byte, nm)] += 1
print("images joined %d, actors aligned %d, misaligned (actor/function count differs) %d" % (images, aligned, misaligned))
for nm in ("main", "talk", "touch", "spawn", "initevent", "parameter", "mapjump", "fieldsign2", "respawn", "talkhold", "talkterm"):
    offs = ", ".join("+0x%02X x%d" % kv for kv in sorted(tally[nm].items()))
    print("  %-10s footer byte offsets: %-40s printed numbers: %s" % (nm, offs, dict(printed[nm])))
print("__MJ_CTRL actors, their non-init footer word:", dict(mj))
p = tally["parameter"]; mjp = tally["mapjump"]
ok = aligned > 0 and set(p) == {0x18} and set(mjp) == {0x1A} and set(tally["main"]) == {0x04}
print("RESULT: +0x18 holds only `parameter`, +0x1A only `mapjump`, +0x04 only `main`: %s" % ("YES" if ok else "NO"))
