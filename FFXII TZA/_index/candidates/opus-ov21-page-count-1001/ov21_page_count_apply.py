"""ov21_page_count_apply.py [--apply] - consume ASTRA's two OV-21 packets into the RenderResourceEntryBank rows
(OPUS, 2026-10-01; every cited instruction re-read at the bytes, control ov21_page_count_check.py).

1. ov21-page-selection-invariant: the descriptor's +0x018 is two DWORD page-list endpoints, head +0x018 and tail
   +0x01C, not an unread u8[8]. The +0x022 row's "0051F7A0 returns at once when it is <= 0" is wrong: the selector goes
   to the acquisition 0051F6B0 (jle 0051F825, call at 0051F828).
2. ov21-count-publication-window: the acquire raises the page count before the bank total and the release lowers the
   page before the total, so the two agree only between operations.

The row split keeps each line's EOL; the other edits replace or append inside one cell. Idempotent (tags); refuses
tabs, newlines or pipes in new text; dry run unless --apply; FAILS n.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
F = os.path.normpath(os.path.join(HERE, "..", "..", "..", "_types", "fields.tsv"))
T = "RenderResourceEntryBank"
SPLIT_TAG = "SPLIT 2026-10-01 (OPUS, consuming ASTRA's ov21-page-selection-invariant"
HEAD_MEANING = ("head of the active page list: the page index the selector 0051F7A0 starts its walk from (0051F7E9; -1 "
                "means no active page, which sends it to the acquisition at 0051F825). The append 0051F6B0 sets it "
                "when the list is empty (0051F743 / 0051F749) and the unlink 0051F880 moves it (0051F930 / 0051F938). "
                "The initialiser (0051FA19) and the reset (0051FB72) set it and +0x01C to -1 with one qword store. "
                + SPLIT_TAG + ", re-read at the bytes): the old single row - minusOneSlot018, u8[8], read on no path, "
                "two dwords or one qword not determined - is withdrawn; the eight bytes are two DWORD list endpoints.")
TAIL_MEANING = ("tail of the active page list: the append 0051F6B0 reads it (0051F74C) to link the new page after it and "
                "stores the new page (0051F782); the unlink 0051F880 moves it (0051F93B / 0051F943). Set to -1 together "
                "with +0x018 by the initialiser's and the reset's qword store. " + SPLIT_TAG + ", re-read at the "
                "bytes).")
OLD22 = "0051F7A0 returns at once when it is <= 0"
NEW22 = ("0051F7A0 goes straight to the acquisition when it is <= 0 (signed jle 0051F825, call 0051F6B0 at 0051F828; "
         "CORRECTED 2026-10-01, OPUS, on ASTRA's ov21-page-selection-invariant - it read 'returns at once'; no claim "
         "that a negative count is reachable)")
PHASE_TAG = "PHASE 2026-10-01 (OPUS, on ASTRA's ov21-count-publication-window"
PHASE = (" " + PHASE_TAG + ", re-read at the bytes): the acquire 0051FBB0 raises the page's count (0051FC71) before this "
         "total (0051FCB2), and the release 0051FCF0 lowers the page (0051FD5E) before the total (0051FE0C). So the sum "
         "of the page counts equals this total only between operations, and an observer must name the phase. The "
         "direct calls between the writes (003AB7F0 and its 0036B130, 0020E620, the unlink 0051F880) make no callback "
         "or indirect call. Thread ownership, interference and atomicity are not established. ASTRA's conditional "
         "lemma (a coherent ten-page bank below 320 always yields a slot) is a conditional proof, not an all-writer "
         "invariant.")


def cells_of(line):
    return line.rstrip(b"\r\n").decode("utf-8").split("\t")


def main():
    apply = "--apply" in sys.argv
    raw = open(F, "rb").read()
    lines = raw.splitlines(keepends=True)
    fails = 0
    for txt in (HEAD_MEANING, TAIL_MEANING, NEW22, PHASE):
        if any(c in txt for c in "\t\n|"):
            print("REFUSING: tab, newline or pipe in new text"); print("FAILS 1"); return 1

    def find(off):
        return [i for i, l in enumerate(lines) if cells_of(l)[:2] == [T, off]]

    # 1. split +0x018
    h18 = find("0x018")
    if len(h18) == 1 and SPLIT_TAG in cells_of(lines[h18[0]])[5]:
        print("ALREADY split")
    elif len(h18) != 1:
        print("REFUSING +0x018 rows", len(h18)); fails += 1
    else:
        i = h18[0]
        c = cells_of(lines[i])
        if c[2:5] != ["8", "minusOneSlot018", "u8[8]"]:
            print("REFUSING +0x018 is not the old row", c[2:5]); fails += 1
        else:
            eol = lines[i][len(lines[i].rstrip(b"\r\n")):]
            ev = c[8] if len(c) > 8 else ""
            a = [T, "0x018", "4", "pageHead", "int32", HEAD_MEANING, "SEMANTICALLY IDENTIFIED", "PROVEN", ev] + c[9:]
            b = [T, "0x01C", "4", "pageTail", "int32", TAIL_MEANING, "SEMANTICALLY IDENTIFIED", "PROVEN", ev] + c[9:]
            lines[i:i + 1] = ["\t".join(a).encode("utf-8") + eol, "\t".join(b).encode("utf-8") + eol]
            print(("PATCHED " if apply else "WOULD PATCH ") + "split +0x018 into +0x018 / +0x01C")
    # 2. +0x022 wording
    h22 = find("0x022")
    if len(h22) != 1:
        print("REFUSING +0x022 rows", len(h22)); fails += 1
    else:
        i = h22[0]
        c = cells_of(lines[i])
        eol = lines[i][len(lines[i].rstrip(b"\r\n")):]
        if NEW22 in c[5]:
            print("ALREADY +0x022")
        elif c[5].count(OLD22) != 1:
            print("REFUSING +0x022 text"); fails += 1
        else:
            c[5] = c[5].replace(OLD22, NEW22)
            lines[i] = "\t".join(c).encode("utf-8") + eol
            print(("PATCHED " if apply else "WOULD PATCH ") + "+0x022")
    # 3. +0x058 phase
    h58 = find("0x058")
    if len(h58) != 1:
        print("REFUSING +0x058 rows", len(h58)); fails += 1
    else:
        i = h58[0]
        c = cells_of(lines[i])
        eol = lines[i][len(lines[i].rstrip(b"\r\n")):]
        if PHASE_TAG in c[5]:
            print("ALREADY +0x058")
        else:
            c[5] = c[5] + PHASE
            lines[i] = "\t".join(c).encode("utf-8") + eol
            print(("PATCHED " if apply else "WOULD PATCH ") + "+0x058")
    if apply and not fails:
        open(F, "wb").write(b"".join(lines))
    print("FAILS", fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
