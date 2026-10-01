"""PENDING PATCH FOR ORACLE (prepared by OPUS 2026-09-25, block 266) - applied and run by OPUS on a scratch COPY only (block 287); ORACLE's file untouched.

Target: _experiments/evidence/s02-world-tick-stop-registry-exec/check.py (EXP-191's harness). Independent of the
block-263 patch (different anchors; either order).

Why: SS-7 ('how many actor managers a request reaches is a bit in its own record') is computed in 00226BE0 from
record A's low dword - reach = (~(A >> 30) & 2) | 1 (00226C77-00226C94) - and record A is BUILT by 00227680 just
before (00226C72), from a per-request-id template (base bits, then a 28-way jump table on the id, 00227680-0022773E,
then per-id tail branches). So the reach is authored per request id. No record has executed either function
(block 260). CORRECTED 2026-09-25 (OPUS, block 287): 00227680 (1,588 B) is NOT call-free - some id paths call
00182CD0 / 002DDC30 and tail-jump 00182D10 / 00182CF0. The replay in candidates/s02-opus-replay-26a5f0-and-reach/
measured which: ids 1-11, 14, 16, 18-27 enter no other function (stub-free); ids 0, 12, 13, 15, 17 do not.

What the patch adds:
  - 28 cases 'ss-record-id-NN' (NN = 0..27): entry 00227680, rcx = id, rdx = &bankA[id] (REG + id*0x18),
    r8 = &bankB[id] (REG + 0x2A0 + id*0x18), r9 = 0 - exactly 00226BE0's call (r15 / r12, 00226C27-00226C5A).
  - their check: no fault; the measured record A / B qwords and reach = (~(A>>30)&2)|1 are written into the case's
    notes (so they land in result.json). It asserts no reach value: this is a MEASUREMENT for the per-request
    reach table, which the static reading could only give by emulating 28 control paths (ORACLE's lane).
Then the SS-7 execution proper is a 00226BE0 case with a chosen id of each reach, counting 00263FF0 calls
(predicted: reach calls, i = 0..reach-1) - left to ORACLE, because 00226BE0's per-manager body reaches
003588B0 / 003590D0 / 002647B0 / 00263BE0 / 00263750, which this harness does not yet script.
Usage (ORACLE): python pending_oracle_s02_ss7_reach_table.py <path-to-check.py>; run; record per ORACLE's process.
"""
import io
import sys

A_CASES = "}\n\n\ndef main():\n"
N_CASES = ("}\n\n# OPUS block 266 patch: SS-7 per-request record template 00227680 (stub-free leaf), ids 0..27\n"
           "for _id in range(28):\n"
           "    CASES[\"ss-record-id-%02d\" % _id] = bc(entry=0x227680, rcx=_id, edx=REG + _id * 0x18,\n"
           "                                         r8=REG + 0x2A0 + _id * 0x18, r9=0)\n"
           "\n\ndef main():\n")
A_CHECK = "        elif name.startswith(\"ss-start\"):\n"
N_CHECK = ("        elif name.startswith(\"ss-record-id-\"):   # OPUS block 266 patch: measurement, no prediction\n"
           "            _i = case[\"rcx\"]\n"
           "            _a = gm.q(REG + _i * 0x18)\n"
           "            _b = gm.q(REG + 0x2A0 + _i * 0x18)\n"
           "            _reach = ((~(_a >> 30)) & 2) | 1\n"
           "            notes.append(\"id=%d A=%016X B=%016X reach=%d\" % (_i, _a, _b, _reach))\n"
           "\n") + A_CHECK


def main(path):
    s = io.open(path, encoding="utf-8", newline="").read()
    if "OPUS block 266 patch" in s:
        print("already patched")
        return 0
    eol = "\r\n" if "\r\n" in s else "\n"

    def e(t):
        return t.replace("\n", eol)
    for a in (A_CASES, A_CHECK):
        if s.count(e(a)) != 1:
            print("anchor not unique/missing:", a.strip()[:60])
            return 1
    s = s.replace(e(A_CASES), e(N_CASES)).replace(e(A_CHECK), e(N_CHECK))
    io.open(path, "w", encoding="utf-8", newline="").write(s)
    print("patched")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
