# OPUS block 301 check of the S-38 draft's counterfactual: with RINIT's first store applied (0042049A `or [rcx+0x284],
# 0x2010F9`), does each ALOC case RETURN, or stop at the harness's 4,000,000-instruction cap? Prints the final RIP.
import struct
import sys

sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\FFXII TZA\_experiments\evidence\render-pool-lifecycle-exec")
sys.dont_write_bytecode = True
import check as C  # noqa: E402
from unicorn import Uc  # noqa: E402
from unicorn.x86_const import UC_X86_REG_RCX, UC_X86_REG_RIP  # noqa: E402

orig = C.World.on_call
final = {}


def on_call(self, uc, addr, size, u):
    if addr == C.RINIT and APPLY:
        rcx = uc.reg_read(UC_X86_REG_RCX)
        v = struct.unpack("<I", self.gm.r(rcx + 0x284, 4))[0] | 0x2010F9
        self.gm.w(rcx + 0x284, struct.pack("<I", v))
    final["rip"] = uc.reg_read(UC_X86_REG_RIP)
    return orig(self, uc, addr, size, u)


C.World.on_call = on_call
orig_start = Uc.emu_start


def emu_start(self, begin, until, timeout=0, count=0):
    r = orig_start(self, begin, until, timeout, count)
    final["end_rip"] = self.reg_read(UC_X86_REG_RIP)
    final["until"] = until
    return r


Uc.emu_start = emu_start
raw, secs = C.load_image()
for APPLY in (False, True):
    for case in C.build_cases():
        if case["name"].startswith("aloc-") and case["name"] not in ("aloc-exists", "aloc-exists-pend", "aloc-full"):
            final.clear()
            tr, faults, obs = C.run_case(dict(case), raw, secs)
            print("%-6s %-16s returned=%s end_rip=%#x nextFree=%#x faults=%s" % ("store" if APPLY else "stub", case["name"],
                  final.get("end_rip") == final.get("until"), final.get("end_rip", 0), obs["nextFree"], faults))
