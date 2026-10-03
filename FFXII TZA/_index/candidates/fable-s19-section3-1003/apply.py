"""apply.py [--apply] - FABLE's correction of CONTRACT-separation-pass.md section 3 (MovementBody fields) on
OPUS-REQ-FABLE-S19-SEPARATION-CONTRACT-1003, with the two stale restatements on FABLE's pool page (2026-10-03).

Anchored strike-and-replace: every OLD string must occur exactly once in its page, and every struck span quotes
text the page says at HEAD. The script refuses a page whose content differs from HEAD (a line-ending-only
difference is fine), keeps each page's line endings, and is idempotent (an edit whose NEW text is present is
reported ALREADY). Dry-run unless --apply. Prints FAILS N last.
"""
import io
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
CONTRACT = "06-Movement-And-Navigation/CONTRACT-separation-pass.md"
POOL = "06-Movement-And-Navigation/the-movement-body-pool-and-the-separation-pass.md"
REQ = "OPUS-REQ-FABLE-S19-SEPARATION-CONTRACT-1003"
# inside the contract's code block a link would not render, so the record is named by its path
TAG_FENCE = "*(corrected 2026-10-03, FABLE, on %s; record _index/candidates/fable-s19-section3-1003/README.md)*" % REQ
TAG_PROSE = ("*(corrected 2026-10-03, FABLE, on %s; record "
             "[fable-s19-section3-1003](../_index/candidates/fable-s19-section3-1003/README.md))*" % REQ)
IND = " " * 17   # continuation lines line up under the field text

EDITS = [
    # ---- the contract, section 3 (the code block of MovementBody fields)
    (CONTRACT, "point 3: +0x08 is f32",
     "  +0x08   ?      weight\n",
     "  +0x08   ~~?~~ f32  weight: read as f32 for both bodies (00315017, 0031502A); 00314E10 forms A's share "
     "from the two (00314E16-00314E27)  " + TAG_FENCE + "\n"),
    (CONTRACT, "point 2: +0xE8 is the partner's increment",
     "  +0xE8   f32    squared push length\n",
     "  +0xE8   f32    ~~squared push length~~ squared length of the increment the latest push-mode contact gave "
     "the OTHER body\n"
     + IND + "(00315303 stores B's from A's increment, 0031533F A's from B's); overwritten per contact, not "
     "accumulated;\n"
     + IND + "the one reader found is 002E5380, which tests it against 0 (002E53B4)  " + TAG_FENCE + "\n"),
    (CONTRACT, "point 5: +0xEE marks the body that took the whole push",
     "  +0xEE   u8     immovable-contact marker\n",
     "  +0xEE   u8     ~~immovable-contact marker~~ sole-share marker: 1 on the body that took the whole push of a "
     "push-mode contact\n"
     + IND + "(B at 00315263 when w = 0, A at 00315287 when w = 1), 0 on both when they share it (003152A4, "
     "003152AB),\n"
     + IND + "left as it was on the partner that took none; read by 002E5380 (002E53C6), which sets +0xEF when "
     "+0xEC is set,\n"
     + IND + "+0xE8 is 0 and this byte is non-zero (002E53CF)  " + TAG_FENCE + "\n"),
    (CONTRACT, "point 4: +0x104 is push y, the middle component",
     "  +0x100  f32    accumulated push x     +0x104  f32  (third component)     +0x108  f32  push z\n",
     "  +0x100  f32    accumulated push x     +0x104  f32  ~~(third component)~~ push y     +0x108  f32  push z\n"
     + IND + "+0x104 is written only as the high half of the qword zero with +0x100 (the clear, 003DA9F2, and at "
     "allocation),\n"
     + IND + "so it is always 0; the pass's six bodies never touch it alone; 002E5380 reads it alone, as f32, and "
     "adds it to\n"
     + IND + "the delta's middle float (002E53F1-002E53FF), between x (002E53DF) and z (002E5405)  "
     + TAG_FENCE + "\n"),
    (CONTRACT, "point 1: +0x120 is a u32 cell set",
     "  +0x120  u128   the cells this body registered in\n",
     "  +0x120  ~~u128~~ u32    the cells this body registered in, one bit per 16-byte mask at 02B57CE0: read as a "
     "dword by\n"
     + IND + "registration (003DB078, one mask per bit) and by the walk (003DACAF); the cell routine called at "
     "003DB020+0x48\n"
     + IND + "writes the 16 bytes from +0x120: +0x124 a dword nothing found reads, +0x128 / +0x12C two f32 the walk "
     "hands to\n"
     + IND + "the visit (003DACC8, 003DACBD)  " + TAG_FENCE + "\n"),
    # ---- FABLE's pool page: the two places that restate the old +0xE8 / +0xEE readings
    (POOL, "pool 2.7: the 0 / 1 arms mark the body that takes the push",
     "0 or 1 marks one body immovable\n",
     "0 or 1 ~~marks one body immovable~~ gives one body the whole separation and sets that body's `+0xEE` "
     "(`00315263` marks B when `w` = 0, `00315287` marks A when `w` = 1), not the body that stays " + TAG_PROSE + "\n"),
    (POOL, "pool 2.7: +0xE8 is the other body's increment",
     "with `+0xE8` the squared length and `+0xEC` set\n",
     "with `+0xE8` ~~the squared length~~ the squared length of the increment just given to the OTHER body, "
     "overwritten per contact (`00315303` stores B's from A's increment, `0031533F` A's from B's) " + TAG_PROSE
     + " and `+0xEC` set\n"),
    (POOL, "pool 4 layout: +0xE8 name",
     "  +0x0E0 f32 height  +0x0E4 f32 baseOffset  +0x0E8 f32 pushLengthSq\n",
     "  +0x0E0 f32 height  +0x0E4 f32 baseOffset  +0x0E8 f32 ~~pushLengthSq~~ partnerPushSqLength (00315303, "
     "0031533F)  " + TAG_FENCE + "\n"),
]


def head_text(rel):
    r = subprocess.run(["git", "show", "HEAD:./" + rel], cwd=DB, capture_output=True)
    if r.returncode != 0:
        return None
    return r.stdout.decode("utf-8").replace("\r\n", "\n")


def main():
    write = "--apply" in sys.argv
    fails = 0
    pages = []
    for rel, _n, _o, _w in EDITS:
        if rel not in pages:
            pages.append(rel)
    for rel in pages:
        path = os.path.join(DB, rel)
        raw = io.open(path, encoding="utf-8", newline="").read()
        crlf = raw.count("\r\n")
        eol = "\r\n" if crlf and crlf * 2 >= raw.count("\n") else "\n"
        text = raw.replace("\r\n", "\n")
        head = head_text(rel)
        if head is None:
            print("REFUSED %s: not at HEAD" % rel)
            fails += 1
            continue
        pending = [e for e in EDITS if e[0] == rel]
        # a page may differ from HEAD only by this script's own edits (re-run) or by line endings
        undone = text
        for _r, _n, old, new in pending:
            if new in undone:
                undone = undone.replace(new, old)
        if undone != head:
            print("REFUSED %s: content differs from HEAD beyond this script's edits (a peer's change?)" % rel)
            fails += 1
            continue
        print("page %s: eol %s, clean against HEAD" % (rel, "CRLF" if eol == "\r\n" else "LF"))
        out = text
        changed = 0
        for _r, name, old, new in pending:
            if new in out:
                print("  ALREADY  %s" % name)
                continue
            n = out.count(old)
            if n != 1:
                print("  MISS     %s (anchor found %d times)" % (name, n))
                fails += 1
                continue
            out = out.replace(old, new)
            changed += 1
            print("  %s %s" % ("PATCHED " if write else "WOULD   ", name))
            for ln in old.rstrip("\n").split("\n"):
                print("      - " + ln)
            for ln in new.rstrip("\n").split("\n"):
                print("      + " + ln)
        if write and changed and not fails:
            io.open(path, "w", encoding="utf-8", newline="").write(out.replace("\n", eol))
    print("edits %d, pages %d, mode %s" % (len(EDITS), len(pages), "apply" if write else "dry-run"))
    print("FAILS %d" % fails)
    return fails


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
