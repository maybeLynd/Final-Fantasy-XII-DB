"""apply.py [--apply] - add the TABLE row for 002994BC to text-gap-citations-250.tsv, right after 002994A0's row
(FABLE 2026-10-02, OPUS-NOTICE-FABLE-TEXTGAP-002994BC-1002). Refuses if the row already exists or the anchor row is
missing. Run from the repository root or anywhere: the path is resolved from this file."""
import io, os, sys
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "text-gap-citations-250.tsv")
ROW = "\t".join([
    "002994BC", "00299090", "FUN_00299090", "002994BC", "0", "002994E0", "yes", "00 01 06 06 06 02 06 06", "TABLE",
    "00299090's byte index table: 002990AC bounds dword [rdx] - 1 at 0x1C, 002990BE reads [image base + rax + 0x1794bc] "
    "(29 bytes, values 0..6) to pick one of the 7 offsets at 002994A0, whose entries end at 002994BC (FABLE 2026-10-02 on "
    "OPUS-NOTICE-FABLE-TEXTGAP-002994BC-1002, cited by its interior row)",
    "99-Unresolved-Residual/Glyph-Run-Rendering/the-text-element-dispatch-table.md"])
t = io.open(P, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in t else "\n"
lines = t.split(nl)
if any(l.startswith("002994BC\t") for l in lines):
    print("row exists"); print("FAILS 1"); sys.exit(1)
i = [k for k, l in enumerate(lines) if l.startswith("002994A0\t")]
if len(i) != 1:
    print("anchor row 002994A0 not found once"); print("FAILS 1"); sys.exit(1)
lines.insert(i[0] + 1, ROW)
if "--apply" in sys.argv:
    io.open(P, "w", encoding="utf-8", newline="").write(nl.join(lines)); print("APPLIED")
else:
    print("DRY: would insert after line", i[0] + 1)
print("FAILS 0")
