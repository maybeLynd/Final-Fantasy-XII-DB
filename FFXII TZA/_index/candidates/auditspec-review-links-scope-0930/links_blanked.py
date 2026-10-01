"""links_blanked.py - for the code-span exemptions whose target RESOLVES at HEAD, show which backtick span the
checker's CODE_SPAN blanked, the paragraph's backtick-run structure, and a CommonMark-style pairing (runs of EQUAL
length pair left to right, across the whole paragraph) to decide whether Markdown renders the link as a link."""
import re, subprocess
REPO = r"C:\Users\Kristian\source\repos\XIIOnline"
CODE_SPAN = re.compile(r"`[^`\n]*`")
FENCE = re.compile(r"```.*?```", re.S)
CASES = [("Database/FFXII TZA/06-Movement-And-Navigation/Facing-And-Steering/how-a-character-turns.md", "../../_index/ADDRESS-INDEX.md"),
         ("Database/FFXII TZA/13-Rewards-Progression-Economy/world-loot-pickups-the-ten-slot-pool-and-the-despawn.md", "loot-drops-and-enemy-chain.md"),
         ("Database/FFXII TZA/17-Presentation-Rendering/Graphics-Thread-Handshake/the-shared-command-state-word.md", "../../_index/ADDRESS-INDEX.md")]
import os
# all 13 code-span exemptions from links_live.out (resolving and missing)
CASES = []
for ln in open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "links_live.out"), encoding="utf-8"):
    if ln.startswith("    ") and " -> " in ln and ln.rstrip().endswith((" resolves", " missing")):
        src, rest = ln.strip().split(" -> ", 1)
        CASES.append(("Database/FFXII TZA/" + src, rest.rsplit(" ", 1)[0]))
def cm_spans(par):
    """CommonMark code spans: a backtick run opens; the next run of the SAME length closes; unmatched runs are literal."""
    runs = [(m.start(), m.end()) for m in re.finditer(r"`+", par)]
    spans, i = [], 0
    while i < len(runs):
        s, e = runs[i]; n = e - s
        j = next((k for k in range(i + 1, len(runs)) if runs[k][1] - runs[k][0] == n), None)
        if j is None: i += 1; continue
        spans.append((s, runs[j][1])); i = j + 1
    return spans
for path, tgt in CASES:
    text = FENCE.sub("", subprocess.run(["git", "-C", REPO, "show", "HEAD:" + path], capture_output=True).stdout.decode("utf-8"))
    pars = re.split(r"\n\s*\n", text)
    for par in pars:
        hit = None
        for m in re.finditer(re.escape("(" + tgt + ")"), par):
            k = m.start()
            line_start = par.rfind("\n", 0, k) + 1
            line_end = par.find("\n", k); line_end = len(par) if line_end < 0 else line_end
            line = par[line_start:line_end]
            for c in CODE_SPAN.finditer(line):
                if "](" in c.group(0) and line_start + c.start() <= k < line_start + c.end():
                    hit = (k, line, c.group(0)); break
            if hit: break
        if not hit: continue
        link_pos, line, b = hit
        blanked = [b]
        in_cm = any(s <= link_pos < e for s, e in cm_spans(par))
        print("%s\n  line backticks=%d, paragraph backticks=%d, paragraph lines=%d" % (path.split("/")[-1], line.count("`"), par.count("`"), par.count("\n") + 1))
        print("  checker blanks span: %r" % (blanked[0][:120] if blanked else None))
        print("  CommonMark pairing puts the link inside a code span: %s  -> %s" % (in_cm, "not a link (exemption right)" if in_cm else "REAL LINK blanked"))
        break
