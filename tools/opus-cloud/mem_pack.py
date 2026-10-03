"""mem_pack.py PAGE FAMILY_SUBSTRING [--chunk N] [--stats] - drafting packs for unexplained members of a family the page
declares in its `function_families:` front matter (OPUS, 2026-10-03). For heterogeneous classification families (e.g.
the Phyre module families), whose members are ordinary functions grouped by module, not template copies: each member
gets its own sentence and interior anchors, like an F-interior row. Writes inbox/ee/<slug>-<family>-<k>.md; rows come
back as {"mode": "member"} reports and are applied by interior_ingest.py."""
import io
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cloudlib as cl  # noqa: E402
import listing as L  # noqa: E402
import f_pack  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def families(page):
    """[(name, members_path_abs)] from the page's function_families front matter."""
    p = os.path.join(cl.DB, *page.split("/"))
    t = io.open(p, encoding="utf-8", errors="replace").read()
    m = re.match(r"---\r?\n(.*?)\r?\n---", t, re.S)
    out = []
    for l in (m.group(1) if m else "").splitlines():
        mm = re.match(r'\s*-\s*"([^|]+?)\s*\|\s*[A-Z]\s*\|\s*([^|]+?)\s*\|', l)
        if mm:
            out.append((mm.group(1), os.path.normpath(os.path.join(os.path.dirname(p), mm.group(2)))))
    return out


def members(path):
    return [int(l.split("\t")[0], 16) for l in io.open(path, encoding="utf-8", errors="replace")
            if re.match(r"[0-9A-Fa-f]{8}\b", l)]


def explained():
    sys.path.insert(0, cl.KIT)
    import check_dispositions as CD
    sizes = CD.load_functions()
    return set(CD.evaluate(os.path.join(cl.DB), sizes)["explained_set"]), sizes


def unexplained_members(page, sub=None, exp=None):
    exp = exp if exp is not None else explained()[0]
    out = {}
    for name, path in families(page):
        if sub and sub.lower() not in name.lower():
            continue
        out[name] = [f for f in members(path) if f not in exp and f in L.sizes()]
    return out


def main():
    a = sys.argv[1:]
    page, sub = a[0], a[1]
    chunk = int(a[a.index("--chunk") + 1]) if "--chunk" in a else 40
    exp, _ = explained()
    fams = unexplained_members(page, sub, exp)
    for name, fs in fams.items():
        sz = sorted(L.sizes()[f] for f in fs)
        print("%-50s %4d unexplained; sizes min %s median %s max %s; total %d B" % (
            name, len(fs), sz[0] if sz else "-", sz[len(sz) // 2] if sz else "-", sz[-1] if sz else "-", sum(sz)))
        if "--stats" in a:
            continue
        slug = f_pack.slug_of(page) + "-" + re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
        for k in range(0, len(fs), chunk):
            part = fs[k:k + chunk]
            out = ["# member drafting pack: `%s`, family `%s`, part %d (OPUS, %s) - %d bodies" % (
                page, name, k // chunk + 1, cl.stamp(), len(part)), "",
                "Each body is an unexplained member of this family; no page explains it. Write one row per body: a "
                "sentence of what THIS body does (access and representation, every path), with 1-5 anchors strictly "
                "inside it. Report mode is \"member\".", ""]
            for f in part:
                lines, _t = L.listing(f)
                out += ["## %08X (%d B)" % (f, L.sizes()[f]), "", "```"] + lines + ["```", ""]
            p = os.path.join(HERE, "inbox", "ee", "%s-%d.md" % (slug, k // chunk + 1))
            io.open(p, "w", encoding="utf-8", newline="\n").write("\n".join(out))
            print("  wrote", os.path.basename(p), len(part))


if __name__ == "__main__":
    main()
