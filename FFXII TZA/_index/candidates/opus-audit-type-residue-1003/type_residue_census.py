"""Type/field residue that the load-bearing contracts actually use (OPUS, 2026-10-03).

Answers FABLE-REQ-OPUS-AUDIT-TYPE-RESIDUE-1003 (independent corpus audit, section 8): not "how many of
the 9,146 field rows are immature", but which immature rows sit under a contract that a MET system
rests on.

LOAD-BEARING CONTRACTS. A production contract registered on a MET system (important-subsystems.tsv
`contracts`) or named by file in its L2-VERDICTS verdict contract cell, read with the sibling
census `../opus-audit-l1-contracts-1003/l1_contract_census.py` (imported, not copied). L2 contracts
are the headline; L1 ones are reported in their own column because that audit found all 29
load-bearing too.

THREE CITATION TIERS, each a different strength of "the contract uses this field":
  A  ACCESS  the contract's own `entries:` functions read/write the field: a field-access-index.tsv
             row whose `function` is an entry, at a `disp` inside the field. Strongest: the operation
             the contract specifies touches these bytes.
  S  STATIC  a static address named in the contract's Types/State sections resolves into the field:
             contract_named_state_census.py's own reader (imported), the denominator SWE2-AUDIT-SEM
             accepted for the `types` cell.
  R  RECORD  a contract line names the type (word match on types.tsv names) and an offset `+0xNN`
             inside the field. Weakest: line co-occurrence, so a line naming two types can mis-assign.

FLAGS on a cited field row (fields.tsv status columns; any one flags it):
  RUNG   readiness DISCOVERED or CLASSIFIED (the two lowest rungs present in the store)
  CONF   confidence UNKNOWN
  NAME   a placeholder name (field_/dword_/qword_/byte_/word_/ptr_/float_/span_/unk/vNN/qNN...)
  GAP    an unobserved span/tail/gap row (the same test contract_named_state_census uses)
  CTYPE  ctype empty or containing UNRESOLVED / '?'
A cited TYPE is flagged when its types.tsv readiness is DISCOVERED or CLASSIFIED.

fields.tsv and types.tsv are read with str.splitlines() (the store has carried mixed line endings).

Read-only. Re-run from anywhere:
    python -B "Database/FFXII TZA/_index/candidates/opus-audit-type-residue-1003/type_residue_census.py"
Options: --rows PATH writes every flagged (contract, field, tier) row as TSV.
"""
import argparse
import collections
import importlib.util
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
TYPES = os.path.join(DB, "_types")
KIT = os.path.normpath(os.path.join(DB, "..", "Tools", "analysis-kit", "gfz-scripts"))
L1C = os.path.normpath(os.path.join(HERE, "..", "opus-audit-l1-contracts-1003", "l1_contract_census.py"))

LOW_RUNGS = {"DISCOVERED", "CLASSIFIED"}
PLACEHOLDER = re.compile(r"^(field|dword|qword|byte|word|ptr|float|span|unk|unknown|pad|padding|reserved|"
                         r"v|q|p|f|u|val|mix|data)_?(0x)?[0-9A-Fa-f]*(_[0-9A-Fa-f]+)?$", re.I)
OFFSET = re.compile(r"\+\s*0x([0-9A-Fa-f]{1,5})\b")


def load_module(name, path):
    if os.path.dirname(path) not in sys.path:
        sys.path.insert(0, os.path.dirname(path))
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def tsv(path):
    lines = open(path, encoding="utf-8", errors="replace").read().splitlines()
    head = lines[0].split("\t")
    return [dict(zip(head, l.split("\t"))) for l in lines[1:] if l.strip() and not l.startswith("#")]


def num(x):
    try:
        return int(x, 16) if x.lower().startswith(("0x", "-0x")) else int(x, 16)
    except (ValueError, AttributeError):
        return None


def flags_of(f):
    out = []
    rd = f["readiness"].split("#")[0].strip()
    if rd in LOW_RUNGS:
        out.append("RUNG")
    if f["confidence"].split("#")[0].strip().upper() == "UNKNOWN":
        out.append("CONF")
    nm = f["name"].strip()
    if PLACEHOLDER.match(nm):
        out.append("NAME")
    if nm.lower().startswith(("unobserved", "gap", "unresolved")) or "Span" in nm:   # cnsc.field_at's test
        out.append("GAP")
    ct = f["ctype"].strip()
    if not ct or "UNRESOLVED" in ct.upper() or "?" in ct:
        out.append("CTYPE")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", default=None)
    a = ap.parse_args()

    l1c = load_module("l1_contract_census", L1C)
    cnsc = load_module("contract_named_state_census", os.path.join(KIT, "contract_named_state_census.py"))
    g26 = l1c.gate26()
    cs = l1c.contracts(g26)
    reg, ver = l1c.registry(), l1c.verdicts()
    met = {s for s, v in ver.items() if re.match(r"^MET\b", v["verdict"])}

    load_bearing = collections.defaultdict(set)          # contract path -> MET systems
    for s in met:
        names = set(re.findall(r"CONTRACT-[\w-]+\.md", ver[s]["contract"]))
        for c in cs:
            if c["path"] in reg[s]["contracts"] or c["base"] in names:
                load_bearing[c["path"]].add(s)

    types = {t["type"]: t for t in tsv(os.path.join(TYPES, "types.tsv"))}
    fields = collections.defaultdict(list)
    nfields = 0
    for f in tsv(os.path.join(TYPES, "fields.tsv")):
        o, n = num(f.get("offset", "")), None
        try:
            n = int(f.get("size", ""))
        except ValueError:
            n = None
        if o is None:
            continue
        f["_lo"], f["_hi"] = o, o + max(n or 1, 1)
        f["_flags"] = flags_of(f)
        fields[f["type"]].append(f)
        nfields += 1
    access = collections.defaultdict(list)                # function -> [(type, disp, kind)]
    for r in tsv(os.path.join(TYPES, "field-access-index.tsv")):
        d = num(r["disp"])
        if d is not None:
            access[r["function"].upper()].append((r["type"], d, r["kind"]))

    def covering(t, off):
        return [f for f in fields.get(t, ()) if f["_lo"] <= off < f["_hi"]]

    type_re = re.compile(r"(?<![\w])(%s)(?![\w])" % "|".join(sorted(map(re.escape, types), key=len, reverse=True)))
    spans, sfields, sizes = cnsc.load_store()

    cites = []                                            # (contract, level, systems, tier, type, field-row)
    type_cites = collections.defaultdict(set)             # contract -> types named
    for c in cs:
        if c["path"] not in load_bearing:
            continue
        text = c["text"]
        sysl = ",".join(sorted(load_bearing[c["path"]], key=lambda s: int(s[2:])))
        fm = l1c.front_matter(text.splitlines()) or []
        entries = {e.upper() for e in re.findall(r"\b([0-9A-Fa-f]{8})\b", l1c.block_key(fm, "entries"))}
        seen = set()

        def add(tier, t, f):
            k = (tier, t, f["offset"])
            if k not in seen:
                seen.add(k)
                cites.append((c["path"], c["level"], sysl, tier, t, f))

        # A - accesses by the contract's own entry functions
        for e in entries:
            for t, d, _k in access.get(e, ()):
                for f in covering(t, d):
                    add("A", t, f)
        # S - static addresses in Types/State sections, the accepted denominator
        for _sec, line, fenced in cnsc.state_sections(text):
            for m in (cnsc.FENCE_ADDR if fenced else cnsc.ADDR).finditer(line):
                v = int(m.group(1), 16)
                if not (cnsc.DATA_LO <= v < cnsc.DATA_HI):
                    continue
                hits = [sp for sp in spans if sp[0] <= v < sp[1] and sp[3] != "pointer cell"]
                if hits:
                    lo, _hi, t, _kind, stride = hits[0]
                    off = (v - lo) % stride if stride else v - lo
                    for f in covering(t, off):
                        add("S", t, f)
        # R - a type and an offset on one line
        for line in text.splitlines():
            named = set(type_re.findall(line))
            type_cites[c["path"]].update(named)
            if not named:
                continue
            for m in OFFSET.finditer(line):
                off = int(m.group(1), 16)
                for t in named:
                    for f in covering(t, off):
                        add("R", t, f)

    # ---- report
    lb_l2 = sorted(p for p in load_bearing if next(c for c in cs if c["path"] == p)["level"] == "L2")
    lb_l1 = sorted(p for p in load_bearing if next(c for c in cs if c["path"] == p)["level"] == "L1")
    print("# store: %d types, %d field rows" % (len(types), nfields))
    allflag = collections.Counter(fl for fs in fields.values() for f in fs for fl in f["_flags"])
    anyflag = sum(1 for fs in fields.values() for f in fs if f["_flags"])
    print("# store-wide flagged field rows: %d of %d   by flag: %s" % (anyflag, nfields, dict(sorted(allflag.items()))))
    print("# MET systems: %d   load-bearing contracts: %d (L2 %d, L1 %d)" % (len(met), len(load_bearing), len(lb_l2), len(lb_l1)))
    print("#")

    def uniq(rows):
        return {(r[4], r[5]["offset"]) for r in rows}

    for lvl in ("L2", "L1"):
        rows = [r for r in cites if r[1] == lvl]
        flagged = [r for r in rows if r[5]["_flags"]]
        print("# %s load-bearing contracts: cited field rows (distinct type+offset)" % lvl)
        for tier in ("A", "S", "R"):
            t_rows = [r for r in rows if r[3] == tier]
            t_flag = [r for r in t_rows if r[5]["_flags"]]
            print("#   tier %s  cited %5d   flagged %5d" % (tier, len(uniq(t_rows)), len(uniq(t_flag))))
        print("#   any    cited %5d   flagged %5d" % (len(uniq(rows)), len(uniq(flagged))))
        fc = collections.Counter()
        for k in uniq(flagged):
            f = next(r[5] for r in flagged if (r[4], r[5]["offset"]) == k)
            for fl in f["_flags"]:
                fc[fl] += 1
        print("#   flagged by flag (a row can carry several): %s" % dict(sorted(fc.items())))
        rc = collections.Counter(next(r[5] for r in flagged if (r[4], r[5]["offset"]) == k)["readiness"] for k in uniq(flagged))
        print("#   flagged by readiness: %s" % dict(rc.most_common()))
        print("#")

    # The core worklist: L2, tier A or S (the contract's operations touch it / its state names it),
    # flagged by RUNG or CONF, and NOT a gap row (a gap row is a declared opaque extent by construction).
    core = collections.OrderedDict()
    for r in cites:
        f = r[5]
        if r[1] != "L2" or r[3] not in ("A", "S"):
            continue
        fl = set(f["_flags"])
        if not (fl & {"RUNG", "CONF"}) or "GAP" in fl:
            continue
        k = (r[4], f["offset"])
        e = core.setdefault(k, dict(f=f, contracts=set(), systems=set(), tiers=set()))
        e["contracts"].add(os.path.basename(r[0]))
        e["systems"].update(r[2].split(","))
        e["tiers"].add(r[3])
    print("# CORE WORKLIST - L2 load-bearing, tier A or S, flagged RUNG or CONF, not a gap row: %d field rows" % len(core))
    by_type = collections.Counter(k[0] for k in core)
    print("#   over %d types: %s" % (len(by_type), ", ".join("%s=%d" % kv for kv in by_type.most_common())))
    print("# columns: type  offset  size  name  ctype  readiness  confidence  flags  tiers  systems  contracts")
    for (t, off), e in sorted(core.items(), key=lambda kv: (kv[0][0], num(kv[0][1]))):
        f = e["f"]
        print("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (
            t, f["offset"], f["size"], f["name"], f["ctype"] or "-", f["readiness"], f["confidence"],
            "+".join(f["_flags"]), "".join(sorted(e["tiers"])),
            ",".join(sorted(e["systems"], key=lambda s: int(s[2:]))), " ".join(sorted(e["contracts"]))))

    # A declared gap the contract's own entry functions touch is the one place a gap row can hide behaviour:
    # "unobserved" is the row's claim, the access index is the counter-claim.
    print("#")
    print("# GAP rows touched by a load-bearing contract's own entry functions (tier A), with the touching accesses:")
    print("# columns: level  type  offset  size  name  readiness  confidence  contract  accesses(kind@site)")
    acc_by = collections.defaultdict(list)
    for fn, lst in access.items():
        for t, d, k in lst:
            acc_by[(t, d)].append((fn, k))
    site = collections.defaultdict(list)
    for r in tsv(os.path.join(TYPES, "field-access-index.tsv")):
        d = num(r["disp"])
        if d is not None:
            site[(r["type"], r["function"].upper())].append((d, r["kind"], r["site"]))
    gseen = set()
    ngap = collections.Counter()
    for r in cites:
        f = r[5]
        if r[3] != "A" or "GAP" not in f["_flags"]:
            continue
        k = (r[1], r[4], f["offset"], os.path.basename(r[0]))
        if k in gseen:
            continue
        gseen.add(k)
        ngap[r[1]] += 1
        fm = l1c.front_matter(next(c for c in cs if c["path"] == r[0])["text"].splitlines()) or []
        ents = {e.upper() for e in re.findall(r"\b([0-9A-Fa-f]{8})\b", l1c.block_key(fm, "entries"))}
        hits = ["%s@%s" % (kd, st) for e in sorted(ents) for d, kd, st in site.get((r[4], e), ())
                if f["_lo"] <= d < f["_hi"]]
        print("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (r[1], r[4], f["offset"], f["size"], f["name"], f["readiness"],
                                                   f["confidence"], os.path.basename(r[0]), " ".join(hits[:8])))
    print("# GAP rows touched by entry functions: L2 %d, L1 %d" % (ngap["L2"], ngap["L1"]))

    print("#")
    print("# cited TYPES at the lowest rungs (types.tsv readiness), named by L2 load-bearing contracts:")
    tn = collections.defaultdict(set)
    for p in lb_l2:
        for t in type_cites[p]:
            if types[t]["readiness"].split("#")[0].strip() in LOW_RUNGS:
                tn[t].add(os.path.basename(p))
    for t in sorted(tn):
        print("%s\t%s\t%s\t%s" % (t, types[t]["size"], types[t]["readiness"], " ".join(sorted(tn[t]))))
    print("# %d types" % len(tn))

    if a.rows:
        with open(a.rows, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("contract\tlevel\tsystems\ttier\ttype\toffset\tsize\tname\tctype\treadiness\tconfidence\tflags\n")
            for r in cites:
                f = r[5]
                if f["_flags"]:
                    fh.write("\t".join([r[0], r[1], r[2], r[3], r[4], f["offset"], f["size"], f["name"],
                                        f["ctype"], f["readiness"], f["confidence"], "+".join(f["_flags"])]) + "\n")


if __name__ == "__main__":
    sys.exit(main())
