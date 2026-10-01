"""round5_notes.py DB - A-drift round 5 (OPUS for SWE2-EC7, 2026-10-01): set each repaired row's count and append the
dated sentence. Same mechanics as EC7's rows_notes.py (ec7-dd-adrift-pairing-0930): idempotent on TAG, keeps line
endings, asserts the members file holds the new count, no addresses in the notes (a hex word in a row note is read as a
citation; the addresses and causing pages are in the record)."""
import io, os, re, sys

DB = sys.argv[1]
TAG = " 2026-10-01 (OPUS for SWE2-EC7, A-drift round 5, record _index/candidates/opus-adrift-round5-1001):"
REC = "; addresses and causing pages in the record."


def left(n, why):
    return " %d member(s) left the family, since measured as A (A beats a declaration) after %s" % (n, why)


def same(sel, n):
    return "; %s re-run on a clean HEAD export drops exactly %s and admits nothing; the members file is the selector's output" % (
        sel, "it" if n == 1 else "these %s" % {2: "two", 3: "three"}[n])


INV = "OPUS re-statused the third-party middleware inventory (6d9fb5a1f) DOCUMENTED"
TR = "OPUS re-statused the authored data table registry (d526b865b) DOCUMENTED"
GF = "24-Compiler-And-CRT-Runtime/Generated-Families/generated-function-families.md"
TP = "23-Third-Party-Libraries/third-party-middleware-inventory.md"
ROWS = [
 ("01-Script-VM-Native-Bridge/Verb-Dispatch/the-shape-of-the-verb-population.md", "ScriptVM.VerbAdapter", 1033,
  left(2, "OPUS re-statused the capability-inhibition policy (eef738450) and the gambit evaluation page (95cf8c42f) DOCUMENTED")
  + "; select_verb_adapters.py re-run on a clean HEAD export drops exactly these two, admits nothing and leaves the leftovers file unchanged"),
 (TP, "Tremor with vorbisfile.c", 99, left(3, INV) + same("../18-Audio/members/select_audio_libraries.py", 3)
  + "; its other library files are unchanged"),
 (TP, "libvorbis float codec", 115, left(1, INV) + same("../18-Audio/members/select_audio_libraries.py", 1)),
 (TP, "zlib 1.2.11", 54, left(1, INV) + same("members/select_zlib.py", 1)),
 (TP, "Dear ImGui context object", 9, left(1, INV)
  + "; exact A removal. select_imgui.py does not re-run at HEAD: it asserts the departed context-object body is a member,"
    " so its assertion has to admit an A body before the selector can reproduce this file - recorded as follow-up work"),
 ("23-Third-Party-Libraries/PostEffects-Yebis-PPFX/yebis-ppfx-source-map.md", "PPFX post-effect library", 1600,
  left(1, "OPUS re-statused the script VM interpreter page (56a49cc8c) DOCUMENTED") + same("members/select_ppfx.py", 1)),
 (GF, "NativeLeaf.DocumentedGlobalAccessor", 230, left(1, TR)
  + ", and the selector binds one frontier leaf again: the page citing its target exactly, the field runtime pass, is"
    " DOCUMENTED again (56a49cc8c) after the REOPENED spell that dropped it on 2026-09-29; the count guard stays 230;"
    " the members file is the selector's output"),
 (GF, "NativeAdapter.ExplainedCalleeForwarder", 488,
  left(3, "OPUS re-statused the gambit evaluation page (95cf8c42f), the field runtime pass (56a49cc8c) and the authored"
          " reference lifetime page (dd651efd2) DOCUMENTED")
  + "; the derived selector, run last on a clean HEAD export, drops exactly these three and admits two frontier adapters"
    " whose single callee became A in the same re-statuses (the FCP block and the table registry, d526b865b); the"
    " members file is the selector's output"),
 (GF, "NativeAdapter.CallResultTailCall", 62, left(1, INV)
  + "; exact A removal, which select_frontier_form_clusters.py re-run on the repaired export reproduces"),
 (GF, "NativeAdapter.CallThenReturnZero", 18, left(1, INV) + "; exact A removal (no selector writes this file)"),
 (GF, "NativeLeaf.StaticHandleReplaceWithPreRelease", 11, left(1, TR) + "; exact A removal (no selector writes this file)"),
 (GF, "NativeAdapter.DoubleCallResultTailCallSavedThis", 4, left(1, TR)
  + "; exact A removal, which select_frontier_form_clusters_3.py re-run on the repaired export reproduces"),
 ("24-Compiler-And-CRT-Runtime/Static-Initialization-And-Teardown/static-initialisers-and-teardowns.md",
  "xc-registered static-object teardowns", 107,
  left(1, "OPUS re-statused the authored reference lifetime page (dd651efd2) DOCUMENTED")
  + "; exact A removal - the named selector rewrites every XC-array cluster file and is not re-run for one removal"),
]
for rel, name, new, s in ROWS:
    path = os.path.join(DB, rel)
    L = io.open(path, encoding="utf-8", newline="").read().split("\n")
    h = [i for i, l in enumerate(L) if l.startswith('  - "' + name + " | ")]
    assert len(h) == 1, (name, h)
    l = L[h[0]]
    cr = l.endswith("\r")
    l = l.rstrip("\r")
    if TAG in l:
        l = l[:l.index(TAG)].rstrip() + '"'
    p = l.split(" | ")
    assert p[3].strip().isdigit(), (name, p[3])
    old = int(p[3])
    mf = os.path.join(os.path.dirname(path), p[2].strip().replace("/", os.sep))
    n = 0
    first = True
    for ml in io.open(mf, encoding="utf-8", errors="replace"):
        ml = ml.split("#", 1)[0].strip()
        if not ml:
            continue
        tok = ml.split()[0].replace("0x", "")
        if first:
            first = False
            if not re.fullmatch(r"[0-9A-Fa-f]{6,8}", tok):
                continue
        n += 1
    assert n == new, (name, "members file holds", n, "want", new)
    assert not re.search(r"\b[0-9A-Fa-f]{8}\b", s), (name, "hex word in note")
    p[3] = str(new)
    l = " | ".join(p)
    assert l.endswith('"')
    body = l[:-1].rstrip()
    sep = "" if body.endswith(".") else "."
    L[h[0]] = body + sep + TAG + s + REC + '"' + ("\r" if cr else "")
    io.open(path, "w", encoding="utf-8", newline="").write("\n".join(L))
    print("edited", rel, "::", name, old, "->", new)
