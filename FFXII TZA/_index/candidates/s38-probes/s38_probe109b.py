# Counterfactual: give the scripted RINIT (00420480) the one effect its first store has in shipped bytes,
# 0042049A `or dword [rcx+0x284], 0x2010F9`, and see where ALOC's free-cursor scan stops.
import sys, struct
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\FFXII TZA\_experiments\evidence\render-pool-lifecycle-exec")
sys.dont_write_bytecode = True
import check as C
from unicorn.x86_const import UC_X86_REG_RCX, UC_X86_REG_RIP
orig = C.World.on_call
def on_call(self, uc, addr, size, u):
    if addr == C.RINIT:
        rcx = uc.reg_read(UC_X86_REG_RCX)
        v = struct.unpack("<I", self.gm.r(rcx + 0x284, 4))[0] | 0x2010F9
        self.gm.w(rcx + 0x284, struct.pack("<I", v))
    return orig(self, uc, addr, size, u)
C.World.on_call = on_call
raw, secs = C.load_image()
for case in C.build_cases():
    if case["name"].startswith("aloc-"):
        w_holder = {}
        tr, faults, obs = C.run_case(dict(case), raw, secs)
        print("%-18s live=%#x nextFree=%#x faults=%s trace_tail=%s" % (case["name"], obs["live"], obs["nextFree"], faults, tr[-40:]))
