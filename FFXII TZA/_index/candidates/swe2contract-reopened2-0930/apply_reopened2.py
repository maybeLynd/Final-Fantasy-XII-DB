"""apply_reopened2.py - the page edits of swe2contract-reopened2-0930 (SWE2-CONTRACT for OPUS, 2026-10-01).

Each edit is an exact anchor that must occur once (or the edit is already applied, when its marker is present). New
text takes the page's own line ending (page 1 is LF-only, page 2 CRLF-only). Idempotent. Status lines and front matter
are not touched.
"""
import io, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
P1 = os.path.join(ROOT, "01-Script-VM-Native-Bridge", "Interpreter-Core", "worldactor-scriptvm-interpreter.md")
P2 = os.path.join(ROOT, "04-Actor-Entity", "the-field-runtime-pass.md")
NOTE = "*Corrected 2026-10-01 (SWE2-CONTRACT for OPUS)"
PTR = "*Pointer 2026-10-01 (SWE2-CONTRACT for OPUS)"

E1 = []  # (marker that shows the edit is applied, old, new)

# --- page 1, section 13.3: RC-16 restated to FABLE's adjudication -------------------------------------------------
E1.append((
    "on FABLE's adjudication of `OPUS-NOTICE-FABLE-RC12-RC16-RC17-0930`",
    "read a register before their own first write** (67 actors touch `regI1` first with a read). **ORACLE",
    "read a register before their own first write** ~~(67 actors touch `regI1` first with a read)~~. **ORACLE"))
E1.append((
    "on FABLE's adjudication of `OPUS-NOTICE-FABLE-RC12-RC16-RC17-0930`",
    "the residue is which record a spawn entry's function runs on. **FABLE adjudication pending** "
    "(`OPUS-NOTICE-FABLE-RC12-RC16-RC17-0930`).",
    "the residue is which record a spawn entry's function runs on. ~~**FABLE adjudication pending** "
    "(`OPUS-NOTICE-FABLE-RC12-RC16-RC17-0930`).~~\n"
    "  " + NOTE + ", on FABLE's adjudication of `OPUS-NOTICE-FABLE-RC12-RC16-RC17-0930` "
    "([`auditsem-corrections-fable-0930/consumer-check.md`](../../_index/candidates/auditsem-corrections-fable-0930/consumer-check.md), "
    "commit `a8aed6ca9`) and SWE2-AUDIT-SEM's review "
    "([`auditsem-review-rc151617-0930`](../../_index/candidates/auditsem-review-rc151617-0930/REVIEW.md) §2, §5 N1); the "
    "struck count is produced by no committed output.* **FABLE accepts ORACLE's NARROWED.** The register file persists "
    "for the life of a pool; the only native clear is the pool memset `00267A8B` when a manager builds its runtime. "
    "`rc16_regfile_reads.py` finds 434 bytecode scripts whose first linear `regI1` touch is a read; in the decompiled "
    "US corpus the dominant case is the monster spawn-group functions, `fn_spawn spawnNN()` and `fn_respawn "
    "respawnNN()` (516 instances in 12 scripts), which on a fresh spawn (`btlAtelGetRespawnCause() == -1`) test "
    "`regI1` before writing it. The `SND_WOMAN_A` F0..F3 read is not shown to run. RC-16's stated limit: which record "
    "a spawn entry's function runs on (static, not traced)."))

# --- page 1, section 13.2: the SND_WOMAN_A conclusion narrowed ------------------------------------------------------
E1.append((
    "it is not a decoder gap (the bytecode census agrees",
    "its file (`SND_WOMAN_A`'s release function): that is the register file behaving as actor state, not\n"
    "  a decoder gap.",
    "its file (`SND_WOMAN_A`'s release function): ~~that is the register file behaving as actor state, not\n"
    "  a decoder gap.~~ it is not a decoder gap (the bytecode census agrees: F0–F3 are read and never written in\n"
    "  `rbn_a03.ebp@286AE`, all nine language copies), but the function is not shown to run, so it is not evidence\n"
    "  that the file carries state into it. " + NOTE + ", on FABLE's RC-16 adjudication and\n"
    "  [`auditsem-review-rc151617-0930`](../../_index/candidates/auditsem-review-rc151617-0930/REVIEW.md) §2.*"))

# --- page 1, residue pointers -----------------------------------------------------------------------------------------
E1.append((
    "the aside only measures sizes to correct the headline",
    "`006E5A20` 15,896 B remains the one unplaced giant;",
    "`006E5A20` 15,896 B remains the one unplaced giant (" + PTR[1:] + ": not this page's residue; the aside only "
    "measures sizes to correct the headline. `006E5A20` is called from `00731EA0` at `007321BE` and `0073228A`, and "
    "placing it belongs to the unlisted-code census in `99-Unresolved-Residual/Unlisted-Code/`, not to the interpreter);"))
E1.append((
    "no reader means no engine meaning to read",
    "| `+16`, `+20` | `u32` unknown — **no reader of any field but `+0` exists anywhere in `.text`** |",
    "| `+16`, `+20` | `u32` unknown — **no reader of any field but `+0` exists anywhere in `.text`** "
    "(" + PTR[1:] + ": no reader means no engine meaning to read; the absence is BQ-6's positive-controlled measurement, "
    "§7 and §12) |"))
E1.append((
    "the popped value is used by the POPF handlers",
    "Those 51 are undetermined in\nthe interesting direction:",
    "Those 51 are undetermined in\nthe interesting direction (" + PTR[1:] + ": a limit on the helper's name, not an "
    "open question about the interpreter; the popped value is used by the POPF handlers, §13.1, which is all this "
    "page relies on):"))
E1.append((
    "no live observation is needed for either",
    "requested, while live automation is paused.",
    "requested, while live automation is paused. (" + PTR[1:] + ": both halves are answered statically, RC-15 and "
    "RC-16 above; no live observation is needed for either.)"))

FP1 = """
## Falsification pass 2026-10-01 (SWE2-CONTRACT for OPUS)

*A non-author pass: SWE2-CONTRACT wrote none of the dispatch sections it attacks. Static, on the certified image
`73461d08…`; nothing was executed. Record: [`swe2contract-reopened2-0930`](../../_index/candidates/swe2contract-reopened2-0930/README.md).*

**The claim attacked, and why it carries the page.** The 100-entry computed-goto dispatch (§2, §3, §4, §13.1): the
image-base rebase, the `0x63` bound and its default `0025E60A`, the 32-bit RVA table at `00261DF8`, every target inside
the one 14,646-byte body, 92 distinct targets in exactly three shared groups, and the register-file handlers
`0x36`–`0x45`. Every other result on the page is read through this table: BF-1's per-opcode effects, BF-5's inert six,
§11's name alignment, §13's register file and §6's modding notes. Also attacked: the two SECTION-11 entry facts that
reopened the page (the shared value-stack depth at `02099AC0` is zeroed before the refusal test; the 65,536-instruction
budget) and §4's operand pre-decode from `0x47`.

**Method.** `falsify_interp_dispatch.py` decodes the body linearly with capstone from its `functions.tsv` extent,
resolves the `lea` displacement with its sign, reads the 100 table dwords from the image and compares every figure with
the page's. Positive controls: three corrupted copies of the table (one handler moved outside the body, one extra
shared target, one opcode taken out of the default group). Each must fail its matching check, and each does.

**Result: SURVIVED.**

| check | clause attacked | result |
|---|---|---|
| I1 | 14,646 B and 3,229 instructions | survives exactly; the table starts two bytes past the body end (`00261DF6`) |
| I2–I4 | `lea r8, [rip-0x13E5DD]` = `00120000`; `cmp eax, 0x63` / `ja 0025E60A`; the dword table at base + `0x141DF8` = `00261DF8` | survives |
| I5–I6 | all 100 entries land inside the body, each on an instruction start | survives, 100 of 100 |
| I7–I9 | 92 distinct targets; shared `0025E60A` ← 01 02 19 1A 31 47, `0026121A` ← 2A 2B 2C, `002618A8` ← 51 60; span `0025E5EA`–`00261D36` | survives exactly |
| I10–I11 | `0x36`–`0x45` reach the sixteen §13.1 handlers, which move I0–I3 at `r15+0x64`.. and F0–F3 at `r15+0x74`.. through the pop and push helpers | survives |
| I12 | SECTION-11: `0025E4D2 xor r11d, r11d`, then `0025E4D8` stores it to `02099AC0` before any branch; the refusal at `0025E4FF`/`0025E502` returns 1 | survives |
| I13 | SECTION-11: `mov ecx, 0x10000`, then `sub ecx, ebp` with `ebp` = 1 per instruction | survives |
| I14–I15 | the pre-decode starts at `0x47`; `0025E60A` is `mov [rsp+0xC0], ebp ; mov edi, ebp` | survives |
| C1–C3 | the positive controls | each corruption is caught |

Output `falsify_interp_dispatch.out`, `FAILS 0`. The attacked claim needs no correction. The same pass applied FABLE's
RC-16 adjudication to §13.2 and §13.3 (struck and corrected there) and added pointers to four residue sentences that
carried no id.
"""

E2 = []
E2.append((
    "mode 0 when that speed is positive and mode 2 when it is zero",
    "`Movement_SetRequestedSpeed(actor, request.+0x7C × [01DFE0BC], mode)` with mode 2 when that\n"
    "      speed is positive and 0 otherwise (`0025DF49`–`0025DF83`) — the scaled-speed variant inline,",
    "`Movement_SetRequestedSpeed(actor, request.+0x7C × [01DFE0BC], mode)` with ~~mode 2 when that\n"
    "      speed is positive and 0 otherwise~~ mode 0 when that speed is positive and mode 2 when it is zero, negative\n"
    "      or unordered (`0025DF6F mov r8d, 2`, `comiss xmm2, xmm0` against 0.0, `cmova r8d, ebp` with `ebp` = 0;\n"
    "      " + NOTE + ": check W13 of the falsification pass below runs these bytes*) (`0025DF49`–`0025DF83`)\n"
    "      — the scaled-speed variant inline,"))
E2.append((
    "it is the move verb's speed operand",
    "What the request's `+0x7C` speed is set from is that\n      page's matter.",
    "What the request's `+0x7C` speed is set from is that\n      page's matter. (" + PTR[1:] + ": it is the move verb's "
    "speed operand, `0026A640`, per [the steering-slots page](../06-Movement-And-Navigation/Facing-And-Steering/the-two-steering-slots-and-what-a-character-resumes.md) field `+0x7C`.)"))
E2.append((
    "the next paragraph reads the writers",
    "save meaning comes from the ledger name and from whoever writes `02CA99E8`, which this document\n"
    "> has not read.",
    "save meaning comes from the ledger name and from whoever writes `02CA99E8`, which this document\n"
    "> has not read. (" + PTR[1:] + ": read since 2026-09-11; the next paragraph reads the writers.)"))

FP2 = """
## Falsification pass 2026-10-01 (SWE2-CONTRACT for OPUS)

*A non-author pass: SWE2-CONTRACT wrote neither §11's SECTION-12 table nor the bound it attacks. Static, on the
certified image `73461d08…`; the only execution is check W13, which runs five of the image's own instructions under
Unicorn. Record: [`swe2contract-reopened2-0930`](../_index/candidates/swe2contract-reopened2-0930/README.md).*

**The claim attacked, and why it carries the page.** §11's SECTION-12 wait-completion polarity table, the correction
that reopened the page: which predicate each wait kind runs, which result holds the wait and which completes it, which
kinds set the wait slot's `+0x27`, and that `0025E127` is the blocked exit and `0025E0BE` the interpreter arm. Also
attacked: the bound §8 and §9 draw from that table, that one `0025DF00` call dispatches at most twice. This is what
decides when a waiting script resumes, and the interpreter page, the request-chain page and GR-1's answer all read it.

**Method.** `falsify_wait_polarity.py` decodes `0025DF00` linearly from its `functions.tsv` extent and resolves `r14`
from its `lea`. It decodes the eight-entry table at `0025E3CC` from the image and reads each arm's call, compare,
branch polarity and stores. It runs a store census over the body for `+0x14` and `+0x27` on the wait-slot base, and a
back-edge analysis of the loop head `0025DFA0`. Positive controls: a table copy with kind 3 repointed, a planted
`+0x27` store and a dword store at `+0x24`, each of which the matching check must see.

**Result: SURVIVED for the attacked claim. One adjacent sentence is CORRECTED.**

| check | clause attacked | result |
|---|---|---|
| W1 | 1,228 B, 329 instructions, `ret` at `0025E3CB`, no jump leaving the extent | survives exactly |
| W2–W3 | dispatch on wait `+0x14`, `cmp 7` / `ja 0025E127`; kinds 0→`0025E127`, 1 and 2→`0025E0BE`, 3→`0025E027`, 4→`0025E091`, 5→`0025E00A`, 6→`0025E058`, 7→`0025E083` | survives exactly |
| W4 | kind 3 holds while `003DBF60` finds an entry; `0xFF` completes and sets `+0x27` | survives |
| W5 | kind 4 holds while `003DC050` finds none; a found notification is removed by `003DB2A0`; no `+0x27` store | survives |
| W6–W8 | kind 5 (`002674B0`) and kind 6 (`003DB640`) hold while active; kind 7 calls `00267420` and jumps into kind 6's tail at `0025E06E`, sharing its `+0x27` store | survives |
| W9–W10 | `0025E127` sets wait `+0x16` = 1 and falls to `0025E12B` with no interpreter call; `0025E0BE` calls `0025E4C0(slot, record, wait slot)` | survives |
| W11 | stores covering wait `+0x27` are exactly `0025E04F` and `0025E07A`; the four `= 1` stores to wait `+0x14` are `0025E01E`, `0025E04B`, `0025E076`, `0025E0B5` | survives exactly |
| W12 | at most two dispatches: the four back-edges to `0025DFA0` each follow a `+0x14 = 1` store, and nothing at or after the interpreter arm branches back into the dispatch | survives, within the limit below |
| W13 | §11's early movement path, the mode passed to `Movement_SetRequestedSpeed` | **corrected**: mode 0 for a positive speed and 2 otherwise, measured by running the bytes; the page had the two inverted |
| C1–C3 | the positive controls | each is caught |

**Limit of W12.** The re-dispatch re-reads the wait-slot index from record `+0x11` (`0025DFB6`). In the direct closure
of the ten functions the loop head and the arms call (168 functions), the byte stores covering `+0x11` are all on
`0x14`-stride resource-entry bases (`003DB7A0`, `003DC130`, `003DC1B0`). Four wider stores covering it
(`00226280`, `00226BE0`, `002EBFA0`, `002EC2C0`) are not typed here, and indirect calls are not followed.

Output `falsify_wait_polarity.out`, `FAILS 0`. GR-1's answer is already on the page (the §8 box and §11's `+0x27` item),
and W11 reproduces the store half of it.
"""

E1.append(("## Falsification pass 2026-10-01 (SWE2-CONTRACT for OPUS)",
           "every actor running under that manager interprets the same image through the same slot.\n",
           "every actor running under that manager interprets the same image through the same slot.\n" + FP1))
E2.append(("## Falsification pass 2026-10-01 (SWE2-CONTRACT for OPUS)",
           "\n## Cross-subsystem neighbours — FINAL-AUDIT pass 22\n",
           FP2 + "\n## Cross-subsystem neighbours — FINAL-AUDIT pass 22\n"))


def apply(path, edits, eol):
    raw = io.open(path, "rb").read().decode("utf-8")
    text = raw.replace("\r\n", "\n") if eol == "\r\n" else raw
    if eol == "\n" and "\r" in raw:
        sys.exit("page has CR bytes, expected LF-only: %s" % path)
    if eol == "\r\n" and raw.count("\n") != raw.count("\r\n"):
        sys.exit("page is not CRLF-only: %s" % path)
    done = 0
    for marker, old, new in edits:
        if marker in text:
            continue
        n = text.count(old)
        if n != 1:
            sys.exit("anchor occurs %d times in %s: %r" % (n, os.path.basename(path), old[:90]))
        text = text.replace(old, new, 1)
        done += 1
    out = text.replace("\n", "\r\n") if eol == "\r\n" else text
    io.open(path, "wb").write(out.encode("utf-8"))
    print("%s: %d edits applied, %d already present" % (os.path.relpath(path, ROOT), done, len(edits) - done))


if __name__ == "__main__":
    apply(P1, E1, "\n")
    apply(P2, E2, "\r\n")
