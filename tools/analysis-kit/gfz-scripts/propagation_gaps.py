"""Which UNRESOLVED fields does the type's OWN declared document already name?

The CharacterRenderSystemTail round found the store reading UNRESOLVED for four fields a page had
named on 2026-09-11. That is a propagation gap, not a discovery gap, and if it happened once it is
worth asking how often.

TWO EARLIER VERSIONS FAILED THEIR OWN CONTROL, which is the part worth recording.

  1. Search every document that mentions the type. Four hits a row, all noise: `+0x008` appears on
     the BattleUnit page, the movement pages and a dozen others, each beside some other type's field
     name. An offset is not a key.
  2. Keep a hit only when the row's type is named nearby. It still could not find the case it was
     built from: `the-character-render-record-array.md` writes "CharacterRenderSystemTail" exactly
     ONCE, at line 778, and documents the tail's fields at line 514 under the prose name "the tail".
     No rule keyed on the store's type name can reach that text.

The store already carries the link both of them were guessing at. `_types/types.tsv` has a
`documents` column, populated for 250 of 251 types, and for this type it names exactly the page the
naming lives on. So: read the type's declared documents, and only those. No heuristic.

IT PROPOSES, IT DOES NOT DECIDE. A hit is a place to read: the page may be speculating, or may be
the very source the row's evidence already cites. Every one is adjudicated by hand.

usage: propagation_gaps.py [--type NAME] [--db DB] [--store FIELDS.TSV] [--self-test]
"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", "..", ".."))
DB = (sys.argv[sys.argv.index("--db") + 1] if "--db" in sys.argv
      else os.path.join(ROOT, "Database", "FFXII TZA"))
STORE = (sys.argv[sys.argv.index("--store") + 1] if "--store" in sys.argv
         else os.path.join(DB, "_types", "fields.tsv"))
TYPES = os.path.join(DB, "_types", "types.tsv")

NAME = re.compile(r"\*\*([^*\n]{3,60})\*\*|`([A-Za-z_][A-Za-z0-9_]{2,40})`")
NOTNAME = re.compile(r"^(?:0x[0-9A-Fa-f]+|[re][a-z][a-z]|r\d+|xmm\d+|[0-9A-Fa-f]{6,8})$")


def load_docs():
    head = io.open(TYPES, encoding="utf-8").readline().rstrip("\r\n").split("\t")
    di = head.index("documents")
    out = {}
    for line in io.open(TYPES, encoding="utf-8").read().splitlines()[1:]:
        c = line.rstrip("\r").split("\t")
        if len(c) > di and c[di].strip():
            out[c[0]] = [d.strip() for d in re.split(r"[;,]\s*", c[di]) if d.strip()]
    return out


_CACHE = {}


def body_of(rel):
    if rel not in _CACHE:
        p = os.path.join(DB, rel.replace("/", os.sep))
        _CACHE[rel] = (io.open(p, encoding="utf-8", errors="replace").read()
                       if os.path.exists(p) else None)
    return _CACHE[rel]


def hits_for(type_, off, docs):
    n = int(off, 16)
    forms = sorted({"+0x%X" % n, "+0x%x" % n, "+0x%03X" % n, "+0x%03x" % n}, key=len, reverse=True)
    # NOT followed by another hex digit, or `+0x14` matches inside `+0x140` and the survey fills
    # with rows whose "hit" is a different, longer offset on the same line.
    pat = re.compile("(?:%s)(?![0-9A-Fa-f])" % "|".join(re.escape(f) for f in forms))
    out = []
    for rel in docs.get(type_, []):
        body = body_of(rel)
        if body is None:
            continue
        for m in pat.finditer(body):
            ls = body.rfind("\n", 0, m.start()) + 1
            le = body.find("\n", m.end())
            line = body[ls:le if le > 0 else len(body)]
            for nm in NAME.finditer(line):
                word = (nm.group(1) or nm.group(2)).strip()
                if NOTNAME.match(word) or word.startswith("+0x"):
                    continue
                out.append((rel, body.count("\n", 0, ls) + 1, line.strip()))
                break
            if out:
                break
    return out


def self_test():
    """The control: against the store as it stood before e3adfff0, the tail's +0x1C must be found
    on its page. Both earlier designs failed exactly here and would have reported a clean survey."""
    import subprocess
    tsv = subprocess.run(["git", "show", "e3adfff0^:Database/FFXII TZA/_types/fields.tsv"],
                         cwd=ROOT, capture_output=True, text=True).stdout
    if not tsv:
        print("CONTROL SKIPPED - cannot read the pre-fix store from git")
        return 2
    was = [l.split("\t") for l in tsv.splitlines()[1:] if l.count("\t") >= 8]
    row = [r for r in was if r[0] == "CharacterRenderSystemTail" and r[1] == "0x01C"]
    if not row or row[0][3] != "UNRESOLVED":
        print("CONTROL INVALID - +0x01C was not UNRESOLVED in that revision")
        return 2
    got = hits_for("CharacterRenderSystemTail", "0x01C", load_docs())
    ok = any("fade start distance" in line for _rel, _ln, line in got)
    print("control: %s" % ("PASS - the page's naming of +0x1C is found" if ok else
                           "FAIL - the motivating case is not found; a clean survey would mean nothing"))
    for rel, ln, line in got[:2]:
        print("   %s:%d  %s" % (rel, ln, line[:120]))
    return 0 if ok else 1


def main():
    if "--self-test" in sys.argv:
        return self_test()
    docs = load_docs()
    rows = [l.rstrip("\r").split("\t") for l in io.open(STORE, encoding="utf-8").read().splitlines()]
    unres = [r for r in rows[1:] if len(r) > 8 and r[3] == "UNRESOLVED"]
    only = sys.argv[sys.argv.index("--type") + 1] if "--type" in sys.argv else None
    if only:
        unres = [r for r in unres if r[0] == only]
    print("%d UNRESOLVED field(s); %d type(s) declare documents" % (len(unres), len(docs)))
    nodocs = sorted({r[0] for r in unres if r[0] not in docs})
    if nodocs:
        print("no declared document, invisible to this survey: %s" % ", ".join(nodocs))
    found = 0
    for r in unres:
        got = hits_for(r[0], r[1], docs)
        if not got:
            continue
        found += 1
        print("\n%s %s" % (r[0], r[1]))
        for rel, ln, line in got[:2]:
            print("    %s:%d" % (rel, ln))
            print("      %s" % line[:150])
    print("\n%d of %d UNRESOLVED rows have their own type's document saying something on the "
          "offset's line" % (found, len(unres)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
