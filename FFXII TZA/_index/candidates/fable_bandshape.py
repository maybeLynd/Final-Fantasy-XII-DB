# bandshape.py LO HI : for every referenced address in a band, the ACCESS WIDTH and kind, so a
# "stride" can be read off what the instructions actually do rather than off the gaps between them.
# A qword load is a pointer slot; a movss is a float; a byte test is a flag. Gaps only say where the
# referenced addresses are - widths say what they ARE.
# Control: 02EBF000 must come back as a FLOAT written by 0039AF20 (FABLE, 2026-09-12) or this is not
# measuring the band the question is about.
import sys, collections
exec(open('disw.py').read().split("fn = int")[0])
lo = int(sys.argv[1],16); hi = int(sys.argv[2],16)
# LONGEST FIRST, and matched as a whole token: "qword ptr" CONTAINS "word ptr", so a substring test
# in short-to-long order labels every qword a word. That is the same defect as the capstone size
# prefix one, mirrored, and it cost a wrong reading of this very band before the raw instructions
# were printed.
WIDTH = [("xmmword",16),("qword",8),("dword",4),("tbyte",10),("word",2),("byte",1)]
rows = collections.defaultdict(lambda: collections.Counter())
who  = collections.defaultdict(set)
for fn in sorted(funcs):
    o = off(fn)
    if o is None: continue
    try: ins = list(md.disasm(d[o:o+funcs[fn]], fn))
    except Exception: continue
    for x in ins:
        ops = x.op_str
        if "rip + " not in ops and "rip - " not in ops: continue
        sgn = 1 if "rip + " in ops else -1
        try: disp = int(ops.split("rip + " if sgn>0 else "rip - ")[1].split("]")[0],16)
        except (IndexError,ValueError): continue
        t = x.address + x.size + sgn*disp
        if not (lo <= t < hi): continue
        m = x.mnemonic
        w = next((k for k,_ in WIDTH if k+" ptr" in ops), None)
        if m == "lea": kind = "lea"
        elif m in ("movss","movsd","comiss","addss","mulss","subss","divss","ucomiss"): kind = "float"
        elif w: kind = "%s(%s)" % (w, m)
        else: kind = m
        rows[t][kind] += 1
        who[t].add(fn)
print("referenced addresses in %08X..%08X : %d" % (lo, hi, len(rows)))
prev = None
for t in sorted(rows):
    gap = "" if prev is None else "+%d" % (t - prev)
    kinds = ", ".join("%s x%d" % (k, n) for k, n in rows[t].most_common(4))
    print("%08X %-5s %3d fn  %s" % (t, gap, len(who[t]), kinds))
    prev = t
print("\nCONTROL 02EBF000 float, and 0039AF20 among its functions:",
      any(k.startswith("float") or "dword(mov" in k for k in rows.get(0x2EBF000, {})),
      0x39AF20 in who.get(0x2EBF000, set()))
