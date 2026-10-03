"""L1 production-contract census against the L2-MET systems (OPUS, 2026-10-03).

Answers FABLE-REQ-OPUS-AUDIT-L1-CONTRACTS-1003 (independent corpus audit, section 7).

A production contract is a .md file outside the underscore folders (_index, _templates,
_experiments, _types) whose YAML front matter (between the first two '---' lines) carries a
top-level `contract:` key. A `contract:` key further down a page body is not front matter and
is not counted (gi-render-command-family.md carries one at line 655).

For each L1 contract it reports, per registered system S-NN:
  REG   - listed in that system's `contracts` column of important-subsystems.tsv
  CELL  - named by file name in that system's verdict-row contract cell (L2-VERDICTS.md)
  ROW   - named by file name elsewhere in that system's verdict row
  IMPL  - one of the contract's `implements:` pages is one of that system's primary_pages
  SOLE  - IMPL, and no other production contract implements that page
The verdict row and its MET cell are read exactly as goal_gate.py check_verdicts reads them
(header width, last full-width row wins, a leading MET token counts).

The census does not decide load-bearing on its own: a verdict cell often credits a contract by
subject ("update gate (pre-existing)") rather than by file name. It prints the mechanical links;
README.md records the reading of each cell. As a mechanical floor, CELL or SOLE on a MET system
is printed as `mech_load_bearing`.

It also prints, for every production contract, level x section-13 evidence class (read by
check_gate26.runtime_class, imported, not re-implemented) x scope x the date the file was
first added (git), which is what shows what the `level:` key does and does not record.

Read-only. Re-run from anywhere (git must be on PATH for the dates):
    python -B "Database/FFXII TZA/_index/candidates/opus-audit-l1-contracts-1003/l1_contract_census.py"
"""
import importlib.util
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
IDX = os.path.join(DB, "_index")
GATE26 = os.path.normpath(os.path.join(DB, "..", "Tools", "analysis-kit", "gfz-scripts", "check_gate26.py"))
READINESS = ["CONTRACT READY", "BEHAVIORALLY UNDERSTOOD", "DIFFERENTIAL TESTED",
             "RUNTIME VALIDATED", "PARITY CERTIFIED", "STRUCTURALLY UNDERSTOOD"]


def read_text(path):
    with open(path, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def front_matter(lines):
    if not lines or lines[0].strip() != "---":
        return None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return lines[1:i]
    return None


def top_key(fm, key):
    for l in fm:
        m = re.match(r"^%s:\s*(.*)$" % re.escape(key), l)
        if m:
            return m.group(1).strip()
    return None


def block_key(fm, key):
    """A key's value including indented continuation lines (YAML list or folded block)."""
    out, on = [], False
    for l in fm:
        if re.match(r"^%s:" % re.escape(key), l):
            on = True
            out.append(l.split(":", 1)[1])
        elif on and (l.startswith(" ") or l.startswith("\t")):
            out.append(l)
        elif on:
            break
    return " ".join(out)


def rel(path):
    return os.path.relpath(path, DB).replace("\\", "/")


def resolve_impl(contract_path, value):
    """`implements:` names one or more .md pages, DB-root-relative on most contracts and
    contract-folder-relative on some (CONTRACT-transform-primitives.md, CONTRACT-ui-request-router.md);
    each is taken from whichever base exists, root first."""
    out = []
    for tok in re.findall(r"[\w./-]+\.md", value.split(" #")[0]):
        for base in (DB, os.path.dirname(contract_path)):
            p = os.path.normpath(os.path.join(base, tok))
            if os.path.isfile(p):
                out.append(rel(p))
                break
        else:
            out.append("UNRESOLVED:" + tok)
    return out


def gate26():
    spec = importlib.util.spec_from_file_location("check_gate26", GATE26)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def first_added(path):
    try:
        r = subprocess.run(["git", "log", "--diff-filter=A", "--follow", "--format=%ad", "--date=short",
                            "--", path], cwd=DB, capture_output=True, text=True, timeout=60)
        dates = r.stdout.split()
        return dates[-1] if dates else "?"
    except Exception:
        return "?"


def contracts(g26):
    out = []
    for root, dirs, files in os.walk(DB):
        if os.path.normpath(root) == DB:
            dirs[:] = [d for d in dirs if not d.startswith("_")]
        dirs.sort()
        for f in sorted(files):
            if not f.endswith(".md"):
                continue
            p = os.path.join(root, f)
            text = read_text(p)
            fm = front_matter(text.splitlines())
            if fm is None or top_key(fm, "contract") is None:
                continue
            lvl = (top_key(fm, "level") or "").split("#")[0].strip()
            rdy = top_key(fm, "readiness") or ""
            rprefix = next((r for r in READINESS if rdy.upper().startswith(r)), "OTHER:" + rdy[:30])
            secs = g26.sections(text)
            out.append(dict(path=rel(p), base=f, level=lvl or "(none)", readiness=rprefix,
                            scope=(top_key(fm, "scope") or "").split("#")[0].strip(),
                            implements=resolve_impl(p, block_key(fm, "implements")),
                            s13=g26.runtime_class(secs.get(g26.RUNTIME_SECTION, "")),
                            added=first_added(rel(p)), text=text))
    return out


def registry():
    reg = {}
    for l in read_text(os.path.join(IDX, "important-subsystems.tsv")).splitlines()[1:]:
        c = l.split("\t")
        if len(c) < 6 or not re.match(r"^S-\d+$", c[0]):
            continue
        norm = lambda s: [rel(os.path.normpath(os.path.join(IDX, x.strip()))) for x in s.split(";") if x.strip()]
        reg[c[0]] = dict(name=c[2], pages=norm(c[4]), contracts=norm(c[5]))
    return reg


def verdicts():
    """goal_gate.check_verdicts' reading, plus the contract cell and the raw row."""
    lines = read_text(os.path.join(IDX, "L2-VERDICTS.md")).splitlines()
    width = None
    for l in lines:
        if re.match(r"^\|\s*system\b", l, re.I) and "binding gap" in l:
            width = len([c for c in re.split(r"(?<!\\)\|", l) if c.strip()])
    rows = {}
    for l in lines:
        m = re.match(r"^\|\s*(?:\*\*)?(S-\d+)\b([^|]*)\|(.*)$", l)
        if not m:
            continue
        cells = [c.strip().strip("*").strip() for c in re.split(r"(?<!\\)\|", m.group(3))]
        cells = [c for c in cells if c]
        if len(cells) == width - 1:
            rows[m.group(1)] = dict(verdict=cells[-2], contract=cells[0], row=l)
    return rows


def sid(s):
    return int(s[2:])


def require_level_key(cs):
    """Refuse to report when no contract carries `level:` (OPUS, 2026-10-03, SWE2CONTRACT-REQ-OPUS-LEVEL-READER-CENSUS-
    PIN-1003). FABLE retired the key (ruling rev 49820; 015712a7a). This census splits contracts by it, so at a tree
    without it, it printed '0 L1 contracts' and exited 0 - a false current result. It reproduces at c49f03691, the last
    tree that carried the key; elsewhere it exits 2 and says why. (The grain is now `scope:`.)"""
    if cs and all(c["level"] == "(none)" for c in cs):
        print("REFUSED: none of the %d production contracts carries the front-matter key `level:` - FABLE retired it "
              "(ruling rev 49820, 015712a7a). This census splits by that key and reproduces only at c49f03691; "
              "nothing it would print here is a measurement." % len(cs))
        sys.exit(2)


def main():
    g26 = gate26()
    cs = contracts(g26)
    require_level_key(cs)
    reg = registry()
    ver = verdicts()
    met = {s for s, v in ver.items() if re.match(r"^MET\b", v["verdict"])}

    print("# production contracts: %d" % len(cs))
    for k, n in sorted(Counter(c["level"] for c in cs).items()):
        print("#   level %-6s %d" % (k, n))
    for k, n in sorted(Counter(c["readiness"] for c in cs).items()):
        print("#   readiness %-26s %d" % (k, n))
    print("# registered systems: %d   verdict rows: %d   MET: %d" % (len(reg), len(ver), len(met)))
    notmet = sorted((s for s in reg if s not in met), key=sid)
    print("# not MET: %s" % (", ".join(notmet) or "none"))
    unres = [(c["base"], i) for c in cs for i in c["implements"] if i.startswith("UNRESOLVED:")]
    print("# unresolved implements tokens: %d %s" % (len(unres), unres[:5]))
    print("#")
    print("# what the level key tracks - level x section-13 class (check_gate26.runtime_class):")
    for (lv, s13), n in sorted(Counter((c["level"], c["s13"]) for c in cs).items()):
        print("#   %-3s %-9s %d" % (lv, s13, n))
    print("# level x scope:")
    for (lv, sc), n in sorted(Counter((c["level"], c["scope"]) for c in cs).items()):
        print("#   %-3s %-14s %d" % (lv, sc, n))
    print("# level x date first added (git):")
    for lv in sorted({c["level"] for c in cs}):
        ds = sorted(c["added"] for c in cs if c["level"] == lv)
        print("#   %-3s first %s  last %s  added on/after 2026-09-21: %d of %d"
              % (lv, ds[0], ds[-1], sum(d >= "2026-09-21" for d in ds), len(ds)))
    print("#")

    by_page = defaultdict(list)
    for c in cs:
        for p in c["implements"]:
            by_page[p].append(c)

    by_base = {c["base"]: c for c in cs}

    def on_system(s):
        """Contracts registered on S-NN, or named by file name in its verdict contract cell."""
        out = [c for c in cs if c["path"] in reg[s]["contracts"]]
        out += [by_base[b] for b in re.findall(r"CONTRACT-[\w-]+\.md", ver.get(s, {}).get("contract", ""))
                if b in by_base and by_base[b] not in out]
        return out

    comps = defaultdict(set)
    l1 = [c for c in cs if c["level"] == "L1"]
    print("# L1 contracts: %d" % len(l1))
    print("# COMP = a `scope: subsystem` L2 contract registered on, or credited in the cell of, the same system names this contract's file")
    print("# columns: n  contract  readiness  scope  s13  added  mech_load_bearing  links(S-id[*=MET]:kinds)  co-implementers(level)")
    summary = Counter()
    for i, c in enumerate(l1, 1):
        links = defaultdict(set)
        for s, r in reg.items():
            if c["path"] in r["contracts"]:
                links[s].add("REG")
            for p in c["implements"]:
                if p in r["pages"]:
                    links[s].add("IMPL")
                    if all(o is c for o in by_page[p]):
                        links[s].add("SOLE")
        for s, v in ver.items():
            if c["base"] in v["contract"]:
                links[s].add("CELL")
            elif c["base"] in v["row"]:
                links[s].add("ROW")
        for s in list(links):
            for o in on_system(s):
                if o is not c and o["level"] == "L2" and o["scope"] == "subsystem" and c["base"] in o["text"]:
                    links[s].add("COMP")
                    comps[c["base"]].add("%s<-%s" % (s, o["base"]))
        lb = sorted((s for s, k in links.items() if s in met and k & {"SOLE", "CELL"}), key=sid)
        summary["mech load-bearing (CELL or SOLE)" if lb else "no CELL/SOLE link - read the cell"] += 1
        ls = " ".join("%s%s:%s" % (s, "*" if s in met else "", "+".join(sorted(links[s])))
                      for s in sorted(links, key=sid))
        co = sorted({"%s(%s)" % (o["base"], o["level"]) for p in c["implements"] for o in by_page[p] if o is not c})
        print("%2d\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (i, c["path"], c["readiness"], c["scope"], c["s13"], c["added"],
                                                     ",".join(lb) or "-", ls or "-", " ".join(co) or "-"))
    print("#")
    for k, n in sorted(summary.items()):
        print("# %s: %d" % (k, n))
    print("#")
    print("# composing L2 subsystem contracts (COMP), per L1 contract:")
    for c in l1:
        print("#   %-48s %s" % (c["base"], " ".join(sorted(comps[c["base"]])) or "NONE"))
    no_comp = [c["base"] for c in l1 if not comps[c["base"]]]
    print("# L1 contracts with no composing L2 subsystem contract: %d %s" % (len(no_comp), " ".join(no_comp)))

    print("#")
    print("# primary pages of the MET systems these L1 contracts touch, and every contract implementing each:")
    touched = sorted({s for c in l1 for s, r in reg.items()
                      if c["path"] in r["contracts"] or set(c["implements"]) & set(r["pages"])}, key=sid)
    for s in touched:
        for p in reg[s]["pages"]:
            imps = " ".join("%s(%s)" % (o["base"], o["level"]) for o in by_page.get(p, [])) or "NONE"
            print("%s%s\t%s\t%s" % (s, "*" if s in met else "", p, imps))


if __name__ == "__main__":
    sys.exit(main())
