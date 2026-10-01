# kind_args.py - for each raw call to ActorResource_SubmitRequestDescriptor 003DBB60, the 5th argument ([rsp+0x20] at the
# call; 003DBB60 reads it as [rsp+0x28] after its return address, 003DBB64) = desc+8 = the entry byte +0x12; kind = value >> 1.
# Also rdx/r8/r9 set nearby (channel / function id candidates). Prints the last store to [rsp + 0x20] before each call.
import os, re, json
os.chdir(r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\pub140-scratch")
g = {}
exec(open("disw.py").read().split("fn = int")[0], g)
funcs, off, d = g["funcs"], g["off"], g["d"]
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
md = Cs(CS_ARCH_X86, CS_MODE_64)
idx = json.load(open("tools/rawcalls.json"))
sites = []
for k, v in idx.items():
    if int(k, 16) == 0x003DBB60:
        sites = [int(s[0], 16) if isinstance(s, (list, tuple)) else int(s, 16) for s in v]
if not sites:
    raise SystemExit("rawcalls.json layout not understood: %s" % str(list(idx.items())[:1])[:200])
owner = lambda a: max((f for f in funcs if f <= a), default=None)
for s in sorted(sites):
    fn = owner(s)
    ins = [i for i in md.disasm(bytes(d[off(fn):off(fn) + funcs[fn]]), fn) if i.address <= s]
    back = ins[-25:]
    arg5 = [i for i in back if re.match(r"(byte|dword|qword) ptr \[rsp \+ 0x20\], ", i.op_str)]
    regs = {r: [i for i in back if i.op_str.startswith(r + ",") or i.op_str.startswith(r + "d,") or i.op_str.startswith(r[1:] + "l,")]
            for r in ("rdx", "r8", "r9")}
    a5 = "%s %s" % (arg5[-1].mnemonic, arg5[-1].op_str) if arg5 else "?"
    rr = "; ".join("%s: %s" % (r, (v[-1].mnemonic + " " + v[-1].op_str) if v else "?") for r, v in regs.items())
    print("%08X in %08X | arg5 %s | %s" % (s, fn, a5, rr))
