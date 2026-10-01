"""f_pack.py [--pages N] [--page PATH ...] [--min-fns K] - write F-interior input packs for cloud sessions (OPUS, 2026-10-01).

For each chosen DOCUMENTED page with F-frontier functions it cites only at their entry, writes
  <GitHub DB checkout>/cloud-input/f-interior/<slug>.md
holding the page path, then every such function's annotated disassembly (listing.py: rip targets, image-base tables,
decoded constants and strings, function-entry branch targets), and appends the page to cloud-input/f-interior/INDEX.tsv.

Pages are chosen by entry-only count (largest first) and must pass scope_guard (BLOCK pages are skipped and listed),
so no cloud draft duplicates a page another identity or lane is working. vtable-method-index.md is never packed (a
generated index page; interior rows there would be metric gaming). Pages already packed (in INDEX.tsv) are skipped.
The packs are text derived from the certified executable: they go only into the private GitHub DB repo, never into the
RE repo or anywhere public."""
import argparse, collections, io, json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cloudlib as cl  # noqa: E402
import listing as L  # noqa: E402
sys.path.insert(0, cl.KIT)
import check_dispositions as cd  # noqa: E402
import frontier_census as fc  # noqa: E402

NEVER = {"00-Engine-Core-Runtime/Object-Model/vtable-method-index.md"}
OUT = os.path.join(cl.GHDB, "cloud-input", "f-interior")


def slug_of(page):
    s = os.path.splitext(os.path.basename(page))[0].lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")[:60]


def entry_only_pages():
    sizes = L.sizes()
    a_set, entry_only, _ai, _da = cd.measure_a(cl.DB, sizes)
    front = fc.frontier_set(cl.DB, sizes) - fc.uc1_band.frontier_starts()
    targets = front & set(entry_only)
    by_page = collections.defaultdict(set)
    for p in cd.docs(cl.DB):
        t = io.open(p, encoding="utf-8", errors="replace").read()
        if not cd._bearing(t):
            continue
        for h in cd.CITE.findall(t):
            v = int(h, 16)
            if v in targets:
                by_page[os.path.relpath(p, cl.DB).replace(os.sep, "/")].add(v)
    return by_page


def context(text, fn):
    m = re.search("%08X" % fn, text)
    return text[max(0, m.start() - 200):m.start() + 240].replace("\n", " ").replace("`", "'") if m else ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pages", type=int, default=3)
    ap.add_argument("--page", action="append", default=[])
    ap.add_argument("--min-fns", type=int, default=8)
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    idx_path = os.path.join(OUT, "INDEX.tsv")
    done = set()
    if os.path.exists(idx_path):
        done = {l.split("\t")[1] for l in io.open(idx_path, encoding="utf-8") if l.strip() and not l.startswith("#")}
    by_page = entry_only_pages()
    ranked = [p for p, fs in sorted(by_page.items(), key=lambda kv: -len(kv[1]))
              if p not in NEVER and p not in done and len(fs) >= a.min_fns]
    if a.page:
        ranked = [p for p in a.page if p in by_page]
    chosen = []
    for p in ranked:
        if len(chosen) >= (len(a.page) if a.page else a.pages):
            break
        fns = sorted(by_page[p])
        r = subprocess.run([sys.executable, "-B", os.path.join(cl.HERE, "scope_guard.py"), p, "--json", "--fns",
                            ",".join("%08X" % f for f in fns)], capture_output=True, text=True)
        g = json.loads(r.stdout)[0]
        if g["verdict"] == "BLOCK":
            print("SKIP  %s  (%s)" % (p, "; ".join(x[:90] for x in g["reasons"][:2])))
            continue
        chosen.append((p, fns, g))
    new_idx = []
    for p, fns, g in chosen:
        slug = slug_of(p)
        text = io.open(os.path.join(cl.DB, p), encoding="utf-8", errors="replace").read()
        out = ["# F-interior pack: `%s`" % p, "",
               "Generated %s by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: "
               "`docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/%s.json`." % (cl.stamp(), slug),
               "", "Functions: %d. Each is cited on the page only at its entry and is still in the F frontier." % len(fns), ""]
        if g["warnings"]:
            out += ["Scope guard: WARN (%s). OPUS read these before packing." % "; ".join(g["warnings"]), ""]
        total = 0
        for f in fns:
            lines, _tok = L.listing(f)
            n = L.sizes()[f]
            total += n
            out += ["## %08X (%d B, extent %08X-%08X)" % (f, n, f, f + n), "",
                    "Page context: \"%s\"" % context(text, f)[:440], "", "```"] + lines + ["```", ""]
        io.open(os.path.join(OUT, slug + ".md"), "w", encoding="utf-8", newline="\n").write("\n".join(out))
        new_idx.append("\t".join([slug, p, str(len(fns)), str(total), cl.stamp(), "PACKED"]))
        print("PACK  %s  %d fns %d B -> cloud-input/f-interior/%s.md" % (p, len(fns), total, slug))
    if new_idx:
        head = "" if os.path.exists(idx_path) else "# slug\tpage\tfunctions\tbytes\tpacked\tstate\n"
        with io.open(idx_path, "a", encoding="utf-8", newline="\n") as fh:
            fh.write(head + "\n".join(new_idx) + "\n")


if __name__ == "__main__":
    main()
