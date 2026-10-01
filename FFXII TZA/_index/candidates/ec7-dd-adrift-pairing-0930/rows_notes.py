"""rows_notes.py DB BATCH - set the count and append the dated A-drift sentence on each row of BATCH (A or B).
Idempotent (a row already carrying TAG is rewritten from before TAG). Keeps line endings. No addresses in the notes:
the removed addresses and their causing pages are in the record (a hex word in a row note is read as a citation)."""
import io, os, re, sys

DB, BATCH = sys.argv[1], sys.argv[2]
TAG = " 2026-09-30 (SWE2-EC7, DD re-status A-drift, record _index/candidates/ec7-dd-adrift-pairing-0930):"
REC = "; addresses and causing pages in the record."
SAME = "; the selector re-run on a clean HEAD export drops exactly these and admits nothing; the members file is the selector's output"


def left(n, why):
    return " %d member(s) left the family, since measured as A (A beats a declaration) after %s" % (n, why)


ROWS = {
 "A": [
  ("01-Script-VM-Native-Bridge/Verb-Dispatch/the-shape-of-the-verb-population.md", "ScriptVM.VerbAdapter", 1037, 1035,
   left(2, "OPUS re-statused the version-stamps page (8c8406bfd) and the source-block mover page (9bda44687) DOCUMENTED")
   + "; select_verb_adapters.py re-run on a clean HEAD export drops exactly these two, admits nothing and leaves the leftovers file's membership unchanged" + REC),
  ("18-Audio/sead-function-identification.md", "SQEX SEAD sound library span", 1136, 1130,
   left(6, "OPUS re-statused the two SEAD audio architecture pages (d39c8ccbd, 4) and the EASTL strings page (8c8406bfd, 2) DOCUMENTED")
   + "; select_audio_libraries.py re-run on a clean HEAD export drops exactly these six, admits nothing and leaves its five other library files unchanged; the members file is the selector's output" + REC),
  ("24-Compiler-And-CRT-Runtime/Generated-Families/generated-function-families.md", "NativeAdapter.ExplainedCalleeForwarder", 481, 482,
   left(1, "OPUS re-statused the EASTL strings page (8c8406bfd) DOCUMENTED")
   + "; the selector re-run on a clean HEAD export drops exactly it and admits two frontier adapters, both released by the Phyre PAnimation row's exclusive-closure cascade after the same day's re-status of the animation channel binding page (that row's repair drops them); the members file is the selector's output" + REC),
  ("24-Compiler-And-CRT-Runtime/Generated-Families/generated-function-families.md", "NativeAdapter.CallResultTailCall", 62, 61,
   left(1, "OPUS re-statused what-each-script-verb-touches.md (2db6cdb59) DOCUMENTED") + "; exact A removal (a form family, no selector)" + REC),
  ("24-Compiler-And-CRT-Runtime/Static-Initialization-And-Teardown/static-initialisers-and-teardowns.md", "counter-append static-table initialisers", 19, 18,
   left(1, "OPUS re-statused the animation channel binding page (46c98f222) DOCUMENTED")
   + "; exact A removal - the named selector rewrites every XC-array cluster file and is not re-run for one removal" + REC),
 ],
 "B": [
  ("23-Third-Party-Libraries/PostEffects-Yebis-PPFX/yebis-ppfx-source-map.md", "PPFX post-effect library", 1609, 1601,
   left(8, "OPUS re-statused the MSVC ordered-container page (3dac81ee9) DOCUMENTED") + SAME + REC),
  ("22-Middleware-PhyreEngine/Subsystem-Map/the-fifteen-modules-registered-before-main.md", "Phyre PAnimation module", 202, 119,
   left(8, "OPUS re-statused the animation channel binding page (46c98f222) DOCUMENTED")
   + ", and 75 more left as the exclusive-closure cascade of those departures (their inbound references now include the A bodies, which are not members); re-running ../members/select_phyre_panimation.py drops exactly these 83 and admits nothing. Control: with only the 8 departed bodies held non-A the selector reproduces the pre-re-status 202-member file exactly, so every departure is the A promotion or its cascade; 2 of the 75 are now declared by NativeAdapter.ExplainedCalleeForwarder, 73 are frontier" + REC),
  ("22-Middleware-PhyreEngine/Subsystem-Map/the-fifteen-modules-registered-before-main.md", "Phyre PhyreCore module", 430, 427,
   left(3, "OPUS re-statused the animation channel binding page (46c98f222, 2) and how-a-path-is-resolved-to-bytes (30f461a92, 1) DOCUMENTED")
   + "; re-running ../members/select_phyre_module.py PhyreCore drops exactly these three and admits nothing" + REC),
  ("22-Middleware-PhyreEngine/Subsystem-Map/the-fifteen-modules-registered-before-main.md", "Phyre PSerialization module", 21, 19,
   left(2, "OPUS re-statused how-a-path-is-resolved-to-bytes (30f461a92) DOCUMENTED")
   + "; re-running ../members/select_phyre_module.py PSerialization drops exactly these two and admits nothing" + REC),
  ("22-Middleware-PhyreEngine/Subsystem-Map/the-fifteen-modules-registered-before-main.md", "Phyre PPostProcessing module", 156, 134,
   left(4, "OPUS re-statused the reflected render parameters page (d46835689) DOCUMENTED")
   + ", and 18 more left as the exclusive-closure cascade of those departures; re-running ../members/select_phyre_module.py PPostProcessing drops exactly these 22 and admits nothing. Control: with only the 4 departed bodies held non-A the selector reproduces the pre-re-status 156-member file exactly" + REC),
  ("23-Third-Party-Libraries/third-party-middleware-inventory.md", "zlib 1.2.11", 56, 55,
   left(1, "OPUS re-statused the save-image buffers page (e696ef86e) DOCUMENTED") + SAME + REC),
  ("23-Third-Party-Libraries/third-party-middleware-inventory.md", "JsonBox JSON library", 57, 55,
   left(2, "OPUS re-statused the EASTL strings page (8c8406bfd) and the CL2 menu colour tables page (9bda44687) DOCUMENTED")
   + "; exact A removal. select_jsonbox.py does not re-run at HEAD: it excludes rows named 'JsonBox', not this row's name, so it sees every member as declared elsewhere, and with the name matched its closure assertion refuses the two departed bodies, which call members from inside the runs, as unexplained foreign callers - the selector repair is recorded as follow-up work" + REC),
 ],
}
for rel, name, old, new, s in ROWS[BATCH]:
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
    p[3] = str(new)
    l = " | ".join(p)
    assert l.endswith('"')
    body = l[:-1].rstrip()
    sep = "" if body.endswith(".") else "."
    L[h[0]] = body + sep + TAG + s + '"' + ("\r" if cr else "")
    io.open(path, "w", encoding="utf-8", newline="").write("\n".join(L))
    print("edited", rel, "::", name, old, "->", new)
