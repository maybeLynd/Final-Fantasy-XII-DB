"""apply.py [--apply] - consume FABLE's four filecache zero-view reviews into the path-resolution page (FABLE, 2026-10-02).

The edit text is not repeated here: it is read from the reviewed draft
../fable-review-astra-filecache-close-zero-sentinel-1002/consumption-draft.md (E1-E8), so the published page text is
exactly the reviewed text. E1-E5 are OLD -> NEW fenced pairs; E6 is inserted before "## 6. Route 2"; E7 and E8 are table
rows inserted after named rows. Dry run by default; prints FAILS N last."""
import io, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
PAGE = os.path.join(DB, "02-Resource-And-Asset-Pipeline", "VBF-Archive-And-Authored-Tables", "how-a-path-is-resolved-to-bytes.md")
DRAFT = os.path.join(HERE, "..", "fable-review-astra-filecache-close-zero-sentinel-1002", "consumption-draft.md")

def sections(text):
    out, cur = {}, None
    for line in text.split("\n"):
        m = re.match(r"## (E\d)[. ]", line)
        if m:
            cur = m.group(1); out[cur] = []
        elif line.startswith("## ") or line.startswith("---"):
            cur = None
        elif cur:
            out[cur].append(line)
    return {k: "\n".join(v) for k, v in out.items()}

def fences(block):
    return re.findall(r"```\n(.*?)\n```", block, re.S)

def main():
    write = "--apply" in sys.argv
    d = io.open(DRAFT, encoding="utf-8").read().replace("\r\n", "\n")
    # the draft shows page-relative links as plain text so it lints from its own folder; restore them for the page
    d = re.sub(r"(\[[^\]]*\]) \(page-relative link: `([^`]+)`\)", r"\1(\2)", d)
    S = sections(d)
    t = io.open(PAGE, encoding="utf-8", newline="").read()
    crlf = "\r\n" in t
    t = t.replace("\r\n", "\n")
    edits = []
    for k in ("E1", "E2", "E3", "E4", "E5"):
        f = fences(S[k]); assert len(f) == 2, (k, len(f)); edits.append((k, f[0], f[1]))
    e6 = fences(S["E6"])[0]
    edits.append(("E6", "## 6. Route 2", e6 + "\n\n## 6. Route 2"))
    r7 = fences(S["E7"])[0]
    a7 = [l for l in t.split("\n") if l.startswith("| `0020C440` / `00674A00` |")]
    assert len(a7) == 1; edits.append(("E7", a7[0], a7[0] + "\n" + r7))
    r8 = fences(S["E8"])[0]
    a8 = [l for l in t.split("\n") if l.startswith("| Route 1's key, hash and tree |")]
    assert len(a8) == 1; edits.append(("E8", a8[0], a8[0] + "\n" + r8))
    fails = 0
    for k, old, new in edits:
        if new in t:
            print("ALREADY", k); continue
        if t.count(old) != 1:
            print("MISS %s (%d)" % (k, t.count(old))); fails += 1; continue
        t = t.replace(old, new); print("WOULD PATCH" if not write else "PATCHED", k)
    if write and not fails:
        io.open(PAGE, "w", encoding="utf-8", newline="").write(t.replace("\n", "\r\n") if crlf else t)
    print("FAILS %d" % fails); sys.exit(1 if fails else 0)

main()
