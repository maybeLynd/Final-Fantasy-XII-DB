#!/usr/bin/env python3
"""recon_depgraph.py - reconstruction dependency graph, level 0 (category nodes). SWE2-CONTRACT, 2026-10-03.

Design: Database/FFXII TZA/_index/candidates/swe2contract-design-reconstruction-dependency-graph-1003/README.md
(addendum 2026-10-03 section 4). A PLANNING AID, NOT A METRIC: nothing here feeds goal_gate, DB_GOAL or any verdict.

Minimal first increment of the design's section 11. It reads sources S1-S4:
  S1  graph/functions.tsv + graph/edges.tsv (ledger owner -> folder through _index/CODEDOMAIN-OWNER-MAP.tsv)
  S2  _index/candidates/neighbour-dispositions.tsv (page -> far layer, example pairs, verdict, label note)
  S3  _types/field-access-index.tsv x _types/types.tsv (accessing function's folder -> the type's category)
  S4  01-.../Verb-Dispatch/scriptvm-dispatch.tsv (script VM -> handler folder; always sequencing)
S5 (CONTRACT sections) and S6 (completion-package dependencies) are later increments.

Rules (design sections 3-5), per fact and never by count:
  * hard: an S1 call, an S2 outbound (SERVICE-direction) crossing, an S3 field access;
  * sequencing: an S2 MECHANICAL / GENUINELY-IRRELEVANT row and the S1 calls it names, every S4 binding;
  * dropped: S2 FALSE-SUBJECT rows, substrate ends (audit_crossrefs.is_substrate), callees with more than
    audit_crossrefs.HUB_FANIN callers, same-folder facts. Folder ORDER is never read (check C1);
  * an unowned S2 subject claimed by pages in more than one folder is flagged `ambiguous`; a subject whose ledger
    owner's folder differs from its page's folder is flagged `owner-conflict` (from = ledger folder, which is the
    authority). Every flag is listed and none is resolved here (check C6); `ambiguous` and `unresolved-endpoint` rows
    are kept out of the component computation.
Components: SCCs of the hard subgraph without the base layer (00, 22, 23, 24) and without flagged rows; topological
layers of the condensation; weakly connected components.

Outputs: <out>.tsv (header comments carry the input fingerprints) and <out>.json.
  recon_depgraph.py build --out PREFIX       write PREFIX.tsv / PREFIX.json
  recon_depgraph.py check PREFIX.tsv          STALE (exit 1) naming every moved input, else CURRENT
"""
import argparse, collections, hashlib, io, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit_paths as KP  # noqa: E402
import audit_crossrefs as ac  # noqa: E402

BASE = {"00", "22", "23", "24"}
NOT_NODE = {"99"}
EXCLUDED = {"ambiguous", "unresolved-endpoint"}   # kept out of components; owner-conflict is listed, not excluded
PAIR = re.compile(r"\b([0-9A-F]{8}) (caller|callee) ([0-9A-F]{8})\b")


def default_inputs():
    db = KP.DB
    return {
        "functions": os.path.join(KP.WORK, "graph", "functions.tsv"),
        "edges": os.path.join(KP.WORK, "graph", "edges.tsv"),
        "owner_map": os.path.join(db, "_index", "CODEDOMAIN-OWNER-MAP.tsv"),
        "dispositions": os.path.join(db, "_index", "candidates", "neighbour-dispositions.tsv"),
        "field_access": os.path.join(db, "_types", "field-access-index.tsv"),
        "types": os.path.join(db, "_types", "types.tsv"),
        "verbs": os.path.join(db, "01-Script-VM-Native-Bridge", "Verb-Dispatch", "scriptvm-dispatch.tsv"),
    }


def fingerprint(path):
    """sha256 over CRLF-normalised bytes, as DERIVED-DATA.md requires."""
    with open(path, "rb") as f:
        return hashlib.sha256(f.read().replace(b"\r\n", b"\n")).hexdigest()


def rel(path, root):
    try:
        return os.path.relpath(path, root).replace("\\", "/")
    except ValueError:
        return path.replace("\\", "/")


def data_lines(path):
    """(1-based line number, fields) for every non-comment, non-blank line."""
    with io.open(path, encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            if line.startswith("#") or not line.strip():
                continue
            yield n, line.rstrip("\r\n").split("\t")


def folder_of_dir(category_dir):
    return category_dir.split("-", 1)[0] if category_dir else ""


def load_owner_map(path):
    m = {}
    for _, f in data_lines(path):
        if f[0] == "chain_label" or len(f) < 3:
            continue
        m[f[1]] = f[2]
    return m


class Graph:
    def __init__(self, inputs, root):
        self.inp, self.root = inputs, root
        self.facts = []          # dicts: from, to, kind, basis, tier, representative, citation, flags
        self.unparsed = collections.Counter()
        self.owner_map = load_owner_map(inputs["owner_map"])
        self.fn = ac.load_functions(inputs["functions"])
        self.callers, _ = ac.load_edges(inputs["edges"])

    # -- node attribution ---------------------------------------------------------------------------
    def node_of_owner(self, owner):
        if not owner:
            return None
        d = self.owner_map.get(owner)
        return d if d else "unresolved:" + owner

    def node_of_fn(self, addr):
        rec = self.fn.get(addr)
        return self.node_of_owner(rec["owner"]) if rec else None

    def cite(self, key, line):
        return "%s:%d" % (rel(self.inp[key], self.root), line)

    def add(self, frm, to, kind, basis, rep, citation, tier="", flags=()):
        if not frm or not to or frm == to:
            return
        flags = set(flags)
        for end in (frm, to):
            if end.startswith("unresolved:") or folder_of_dir(end) in NOT_NODE:
                flags.add("unresolved-endpoint")
        self.facts.append(dict(frm=frm, to=to, kind=kind, basis=basis, tier=tier, rep=rep,
                               citation=citation, flags=flags))

    # -- S2 first: it supplies the MECHANICAL pairs S1 must treat as sequencing ----------------------------
    def read_dispositions(self):
        claims = collections.defaultdict(set)      # unowned subject -> page folders
        rows = []
        for n, f in data_lines(self.inp["dispositions"]):
            if len(f) < 6:
                self.unparsed["S2 undispositioned row (no verdict column)"] += 1
                continue
            page, far, example, verdict = f[0], f[1], f[4], f[5]
            note = f[6] if len(f) > 6 else ""
            page_node = page.split("/", 1)[0]
            pairs = PAIR.findall(example)
            rows.append((n, page_node, far, pairs, verdict, note))
            for subj, _, _ in pairs:
                rec = self.fn.get(subj)
                if rec is not None and not rec["owner"]:
                    claims[subj].add(page_node)
        self.mechanical_pairs = set()
        for n, page_node, far, pairs, verdict, note in rows:
            if verdict == "FALSE-SUBJECT":
                continue
            lead = note.lstrip("*").strip()
            mech = verdict == "GENUINELY-IRRELEVANT" or lead.upper().startswith("MECHANICAL") \
                or re.match(r"(CLIENT|SERVICE)[^.:]{0,40}\bmechanical\b", lead, re.I) is not None
            tier = (re.search(r"\btier (\d+)", lead) or [None, ""])[1]
            label_node = self.node_of_owner(far)   # S2's far column: an owner token, or a CodeDomain family when unowned
            if not pairs:
                self.unparsed["S2 no example pair"] += 1
                continue
            for subj, rel_, other in pairs:
                flags = set()
                own_node = self.node_of_fn(subj)
                if own_node is None:
                    near = page_node
                    if len(claims.get(subj, ())) > 1:
                        flags.add("ambiguous")
                else:
                    near = own_node
                    if folder_of_dir(own_node) != folder_of_dir(page_node):
                        flags.add("owner-conflict")
                far_node = self.node_of_fn(other) or label_node   # the far body's own ledger owner first
                if rel_ == "callee":          # subject calls far body: outbound, page needs far layer
                    frm, to, a, b = near, far_node, subj, other
                else:                         # far body calls subject: inbound, far layer needs page
                    frm, to, a, b = far_node, near, other, subj
                if mech:
                    self.mechanical_pairs.add((a, b))
                self.add(frm, to, "sequencing" if mech else "hard", "call-dispositioned",
                         "%s -> %s" % (a, b), self.cite("dispositions", n), tier, flags)

    def read_calls(self):
        for n, f in data_lines(self.inp["edges"]):
            if f[0] == "caller" or len(f) < 2:
                continue
            if len(f) > 2 and f[2].lower() == "true":
                continue                                   # external import
            a, b = f[0].upper(), f[1].upper()
            ra, rb = self.fn.get(a), self.fn.get(b)
            if ra is None or rb is None or ac.is_substrate(ra) or ac.is_substrate(rb):
                continue
            if len(self.callers.get(b, ())) > ac.HUB_FANIN:
                continue
            na, nb = self.node_of_fn(a), self.node_of_fn(b)
            if not na or not nb:
                continue
            kind = "sequencing" if (a, b) in self.mechanical_pairs else "hard"
            self.add(na, nb, kind, "call", "%s -> %s" % (a, b), self.cite("edges", n))

    def read_field_access(self):
        cat = {}
        for _, f in data_lines(self.inp["types"]):
            if f[0] == "type" or len(f) < 3:
                continue
            cat[f[0]] = f[2]
        for n, f in data_lines(self.inp["field_access"]):
            if f[0] == "type" or len(f) < 6:
                continue
            ty, fnc, site = f[0], f[4].upper().zfill(8), f[5].upper()
            to = cat.get(ty)
            frm = self.node_of_fn(fnc)
            if not to or not frm:
                continue
            self.add(frm, to, "hard", "type-layout", "%s %s +%s at %s" % (fnc, ty, f[1], site),
                     self.cite("field_access", n))

    def read_verbs(self):
        vm = None
        for d in self.owner_map.values():
            if folder_of_dir(d) == "01":
                vm = d
                break
        vm = vm or "01-Script-VM-Native-Bridge"
        for n, f in data_lines(self.inp["verbs"]):
            if f[0] == "call_id" or len(f) < 6:
                continue
            node = self.node_of_owner(f[5])
            self.add(vm, node, "sequencing", "script-binding", "verb %s -> %s" % (f[0], f[3].upper()),
                     self.cite("verbs", n))

    def build(self):
        self.read_dispositions()
        self.read_calls()
        self.read_field_access()
        self.read_verbs()
        return self


def aggregate(facts):
    groups = collections.OrderedDict()
    for x in sorted(facts, key=lambda x: (x["frm"], x["to"], x["kind"], x["basis"], sorted(x["flags"]), x["rep"])):
        k = (x["frm"], x["to"], x["kind"], x["basis"], tuple(sorted(x["flags"])))
        g = groups.setdefault(k, dict(frm=x["frm"], to=x["to"], kind=x["kind"], basis=x["basis"], count=0,
                                      tiers=set(), rep=x["rep"], citation=x["citation"], flags=set()))
        g["count"] += 1
        if x["tier"]:
            g["tiers"].add(x["tier"])
        g["flags"] |= x["flags"]
    return list(groups.values())


def components(edges):
    """SCCs (Tarjan, iterative), topological layers of the condensation, weakly connected components.
    Hard edges only, without EXCLUDED flags, base layer excluded."""
    adj = collections.defaultdict(set)
    nodes = set()
    for e in edges:
        if e["kind"] != "hard" or e["flags"] & EXCLUDED or folder_of_dir(e["frm"]) in BASE                 or folder_of_dir(e["to"]) in BASE:
            continue
        adj[e["frm"]].add(e["to"])
        nodes |= {e["frm"], e["to"]}
    index, low, on, stack, sccs, counter = {}, {}, set(), [], [], [0]
    for root in sorted(nodes):
        if root in index:
            continue
        work = [(root, iter(sorted(adj[root])))]
        index[root] = low[root] = counter[0]; counter[0] += 1; stack.append(root); on.add(root)
        while work:
            v, it = work[-1]
            w = next(it, None)
            if w is not None:
                if w not in index:
                    index[w] = low[w] = counter[0]; counter[0] += 1; stack.append(w); on.add(w)
                    work.append((w, iter(sorted(adj[w]))))
                elif w in on:
                    low[v] = min(low[v], index[w])
                continue
            work.pop()
            if work:
                low[work[-1][0]] = min(low[work[-1][0]], low[v])
            if low[v] == index[v]:
                comp = []
                while True:
                    w = stack.pop(); on.discard(w); comp.append(w)
                    if w == v:
                        break
                sccs.append(sorted(comp))
    of = {n: i for i, c in enumerate(sccs) for n in c}
    dag = collections.defaultdict(set)
    for a in adj:
        for b in adj[a]:
            if of[a] != of[b]:
                dag[of[a]].add(of[b])
    # layer = longest chain of prerequisites below the component (edges point at prerequisites)
    memo = {}

    def depth(c):
        if c not in memo:
            memo[c] = 0
            memo[c] = 1 + max((depth(d) for d in dag[c]), default=-1)
        return memo[c]
    layers = collections.defaultdict(list)
    for i, c in enumerate(sccs):
        layers[depth(i)].append(c)
    und = collections.defaultdict(set)
    for a in adj:
        for b in adj[a]:
            und[a].add(b); und[b].add(a)
    seen, weak = set(), []
    for n in sorted(nodes):
        if n in seen:
            continue
        comp, todo = [], [n]
        seen.add(n)
        while todo:
            v = todo.pop(); comp.append(v)
            for w in und[v]:
                if w not in seen:
                    seen.add(w); todo.append(w)
        weak.append(sorted(comp))
    return {"sccs": sorted(sccs, key=lambda c: (-len(c), c)),
            "layers": [sorted(layers[k]) for k in sorted(layers)],
            "weak_components": sorted(weak, key=lambda c: (-len(c), c)),
            "base_layer": sorted(BASE)}


def verify_citations(edges, root):
    """C2: every citation resolves to an existing line that carries the representative's addresses."""
    bad, cache = [], {}
    for e in edges:
        path, line = e["citation"].rsplit(":", 1)
        full = os.path.join(root, path)
        if full not in cache:
            with io.open(full, encoding="utf-8") as f:
                cache[full] = f.read().split("\n")
        text = cache[full][int(line) - 1] if int(line) <= len(cache[full]) else ""
        need = re.findall(r"\b[0-9A-F]{8}\b", e["rep"])
        have = set(re.findall(r"\b[0-9A-F]{8}\b", text.upper()))   # whole tokens: FUN_xxxxxxxx does not count
        if not text or any(a not in have for a in need):
            bad.append(e["citation"])
    return bad


COLUMNS = ["from", "to", "kind", "basis", "evidence_class", "tier", "count", "representative", "citation", "flags"]


def write_outputs(prefix, edges, comp, inputs, root, unparsed):
    gen = fingerprint(os.path.abspath(__file__))
    head = ["# recon_depgraph.py level-0 reconstruction dependency graph - PLANNING AID, NOT A METRIC",
            "# design: _index/candidates/swe2contract-design-reconstruction-dependency-graph-1003/README.md",
            "# generator_sha256\t%s" % gen]
    for k in sorted(inputs):
        head.append("# input\t%s\t%s\t%s" % (k, rel(inputs[k], root), fingerprint(inputs[k])))
    for k, v in sorted(unparsed.items()):
        head.append("# unparsed\t%s\t%d" % (k, v))
    with io.open(prefix + ".tsv", "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(head) + "\n" + "\t".join(COLUMNS) + "\n")
        for e in edges:
            f.write("\t".join([e["frm"], e["to"], e["kind"], e["basis"], "static", ",".join(sorted(e["tiers"])),
                               str(e["count"]), e["rep"], e["citation"], ",".join(sorted(e["flags"]))]) + "\n")
    js = {"generator_sha256": gen, "inputs": {k: fingerprint(v) for k, v in inputs.items()},
          "edges": [{c: v for c, v in zip(COLUMNS, [e["frm"], e["to"], e["kind"], e["basis"], "static",
                                                    sorted(e["tiers"]), e["count"], e["rep"], e["citation"],
                                                    sorted(e["flags"])])} for e in edges]}
    js.update(comp)
    with io.open(prefix + ".json", "w", encoding="utf-8", newline="\n") as f:
        json.dump(js, f, indent=1, sort_keys=True)


def check(tsv, root):
    """C5: recompute every recorded input fingerprint; STALE names each moved input."""
    moved = []
    with io.open(tsv, encoding="utf-8") as fh:
        lines = [l.rstrip("\n").split("\t") for l in fh]
    for f in lines:
        if f[0] == "# input" and len(f) == 4:
            p = os.path.join(root, f[2])
            if not os.path.exists(p) or fingerprint(p) != f[3]:
                moved.append(f[1] + " (" + f[2] + ")")
        elif f[0] == "# generator_sha256" and fingerprint(os.path.abspath(__file__)) != f[1]:
            moved.append("generator")
    return moved


def run(inputs, root):
    g = Graph(inputs, root).build()
    edges = aggregate(g.facts)
    return edges, components(edges), g.unparsed


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build"); b.add_argument("--out", required=True)
    c = sub.add_parser("check"); c.add_argument("tsv")
    a = ap.parse_args(argv)
    root = KP.ROOT
    if a.cmd == "check":
        moved = check(a.tsv, root)
        print("STALE: moved %s" % ", ".join(moved) if moved else "CURRENT")
        return 1 if moved else 0
    inputs = default_inputs()
    edges, comp, unparsed = run(inputs, root)
    bad = verify_citations(edges, root)
    if bad:
        print("C2 FAIL: %d citation(s) do not carry their representative, e.g. %s" % (len(bad), bad[:3]))
        return 2
    write_outputs(a.out, edges, comp, inputs, root, unparsed)
    hard = [e for e in edges if e["kind"] == "hard"]
    print("edges %d (hard %d, sequencing %d, flagged %d); largest SCC %d nodes; layers %d; wrote %s.tsv/.json"
          % (len(edges), len(hard), len(edges) - len(hard), sum(1 for e in edges if e["flags"]),
             len(comp["sccs"][0]) if comp["sccs"] else 0, len(comp["layers"]), a.out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
