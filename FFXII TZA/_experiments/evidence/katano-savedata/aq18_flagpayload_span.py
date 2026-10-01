"""AQ-18 answered from SHIPPED DATA: is PersistentFlagPayload +0xCF6 ever non-zero?

Read-only over FFXII_TZA.vbf (set FF12_VBF), the same sixteen
ps2data/image/ff12/katano/ff12savedataNN.sav files census.py walks.

WHY THIS EXISTS.  `PersistentFlagPayload +0xCF6` (778 bytes) had been routed to a live read
as ASTRA-QUEUE AQ-18, to see whether the region is ever non-zero.
`ASTRA-CONTRA-OPUS-AQ18-AQ19-NEGATIVE-INFERENCE` made two points and both stand:

  * an all-zero SAMPLE cannot establish "dead / reserved / padding", because a zero is also
    what meaningful storage holding its default looks like - so the live run was being asked
    for an inference no sample can support;
  * the bytes might already be available offline.

They are.  The save-image page establishes payload +0x1044 = image +0x1244, so
image = payload + 0x200 and the span is image 0xEF6..0x1200.

WHAT A RESULT HERE SETTLES, fixed before running it:
  * Sampled non-zero content in ANY save would show the region CARRIES CONTENT in shipped
    data.  It would NOT identify a writer and would NOT establish what the bytes mean.
  * All-zero across sixteen does NOT prove nothing ever writes it.  It is sixteen
    independent saved sessions instead of one sampled moment, which is a better negative
    and a free one - and it means a live read would be a SEVENTEENTH SAMPLE OF THE SAME
    KIND, discriminating nothing.  That is why AQ-18 was withdrawn rather than narrowed.

THE CONTROLS ARE ENFORCED, NOT PRINTED - corrected 2026-09-20 after
`ASTRA-CONTRA-OPUS-AQ18-ZERO-CASE-VERDICT`, which was right.  The first version of this
script PRINTED its population and control figures and then emitted its verdict regardless:
fed an empty index it reported "expected 16, observed 0", "distinct area ids 0", "0 of 0",
printed the negative verdict and exited 0.  A negative verdict earned by a run that read
nothing is the green-gate-that-measured-nothing shape, and a control that is printed but
not acted on is not a control.  This version REFUSES:

  * fewer than the expected 16 save files                -> exit 2, no verdict
  * any file too short to contain the span or the control -> exit 2, no verdict
  * fewer than 2 distinct control values                  -> exit 2, no verdict

so a zero, truncated or unrepresentative population cannot produce a negative result.

OPUS, 2026-09-20.
"""
import io
import os
import sys
import zlib

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "../../../../Tools/analysis-kit/gfz-scripts"))
from census_format_magics import load_index                       # noqa: E402

BLOCK = 0x10000
PAY_TO_IMG = 0x200
SPAN_PAY, SPAN_LEN = 0xCF6, 778
CTRL_PAY, CTRL_LEN = 0x1044, 4
EXPECTED_FILES = 16
MIN_DISTINCT_CONTROLS = 2


def refuse(why):
    sys.stderr.write("AQ-18 CONTROL FAILED, NO VERDICT ISSUED: %s\n" % why)
    raise SystemExit(2)


f = io.open(os.environ["FF12_VBF"], "rb")
names, blocks = load_index(f)


def read_all(path):
    sb, size, off = names[path]
    n = (size + BLOCK - 1) // BLOCK
    out = b""
    f.seek(off)
    for i in range(n):
        csize = blocks[sb + i] or BLOCK
        expected = BLOCK if i < n - 1 else size - BLOCK * (n - 1)
        chunk = f.read(csize)
        if csize != expected:
            chunk = zlib.decompress(chunk)
        out += chunk
    return out[:size]


lo, hi = SPAN_PAY + PAY_TO_IMG, SPAN_PAY + PAY_TO_IMG + SPAN_LEN
ctrl_lo, ctrl_hi = CTRL_PAY + PAY_TO_IMG, CTRL_PAY + PAY_TO_IMG + CTRL_LEN
cands = sorted(p for p in names if "katano" in p and p.endswith(".sav"))

print("population: %d .sav entries under katano (required %d)" % (len(cands), EXPECTED_FILES))
if len(cands) != EXPECTED_FILES:
    refuse("population is %d, not %d - the index is empty, filtered or has moved"
           % (len(cands), EXPECTED_FILES))

print("span: payload 0x%X..0x%X -> image 0x%X..0x%X (%d bytes)\n"
      % (SPAN_PAY, SPAN_PAY + SPAN_LEN, lo, hi, SPAN_LEN))

seen_ctrl, any_nonzero, rows = set(), 0, []
for p in cands:
    d = read_all(p)
    if len(d) < max(hi, ctrl_hi):
        refuse("%s is %d bytes, short of the span end 0x%X - a truncated read cannot "
               "support a negative" % (os.path.basename(p), len(d), hi))
    span = d[lo:hi]
    nz = sum(1 for b in span if b)
    ctrl = d[ctrl_lo:ctrl_hi]
    seen_ctrl.add(ctrl)
    any_nonzero += 1 if nz else 0
    rows.append((os.path.basename(p), len(d), nz, ctrl.hex()))
    print("%-22s size %6d  nonzero %4d  control(area id) %s" % rows[-1])

print("\ncontrol: distinct area ids seen: %d (required >= %d)"
      % (len(seen_ctrl), MIN_DISTINCT_CONTROLS))
if len(seen_ctrl) < MIN_DISTINCT_CONTROLS:
    refuse("only %d distinct control value(s) - a constant area id means the read is not "
           "landing in decoded per-file data" % len(seen_ctrl))

print("files with ANY nonzero byte in the span: %d of %d" % (any_nonzero, len(cands)))
if any_nonzero:
    print("VERDICT: the span CARRIES SAMPLED NON-ZERO CONTENT in shipped saves. This shows "
          "content is present; it does NOT identify a writer and does NOT establish what "
          "the bytes mean.")
else:
    print("VERDICT: zero in every sampled save - which does NOT prove that nothing ever "
          "writes it, and is not treated as closing the question.")
