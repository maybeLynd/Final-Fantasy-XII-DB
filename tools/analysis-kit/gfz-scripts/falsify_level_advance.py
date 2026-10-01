"""falsify_level_advance.py - falsification pass 1 on 13-Rewards-Progression-Economy/CONTRACT-level-advance-and-growth.md
(OPUS, 2026-09-30). Static; reads only the shipping image. Each check is one of the contract's clauses at its bytes.

V1  §2 0030C650: 570 B, 150 instructions, one ret at 0030C889, one back-edge 0030C865 jl 0x30c6a3
V2  LU-1 the three 99 guards: cmovg at 0030C682, the loop-top cmp byte [rdi+0x1c2], 0x63 / jae at 0030C6CC/0030C6D3,
    inc at 0030C7B3 and cmova at 0030C7B8
V3  LU-2 0030C686 cmp ecx, r14d / jge leaves before the loop; the level is only ever incremented
V4  LU-3 notify = ~(flags >> 1) & 1 at 0030C660-0030C676; the final-level test at 0030C7C1-0030C7C7
V5  LU-4 0030C6D9 cmp byte [rdi + 5], 0 / jne 0x30c7a7
V6  LU-5 both resolve failures reach 0030C721 xor ebp, ebp; HP/MP calls at 0030C730/0030C746; the float calls read
    byte [rbp + 0x1f / 0x22 / 0x25 / 0x28]
V7  LU-6 the first resolve (0030C6F2) is null-tested at 0030C6F7; the second (0030C706) feeds 0030C71D add ebp, eax untested
V8  LU-7 0030C6BC call 0031B860 (whose 0031B892 compares [rax + 0x698] with rdi); the poster 0046A690 at 0030C7E4 before
    the owner test 0030C7ED; 0030C7F2 loads [r15 + 0x698]; 0030C7FE reads byte [rax + 5]
V9  LU-3 note: the thunk 0035D8C0 has one caller, 0030C815; 002905D0 is reached only through it; 002905EA edx = 6,
    002905F6 lea r9d, [rdx - 5]; 002966E0 strides 0x110 (00296799, 002967A0)
V10 LU-8 the HP and MP helpers draw the generator (00379CD0); the float helper does not
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "FFXII TZA", "_index", "candidates", "rc9-log-channels-0930"))
import rc9_channels as R  # noqa: E402
from capstone import x86 as X  # noqa: E402

at, md, ext = R.at, R.md, R.ext
F = 0x0030C650
results = []


def check(cid, ok, what):
    results.append((cid, ok))
    print("%-4s %-9s %s" % (cid, "SURVIVES" if ok else "BROKEN", what))


def body(f):
    return list(md.disasm(at(f, ext[f]), f))


def ins(a):
    i = R.dec(a)
    return "%s %s" % (i.mnemonic, i.op_str)


def imm0(i):
    return i.operands[0].imm if i.operands and i.operands[0].type == X.X86_OP_IMM else None


b = body(F)
bx = {i.address: k for k, i in enumerate(b)}
rets = [i.address for i in b if i.mnemonic == "ret"]
back = [(i.address, i.mnemonic, imm0(i)) for i in b if i.mnemonic.startswith("j") and imm0(i) is not None and imm0(i) < i.address and F <= imm0(i)]
check("V1", ext[F] == 570 and len(b) == 150 and rets == [0x0030C889] and back == [(0x0030C865, "jl", 0x0030C6A3)],
      "extent %d B, %d instructions, rets %s, back-edges %s" % (ext[F], len(b), ["%08X" % r for r in rets],
                                                                  ["%08X %s %08X" % x for x in back]))

v2 = [ins(a) for a in (0x0030C682, 0x0030C6CC, 0x0030C6D3, 0x0030C7B3, 0x0030C7B8)]
check("V2", v2[0].startswith("cmovg") and v2[1] == "cmp byte ptr [rdi + 0x1c2], 0x63" and v2[2] == "jae 0x30c85c"
      and v2[3] == "inc eax" and v2[4].startswith("cmova"), " | ".join(v2))

v3 = [ins(0x0030C686), ins(b[bx[0x0030C686] + 1].address)]
lvl_writes = [i for i in b if i.op_str.startswith("byte ptr [rdi + 0x1c2],") and i.mnemonic not in ("cmp",)]
decs = [i for i in b if i.mnemonic in ("dec", "sub") and "0x1c2" in i.op_str]
exit_ok = imm0(b[bx[0x0030C686] + 1]) is not None and imm0(b[bx[0x0030C686] + 1]) > 0x0030C865
check("V3", v3[0] == "cmp ecx, r14d" and v3[1].startswith("jge") and exit_ok and not decs,
      "%s; the jge target is past the loop: %s; level writes %s; decrements of +0x1C2: %d" % (
          " | ".join(v3), exit_ok, ["%08X %s %s" % (i.address, i.mnemonic, i.op_str) for i in lvl_writes], len(decs)))

v4n = ["%s %s" % (i.mnemonic, i.op_str) for i in b[bx[0x0030C660]:bx.get(0x0030C676, bx[0x0030C660] + 6) + 1]]
v4f = ["%s %s" % (i.mnemonic, i.op_str) for i in b[bx[0x0030C7C1]:bx[0x0030C7C7] + 1]]
notify_ok = any(x.startswith(("shr", "sar", "bt")) for x in v4n) and any(x.startswith(("not", "xor", "and", "sete", "setae", "setb")) for x in v4n)
final_ok = any("r14" in x for x in v4f) and any(x.startswith("cmp esi") for x in v4f)
check("V4", notify_ok and final_ok, "notify %s || final level %s" % (v4n, v4f))

check("V5", ins(0x0030C6D9) == "cmp byte ptr [rdi + 5], 0" and ins(b[bx[0x0030C6D9] + 1].address) == "jne 0x30c7a7",
      "%s | %s" % (ins(0x0030C6D9), ins(b[bx[0x0030C6D9] + 1].address)))

f1, f2 = R.dec(0x0030C6ED), R.dec(0x0030C6FA)
flt = []
for i in b:
    for op in i.operands:
        if op.type == X.X86_OP_MEM and md.reg_name(op.mem.base) == "rbp" and op.mem.disp in (0x1F, 0x22, 0x25, 0x28) and op.size == 1:
            flt.append(op.mem.disp)
check("V6", imm0(f1) == 0x0030C721 and imm0(f2) == 0x0030C721 and ins(0x0030C721) == "xor ebp, ebp"
      and R.dec(0x0030C730).mnemonic == "call" and R.dec(0x0030C746).mnemonic == "call" and sorted(set(flt)) == [0x1F, 0x22, 0x25, 0x28],
      "0030C6ED `%s %s`, 0030C6FA `%s %s` -> 0030C721 `%s`; growth-byte reads %s" % (
          f1.mnemonic, f1.op_str, f2.mnemonic, f2.op_str, ins(0x0030C721), sorted(set(hex(x) for x in flt))))

seg = ["%08X %s %s" % (i.address, i.mnemonic, i.op_str) for i in b[bx[0x0030C6EF]:bx[0x0030C71D] + 1]]
first_call = R.dec(0x0030C6F2).mnemonic == "call"
test1 = R.dec(0x0030C6F7).mnemonic == "test"
second_call = R.dec(0x0030C706).mnemonic == "call"
between = [s for s in seg if int(s[:8], 16) > 0x0030C706 and int(s[:8], 16) < 0x0030C71D and (" test " in s or " cmp " in s or s.split(" ")[1].startswith("j"))]
check("V7", first_call and test1 and second_call and ins(0x0030C71D) == "add ebp, eax" and not between,
      "first resolve call %s, null test at 0030C6F7 %s, second resolve call %s, 0030C71D `%s`, tests/branches between the "
      "second call and the add: %s" % (first_call, test1, second_call, ins(0x0030C71D), between))

own = [ins(a) for a in (0x0030C6BC, 0x0031B892, 0x0030C7E4, 0x0030C7ED, 0x0030C7F2, 0x0030C7FE)]
check("V8", own[0] == "call 0x31b860" and own[1] == "cmp qword ptr [rax + 0x698], rdi" and own[2] == "call 0x46a690"
      and own[3] == "test r15, r15" and own[4].endswith("[r15 + 0x698]") and own[5] == "movzx eax, byte ptr [rax + 5]",
      " | ".join(own))

# a raw E8/E9 rel32 census over the whole image (edges.tsv does not carry thunk tail jumps)
import struct  # noqa: E402


def rel32_sites(target):
    out = []
    for f in ext:
        blob = at(f, ext[f])
        for k in range(len(blob) - 4):
            if blob[k] in (0xE8, 0xE9) and f + k + 5 + struct.unpack_from("<i", blob, k + 1)[0] == target:
                i = R.dec(f + k)
                if i is not None and i.address == f + k and imm0(i) == target:
                    out.append(f + k)
    return sorted(set(out))


thunk_sites = rel32_sites(0x0035D8C0)
prod_sites = rel32_sites(0x002905D0)
v9 = [ins(0x0035D8C0), ins(0x002905EA), ins(0x002905F6), ins(0x00296799), ins(0x002967A0)]
check("V9", thunk_sites == [0x0030C815] and prod_sites == [0x0035D8C0] and v9[0] == "jmp 0x2905d0" and v9[1] == "mov edx, 6"
      and v9[2] == "lea r9d, [rdx - 5]" and "0x110" in v9[3] and v9[4].startswith("cmp "),
      "rel32 sites to 0035D8C0 %s, to 002905D0 %s; %s" % (
          ["%08X" % a for a in thunk_sites], ["%08X" % a for a in prod_sites], " | ".join(v9)))

hp, mp = imm0(R.dec(0x0030C730)), imm0(R.dec(0x0030C746))
# the float helper(s): every other call in the growth block, between the MP call and the level write
fl = sorted(set(imm0(i) for i in b if 0x0030C746 < i.address < 0x0030C7A7 and i.mnemonic == "call" and imm0(i) is not None))


def draws(f, seen=None, depth=0):
    seen = seen or set()
    if f in seen or depth > 3 or f not in ext:
        return False
    seen.add(f)
    for i in body(f):
        t = imm0(i) if i.mnemonic in ("call", "jmp") else None
        if t in (0x00379CD0, 0x00863BF0):
            return True
        if t is not None and t in ext and t != f and draws(t, seen, depth + 1):
            return True
    return False


check("V10", hp is not None and mp is not None and draws(hp) and draws(mp) and fl and not any(draws(f) for f in fl),
      "HP helper %08X draws %s; MP helper %08X draws %s; float helper(s) %s draw %s" % (
          hp or 0, draws(hp) if hp else None, mp or 0, draws(mp) if mp else None, ["%08X" % f for f in fl], [draws(f) for f in fl]))

broken = [c for c, ok in results if not ok]
print("BROKEN %d: %s" % (len(broken), " ".join(broken) or "none"))
sys.exit(0)
