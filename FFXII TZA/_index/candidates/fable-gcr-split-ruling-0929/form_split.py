# form_split.py - FABLE's guarded-registrar split ruling, measured (2026-09-29). Runs a copy of the family selector
# select_guarded_class_registrars.py in dry-run mode (never --write) with its orchestrator predicate replaced:
#   membership-based (current): orchestrator = member whose auxiliary calls meet the MEMBER set
#   form-based (ruling):        orchestrator = member whose auxiliary calls meet GUARDED = every census body that calls
#                               _Init_thread_header 008092FC, _Init_thread_footer 0080929C and atexit 00808B90,
#                               whichever family owns it
# Prints both splits and the bodies that differ. Control: under the current predicate the copy must reproduce the
# selector's own dry-run counts (76 leaf / 23 orchestrators on 2026-09-29).
import io, os, sys, contextlib
HERE = os.path.dirname(os.path.abspath(__file__))
SEL = os.path.abspath(os.path.join(HERE, "..", "..", "..", "22-Middleware-PhyreEngine", "Reflection-And-Class-Metadata",
                                   "members", "select_guarded_class_registrars.py"))
src = io.open(SEL, encoding="utf-8").read()
OLD_L = "leaves = sorted(e for e in mem if not (aux[e] & mem))"
OLD_O = "orch = sorted(e for e in mem if aux[e] & mem)"
assert src.count(OLD_L) == 1 and src.count(OLD_O) == 1 and "--write" in src
cut = src.index('if "--write" in sys.argv:')
body = src[:cut]
FORM = ("\nGUARDED = {e for e, sz in sizes.items() if sz <= 8192 and off(e) is not None and {HDR, FTR, AX} <= calls(e)}\n"
        "leaves_f = sorted(e for e in mem if not (aux[e] & GUARDED))\n"
        "orch_f = sorted(e for e in mem if aux[e] & GUARDED)\n")
g = {"__name__": "form_split", "__file__": SEL}
buf = io.StringIO()
argv = sys.argv; sys.argv = [SEL]
with contextlib.redirect_stdout(buf):
    exec(compile(body + FORM, SEL, "exec"), g)
sys.argv = argv
L, O, Lf, Of = g["leaves"], g["orch"], g["leaves_f"], g["orch_f"]
print("selector copy (dry run): members %d" % len(g["mem"]))
print("membership-based split: leaf %d, orchestrators %d" % (len(L), len(O)))
print("form-based split:       leaf %d, orchestrators %d   (GUARDED bodies in census: %d)" % (len(Lf), len(Of), len(g["GUARDED"])))
ctrl = (len(L), len(O)) == (76, 23)
print("CONTROL membership split reproduces the selector's dry run (76 / 23):", "PASS" if ctrl else "FAIL")
moved = sorted(set(O) ^ set(Of))
for e in moved:
    sib = sorted(t for t in g["aux"][e] if t in g["GUARDED"])
    own = [("member" if t in g["mem"] else g["dec"].get(t, "A" if t in g["a_set"] else "frontier")) for t in sib]
    print("  %08X: membership=%s form=%s  guarded callees %s" % (
        e, "orch" if e in O else "leaf", "orch" if e in Of else "leaf",
        ", ".join("%08X(%s)" % (t, o) for t, o in zip(sib, own))))
for e in (0x00665870, 0x00666380):
    print("  %08X form-based: %s" % (e, "orchestrator" if e in Of else ("leaf" if e in Lf else "not a member")))
print("FAILS", 0 if ctrl else 1)
sys.exit(0 if ctrl else 1)
