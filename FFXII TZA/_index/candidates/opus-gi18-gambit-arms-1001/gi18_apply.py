"""gi18_apply.py [--apply] - GI-18 on the gambit page: strike the arm roles the full read refutes, add the GI-18
section, re-word the status texts (OPUS, 2026-10-01).

Each edit is an exact substring that must occur once; the new text carries a tag, so a re-run reads ALREADY. The
section (gi18_section.md) is inserted before "## Falsification pass" with the page's EOL. Dry run unless --apply.
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
PAGE = os.path.join(DB, "16-UI", "Gambit-Screens", "the-gambit-screens.md")
P = " *(corrected 2026-10-01, OPUS: GI-18 section)*"

EDITS = [
    # the pick list
    ("| construct: clears the editor's `+0xC8` byte, builds a two-entry child table (`0056B4D0` `lea`s `0056BB60`/`0056BB70` records), copies `msg->arg` into `+0x5A4`, then installs the editor child |",
     "| construct: ~~clears the editor's `+0xC8` byte, builds a two-entry child table (`0056B4D0` `lea`s `0056BB60`/`0056BB70` records), copies `msg->arg` into `+0x5A4`, then installs the editor child~~ clears `[02CA96D8]+0xC8`, builds the layout descriptors `00D234A8` / `00D234D0` (callbacks `0056BBD0` / `0056A780`), copies `msg->arg` into `+0x5A4` and the create record into `+0xC8`" + P + " |"),
    ("decrements `+0x580`; on the last pending request posts `{0x8000,0,0}` to self via `00247510` |",
     "~~decrements `+0x580`; on the last pending request posts~~ counts the frame countdown `+0x580` (`0xB4` from `0056AC50`) down and at zero posts `{0x8000,0,0}` to self via `00247510`" + P + " |"),
    ("| 8 | `0056B7E9` | enable on: `or +0x5A0,2` and sends id 1 to `+0xC0` |",
     "| 8 | `0056B7E9` | ~~enable on~~ focus gained: `or +0x5A0,2` and ~~sends id 1 to `+0xC0`~~ `002D45C0([+0xC0], 1)`" + P + " |"),
    ("| 9 | `0056B808` | enable off: `and +0x5A0,~2`, zeroes `+0x580` |",
     "| 9 | `0056B808` | ~~enable off~~ focus lost" + P + ": `and +0x5A0,~2`, zeroes `+0x580` |"),
    ("routes confirm/cancel through `002D3A50`/`002D45C0` on `+0xC0` |",
     "~~routes confirm/cancel through `002D3A50`/`002D45C0` on `+0xC0`~~ pages up / down (`0056AAC0` / `0056AD50`) or hands the input to the list child (`002D3A50`)" + P + " |"),
    # the editor
    ("| 8 | `0056961E` | enable on |", "| 8 | `0056961E` | ~~enable on~~ focus gained" + P + " |"),
    ("| 9 | `00569671` | enable off |", "| 9 | `00569671` | ~~enable off~~ focus lost" + P + " |"),
    ("| 16 | `0056955F` | refresh |", "| 16 | `0056955F` | ~~refresh~~ resource batch complete: snapshots the set into `+0x128`" + P + " |"),
    ("| 17 | `00569781` | secondary input |", "| 17 | `00569781` | ~~secondary input~~ position tween finished: commits a pending edit" + P + " |"),
    ("| 18 | `00569236` | close: `002922F0`, checks `[global + 0xDEB]`, commits the edited bank through `003282C0` (`GambitConfig_CommitBankAndRebuildRuntimeOrders`), then clears `+0x35C`/`+0x360` and the global arrays |",
     "| 18 | `00569236` | close: `002922F0`, checks `[global + 0xDEB]`, ~~commits the edited bank~~ only when it is set writes the id-16 snapshot `+0x128` through `003282C0` (`GambitConfig_CommitBankAndRebuildRuntimeOrders`), then ~~clears `+0x35C`/`+0x360` and the global arrays~~ nulls `02CA96E0` / `02CA96F8` at `+0x35C`" + P + " |"),
    ("| 19,20 | `0056960B` | transition flags |", "| 19,20 | `0056960B` | ~~transition flags~~ transition finished: `002D7580(0, 1)`" + P + " |"),
    ("| 22 | `005696B9` | secondary enable |", "| 22 | `005696B9` | ~~secondary enable~~ position tween stepped: `002D78B0(6, rect)`" + P + " |"),
    ("| 26 | `00569ED4` | `+0x331` byte → 6 |", "| 26 | `00569ED4` | ~~`+0x331` byte → 6~~ `00568FE0(self, b, a)`, the per-row slide step (the `+0x331` store is the `0x121` arm)" + P + " |"),
    ("formats through `00291D70`/`00291D80`, stores the prompt id at `+0x344` — the copy/paste-confirm prompt",
     "formats through `00291D70`/`00291D80`, ~~stores the prompt id at `+0x344`~~ stores the tick `[0208F570]` at `+0x344`" + P + " — the copy/paste-confirm prompt"),
    ("- `0x8002` → `00569E42` → `005679D0` (bank clear)", "- `0x8002` → `00569E42` → `005679D0` (~~bank clear~~ pane rebuild" + P + ")"),
    ("- `0x8003` → `0056A1D0` picker, then `00249C60` on the chosen index",
     "- `0x8003` → ~~`0056A1D0` picker, then `00249C60` on the chosen index~~ when `00264150()` is 0, `0056A1D0(self, -1, b, 0, 0)` empties row `b`; a result other than -1 goes to `00249C60`" + P),
    ("- `0x8004` → `005680E0` (bank move) when `+0x342` is clear", "- `0x8004` → `005680E0` (~~bank move~~ pane reset" + P + ") when `+0x342` is clear"),
    ("| `005679D0` | bank clear —", "| `005679D0` | ~~bank clear~~ pane rebuild (the-two-transform-primitives.md)" + P + " —"),
    ("| `005680E0` | bank move —", "| `005680E0` | ~~bank move~~ pane reset (the-two-transform-primitives.md)" + P + " —"),
    # status texts
    ("**Not attacked by this pass**, and still `PARTIAL` on the editor's 12 sub-commands and the\nlist's 19 arms below entry level — registered as **GI-18**.",
     "**Not attacked by this pass**, and ~~still `PARTIAL` on the editor's 12 sub-commands and the\nlist's 19 arms below entry level~~ *(read 2026-10-01, OPUS: the GI-18 section)* — registered as **GI-18**."),
]
STATUS_PREFIX = 'status: "PARTIAL — GI-18 registered 2026-10-01'
STATUS_NEW = ('status: "DOCUMENTED — every register row is closed (owner re-status 2026-10-01, OPUS; documented_rule READY): '
              'GI-18 answered 2026-10-01 (OPUS, static - every arm of both procedures read one level down, see the GI-18 '
              'section; review requested from SWE2-AUDIT-SEM). GI-1 answered 2026-09-29 (FABLE), review '
              '(FABLE-REQ-AUDITSEM-REVIEW-GI-UI, ACCEPT, d998217e2). History: PARTIAL on GI-18 from 2026-10-01 '
              '(SWE2-FRONTIER, on SWE2-AUDIT-SEM\'s REJECT of c97af7156, record dd-restatus-gi-0930); earlier PARTIAL on: '
              'which value of the gambit row\'s +0x14 bit 0 selects condition art and which action art (GI-1); the earlier '
              '02F8F570 was a misread of 0208F570, the tick counter (corrected 2026-09-18)"')
BANNER_OLD = "**Status:** PARTIAL — the four widget procedures"
BANNER_NEW = "~~**Status:** PARTIAL~~ *(Superseded 2026-10-01, OPUS: DOCUMENTED - see the status line; GI-18 answered)* — the four widget procedures"
ANCHOR = "## Falsification pass"
HEAD = "## GI-18: the editor's and the pick list's arms below entry level (OPUS, 2026-10-01)"


def main():
    apply = "--apply" in sys.argv
    raw = open(PAGE, "rb").read().decode("utf-8")
    eol = "\r\n" if "\r\n" in raw else "\n"
    fails = 0

    def sub(old, new, label):
        nonlocal raw, fails
        # match with either EOL inside multi-line edits
        cands = [old, old.replace("\n", "\r\n")]
        if new.replace("\n", "\r\n") in raw or new in raw:
            print("ALREADY", label); return
        hit = [c for c in cands if raw.count(c) == 1]
        if not hit:
            print("REFUSING %s: %s" % (label, [raw.count(c) for c in cands])); fails += 1; return
        c = hit[0]
        n = new.replace("\n", "\r\n") if "\r\n" in c else new
        raw = raw.replace(c, n, 1)
        print(("PATCHED " if apply else "WOULD PATCH ") + label)

    for i, (old, new) in enumerate(EDITS):
        sub(old, new, "edit %d" % (i + 1))
    sub(BANNER_OLD, BANNER_NEW, "banner")
    lines = raw.split("\n")
    st = [k for k, l in enumerate(lines) if l.startswith(STATUS_PREFIX)]
    if any(l.rstrip("\r") == STATUS_NEW for l in lines):
        print("ALREADY status")
    elif len(st) != 1:
        print("REFUSING status: %d" % len(st)); fails += 1
    else:
        cr = "\r" if lines[st[0]].endswith("\r") else ""
        lines[st[0]] = STATUS_NEW + cr
        raw = "\n".join(lines)
        print(("PATCHED " if apply else "WOULD PATCH ") + "status")
    if HEAD in raw:
        print("ALREADY section")
    else:
        sec = io.open(os.path.join(HERE, "gi18_section.md"), encoding="utf-8").read().strip("\n").replace("\n", eol)
        k = raw.find(eol + ANCHOR)
        if k < 0 or raw.count(eol + ANCHOR) != 1:
            print("REFUSING section anchor"); fails += 1
        else:
            raw = raw[:k] + eol + sec + eol + raw[k:]
            print(("PATCHED " if apply else "WOULD PATCH ") + "section")
    if apply and not fails:
        open(PAGE, "wb").write(raw.encode("utf-8"))
    print("FAILS", fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
