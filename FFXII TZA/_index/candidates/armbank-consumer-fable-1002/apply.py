"""apply.py [--apply] [--root R] - finish the consumer cascade of OPUS's engine-B readiness correction (the console's
tuning bank 02CB7FD0.. IS read: 006084B0 copies it whole into the staged shader constants) on FABLE's own text
(FABLE, 2026-10-02). Runs AFTER opus-engine-b-readiness-fixes-1002 has been applied. Every anchor must match exactly
once; any miss refuses the whole edit. --root: repository root (default: resolved from this file)."""
import io, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = sys.argv[sys.argv.index("--root") + 1] if "--root" in sys.argv else os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", ".."))
D = os.path.join(ROOT, "Database", "FFXII TZA", "00-Engine-Core-Runtime", "Developer-Tuning-Console")
TAG = ("*(corrected 2026-10-02, FABLE, Claude Opus 5.5: `006084B0` takes the base `02CB7FD0`, below every range these "
       "checks covered, and copies the whole block with 16-byte loads into the staged shader constants; the "
       "282-command page's ANSWERED 2026-09-27 maps each slot to a SceneWideParameterConstantBuffer variable)*")
EDITS = {
    "arm-catalogue-slice-B-ids-44-75.md": [
        ("**ANSWERED 2026-09-25 (FABLE, Claude Opus 5.5): hair and eye\n      lighting tuning values that nothing outside the console reads.**",
         "**ANSWERED 2026-09-25 (FABLE, Claude Opus 5.5): hair and eye\n      lighting tuning values ~~that nothing outside the console reads~~ that reach the shaders through the "
         "staged copy of the block.** " + TAG),
        ("        - a register-held base: no `lea` anywhere in `02CB8000`–`02CB8120`;",
         "        - a register-held base: no `lea` anywhere in `02CB8000`–`02CB8120` (true, but the copy's `lea` is of "
         "`02CB7FD0`, just below, and its loads run through the block);"),
    ],
    "arm-catalogue-slice-C-ids-76-107.md": [
        ("      - **Read by nothing but the console.** Over the whole array `02CB80A0`–`02CB812C`, the only accesses are:",
         "      - ~~**Read by nothing but the console.**~~ **Read by the console and by the staged shader-constant "
         "copy.** " + TAG + " Over the whole array `02CB80A0`–`02CB812C`, the only rip-relative accesses are:"),
        ("below it is 4 bytes wide, so no wide load reaches in.",
         "below it is 4 bytes wide~~, so no wide load reaches in~~ - but a register-based wide load does: the copy's "
         "16-byte `movups` loads from `02CB7FD0` cover the whole array."),
    ],
}
RTAG = ("*(corrected 2026-10-02, FABLE, Claude Opus 5.5: 006084B0 takes the base 02CB7FD0, below the ranges checked, "
        "and copies the whole block with 16-byte loads into the staged shader constants; see the 282-command page's "
        "ANSWERED 2026-09-27 and the arm-catalogue slices)*")
REG = [
    ("**ANSWERED 2026-09-25 (FABLE, Claude Opus 5.5): hair and eye lighting tuning values that nothing outside the console reads.**",
     "**ANSWERED 2026-09-25 (FABLE, Claude Opus 5.5): hair and eye lighting tuning values ~~that nothing outside the console reads~~ that reach the shaders through the staged copy of the block.** " + RTAG),
    ("All 36 are named, and nothing outside the console reads any of them.**",
     "All 36 are named, ~~and nothing outside the console reads any of them~~ and the staged shader-constant copy reads all of them.** " + RTAG),
    ("So even the scene-set nine are never read by a renderer: the bank is written and displayed, and nothing consumes it.",
     "~~So even the scene-set nine are never read by a renderer: the bank is written and displayed, and nothing consumes it.~~"),
]
EDITS[os.path.join("..", "..", "_index", "OPEN-QUESTIONS.md")] = REG
fails = 0; out = {}
for name, edits in EDITS.items():
    p = os.path.join(D, name)
    t = io.open(p, encoding="utf-8", newline="").read(); crlf = "\r\n" in t; u = t.replace("\r\n", "\n")
    for old, new in edits:
        n = u.count(old)
        if n != 1:
            print("MISS (%d) %s: %s" % (n, name, old[:70])); fails += 1
        else:
            u = u.replace(old, new)
    out[p] = (u.replace("\n", "\r\n") if crlf else u)
if fails:
    print("FAILS %d" % fails); sys.exit(1)
if "--apply" in sys.argv:
    for p, s in out.items():
        io.open(p, "w", encoding="utf-8", newline="").write(s)
    print("APPLIED 7 edits on 3 files")
else:
    print("DRY: 7 edits on 3 files")
print("FAILS 0")
