"""apply.py - FABLE, 2026-10-03: stage section 8a (the board grid and the writers of the owned bits) into the S-31 contract.

  python apply.py            dry run: check the anchors, show what would change, write nothing
  python apply.py --apply    write the edit (only when every check passes)

Edit:
  E1  12-Items-Equipment-Shops-License/CONTRACT-license-check.md: insert section.txt after section 8, before the line
      "## 9. Determinism".

Guards:
  - a page with uncommitted content changes (git diff HEAD, or a staged difference) is REFUSED;
  - the anchors "## 8. Script" and "## 9. Determinism" must each occur exactly once, in that order, with nothing
    between them but section 8's body (no other "## " heading);
  - the page's line endings (CRLF or LF) are detected and kept;
  - idempotent: when the section's heading is already present the edit is reported ALREADY and skipped;
  - every relative link in section.txt must resolve from the contract's folder;
  - the census parser contract_named_state_census.state_sections must NOT read 8a as a Types/State section (so the
    types denominator of the S-31 row is unchanged by this insertion), and must read the same state lines before and
    after;
  - section.txt must carry no address that S1 of check_s31.py has not decoded or indexed (a list check against the
    check's own SITES and indexed entries).

Prints FAILS N last.
"""
import io
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
REPO = os.path.abspath(os.path.join(DB, "..", ".."))
KIT = os.path.join(REPO, "Database", "Tools", "analysis-kit", "gfz-scripts")
CONTRACT = os.path.join(DB, "12-Items-Equipment-Shops-License", "CONTRACT-license-check.md")
MARKER = "## 8a. The board grid and the writers of the owned bits"
APPLY = "--apply" in sys.argv
fails = 0


def report(tag, ok, text):
    global fails
    fails += not ok
    print("%s  %s  %s" % ("PASS" if ok else "FAIL", tag, text))


def rel(p):
    return os.path.relpath(p, REPO).replace(os.sep, "/")


def git(*args):
    return subprocess.run(["git", "-C", REPO] + list(args), capture_output=True)


def dirty(p):
    return git("diff", "--quiet", "HEAD", "--", rel(p)).returncode != 0 or \
        git("diff", "--quiet", "--cached", "--", rel(p)).returncode != 0


def load(p):
    raw = io.open(p, "rb").read()
    eol = "\r\n" if b"\r\n" in raw else "\n"
    return raw.decode("utf-8").replace("\r\n", "\n"), eol


print("FABLE S-31 section 8a, %s" % ("APPLY" if APPLY else "dry run (no file is written)"))
print("HEAD %s" % git("rev-parse", "--short", "HEAD").stdout.decode().strip())

cdirty = dirty(CONTRACT)
report("G1", not cdirty, "%s is %s" % (rel(CONTRACT), "DIRTY - refused (uncommitted content changes)" if cdirty else "clean"))
if cdirty:
    src = git("show", "HEAD:" + rel(CONTRACT)).stdout.decode("utf-8").replace("\r\n", "\n")
    _, eol = load(CONTRACT)
    print("      staging against the HEAD blob instead, to check the anchors; nothing can be applied")
else:
    src, eol = load(CONTRACT)
print("      line endings kept: %s" % ("CRLF" if eol == "\r\n" else "LF"))

lines = src.split("\n")
a8 = [i for i, l in enumerate(lines) if re.match(r"^## 8\. Script", l)]
a9 = [i for i, l in enumerate(lines) if re.match(r"^## 9\. Determinism\s*$", l)]
report("A1", len(a8) == 1, "anchor '## 8. Script' occurs %d time(s)%s" % (len(a8), " at line %d" % (a8[0] + 1) if a8 else ""))
report("A2", len(a9) == 1, "anchor '## 9. Determinism' occurs %d time(s)%s" % (len(a9), " at line %d" % (a9[0] + 1) if a9 else ""))
between = [l for l in lines[a8[0] + 1:a9[0]] if l.startswith("## ")] if (len(a8) == 1 and len(a9) == 1) else ["?"]
already = any(l.startswith(MARKER) for l in lines)
report("A3", len(a8) == 1 and len(a9) == 1 and a8[0] < a9[0] and (not between or (already and len(between) == 1)),
       "8 < 9 and nothing but section 8%s lies between them: %s" % (" and 8a" if already else "", between))

block = io.open(os.path.join(HERE, "section.txt"), encoding="utf-8").read().replace("\r\n", "\n").rstrip("\n")
report("H1", block.split("\n")[0].startswith(MARKER) and "FABLE, 2026-10-03" in block.split("\n")[0],
       "section.txt's heading is the marker and carries 'FABLE, 2026-10-03'")
if already:
    staged = src
    print("      E1 ALREADY: the section is present; nothing to do")
else:
    i = a9[0] if a9 else len(lines)
    pre = lines[:i]
    while pre and not pre[-1].strip():
        pre.pop()
    staged = "\n".join(pre + [""] + block.split("\n") + [""] + lines[i:])
    report("E1", staged != src, "8a inserted before line %d (%s)" % (i + 1, lines[i] if i < len(lines) else "EOF"))

# links
folder = os.path.dirname(CONTRACT)
links = re.findall(r"\]\(([^)#\s]+)(?:#[^)]*)?\)", block)
bad = [l for l in links if not l.startswith("http") and not os.path.exists(os.path.normpath(os.path.join(folder, l)))]
report("L1", not bad, "%d relative links in section.txt resolve from the contract's folder%s" % (len(links), "" if not bad else ": %s" % bad))

# census parser: 8a is not a state section, and the state lines are unchanged
sys.path.insert(0, KIT)
import contract_named_state_census as C  # noqa: E402
before = [(s, l) for s, l, f in C.state_sections(src)]
after = [(s, l) for s, l, f in C.state_sections(staged)]
heads = sorted(set(s for s, l in after))
report("C1", not any(h.startswith("8a") for h in heads), "the census does not read 8a as a state section (state sections: %s)" % heads)
report("C2", before == after, "the census's state lines are identical before and after (%d lines)" % len(after))

# every address cited in section.txt was decoded or indexed by check_s31.py
chk = io.open(os.path.join(HERE, "check_s31.py"), encoding="utf-8").read()
cited = sorted(set(re.findall(r"`([0-9A-F]{8})", block)))
known = set("%08X" % int(x, 16) for x in re.findall(r"0x([0-9A-Fa-f]{5,8})\b", chk))
known |= set(re.findall(r'"([0-9A-F]{8})"', chk))
# addresses carried from other pages (cited, not re-derived here) are listed explicitly
CARRIED = {"00236D5C", "00236D67", "00234349", "002399E9", "0023AF56", "00237E26", "00239AC4", "0023A7A9",
           "00323F52", "02EBF198", "01EF91E0", "00323C18", "00323BB0", "00323EC0", "00322C50", "0020E620",
           "00300B80", "0031B860", "00324470", "0030A310", "00308FF0", "00324020", "0030FED0", "002F9082",
           "003846F0", "003845F0", "02EBF038", "02EBF190", "0208E680", "02EBF1A0", "02EBF1F8", "0055DA60"}
missing = [a for a in cited if a not in known and a not in CARRIED]
report("K1", not missing, "%d addresses cited in section.txt; every one is in check_s31.py or listed as carried%s"
       % (len(cited), "" if not missing else ": missing %s" % missing))

if APPLY:
    if fails:
        print("NOT APPLIED: %d check(s) failed" % fails)
    elif staged == src:
        print("      %s unchanged (ALREADY)" % rel(CONTRACT))
    else:
        io.open(CONTRACT, "wb").write(staged.replace("\n", eol).encode("utf-8"))
        back, _ = load(CONTRACT)
        report("W", back == staged, "wrote %s" % rel(CONTRACT))
else:
    print("      dry run: contract +%d lines" % (len(staged.split("\n")) - len(src.split("\n"))))
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)
