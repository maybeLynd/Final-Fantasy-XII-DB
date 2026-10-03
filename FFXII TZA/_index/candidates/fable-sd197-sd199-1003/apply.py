"""apply.py [--apply] - publish FABLE's verified answers: SD-197 ANSWERED and SD-199 NARROWED in the register, the
kind-0x54 page's status line updated, and the answer section inserted before the page's crossing section.
Anchored, all-or-nothing, refuses dirty files, keeps line endings. Prints FAILS N last."""
import io, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
OQ = os.path.join(DB, "_index", "OPEN-QUESTIONS.md")
PG = os.path.join(DB, "17-Presentation-Rendering", "Effect-File-Formats", "effect-mesh-records-kind-54.md")
REC = "[`fable-sd197-sd199-1003`](candidates/fable-sd197-sd199-1003/README.md)"
SD197 = ("**ANSWERED 2026-10-03 (FABLE; cloud draft verified at the bytes, record " + REC + ", `check_sd197.py` FAILS 0):** "
         "the three addresses are layers of ONE evaluator for a 16-byte record, not three track kinds: per channel a "
         "count of 0 gives 0.0, 1 gives the key's value, 2+ evaluates `{int32 frame, float32 value}` keys (selector 0 "
         "linear, selector 1 with 3+ keys a uniform quadratic B-spline through the inter-key midpoints, 2-3 give 0.0; "
         "time wraps when t > period); `004307C0` combines the two channels by mode 0-5 with the render-local draw "
         "`003D8E50`. Executed bit-exact against a float32 model on 6,000 records. Shipped: the 152 type-`0x05` mode-2 "
         "slots are 21 constant 0.0, 102 single constants, 10 two-constant combinations and 19 keyed curves, no loop, "
         "values within -2.875..2.4. Outside the row: the time unit, and the 12 channel-1 slots' random draws (bounded, "
         "not fixed). (was OPEN 2026-10-03, registered by FABLE) |")
SD199 = ("**ANSWERED 2026-10-03 (FABLE; cloud draft verified at the bytes, records " + REC + " and "
         "[`fable-sd199-remainder-1003`](candidates/fable-sd199-remainder-1003/README.md), `check_sd199.py` and "
         "`check_sd199b.py` FAILS 0, executed under Unicorn), static:** beyond the path, bit 3 picks the vertex transform "
         "(`0039A150` set, `00399B80` clear). Both apply one per-vertex window/depth test (X,Y in [0,0xFFF0], Z in "
         "[0xFF,0xFFFFFF], compared at `0039A0C6`/`0039A6C8`): with the bit clear one failing vertex drops the whole element; "
         "with it set the failing vertex becomes a zero entry (`0039A6CD`) and `00437130`/`00444340` drop only the "
         "primitives using it as a corner. The inline path `00435699`-`00436CFB` never drops a corner and rescales the pass "
         "pair `param+0x50+8p` by 1/1.15 and x1.15, an additive texture-coordinate offset that changes the image (57 "
         "shipped inline slots). Outside the row: how often shipped effects put vertices out of range (live data). "
         "(was OPEN 2026-10-03, registered by FABLE) |")
K_OLD = ("SD-197 the planar scalars authored as resource or curve tracks (static), SD-198 the runtime pass index after a "
         "failed texture lookup (runtime), SD-199 what +0x1F1 bit 3 changes in the drawing beyond selecting the path "
         "(static)")
K_NEW = ("SD-197 answered 2026-10-03 (FABLE, fable-sd197-sd199-1003: one keyed-curve evaluator; 19 shipped keyed curves, "
         "values -2.875..2.4), SD-198 the runtime pass index after a failed texture lookup (runtime), SD-199 "
         "answered 2026-10-03 (FABLE, fable-sd199-remainder-1003: one per-vertex window/depth test; bit 3 clear drops "
         "the element, set drops only the primitives on a failing vertex)")
CROSS = "## Cross-subsystem neighbours"
SEC = io.open(os.path.join(HERE, "page_section.txt"), encoding="utf-8").read().rstrip("\n")

fails, out = 0, []
for p in (OQ, PG):
    if subprocess.run(["git", "diff", "--quiet", "--", p], cwd=HERE).returncode != 0:
        print("REFUSED: %s has uncommitted changes" % os.path.basename(p)); fails += 1
if not fails:
    raw = io.open(OQ, encoding="utf-8", newline="").read(); nl = "\r\n" if "\r\n" in raw else "\n"
    t = raw.replace("\r\n", "\n")
    for rid, new in (("SD-197", SD197), ("SD-199", SD199)):
        m = re.search(r"^(\| %s \|[^\n]*?\| )(\*\*OPEN 2026-10-03 \(registered by FABLE[^\n]*\|)$" % rid, t, re.M)
        if new.split(" (was OPEN")[0] in t:
            continue
        if not m:
            print("MISS register %s" % rid); fails += 1; continue
        t = t[:m.start(2)] + new + t[m.end(2):]
    out.append((OQ, t.replace("\n", nl), raw))
    raw = io.open(PG, encoding="utf-8", newline="").read(); nl = "\r\n" if "\r\n" in raw else "\n"
    t = raw.replace("\r\n", "\n")
    if SEC.split("\n")[0] not in t:
        if t.count(K_OLD) != 1 or t.count(CROSS) != 1:
            print("MISS page (status %d, cross %d)" % (t.count(K_OLD), t.count(CROSS))); fails += 1
        else:
            t = t.replace(K_OLD, K_NEW).replace(CROSS, SEC + "\n\n" + CROSS)
    out.append((PG, t.replace("\n", nl), raw))
if not fails and "--apply" in sys.argv:
    for p, t, raw in out:
        if t != raw:
            io.open(p, "w", encoding="utf-8", newline="").write(t); print("PATCHED %s" % os.path.basename(p))
elif not fails:
    print("WOULD PATCH %d" % sum(1 for p, t, raw in out if t != raw))
print("FAILS %d" % fails)
