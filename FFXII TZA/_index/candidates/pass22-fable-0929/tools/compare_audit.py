"""Compare two audit_crossrefs JSON reports for the FABLE pass-22 pairs.

usage: compare_audit.py BEFORE.json AFTER.json
Prints: FABLE pairs before/after (by the 24 keys in fable_pairs.json), which cleared, which remain, and every
finding present after that was not present before (keyed on kind, document, subject AND detail), plus findings
whose detail changed on the touched pages.
"""
import io, json, sys, collections

before = json.load(io.open(sys.argv[1], encoding="utf-8"))
after = json.load(io.open(sys.argv[2], encoding="utf-8"))
pairs = json.load(io.open(r"C:/x/p22/fable_pairs.json", encoding="utf-8"))
fable = {(p[1], p[2]) for p in pairs}


def un(rep):
    return {(f[1], f[2]): f for f in rep["findings"] if f[0] == "UNACCOUNTED NEIGHBOUR"}


b, a = un(before), un(after)
fb = sorted(k for k in b if k in fable)
fa = sorted(k for k in a if k in fable)
print("UNACCOUNTED NEIGHBOUR total: before %d, after %d" % (len(b), len(a)))
print("FABLE pairs present: before %d (of %d keys), after %d" % (len(fb), len(fable), len(fa)))
missing_before = sorted(fable - set(b))
if missing_before:
    print("  FABLE keys absent already BEFORE (HEAD moved?):", missing_before)
print("cleared (%d):" % len(set(fb) - set(fa)))
for k in sorted(set(fb) - set(fa)):
    print("   ", k[0], "|", k[1], "|", b[k][3].split(" ", 1)[0], "edges")
print("still open FABLE pairs (%d):" % len(fa))
for k in fa:
    print("   ", k[0], "|", k[1], "|", a[k][3][:60])
nb = {tuple(f) for f in before["findings"]}
na = {tuple(f) for f in after["findings"]}
new = sorted(na - nb)
print("findings in AFTER not in BEFORE (exact tuple): %d" % len(new))
for f in new:
    print("   NEW", f[0], "|", f[1], "|", f[2], "|", f[3][:120])
gone = sorted(nb - na)
nonfable_gone = [f for f in gone if (f[1], f[2]) not in fable]
print("findings gone that are not FABLE pairs: %d" % len(nonfable_gone))
for f in nonfable_gone:
    print("   GONE", f[0], "|", f[1], "|", f[2], "|", f[3][:120])
kinds_b = collections.Counter(f[0] for f in before["findings"])
kinds_a = collections.Counter(f[0] for f in after["findings"])
print("by kind before:", dict(kinds_b))
print("by kind after: ", dict(kinds_a))
