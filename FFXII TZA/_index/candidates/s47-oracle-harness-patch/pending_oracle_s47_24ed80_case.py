"""PENDING PATCH FOR ORACLE (prepared by OPUS 2026-09-25, block 265) - applied and run by OPUS on a scratch COPY only (block 289: 53/53 x3); ORACLE's file untouched.

Target: _experiments/evidence/efx-rebase-execution/check.py (EXP-084's harness).
Purpose: run the driver 003B3480's rdx != 0 path with 0024ED80 REAL (EXP-084 stubbed it as 'outside the rebase
claim'; block 244 showed it writes the four walk roots the repair walks read, so it selects whose lists are repaired).

0024ED80(obj) (CORRECTED block 289: NOT a call-free leaf - it ends with jmp 0024FCF0 at 0024EDFF, and 0024FCF0 calls 003A2B20; the harness has no bytes for either, so a real run must load them - see candidates/s47-opus-replay-24ed80/add_ed80_chain.py): ctx = q[obj+0x340]; [02F97340] = ctx; [02F97348] = obj;
[02EBEF70] = ctx+0x18; [02EBEF78] = ctx+0x850; [02EBEF90] = ctx+0x848; [02EBEF88] = obj+0x1B8; plus four more heads.
The fixture's second object SEC is a zeroed 0x400 block, so a real run needs q[SEC+0x340] planted: the contract
(section 14, resolved 2026-09-20) reads the container's +0x340 as its EfxCallerTemplate context, i.e. CTX here.

Changes (exact preimage anchors; refuses if missing or already present):
  1. driver_world gains `sec340=None`; when given, q[SEC+0x340] = sec340.
  2. case 'drv-rdx-390-differs-ed80-real' = 'drv-rdx-390-differs' with stub_ed80=False and sec340=CTX. Checks
     (the block-244 static prediction): the six published cells above; SEC+0x390 rebased to FX+0x1040; 0024D940
     visited, 0024D970 not. A fault would itself be a finding (e.g. the SEC+0x1B8 list walk on the zeroed block).
Usage (ORACLE): python pending_oracle_s47_24ed80_case.py <path-to-check.py>; run; record per ORACLE's process.
"""
import io
import sys

A1 = "                 sec390=None, stub_ed80=False):\n"
N1 = "                 sec390=None, stub_ed80=False, sec340=None):   # OPUS block 265 patch: sec340\n"
A2 = "    if stub_ed80:\n        u.mem_write(0x24ED80, b'\\xC3')   # disclosed boundary stub\n"
N2 = ("    if sec340 is not None:   # OPUS block 265 patch: container +0x340 context for a REAL 0024ED80\n"
      "        u.mem_write(SEC + 0x340, struct.pack('<Q', sec340 & U64))\n") + A2
A3 = "\n# ---------------- combined-path slice 0024D619..0024D686 ----------------\n"
N3 = ("\ncase('drv-rdx-390-differs-ed80-real', 0x3B3480, (CTX, SEC),   # OPUS block 265 patch\n"
      "     setup=lambda u: (driver_world(u, handle=H, stored858=FX + 0x1040,\n"
      "                                   sec390=OLD, stub_ed80=False, sec340=CTX),\n"
      "                      put_slot(u, FX + 0x1000), full_world(u)),\n"
      "     check=lambda u, o, l: [] if (\n"
      "         q(u, G_PUBCTX) == CTX and q(u, G_PUBCTX + 8) == SEC\n"
      "         and q(u, G_LIST) == CTX + 0x18 and q(u, G_TAB768) == CTX + 0x850\n"
      "         and q(u, G_TAB320) == CTX + 0x848 and q(u, G_OUTER) == SEC + 0x1B8\n"
      "         and q(u, SEC + 0x390) == FX + 0x1040 and 0x24D940 in o['visits']\n"
      "         and 0x24D970 not in o['visits']) else\n"
      "         ['0024ED80 real: published roots / +0x390 path differ from the static prediction'],\n"
      "     note='rdx!=0 with 0024ED80 REAL (OPUS block 244/265): it publishes the container context and the '\n"
      "          'walk roots before the rebasers; +0x390 differs -> 0024D940 runs over the published roots.')\n") + A3


def main(path):
    s = io.open(path, encoding="utf-8", newline="").read()
    if "OPUS block 265 patch" in s:
        print("already patched")
        return 0
    eol = "\r\n" if "\r\n" in s else "\n"

    def e(t):
        return t.replace("\n", eol)
    for a in (A1, A2, A3):
        if s.count(e(a)) != 1:
            print("anchor not unique/missing:", a.strip()[:60])
            return 1
    for a, n in ((A1, N1), (A2, N2), (A3, N3)):
        s = s.replace(e(a), e(n))
    io.open(path, "w", encoding="utf-8", newline="").write(s)
    print("patched")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
