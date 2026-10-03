"""apply_ec7corr_b.py [--apply] - SWE2-EC7's corrections of 2026-10-03, set B (Claude stand-in for Devin).

Requests: OPUS-REQ-EC7-00297C10-MATCHED-ROW-1003, FABLE-REQ-EC7-RANDOMNESS-PAGE-COMBINER-1003,
FABLE-REQ-EC7-TRANSFORM-PRIMITIVES-0039A150-1003. Each old text is EC7's own (or, for the 2026-09-17 note, a passage on
the EC7-led page); each edit strikes it and states the reading the bytes support (control: ec7_corr_b_check.py). Same
unique-match rule as OPUS's batch appliers."""
import os
import sys

DB = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
WP = "16-UI/Widget-Object-Model/the-widget-message-protocol.md"
RN = "02-Resource-And-Asset-Pipeline/Authored-Expressions/how-an-authored-number-gets-its-randomness.md"
TP = "00-Engine-Core-Runtime/Shared-Transform-Workbench/the-two-transform-primitives.md"

EDITS = [
    # OPUS - 00297C10: a matched row runs only the tail.
    (WP,
     "`00297C10` (244 B) is the `0209BFBE`-bank lookup `0029A0A0` runs: rows stride `0xC0` from `0209BFBE` to `0209C2BE`, "
     "a row qualifies when its `-0x58`/`+0` flags carry bit `2` and `dword[+0x32] == [rsi+4]`; the hit path pairs "
     "`003F89C0` with `0028F590`, then `003F8A50` with `0028F590`, and commits `[rdi+0x48] = rsi`, `[rdi+0xA0] = rsi`, "
     "`[rdi+0xB0] = ecx` - the static-table widget resolve.",
     "`00297C10` (244 B) is ~~the `0209BFBE`-bank lookup `0029A0A0` runs: rows stride `0xC0` from `0209BFBE` to `0209C2BE`, "
     "a row qualifies when its `-0x58`/`+0` flags carry bit `2` and `dword[+0x32] == [rsi+4]`; the hit path pairs "
     "`003F89C0` with `0028F590`, then `003F8A50` with `0028F590`, and commits `[rdi+0x48] = rsi`, `[rdi+0xA0] = rsi`, "
     "`[rdi+0xB0] = ecx`~~ the `0209BFBE`-bank lookup `0029A0A0` runs over four rows of stride `0xC0` (`rdi` = "
     "`0209BF40` + n*`0xC0`, scan bound `0209C2BE`): a row with bit `0x2` of byte `+0x26` set in either half (`[rdi+0x26]` "
     "or `[rdi+0x7E]`) and dword `+0xB0` equal to `[rsi+4]` is a match, and only the tail runs (`00297C45` `je` "
     "`00297CE2`) - `[rdi+0x48] = rsi`, `[rdi+0xA0] = rsi`, `[rdi+0xB0] = [rsi+4]`, with no initializer call, so the "
     "callbacks at `+0x38`/`+0x90` keep what they held; failing a match, the first row with bit `0x2` clear in both halves "
     "gets `003F89C0(row, 0, 0, rsi, 0029B7D0)` and `003F89C0(row+0x58, 0, 0, rsi, 0029B810)`, each half appended with "
     "`003F8A50(0028F590(), half)`, then the same tail; with no such row it returns 0 having written nothing, otherwise "
     "the row - the static-table widget resolve *(corrected 2026-10-03, SWE2-EC7: the matched row never reaches "
     "`003F89C0`; OPUS's reading, accepted by SWE2-AUDIT-SPEC in the OV-42 gauge-binding review; ec7_corr_b_check.py)*."),
    # FABLE - the 004309C0 combiner tail is 004307C0.
    (RN,
     "operands resolved as `movss` floats, combiner tail `00430540` |",
     "operands resolved as `movss` floats, combiner tail ~~`00430540`~~ `004307C0`, tail-jumped at `00430A56` when "
     "channel 1's count is non-zero; `00430540` is the per-channel keyed evaluator it calls (`004309F7`, `00430A39`) "
     "*(corrected 2026-10-03, SWE2-EC7: FABLE's SD-197 reading; ec7_corr_b_check.py)* |"),
    # FABLE - 00399B80 returns 1 on the first failing vertex, 0 when all pass.
    (TP,
     "`0039A150`/`0024E410`, or — bit 3 clear — `00399B80` may return 0 early after\n"
     "restoring the matrix rows",
     "`0039A150`/`0024E410`, or — bit 3 clear — ~~`00399B80` may return 0 early~~ `00399B80` returns 1 on the first\n"
     "vertex that fails its range test (`0039A0C9` `jne` to the exit that returns `022D8F30`, set to 1 at `00399E37`) and\n"
     "0 when every vertex passes, and the caller rejects the whole element on 1 *(corrected 2026-10-03, SWE2-EC7: FABLE's\n"
     "SD-199 execution; ec7_corr_b_check.py)*, after\n"
     "restoring the matrix rows"),
    # FABLE - 0039A150 / 00399B80 are project / range-test / pack transforms, not scalar-blend members.
    (TP,
     "lane traffic (19 and 23 wide loads), the scalar-blend members of this\nfamily",
     "lane traffic (19 and 23 wide loads), ~~the scalar-blend members of this\nfamily~~ the project / range-test / pack "
     "transforms of this family: float4 vertices times matrix rows 1-4, divided by `w`, truncated to integers (X and Y "
     "scaled by 16), clamped to X, Y in [0, 0xFFF0] and Z in [0xFF, 0xFFFFFF], with the clamp-changed mask compared "
     "against the emulated PS2 `$zero` register `022D8F10` (`0039A0C6` / `0039A6C8`); `0039A150` packs a passing vertex "
     "as X | Y<<16 | Z<<32 | 0xFF<<56 (`0039A712`) and stores a zero entry for a failing one (`0039A6CD`) "
     "*(corrected 2026-10-03, SWE2-EC7: FABLE's SD-199 execution under Unicorn; ec7_corr_b_check.py)*"),
]


def main():
    apply = "--apply" in sys.argv
    fails = 0
    texts = {}
    for rel, old, new in EDITS:
        t = texts.get(rel) or open(os.path.join(DB, rel), "rb").read().decode("utf-8")
        if new in t or new.replace("\n", "\r\n") in t:
            print("ALREADY", rel.split("/")[-1]); texts[rel] = t; continue
        hit = [c for c in (old, old.replace("\n", "\r\n")) if t.count(c) == 1]
        if not hit:
            print("REFUSING", rel.split("/")[-1], old[:40]); fails += 1; texts[rel] = t; continue
        n = new.replace("\n", "\r\n") if "\r\n" in hit[0] else new
        texts[rel] = t.replace(hit[0], n, 1)
        print(("PATCHED " if apply else "WOULD PATCH ") + rel.split("/")[-1])
    if apply and not fails:
        for rel, t in texts.items():
            open(os.path.join(DB, rel), "wb").write(t.encode("utf-8"))
    print("FAILS", fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
