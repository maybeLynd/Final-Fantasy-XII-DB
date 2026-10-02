"""apply_rig.py [--apply] - OPUS's consumption of ASTRA's two rig packages on OPUS's own text (OPUS, 2026-10-02).

ASTRA-REQ-OPUS-RIG-INDEX-LIST-PRODUCER-1001 and ASTRA-REQ-OPUS-RIG-OWNER-REBIND-PRECONDITIONS-1002, each re-read at the
shipping image (rig_check.py). Two insertions, each after a line OPUS wrote: the GI-19 section of the oscillator page
(the rig's +0x78 statement) and the row-lookup contract's 2026-09-20 ruling (the 003E3C30 entry). The rig page itself
is FABLE's and has its own copy of both requests. Anchor-guarded; ALREADY when present; FAILS n.
"""
import os
import sys

DB = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
OSC = "17-Presentation-Rendering/Model-And-Motion-Formats/the-per-model-oscillator-subsystem.md"
ROW = "02-Resource-And-Asset-Pipeline/CONTRACT-authored-table-row-lookup.md"

OSC_ANCHOR = ("record's resource entry (owner `+0x10`, table `+0xD98`, key `+0x18`) and returns that entry's `+0x84`: the skeleton's\n"
              "`0x290`-stride bone array.\n")
OSC_ADD = (
    "\n"
    "**Qualified 2026-10-02 (OPUS, on ASTRA's rig-index-list and rig-owner-rebind packages, re-read at the bytes):**\n"
    "- `003E1C50` rewrites `+0x70` and `+0x78` only when the rig's initial `+0x70` decodes non-zero\n"
    "  (`003E1C66`-`003E1C78`). Otherwise both keep their values; there is no implicit clear.\n"
    "- When WORD `+0x68` is `0xFFFF` (`003E1C7E`) or the indexed render record is inactive (`+0x284` zero,\n"
    "  `003E1C9A`/`003E1CA0`), `+0x70` becomes `encode(0)` and the decoded zero goes to `00421D20`, whose first\n"
    "  read is `[rcx+0x18]` with no input check (`00421D26`). The `encode(00421D20(render record))` above therefore\n"
    "  needs a valid active owner. The helper's miss on key `-1` (`00421D29`) is a result for a valid input, not a NULL\n"
    "  guard. This is a precondition read from the code, not an observed fault.\n"
    "- The secondary pair `+0x74`/`+0x7C` is skipped when the full DWORD `+0x6C` is `-1` (`003E1CD3`). In `003E1C50`\n"
    "  a missing secondary owner sets `+0x6C` to `-1` and stores `encode(0)` without calling the lookup\n"
    "  (`003E1D19`-`003E1D27`). The rebinds `003E3CA0` and `003E3D70` call `00421D20` on the derived secondary\n"
    "  pointer unguarded (`003E3D34`-`003E3D49`, `003E3E18`). The demonstrated writer stores a sign-extended WORD into\n"
    "  `+0x6C` (`004216D3` `movsx ebx, word [rsi]`, `004216DB`), so it writes `0xFFFFFFFF`, never `0x0000FFFF`.\n"
    "- The rig's own `+0x84` is a **raw** low-32-bit self-address cache, compared with `edi` at `003E1D49`-`003E1D51`\n"
    "  and stored raw at `003E27EA`. It is not the render element's encoded `+0x84` that `00421D20` returns.\n"
)

ROW_ANCHOR = ("**Left open exactly as ASTRA asked:** the actual `003E3C30` entry remains unobserved, and the\n"
              "storage-kind question stays separate from encoding and placement.\n")
ROW_ADD = (
    "\n"
    "**The `003E3C30` body, read 2026-10-02 (OPUS, on ASTRA's rig-index-list package, re-read at the bytes).** It\n"
    "decodes the rig's `+0x88` list (`003E3C42`/`003E3C48`) before it tests the **unsigned** DWORD count `+0x8C`\n"
    "(`003E3C52`, `jbe`). Each list entry is an unsigned DWORD index (`003E3C68` `mov ecx, [rbx]`), scaled to\n"
    "`decode(+0x78) + 0x230 + index * 0x290` (`003E3C6A`-`003E3C77`) and passed to `00203170`. The loop compares\n"
    "unsigned (`003E3C8B`, `jb`) and checks no index against a bone count. Its entry remains unobserved, as above.\n"
)

EDITS = [(OSC, OSC_ANCHOR, OSC_ADD), (ROW, ROW_ANCHOR, ROW_ADD)]


def main():
    fails = 0
    for rel, anchor, add in EDITS:
        p = os.path.join(DB, rel)
        t = open(p, "rb").read().decode("utf-8")
        crlf = "\r\n" in t
        a = anchor.replace("\n", "\r\n") if crlf else anchor
        n = add.replace("\n", "\r\n") if crlf else add
        if a + n in t:
            print("ALREADY", rel)
            continue
        if t.count(a) != 1:
            print("REFUSING", rel, t.count(a))
            fails += 1
            continue
        if "--apply" in sys.argv:
            open(p, "wb").write(t.replace(a, a + n, 1).encode("utf-8"))
            print("PATCHED", rel)
        else:
            print("WOULD PATCH", rel)
    print("FAILS", fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
