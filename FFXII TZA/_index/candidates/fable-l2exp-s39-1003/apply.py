"""apply.py - FABLE staged correction applier (2026-10-03, on SWE2-AUDIT-SPEC's L2 expansion). S-39.

Default is a DRY RUN: it reports what it would change and writes nothing. --apply writes the page.
- Anchored: every edit's OLD text must occur EXACTLY ONCE on the page, or the edit FAILs.
- Refuses a dirty page: if `git status --porcelain` lists the page, --apply refuses; a dry run then
  measures against the HEAD blob instead of the working tree and says so.
- Keeps the page's line endings (CRLF or LF) and writes bytes back unchanged elsewhere.
- Idempotent: an edit whose full replacement is already present is SKIPPED (already applied).
- Prints FAILS N last.
"""
import os
import subprocess
import sys

STAMP = "*(corrected 2026-10-03, FABLE, on SWE2-AUDIT-SPEC's L2 expansion)*"
PAGE = "17-Presentation-Rendering/CONTRACT-render-command-list-and-graphics-handshake.md"

E_SEC2_OLD = "Failure is silent everywhere."
E_SEC2_NEW = ("Failure is silent on every path but one: a null left on the owner list faults in the flush `0018C8F0` at "
              "`0018C933` (§10.1).")

E_PROV_OLD = "Section 13 is **empty**: nothing here is observed\n> live."
E_PROV_NEW = ("Section 13 records OPUS's native replay of the list half (isolated shipped code on planted state); nothing\n"
              "> here is observed live.")

E_101_OLD = "So the failure is absorbed silently and the frame draws one job short."
E_101_NEW = (
    "The walks and the frame-end destroy absorb it, and the frame draws one job short. **The owner list's flush does "
    "not:** `0018C8F0`, which the scene teardown `001E0590` runs on the same owner list `[01F7F5E8]` (getter "
    "`0018CA40` at `001E05AE`, flush at `001E05B6`), loads each entry at `0018C930` and reads its `+0x10` at "
    "`0018C933` with **no null test**; only its destroy loop tests (`0018C97A`). A null still on the owner list when "
    "the flush runs is read at address `0x10` and faults. The four ordered-only appenders of I-1 push nothing onto "
    "the owner list, so this concerns the owner-side enqueues (`0018C610` appends the null to the owner list at "
    "`0018C673`, or through the grow arm `0018C680`). Whether a null can still be on the owner list when the "
    "teardown flushes it in play is not established here: the frame-end destroy `0018B810` (`00188211`, `0017CD60`) "
    "skips and drops it if it runs first. The fault is executed on a planted owner list in "
    "[`fable-l2exp-s39-1003`](../_index/candidates/fable-l2exp-s39-1003/README.md) (`check_s39.py` U1), not in a "
    "running game.")

E_13_OLD = ("**Empty. Nothing in this contract has been observed on a running game.** Every claim is static —\n"
            "the shipping image. That is what holds this contract at `BEHAVIORALLY UNDERSTOOD`, and what §16\n"
            "routes.")
E_13_NEW = (
    "**No live observation; the list half has been executed as shipped code in isolation.** Evidence class: "
    "**NATIVE-REPLAY (unicorn 2.1.4), `live_game: false`.** Nothing in this contract has been observed on a running "
    "game, which is what holds it at `BEHAVIORALLY UNDERSTOOD` and what §16 routes; the table below records live "
    "observation and stays empty.\n"
    "\n"
    "The execution is OPUS's [`s39-opus-replay-command-lists`](../_index/candidates/s39-opus-replay-command-lists/README.md) "
    "(block 312). It maps the whole SHA-asserted image, uses no application stub, traps every import except five "
    "bridged allocator and `memmove` imports, and runs every indirect call as shipped code on planted data. `check.py` "
    "passes 7/7 and `i2.py` 5/5; FABLE re-ran both on a scratch copy on 2026-10-03 and got the recorded "
    "`result.json` (md5 `46d4ccb6…`) and `i2_result.json` (md5 `7421772e…`) byte for byte.\n"
    "\n"
    "- **Executed and asserted:** both constructors and the 5,000-entry reserve (§3, I-3); the enqueue appending one "
    "pointer to both lists, and a failed `malloc` appending a null to both (I-1, §10.1's first half); the forward "
    "walk's split, null skip, mask test and I-7 exit (I-4, I-7); two slot-2 calls per entry in the reverse walk (I-5); "
    "the marks and the clear (I-8); the owner destroy skipping a null (I-1); the flush's selection and destroy (I-6); "
    "clear-then-flush at the scene teardown `001E05A9` / `001E05B6` (I-2, one of its three sites); the settle-spin "
    "`0036F2C0` returning at once with bits 2, 3 and 8 clear (I-10's shape).\n"
    "- **Not asserted or not reached:** I-10's premise that no other thread writes `02EBA3F8`. The case plants a "
    "constant on one thread and cannot fail on that premise, so it stays static (`CG-3`, §14.5). `0018B1B0`'s "
    "descending order under `r9b = 1` is recorded, not asserted, and its `+0x2C` / `+0x49C` range selection runs at "
    "`+0x49C = 0` only. **No case puts a null on the owner list before the flush** (the flush case plants three "
    "non-null objects), so §10.1's fault at `0018C933` is not part of this replay; FABLE's `check_s39.py` executes "
    "it on a planted list. The frame-tick and render-pass teardown pairs (`0017CD53`/`0017CD60`, "
    "`00188204`/`00188211`), the other owner-side enqueues and the command classes' own execute bodies are not run.\n"
    "\n"
    "So §13 is no longer empty, but its only evidence class is isolated native replay.")

E_16_OLD = "cannot be claimed while §13 is empty"
E_16_NEW = "cannot be claimed while §13 holds no live observation (its replays are isolated shipped code on planted state)"

EDITS = [
    ("E1 section 2 return semantics", E_SEC2_OLD, E_SEC2_NEW),
    ("E2 provenance note on section 13", E_PROV_OLD, E_PROV_NEW),
    ("E3 section 10.1 null entry", E_101_OLD, E_101_NEW),
    ("E4 section 13 body", E_13_OLD, E_13_NEW),
    ("E5 section 16 FULL SUBSYSTEM", E_16_OLD, E_16_NEW),
]

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
REL = "Database/FFXII TZA/" + PAGE
ABS = os.path.join(ROOT, *REL.split("/"))


def git(*args):
    return subprocess.run(["git", "-C", ROOT] + list(args), capture_output=True).stdout


def replacement(old, new):
    return "~~" + old + "~~ " + new + " " + STAMP


def main():
    do_apply = "--apply" in sys.argv
    fails = 0
    dirty = git("status", "--porcelain", "--", REL).decode("utf-8", "replace").strip()
    if dirty:
        print("NOTE page is dirty in the shared tree: %s" % dirty)
        if do_apply:
            print("FAIL refusing --apply on a dirty page")
            print("FAILS 1")
            return 1
        raw = git("show", "HEAD:" + REL)
        src = "HEAD blob"
    else:
        raw = open(ABS, "rb").read()
        src = "working tree (clean)"
    head = git("rev-parse", "--short", "HEAD").decode().strip()
    print("page %s  source %s  HEAD %s  mode %s" % (REL, src, head, "APPLY" if do_apply else "dry-run"))
    text = raw.decode("utf-8")
    crlf = "\r\n" in text
    nl = "\r\n" if crlf else "\n"
    work = text.replace("\r\n", "\n") if crlf else text
    print("line endings %s" % ("CRLF" if crlf else "LF"))
    changed = 0
    for label, old, new in EDITS:
        rep = replacement(old, new)
        n_old = work.count(old)
        n_rep = work.count(rep)
        if n_rep == 1:
            print("SKIP %s: already applied" % label)
            continue
        if n_old != 1:
            print("FAIL %s: OLD text occurs %d times (needs exactly 1)" % (label, n_old))
            fails += 1
            continue
        work = work.replace(old, rep, 1)
        changed += 1
        print("PASS %s: anchored once, would %s (+%d chars)" % (label, "write" if do_apply else "replace", len(rep) - len(old)))
    out = work.replace("\n", nl) if crlf else work
    if do_apply and changed and not fails:
        with open(ABS, "wb") as f:
            f.write(out.encode("utf-8"))
        print("WROTE %s (%d edits)" % (REL, changed))
    elif do_apply and fails:
        print("not written: failures above")
    print("edits %d, to change %d" % (len(EDITS), changed))
    print("FAILS %d" % fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
