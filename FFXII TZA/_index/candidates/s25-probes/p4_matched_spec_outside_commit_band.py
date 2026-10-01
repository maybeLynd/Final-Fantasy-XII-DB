"""P4 (original-code replay) - can the real evaluator match a spec that the shipped commit then
refuses?

P2 measured that 0030F760 returns 0 exactly when the target word is above 0x21E and more than
0x166 above 0x4000, i.e. for 0x4167 and 0x4168 in the condition band. EXP-095's finding 7 says the
spec table 0x1ED0460 is populated through 0x4167 and returns 0 at 0x4168 and above.

This probe drives EXP-095's own World (harness imported read-only by path; main() not called) with a
one-record subgroup whose spec is 0x4165, 0x4166, 0x4167 or 0x4168 and chance 0. The commit stays
the harness's scripted `ret` answering 1, so the probe only asks whether the REAL evaluator
003014C0 / 00301830 matches and what target it hands the commit.

Recorded per spec: walk return, trace (C<i> t<target>), faults, final RIP, and whether RIP reached
RETQ.
"""
import importlib.util, os, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
HARNESS = os.path.normpath(os.path.join(HERE, "..", "..", "..", "_experiments", "evidence",
                                        "gambit-walk-exec", "check.py"))
spec = importlib.util.spec_from_file_location("exp095", HARNESS)
H = importlib.util.module_from_spec(spec); spec.loader.exec_module(H)
from unicorn.x86_const import UC_X86_REG_RIP

raw, secs, iat = H.load_image()
for s in (0x4165, 0x4166, 0x4167, 0x4168):
    case = dict(name="spec-%04X" % s, counts=[1], recs=[H.rec_spec(spec=s, chance=0)], cm=(1,))
    ret, tr, faults, w = H.run_case(case, raw, secs, iat)
    rip = w.uc.reg_read(UC_X86_REG_RIP)
    eval_matched = " C0 " in (" " + tr + " ")
    print("spec=0x%04X  walk_ret=%d  trace=%-18s eval_matched=%-5s final_rip=%08X reached_RETQ=%s faults=%s"
          % (s, ret, tr, eval_matched, rip, rip == H.RETQ, faults))
    del w
print("commit (P2, shipped bytes) returns 0 for target 0x4167 and 0x4168; 1 for 0x4000..0x4166.")
