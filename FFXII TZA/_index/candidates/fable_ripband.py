# ripband.py LO HI : every rip-relative reference into [LO,HI) image-wide, read/write split.
# Control: the band must contain a site I have already read by hand - 002498BD (a WRITE from the
# rebuilder) and 00253F70 (a WRITE from the arbiter). A sweep that loses either is not a sweep.
import sys
exec(open('disw.py').read().split("fn = int")[0])
lo = int(sys.argv[1],16); hi = int(sys.argv[2],16)
WRITE = ("mov","or","and","add","sub","xor","inc","dec","bts","btr","btc","movzx","movsx",
         "movss","movsd","movaps","movups","stos","xchg","cmpxchg","not","neg","shl","shr","setne","sete")
rows = []
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
        # capstone prints the size prefix: "mov word ptr [rip + 0x..], di" - test the FIRST operand
        # by substring, not startswith, or every write reads as a read.
        first = ops.split(",")[0]
        kind = "W" if (x.mnemonic in WRITE and "rip" in first and "," in ops) else "R"
        if x.mnemonic in ("cmp","test") : kind = "R"
        rows.append((t, kind, fn, x.address, x.mnemonic, ops))
import collections
per = collections.defaultdict(lambda: collections.defaultdict(set))
for t,k,fn,a,m,o_ in rows: per[t][k].add(fn)
print(f"{len(rows)} references into {lo:08X}..{hi:08X} from {len({r[2] for r in rows})} functions")
for t in sorted(per):
    R = sorted(per[t]["R"]); W = sorted(per[t]["W"])
    print(f"{t:08X}  R{len(R):3d}  W{len(W):3d}")
    if W: print("      W: " + ", ".join(f"{f:08X} {names.get(f,'')}" for f in W))
    if R: print("      R: " + ", ".join(f"{f:08X}" for f in R))
