"""BJ-1 (OPUS, 2026-09-26): which of the 1,681 lazily-built function-local statics the S-15 boot world constructs, and where.
NATIVE-REPLAY. _Init_thread_header 008092FC and _Init_thread_footer 0080929C are hooked from process start (block 332's Session is
wrapped before s15-opus-replay-boot-world/world_boot.py builds it, so the CRT tables are covered), then that package's check.py runs
unchanged (its result.json is not rewritten). A guard that reaches the footer is a static constructed. The static population is
re-derived from the image: every `call 008092FC` site and the guard its `lea rcx, [rip + guard]` passes.
Scope: the world's start-up in shipped order up to its device stops, the save-image reset, message 16 to the UI system widget,
two field-script binds and 4 field-pass frames per bound slot. NOT a normal boot: the device, the render layer, the title screen
and the per-frame game update are not run. So the result is a lower bound on what a normal boot constructs, with each constructed
guard attributed to the step that built it. Writes result.json."""
import json, os, re, sys, collections
HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.join(os.path.dirname(HERE), "s15-opus-replay-boot-world")
sys.path.insert(0, PKG)
WDIR = os.path.join(os.path.dirname(PKG), "s21-opus-replay-applier-stub-free")
sys.path.insert(0, WDIR); _c = os.getcwd(); os.chdir(WDIR)
import world as W
os.chdir(_c)
from unicorn import UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_RCX, UC_X86_REG_RSP
import struct
EV = []
G = {}
STAGE = ["crt"]


def stage():
    R = G.get("R")
    if R is None:
        return STAGE[0]
    return "step %d" % len(R["steps"])


_orig = W.Session.__init__


def _init(self, *a, **k):
    _orig(self, *a, **k)
    u0 = self.uc
    q = lambda a_: struct.unpack("<Q", bytes(u0.mem_read(a_, 8)))[0]
    self.uc.hook_add(UC_HOOK_CODE, lambda u, a_, n, _: EV.append(("H", u.reg_read(UC_X86_REG_RCX), stage(), q(u.reg_read(UC_X86_REG_RSP)))),
                     begin=0x8092FC, end=0x8092FC)
    self.uc.hook_add(UC_HOOK_CODE, lambda u, a_, n, _: EV.append(("F", u.reg_read(UC_X86_REG_RCX), stage(), q(u.reg_read(UC_X86_REG_RSP)))),
                     begin=0x80929C, end=0x80929C)


W.Session.__init__ = _init
import world_boot as B                                    # noqa: E402  (the CRT tables run here, hooked)
STAGE[0] = "after crt"
src = open(os.path.join(PKG, "check.py"), encoding="utf-8").read()
src = src.replace('json.dump(res, open(os.path.join(HERE, "result.json"), "w")', 'json.dump(res, open(os.devnull, "w")').replace(
    'sys.exit(0 if res["ok"] else 1)', "pass")
G.update({"__file__": os.path.join(PKG, "check.py"), "__name__": "probe"})
exec(compile(src, "check.py", "exec"), G)

# the static population: every call to _Init_thread_header and the guard its rcx carries (lea rcx, [rip + guard] before it)
import capstone, pefile                                   # noqa: E402
img = B.img
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
guards, sites = set(), 0
text_lo, text_hi = 0x121000, 0x8C0000
for off in range(text_lo - 0x120000, text_hi - 0x120000 - 5):
    if img[off] == 0xE8 and off + 5 + struct.unpack_from("<i", img, off + 1)[0] + 0x120000 == 0x8092FC:
        sites += 1
        a = off + 0x120000
        for back in range(7, 60):
            ins = list(md.disasm(img[a - back - 0x120000:a - 0x120000], a - back))
            if ins and ins[-1].address + ins[-1].size == a:
                for i in reversed(ins):
                    m = re.match(r"rcx, \[rip \+ (0x[0-9a-f]+)\]", i.op_str)
                    if i.mnemonic == "lea" and m:
                        guards.add(i.address + i.size + int(m.group(1), 16))
                        break
                break
done = collections.OrderedDict()
heads = set()
for kind, g, st, ret in EV:
    if kind == "H":
        heads.add(g)
    elif g not in done:
        done[g] = (st, "%08X" % ret)
by_stage = collections.Counter(st for st, _ in done.values())
steps = G["R"]["steps"]
names = {("step %d" % i): st["step"] for i, st in enumerate(steps)}    # while step i runs, i steps are recorded
names["after crt"] = "(between the CRT tables and main)"
names["crt"] = "CRT initialiser tables"
res = {"static_header_sites": sites, "static_guards_resolved": len(guards), "constructed": len(done), "headers_seen": len(heads),
       "constructed_in_static_set": sum(1 for g in done if g in guards),
       "by_step": [[names.get(k, k), v] for k, v in sorted(by_stage.items(), key=lambda x: (len(x[0]), x[0]))],
       "guards": {"%08X" % g: [names.get(st, st), ret] for g, (st, ret) in done.items()}}
cases = {"P1_static_population_reproduces_1732_sites_1681_guards": sites == 1732 and len(guards) == 1681,
         "P2_every_constructed_guard_is_in_the_population": res["constructed_in_static_set"] == len(done) and len(done) > 0,
         "P3_every_header_seen_completes": res["headers_seen"] == len(done)}
out = {"evidence": ["NATIVE-REPLAY", "STATIC"], "live_game": False, "results": res, "cases": cases, "ok": all(cases.values())}
json.dump(out, open(os.path.join(HERE, "result.json"), "w"), indent=1, sort_keys=True)
print(json.dumps({k: v for k, v in res.items() if k != "guards"}, indent=1))
for k, v in cases.items():
    print("%-60s %s" % (k, "PASS" if v else "FAIL"))
print("ALL PASS" if out["ok"] else "FAILED")
