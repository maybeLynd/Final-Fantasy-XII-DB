"""sync_family_counts.py - make a family's declared count match its members file.

`check_dispositions` refuses a family for two independent reasons that arrive together:

  * a member is already measured as A - the members file is stale and its selector must re-run;
  * **the declared count does not match the members file** (its rule 6).

So regenerating a members file is only half the cure. Miss the second half and the family is still
refused, for a different reason, and the whole family - often more than a thousand bodies - stays
out of the declared surface. On 2026-09-14 that sequence fired **four times in one session** across
SEAD and PPFX, and the gate's own comment records two more on 2026-09-13 (Lua, then PPFX).

WHAT THIS DOES AND DELIBERATELY DOES NOT DO. It reads every `function_families` declaration, counts
the rows in the members file each one names, and reports or fixes the count. **It never runs a
selector and never edits a members file.** Those belong to whoever owns the family - running
someone's in-progress `select_*.py` could overwrite work that is not mine - so the mutating half
stays a human step and this closes only the mechanical one.

Order of operations, therefore: re-run the selector yourself (the refusal message names it), then
run this.
"""
import argparse, io, os, re, sys

DB_DEFAULT = "Database/FFXII TZA"
# `- "name | letter | members file | count | note"` inside a document's frontmatter
ROW = re.compile(r'^(\s*-\s*"[^"|]*\|[^"|]*\|\s*)([^"|]+?)(\s*\|\s*)(\d+)(\s*\|)', re.M)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=DB_DEFAULT)
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args(argv)

    checked = ok = fixed = missing = 0
    bad = []
    for root, dirs, files in os.walk(a.db):
        dirs[:] = [d for d in dirs if d != ".git"]
        for f in sorted(files):
            if not f.endswith(".md"):
                continue
            p = os.path.join(root, f)
            t = io.open(p, encoding="utf-8", errors="replace").read()
            if "function_families:" not in t:
                continue
            out, changed = [], False
            pos = 0
            for m in ROW.finditer(t):
                rel = m.group(2).strip()
                mp = os.path.normpath(os.path.join(root, rel))
                checked += 1
                if not os.path.isfile(mp):
                    missing += 1
                    bad.append((os.path.relpath(p, a.db), rel, "members file not found", ""))
                    continue
                rows = sum(1 for l in io.open(mp, encoding="utf-8", errors="replace")
                           if l.strip() and not l.startswith("#"))
                # side files are bare address lists; those with a column header have one
                first = next((l for l in io.open(mp, encoding="utf-8", errors="replace")
                              if l.strip() and not l.startswith("#")), "")
                if not re.match(r"^[0-9A-Fa-f]{8}\s*$", first.split("\t")[0].strip()):
                    rows -= 1
                declared = int(m.group(4))
                if declared == rows:
                    ok += 1
                    continue
                bad.append((os.path.relpath(p, a.db).replace(os.sep, "/"), rel,
                            "declared %d, file has %d" % (declared, rows), rows))
                if a.write:
                    out.append(t[pos:m.start(4)])
                    out.append(str(rows))
                    pos = m.end(4)
                    changed = True
                    fixed += 1
            if a.write and changed:
                out.append(t[pos:])
                io.open(p, "w", encoding="utf-8", newline="\n").write("".join(out))

    print("declared families checked : %d" % checked)
    print("count already correct     : %d" % ok)
    print("members file missing      : %d" % missing)
    print("count mismatched          : %d" % len([b for b in bad if "declared" in b[2]]))
    for doc, rel, why, _n in bad:
        print("    %-58s %-34s %s" % (doc[:58], rel[:34], why))
    if a.write:
        print("\n  counts rewritten: %d" % fixed)
    elif bad:
        print("\n  dry run - pass --write to sync. Re-run the family's SELECTOR first; this only")
        print("  fixes the declared number, never the membership.")
    return 1 if [b for b in bad if "declared" in b[2]] else 0


if __name__ == "__main__":
    sys.exit(main())
