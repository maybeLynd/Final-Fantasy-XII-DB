"""homing_pack.py [--plan] [--hosts N] [--min K] [--max-bytes B] - F homing packs for OPUS's callee-host class
(OPUS, 2026-10-03; FABLE's split FABLE-REQ-OPUS-F-HOMING-SPLIT-1003, board OPUS-F-HOMING-CALLEE-HOST-1003).

For each still-unexplained body in fable-homing-stream-1003/callee-host-bodies.tsv:
- its direct callees are decoded (call / jmp rel32 inside the body);
- every bearing page citing one of those callees is a candidate host;
- the host is the page citing the MOST SPECIFIC callee: the one with the fewest direct callers in the image (a page
  documenting a shared helper such as memset is a weak home). Ties go to the page with more homed bodies.
Hosts the scope guard BLOCKs (OPUS_SWEEPS_OK=1 applies FABLE's sweep rule) are skipped and their bodies re-homed to
the next host. --plan prints the host plan only. Otherwise the chosen hosts' packs are written to
<GitHub DB checkout>/cloud-input/f-homing/<slug>.md, each body with its listing and the callee(s) the host cites,
and appended to cloud-input/f-homing/INDEX.tsv. Bodies already packed (INDEX) are skipped.
"""
import argparse
import bisect
import collections
import io
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cloudlib as cl  # noqa: E402
import listing as L  # noqa: E402
sys.path.insert(0, cl.KIT)
import check_dispositions as cd  # noqa: E402
import retool  # noqa: E402
import f_pack  # noqa: E402
from interior_ingest import homing_targets  # noqa: E402

OUT = os.path.join(cl.GHDB, "cloud-input", "f-homing")


def callees(f, n):
    d = retool.R.at(f, n)
    out = set()
    for i in retool.R.md.disasm(d, f):
        if i.mnemonic in ("call", "jmp") and i.operands and i.operands[0].type == 2:
            t = i.operands[0].imm
            if not (f <= t < f + n):
                out.add(t)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", action="store_true")
    ap.add_argument("--hosts", type=int, default=5)
    ap.add_argument("--min", type=int, default=3)
    ap.add_argument("--max-bytes", type=int, default=6000)
    a = ap.parse_args()
    sizes = L.sizes()
    entries = sorted(sizes)
    todo = homing_targets()
    idx_path = os.path.join(OUT, "INDEX.tsv")
    packed = set()
    if os.path.exists(idx_path):
        for l in io.open(idx_path, encoding="utf-8"):
            if l.strip() and not l.startswith("#"):
                packed |= {int(x, 16) for x in l.split("\t")[2].split(",") if x}
    todo -= packed
    # which bearing pages cite each function (any citation)
    # FABLE's hint (FABLE-NOTICE-OPUS-CALLEE-HOST-RTTI-1003): an RTTI virtual method's natural host is the page
    # documenting its owning class. Among the pages citing one of its callees, a page naming that class wins.
    rtti = collections.defaultdict(set)
    for l in io.open(os.path.join(cl.DB, "00-Engine-Core-Runtime", "Object-Model", "members", "rtti-methods.tsv"),
                     encoding="utf-8"):
        f = l.rstrip("\n").split("\t")
        if len(f) >= 2 and re.match(r"^[0-9A-F]{8}$", f[0]) and int(f[0], 16) in todo:
            rtti[int(f[0], 16)].add(f[1].split("::")[-1].split("<")[0])
    text = {}
    cites = collections.defaultdict(set)
    for p in cd.docs(cl.DB):
        t = io.open(p, encoding="utf-8", errors="replace").read()
        if not cd._bearing(t):
            continue
        rel = os.path.relpath(p, cl.DB).replace(os.sep, "/")
        text[rel] = t
        for h in cd.CITE.findall(t):
            cites[int(h, 16)].add(rel)
    calls = retool.scan()["calls"]
    ncallers = {k: len({c for c, _s in v}) for k, v in calls.items()}
    cand = {}
    for f in todo:
        cs = [c for c in callees(f, sizes[f]) if cites.get(c)]
        if not cs:
            continue
        cs.sort(key=lambda c: (ncallers.get(c, 0), c))
        cand[f] = [(c, sorted(cites[c])) for c in cs]
    guard = {}

    def ok(page):
        if page not in guard:
            r = subprocess.run([sys.executable, "-B", os.path.join(cl.HERE, "scope_guard.py"), page, "--json"],
                               capture_output=True, text=True)
            try:
                guard[page] = json.loads(r.stdout)[0]["verdict"] != "BLOCK"
            except Exception:
                guard[page] = False
        return guard[page]

    # first pass: the most specific callee's pages; count homes per page for tie-breaks
    pref = collections.Counter(p for f, cs in cand.items() for p in cs[0][1])
    home = collections.defaultdict(list)
    for f, cs in sorted(cand.items()):
        placed = False
        for c, pages in cs:
            for p in sorted(pages, key=lambda p: (not any(k and k in text.get(p, "") for k in rtti.get(f, ())),
                                                 -pref[p], p)):
                if p in f_pack.NEVER:
                    continue
                home[p].append((f, c))
                placed = True
                break
            if placed:
                break
    plan = sorted(home.items(), key=lambda kv: -len(kv[1]))
    print("homable bodies: %d of %d still open (packed already: %d); hosts: %d" % (len(cand), len(todo) + len(packed), len(packed), len(plan)))
    if a.plan:
        for p, fs in plan[:40]:
            print("%4d  %s" % (len(fs), p))
        return
    os.makedirs(OUT, exist_ok=True)
    new_idx, n_hosts = [], 0
    for p, fs in plan:
        if n_hosts >= a.hosts:
            break
        if len(fs) < a.min or not ok(p):
            continue
        fs = sorted(fs)
        total, keep = 0, []
        for f, c in fs:
            if total + sizes[f] > a.max_bytes and keep:
                break
            keep.append((f, c)); total += sizes[f]
        slug = f_pack.slug_of(p)
        out = ["# F homing pack: `%s`" % p, "",
               "Generated %s by OPUS (homing_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: "
               "`docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a "
               "function this page documents (named below); the sentence MUST name that callee by address. Report "
               "`\"mode\": \"homing\"`." % (cl.stamp(),), "",
               "Bodies: %d. No bearing page cites them and no documented function calls them directly." % len(keep), ""]
        for f, c in keep:
            lines, _tok = L.listing(f)
            out += ["## %08X (%d B, extent %08X-%08X)" % (f, sizes[f], f, f + sizes[f]), "",
                    "Documented callee on this page: `%08X`" % c, "", "```"] + lines + ["```", ""]
        io.open(os.path.join(OUT, slug + ".md"), "w", encoding="utf-8", newline="\n").write("\n".join(out))
        new_idx.append("\t".join([slug, p, ",".join("%08X" % f for f, _c in keep), str(total), cl.stamp(), "PACKED"]))
        print("PACK  %s  %d bodies %d B -> cloud-input/f-homing/%s.md" % (p, len(keep), total, slug))
        n_hosts += 1
    if new_idx:
        head = "" if os.path.exists(idx_path) else "# slug\tpage\tbodies\tbytes\tpacked\tstate\n"
        with io.open(idx_path, "a", encoding="utf-8", newline="\n") as fh:
            fh.write(head + "\n".join(new_idx) + "\n")


if __name__ == "__main__":
    main()
