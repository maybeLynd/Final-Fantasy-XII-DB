"""apply_title_r3_r4.py [--apply] - FABLE's routed notes R3 and R4 (astra-returns-title-fable-1002) on OPUS's save-image
contract (OPUS, 2026-10-02). Board task FABLE-REQ-OPUS-TITLE-PACKET-CONTRACTS-1002. Idempotent; FAILS n.

R3 scopes "each channel is one-shot" to the guarded dispatcher. R4 adopts the accepted queue, count and selector facts
once, beside the section's NOT CLAIMED list, which they narrow.
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PAGE = os.path.normpath(os.path.join(HERE, "..", "..", "..", "19-Save-Load-Settings", "CONTRACT-save-image-buffers.md"))
REC = "../_index/candidates/astra-returns-title-fable-1002/README.md"

EDITS = [
    ("work and consumed by it.** Each channel is one-shot — running a handler twice without something\n"
     "re-setting its dword does nothing the second time, because the guard will refuse. That is a contract",
     "work and consumed by it.** ~~Each channel is one-shot — running a handler twice without something~~\n"
     "~~re-setting its dword does nothing the second time, because the guard will refuse.~~ Through the guarded "
     "dispatcher `006505A0`, each channel is one-shot: it tests the channel's dword (channel 0: `00625F00`, called at "
     "`006505A0+0x93`) before it tail-jumps to the handler (`006505A0+0xA8`). The handler itself tests nothing, so a "
     "direct call is not guarded. On channel 0, `00616C60` calls `0062BCB0` unconditionally (`00616C60+0x1B`), and "
     "`005DE250` calls it under the guard (`005DE250+0x1F`) and then tail-jumps to `00616C60` (`005DE250+0x2D`). On "
     "normal returns that path runs the handler twice when `+0xBC` is non-zero, and a second run is not shown to do "
     "nothing. *(corrected 2026-10-02, OPUS: ASTRA's title cleanup-guard qualification, SWE2-AUDIT-SPEC ACCEPT, routed "
     "by FABLE as R3 in [`astra-returns-title-fable-1002`](" + REC + "))* That is a contract"),
    ("- **NOT CLAIMED:** what the object is, what the three channels do, what `0062B100`/`0062B170`/\n"
     "  `0062B1E0` are, and what `[inner+0x20]` holds.\n",
     "- **NOT CLAIMED:** what the object is, what the three channels do, what `0062B100`/`0062B170`/\n"
     "  `0062B1E0` are, and what `[inner+0x20]` holds.\n"
     "- **Adopted 2026-10-02 (OPUS), from ASTRA's title packets** (each SWE2-AUDIT-SPEC ACCEPT; routed by FABLE as R4 in\n"
     "  [`astra-returns-title-fable-1002`](" + REC + ")). These narrow the list above for channel 0\n"
     "  and say nothing about channels 1 and 2:\n"
     "  - **Count and selector.** n is the low 31 bits of `+0x30` (`00623DF0` clears bit 31 with `btr` before it\n"
     "    compares). Bit 31 is ignored by the selector and gates `00584730`. Records are `0x58` bytes. `00623DF0`\n"
     "    returns `base + 0x58 * k + 0x38`, the address of a record's `+0x38` field, not a record base. The base is the\n"
     "    pointer at `+0x38` for n > 1, the object's own `+0x38` for n = 1, and 0 for n = 0. There is no index bound\n"
     "    and no write. `0062B100` walks indices up to max(1, n) and calls `005CCB80` with ECX = 1 while the selected\n"
     "    DWORD is positive. With n = 0, its first read is at absolute address `0x38`: a precondition on valid\n"
     "    state, not an observed fault.\n"
     "  - **The deferred-call queue the title cleanup uses.** Entries are 16-byte `{function, data}` pairs, in four\n"
     "    32-byte banks at `ctx+0xC38+32*k`, indexed by `ctx[+0xCB8]`. The consumer `00186230` calls `function(data)`\n"
     "    with RCX = data (`00186230+0x43`, `+0x47`). The flush `00185C20` is called by `0017D6E0` only when\n"
     "    `01FD4A68` is zero, at most once per `0017D6E0` call. The getter `00189120` takes no argument.\n"
     "  - **Heap ownership.** The queued data pointer reaches the CRT `free` import after `005DE250`.\n"
     "  - **Still open:** that n >= 1 holds for the real caller, `005CCB80`'s effects, title lifetime, cancellation and\n"
     "    idempotence.\n"),
]


# Pass-22 neighbours (2026-10-02, OPUS): functions of other layers are named by role in NEW text, so the page
# takes on no unaccounted crossing (check_publish_neighbours.py refused the address form).
ROLE_NAMES = [
    ('is called by `0017D6E0` only when',
     'is called by the per-frame pump only when'),
    ('at most once per `0017D6E0` call.',
     'at most once per pump call.'),
]
_rn = lambda s: __import__('functools').reduce(lambda a, p: a.replace(p[0], p[1]), ROLE_NAMES, s)
EDITS = [(e[0], _rn(e[1])) if len(e) == 2 else (e[0], e[1], _rn(e[2])) + tuple(e[3:]) for e in EDITS]


def main():
    t = io.open(PAGE, encoding="utf-8", newline="").read()
    fails = 0
    for old, new in EDITS:
        # The page has mixed line endings: use whichever form the OLD text actually has here.
        nl = "\n" if (old in t or new in t) else "\r\n"
        old, new = old.replace("\n", nl), new.replace("\n", nl)
        if new in t:
            print("ALREADY", old[:50].replace(nl, " "))
            continue
        if t.count(old) != 1:
            print("NOT FOUND (%d)" % t.count(old), old[:50].replace(nl, " ")); fails += 1
            continue
        t = t.replace(old, new)
        print("WOULD PATCH" if "--apply" not in sys.argv else "PATCHED", old[:50].replace(nl, " "))
    if "--apply" in sys.argv and not fails:
        io.open(PAGE, "w", encoding="utf-8", newline="").write(t)
    print("FAILS", fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
