# leaband.py LO HI : every function that takes the ADDRESS of a cell in [LO,HI) with lea, and any
# absolute 64-bit pointer into the band stored in the image. A rip-relative READ/WRITE sweep is blind
# to accesses made through such a base, so this bounds that blindness instead of ignoring it.
# Control: 002498B0 must appear - it holds `lea rbx, [rip+...] -> 02F97372` and writes through rbx.
import sys, struct
exec(open('disw.py').read().split("fn = int")[0])
lo = int(sys.argv[1],16); hi = int(sys.argv[2],16)
hits = {}
for fn in sorted(funcs):
    o = off(fn)
    if o is None: continue
    try: ins = list(md.disasm(d[o:o+funcs[fn]], fn))
    except Exception: continue
    for x in ins:
        if x.mnemonic != "lea" or ("rip + " not in x.op_str and "rip - " not in x.op_str): continue
        sgn = 1 if "rip + " in x.op_str else -1
        try: disp = int(x.op_str.split("rip + " if sgn>0 else "rip - ")[1].split("]")[0],16)
        except (IndexError,ValueError): continue
        t = x.address + x.size + sgn*disp
        if lo <= t < hi:
            hits.setdefault(fn, []).append((x.address, t, x.op_str))
print("functions taking a lea into %08X..%08X: %d" % (lo, hi, len(hits)))
for fn in sorted(hits):
    for a,t,ops in hits[fn]:
        print("  %08X %-56s  %08X  at %08X   %s" % (fn, names.get(fn,''), t, a, ops))
# absolute pointers stored anywhere in the image
n = 0
for off_ in range(0, len(d)-8, 8):
    q = struct.unpack_from("<Q", d, off_)[0]
    if lo <= q < hi:
        n += 1
        print("  absolute qword pointer into the band at file offset %#x -> %08X" % (off_, q))
print("absolute stored pointers into the band: %d" % n)
