"""P3 (original-code replay, counterfactual) - re-run EXP-095's own 35 cases with the scripted
commit ALSO performing the unit stores the shipped commit makes, and compare to the stub-as-shipped
baseline.

The shipped commit's stores come from P2: on a successful return it writes unit+0x708 = the record
pointer (rdx), unit+0x710 = param (r9d) and unit+0x714 = target (r8w), at 0030F7F9/0030F800/0030F806.
On a 0 return it makes none of them.

EXP-095's harness (`_experiments/evidence/gambit-walk-exec/check.py`) is imported read-only by
path. Its main() is never called, so result.json is not touched. Only World.on_call is wrapped: for
COMMIT, when the scripted answer is nonzero, the three stores are applied before the harness's own
handler runs.

Recorded per case, for both runs: return value, trace, faults, final RIP and whether RIP reached the
harness return sentinel RETQ.
"""
import importlib.util, os, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
HARNESS = os.path.normpath(os.path.join(HERE, "..", "..", "..", "_experiments", "evidence",
                                        "gambit-walk-exec", "check.py"))
spec = importlib.util.spec_from_file_location("exp095", HARNESS)
H = importlib.util.module_from_spec(spec); spec.loader.exec_module(H)
from unicorn.x86_const import UC_X86_REG_RIP, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9

orig_on_call = H.World.on_call


def on_call_with_commit_writes(self, uc, addr, size, _):
    if addr == H.COMMIT:
        i = self.commit_calls
        v = self.commit_script[i] if i < len(self.commit_script) else self.commit_script[-1]
        if v:
            unit = uc.reg_read(UC_X86_REG_RCX)
            self.gm.w(unit + 0x708, struct.pack("<Q", uc.reg_read(UC_X86_REG_RDX)))
            self.gm.w(unit + 0x710, struct.pack("<I", uc.reg_read(UC_X86_REG_R9) & 0xFFFFFFFF))
            self.gm.w(unit + 0x714, struct.pack("<H", uc.reg_read(UC_X86_REG_R8) & 0xFFFF))
    return orig_on_call(self, uc, addr, size, _)


def run_all(patched):
    H.World.on_call = on_call_with_commit_writes if patched else orig_on_call
    raw, secs, iat = H.load_image()
    out = {}
    for case in H.build_cases():
        ret, tr, faults, w = H.run_case(case, raw, secs, iat)
        rip = w.uc.reg_read(UC_X86_REG_RIP)
        out[case["name"]] = (ret, tr, [f for f in faults], rip == H.RETQ, "%08X" % rip,
                             ret == case["want_ret"] and tr == case["want_trace"])
        del w
    return out


base = run_all(False)
cf = run_all(True)
same = 0
print("case | baseline ret/RIP@RETQ/final_rip/matches_record | with commit writes ret/RIP@RETQ/final_rip | identical")
for name in base:
    b, c = base[name], cf[name]
    ident = (b[0], b[1], b[2]) == (c[0], c[1], c[2])
    same += ident
    print("%-18s | ret=%d reached_RETQ=%s rip=%s ok=%s faults=%s | ret=%d reached_RETQ=%s rip=%s faults=%s | %s"
          % (name, b[0], b[3], b[4], b[5], b[2], c[0], c[3], c[4], c[2], ident))
    if not ident:
        print("    baseline trace: %s\n    with writes:    %s" % (b[1], c[1]))
print("identical cases: %d/%d" % (same, len(base)))
