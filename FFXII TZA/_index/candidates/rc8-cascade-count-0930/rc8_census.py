"""rc8_census.py - RC-8 (ORACLE, 2026-09-30).  The forward census the row asks for: every instruction image-wide that writes a
byte range covering +0x13C..+0x13F through a non-stack base register (any width: byte, word, dword, qword, xmmword),
classified against rc8_flow.py's pointer flow:
  OBJECT   - the flow saw the shadow object (offset 0) as the base at this very instruction;
  REACHED  - the function is reached by the flow, but the base at this instruction is not the object;
  UNREACHED- the function is never handed the pointer by any flow the analysis follows.
Also counts the stack-based writes ([rsp], or [rbp] in a function whose prologue makes rbp a frame pointer) separately (the object is heap-allocated, 0xB08 bytes by 00210EC0).
Control: the constructor's store 001EF389 must be OBJECT.  Output rc8_census.tsv and a summary."""
import collections, contextlib, io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
with contextlib.redirect_stdout(io.StringIO()):
    import rc8_flow as F
import memsweep

HERE = os.path.dirname(os.path.abspath(__file__))
recs = memsweep.load()
obj_sites = {int(w[0], 16) for R in F.REPORT.values() for w in R["count_writes"] if w[2] == "object+13C"}
W = [r for r in recs if r[11] and r[5] not in (None, "rip") and r[8] <= 0x13C < r[8] + max(r[9], 1) and r[8] > 0x13C - 16]
stack = [r for r in W if r[5] == "rsp" or (r[5] == "rbp" and F.framebp(r[1]))]
heap = [r for r in W if r not in stack]
rows = []
for r in heap:
    cls = "OBJECT" if r[0] in obj_sites else ("REACHED" if r[1] in F.REPORT else "UNREACHED")
    rows.append((r[0], r[1], "%s %s" % (r[2], r[3]), r[9], cls))
with io.open(os.path.join(HERE, "rc8_census.tsv"), "w", encoding="utf-8", newline="\n") as f:
    f.write("site\tfunction\tinstruction\twidth\tclass\n")
    for r in rows:
        f.write("%08X\t%08X\t%s\t%d\t%s\n" % r)
c = collections.Counter(r[4] for r in rows)
dw = [r for r in rows if r[3] == 4 and "0x13c]" in r[2]]
print("writes covering +0x13C through a non-stack base: %d (dword stores at exactly +0x13C: %d); stack-based: %d" % (len(rows), len(dw), len(stack)))
print("classes:", dict(c))
for r in rows:
    if r[4] != "UNREACHED":
        print("  %08X %08X %-48s w%d %s" % r)
fails = 0
if 0x001EF389 not in obj_sites or [r for r in rows if r[0] == 0x001EF389][0][4] != "OBJECT":
    fails += 1
print("dword stores at exactly +0x13C with a non-3 value source:",
      sum(1 for r in dw if not r[2].endswith(", 3")), "of", len(dw), "(all but the OBJECT one are on other objects by the flow)")
print("FAILS", fails + len(F.FAILS))
