"""Type references spelled with MSVC's class-key code (OPUS, 2026-09-27), answering EVIDENCE-STANDARD.md 13h ('one type
spelled two ways ... routed as a question to the type store's owner').

In an MSVC decorated name a class-type template argument is written V<Name>@ and a struct U<Name>@ - the letter is the
class key, not part of the name (e.g. .?AV?$PClassDataMemberPhyreArray@VPString@Phyre@@@Phyre@@). A reference read out
of such a string keeps the letter unless it is stripped.

  D  (discriminator, per reference) the prefixed spelling occurs in the image ONLY inside decorated names
     ([?@$]<ref>@), never as a bare token, and the name without the letter is a declared type
  R  REGRESSION: no field row's type is such a prefixed spelling of a declared type (FAILS on the store before the fix)
  P  positive control: the decorated contexts exist for every corrected reference (2..15 each)
  N  negative control: a declared type that begins with U or V legitimately (Vu1RegisterBank02064B00) is untouched,
     and UNRESOLVED (a placeholder) is not treated as decorated
With --apply PATH the rows are corrected in PATH (default: print only). Evidence keeps the old spelling.
"""
import re, sys, collections
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
TYPES_P = ROOT / "Database/FFXII TZA/_types/types.tsv"
args = sys.argv[1:]
FIELDS = Path(args[args.index("--fields") + 1]) if "--fields" in args else ROOT / "Database/FFXII TZA/_types/fields.tsv"
APPLY = "--apply" in args
types = {l.split("\t")[0] for l in open(TYPES_P, encoding="utf-8")}
def base_of(ct): return re.sub(r"(\s*\*+|\[[^\]]*\])+$", "", ct).strip()
def decorated(ref):
    dec = len(re.findall(rb"[?@$]" + re.escape(ref.encode()) + rb"@", d))
    bare = len(re.findall(rb"(?<![?@$A-Za-z0-9_])" + re.escape(ref.encode()) + rb"(?![A-Za-z0-9_@])", d))
    return dec, bare
b = FIELDS.read_bytes().decode("utf-8")
lines = b.splitlines(keepends=True)
cands = collections.defaultdict(list)
for i, l in enumerate(lines):
    c = l.rstrip("\r\n").split("\t")
    if len(c) < 9: continue
    ref = base_of(c[4])
    if re.match(r"^[UV][A-Z]\w+$", ref) and ref not in types and ref[1:] in types:
        cands[ref].append(i)
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += not ok
proof = {ref: decorated(ref) for ref in cands}
good = {ref for ref, (dec, bare) in proof.items() if dec > 0 and bare == 0}
check("D every candidate is decoration residue (decorated contexts only, undecorated name declared)", good == set(cands),
      str({r: proof[r] for r in sorted(cands)}))
if APPLY:
    for ref in sorted(good):
        for i in cands[ref]:
            l = lines[i]; eol = l[len(l.rstrip("\r\n")):]; c = l.rstrip("\r\n").split("\t")
            old = c[4]; c[4] = old.replace(ref, ref[1:], 1)
            c[8] += (" || CTYPE DE-DECORATED 2026-09-27 (OPUS): was '%s' - the leading %s is MSVC's class-key code (%s) "
                     "from a decorated template argument (e.g. [?@$]%s@ in the image, %d occurrences, never bare); the "
                     "declared type is %s. _index/candidates/typeref-dedecorate/dedecorate.py" %
                     (old, ref[0], "class" if ref[0] == "V" else "struct", ref, proof[ref][0], ref[1:]))
            lines[i] = "\t".join(c) + eol
    FIELDS.write_bytes("".join(lines).encode("utf-8"))
    print("applied to", len(sum((cands[r] for r in good), [])), "rows")
    b = FIELDS.read_bytes().decode("utf-8"); lines = b.splitlines(keepends=True)
left = [l.split("\t")[:5] for l in lines if len(l.split("\t")) > 4 and re.match(r"^[UV][A-Z]\w+$", base_of(l.split("\t")[4]))
        and base_of(l.split("\t")[4]) not in types and base_of(l.split("\t")[4])[1:] in types]
check("R no field row spells a declared type with a class-key prefix", not left, "(%d left)" % len(left))
FIXED = ["UD3D11_DEPTH_STENCILOP_DESC", "VPMatrix4", "VPMatrix4x3", "VPString"]
marked = [l for l in lines if "CTYPE DE-DECORATED 2026-09-27 (OPUS)" in l]
pf = {r: decorated(r) for r in FIXED}
check("P the decorated contexts exist for the four references, never bare; every corrected row carries the record",
      all(dec >= 2 and bare == 0 for dec, bare in pf.values()) and len(marked) in (0, 41), "(%s; %d marked rows)" % (pf, len(marked)))
vu = [l for l in lines if l.startswith("Vu1RegisterBank02064B00\t")]
check("N a legitimate U/V type name is untouched; UNRESOLVED is not a candidate",
      "Vu1RegisterBank02064B00" in types and bool(vu) and "UNRESOLVED" not in cands and "NRESOLVED" not in types)
print("FAILS", fails)
sys.exit(1 if fails else 0)
