"""SWE2-AUDIT-SEM GCR-UNIFY comparison (own code).
argv: committed members TSV, scratch dir of the re-run selector, old stubs TSV, old orchestrators TSV (at 090f74f38^).
Prints: committed vs re-run byte identity and set identity; old 97 kept; admitted / dropped; the information column's
non-empty count; and FABLE's form_split.out 23/76 split compared with the information column."""
import sys, os, glob, re

def rows(p):
    out = {}
    for l in open(p, encoding="utf-8", errors="replace"):
        if l.startswith("#") or not l.strip():
            continue
        f = l.rstrip("\r\n").split("\t")
        if re.fullmatch(r"[0-9A-Fa-f]{8}", f[0]):
            out[f[0].upper()] = f
    return out

com_p, scratch, old_s, old_o = sys.argv[1:5]
com = rows(com_p)
cand = glob.glob(os.path.join(scratch, "guarded-class-registration-stubs.tsv"))
rr = rows(cand[0]) if cand else {}
if cand:
    a = open(com_p, "rb").read().replace(b"\r", b"")
    b = open(cand[0], "rb").read().replace(b"\r", b"")
    print("re-run TSV byte-identical to committed (CR-stripped):", a == b)
print("committed members %d, re-run members %d, set-identical %s" % (len(com), len(rr), set(com) == set(rr)))
os_, oo = rows(old_s), rows(old_o)
old = set(os_) | set(oo)
print("old stubs %d + old orchestrators %d = %d distinct" % (len(os_), len(oo), len(old)))
print("old kept:", len(old & set(com)), "dropped:", sorted(old - set(com)), "admitted:", sorted(set(com) - old))
info = {k: v[-1].strip() for k, v in com.items()}
ne = [k for k, v in info.items() if v and v not in ("-", "")]
print("information column non-empty: %d of %d" % (len(ne), len(com)))
fs = glob.glob(os.path.join(os.path.dirname(com_p), "..", "..", "..", "_index", "candidates",
                            "fable-gcr-split-ruling-0929", "form_split.out"))
if fs:
    txt = open(fs[0], encoding="utf-8", errors="replace").read()
    print("form_split.out lines mentioning 76 / 23:")
    for l in txt.splitlines():
        if re.search(r"\b(76|23)\b", l):
            print("   ", l[:200])
    # members form_split calls guarded-aux / leaf, if it lists them
    g = set(a.upper() for a in re.findall(r"\b([0-9A-F]{8})\b.*?(?:guarded|GUARDED)", txt))
    print("form_split addresses on 'guarded' lines: %d; overlap with non-empty column: %d" % (len(g), len(g & set(ne))))
