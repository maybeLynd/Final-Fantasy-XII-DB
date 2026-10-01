"""PENDING PATCH FOR ORACLE (prepared by OPUS 2026-09-25, block 263) - applied and run by OPUS on a scratch COPY only (block 287: PASS, stable x3); ORACLE's file untouched.

Target: _experiments/evidence/s02-world-tick-stop-registry-exec/check.py (EXP-191's harness).
Purpose: close S-02's WT-4 exposure by running 0026A5F0 REAL on the first-writer-wins path of 00314410.
Its callees 002E15D0 / 002E1690 are call-free and are NOT in the harness's SCR table, so they run as shipped
bytes once 0026A5F0 itself is un-stubbed via the case's `realbodies` (on_code checks realbodies before SCR).

Adds, with exact preimage anchors (the patcher refuses if an anchor is missing or the patch is already present):
  1. a generic `pokes` fixture hook ({address: bytes}) after the DRAINM seed;
  2. case "wt-latch-store-real": entry 00314410, rcx=9, latch=-1, drainm=0x3,
     realbodies={0x26A5F0}, mailbox pre-seeded non-zero so every clear is observable;
  3. its checks - the static prediction of blocks 243/260:
       latch == 9; DRAINM == 0x3 | 0x10; b[0215F1A0] == 0; b[0215F1A1] == 1;
       d[0215F1A4] == 0; d[0215F1A8] == 0; no fault; no 's26a5f0' scripted call recorded.
Usage (ORACLE): python pending_oracle_s02_26a5f0_case.py <path-to-check.py>; then run the harness; record as a new
EXP (or an EXP-191 addendum) per ORACLE's own process. OPUS makes no claim about the outcome.
"""
import io
import sys

PRE_HOOK = "        gm.w(DRAINM, dw(case.get(\"drainm\", 0)))\n"
NEW_HOOK = PRE_HOOK + ("        for _a, _v in case.get(\"pokes\", {}).items():   # OPUS block 263 patch\n"
                       "            gm.w(_a, _v)\n")
PRE_CASE = "    \"wt-latch-held\": bc(entry=0x314410, rcx=9, latch=5),\n"
NEW_CASE = PRE_CASE + ("    \"wt-latch-store-real\": bc(entry=0x314410, rcx=9, latch=-1, drainm=0x3,   # OPUS block 263 patch\n"
                       "                               realbodies={0x26A5F0},\n"
                       "                               pokes={0x0215F1A0: b\"\\x5A\\xA5\", 0x0215F1A4: b\"\\x11\\x11\\x11\\x11\",\n"
                       "                                      0x0215F1A8: b\"\\x22\\x22\\x22\\x22\"}),\n")
PRE_CHECK = "        elif name == \"wt-latch-held\":\n"
NEW_CHECK = ("        elif name == \"wt-latch-store-real\":   # OPUS block 263 patch: 0026A5F0 run real\n"
             "            ck(w.faults == [], \"faults\")\n"
             "            ck(gm.d(LATCH) == 9, \"latch stored\")\n"
             "            ck(gm.d(DRAINM) == (0x3 | 0x10), \"mask |= 0x10 (26A5F0(4) real)\")\n"
             "            ck(gm.b(0x0215F1A0) == 0, \"mailbox pending byte cleared\")\n"
             "            ck(gm.b(0x0215F1A1) == 1, \"0215F1A1 set by 2E1690\")\n"
             "            ck(gm.d(0x0215F1A4) == 0, \"mailbox arg A cleared\")\n"
             "            ck(gm.d(0x0215F1A8) == 0, \"mailbox arg B cleared\")\n"
             "            ck(not [x for x in calls if x[0] == \"s26a5f0\"], \"26A5F0 not scripted\")\n"
             "\n") + PRE_CHECK


def main(path):
    s = io.open(path, encoding="utf-8", newline="").read()
    if "OPUS block 263 patch" in s:
        print("already patched")
        return 0
    eol = "\r\n" if "\r\n" in s else "\n"   # the harness is CRLF; match its line endings

    def e(t):
        return t.replace("\n", eol)
    for anchor in (PRE_HOOK, PRE_CASE, PRE_CHECK):
        if s.count(e(anchor)) != 1:
            print("anchor not unique/missing:", anchor.strip()[:60])
            return 1
    s = s.replace(e(PRE_HOOK), e(NEW_HOOK)).replace(e(PRE_CASE), e(NEW_CASE)).replace(e(PRE_CHECK), e(NEW_CHECK))
    io.open(path, "w", encoding="utf-8", newline="").write(s)
    print("patched")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
