"""DD residue batch 6 (SWE2-CONTRACT, 2026-09-30): checks behind the section-addressing page's reconciled residue.

Page: 02-Resource-And-Asset-Pipeline/resource-section-addressing.md. Run: python -B b6_section_addressing.py (FAILS 0)

  C1  002ED570 has 87 calling functions (115 direct call sites) - the page's crossref census count, re-counted
  F1  the lookup does not fail closed: 004096C0 adds the low 32 bits of the base to the offset and sign-extends
  T1  the type store declares both row families the page calls undeclared: RenderResourceEntry (0x50), rows of
      RenderResourceEntryBank (0x60), and RenderStrideC0Element (0xC0)
  A1  SECTION-10's section acceptance is on record in a tracked file: SWE2-AUDIT-SPEC's OV batch, OV-28 and OV-44 ACCEPT
"""
import hashlib, io, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))            # .../Database/FFXII TZA
sys.path.insert(0, os.path.join(DB, "..", "Tools", "analysis-kit", "gfz-scripts"))
import retool as T  # noqa: E402

FAILS = 0


def check(name, ok, detail=""):
    global FAILS
    print(("PASS " if ok else "FAIL ") + name + (" - " + detail if detail else ""))
    if not ok:
        FAILS += 1


def pin(name, a, text):
    i = next(T.R.md.disasm(T.R.at(a, 16), a, 1))
    got = "%s %s" % (i.mnemonic, i.op_str)
    check(name, text in got, "%08X  %s" % (a, got))


sha = hashlib.sha256(open(T.R.b.EXE, "rb").read()).hexdigest()
print("image", sha)
check("image identity", sha == "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8")

c = T.scan()["calls"].get(0x002ED570, set())
check("C1 002ED570 calling functions / sites", (len({f for f, _ in c}), len(c)) == (87, 115),
      "%d functions, %d sites" % (len({f for f, _ in c}), len(c)))

pin("F1 32-bit sum", 0x004096DF, "add eax, ebx")
pin("F1 sign-extended", 0x004096E1, "cdqe")

types = {}
for line in io.open(os.path.join(DB, "_types", "types.tsv"), encoding="utf-8"):
    cells = line.rstrip("\n").split("\t")
    if len(cells) > 1:
        types[cells[0]] = cells[1]
for name, size in (("RenderResourceEntry", "0x50"), ("RenderResourceEntryBank", "0x60"), ("RenderStrideC0Element", "0xC0")):
    check("T1 %s declared at %s" % (name, size), types.get(name) == size, str(types.get(name)))
nf = sum(1 for line in io.open(os.path.join(DB, "_types", "fields.tsv"), encoding="utf-8")
         if line.startswith("RenderResourceEntry\t"))
check("T1 RenderResourceEntry has field rows", nf > 0, "%d rows" % nf)

rec = os.path.join(DB, "_index", "candidates", "auditspec-ratify-legacy-verdicts-0929", "source-REVIEW-0929-FINAL-BATCH.md")
tracked = subprocess.run(["git", "ls-files", "--error-unmatch", rec], capture_output=True, cwd=DB).returncode == 0
check("A1 the acceptance copy is tracked", tracked)
t = io.open(rec, encoding="utf-8").read()
for k in ('"OV-28 the-resource-owner-from-copy-or-borrow-to-disposal SECTION-10": "ACCEPT"',
          '"OV-44 the-nonempty-prf-registration-and-specialized-relocation SECTION-10": "ACCEPT"'):
    check("A1 " + k.split('"')[1], k in t)

print("FAILS", FAILS)
sys.exit(1 if FAILS else 0)
