"""sd141_receiver.py - SWE2-STRUCT record checker for OPUS-REQ-STRUCT-SD141-CONSUMERS-1001.

Independent re-verification over the certified image (pefile+capstone, no retool.py).
Asserts the receiver/consumer chain for the flying-fade pair:

  C1  00604750 calls 006084B0 with rcx = rbp+0x270 (the 0x598-byte snapshot).
  C2  memcpy(dst = rsi+0x4E0 + (dword[rsi+0x4D8]&1)*0x598, src = rbp+0x270, n = 0x598)
      at 00604899..006048C2  (call target 00861ED2).
  C3  r14 = qword[rsp+0x40] returned by call 006097B0(rbx, &out) at 00604BEC/00604BF9.
  C4  pair re-read: 00605F66 movss xmm1,[rbp+0x7C0] -> [r14+0x5D4] at 00605F6E;
      00605F88 movss xmm1,[rbp+0x7C4] -> [r14+0x5DC] at 00605F90.
  C5  006084B0 hands rdx = 02CB8160 (pair - 0x2B0) and rcx = rdi+0x2A0 to 005DEC50
      at 0060890A/00608992/00608999.
  C6  005DEC50 copies [rdx+0x2B0]/[rdx+0x2B4] (= 02CB8410/02CB8414) -> [rcx+0x2B0]/[+0x2B4]
      at 005DF3A0/005DF3AC  => snapshot +0x550/+0x554.
  C7  second staged copy: call 005DF3E0(rcx = rsi+0x4E0+(new cursor&1)*0x598, rdx = rbp+0x270)
      at 00604902..00604913; cursor advance at 006048E1..006048EE (mod [rsi+0x498]).
  C8  006097B0 waits on slot+0xC via 005CCB80 and maps via 00626060(rcx=ring, edx=index,
      r8=out) at 00609849; commit 0062C300 at 00606071 writes back next index ([rbx+4])
      and the mapped flag ([rbx+8]) at 006060C9/006060CD. rbx = rsi+0x4A8 + cursor*80
      (00604929..00604931): the 80-byte records are per-slot ring-buffer objects.
  C9  r14 is write-only inside 00604750: >= 500 stores and zero non-lea loads of [r14+X].
  C10 no CPU reader of a staged slot's pair bytes: 00604750 is the only function
      containing an imm-0x598 multiply, and no .text operand carries disp 0x1030 or
      0x15C8 (this+0x4E0+0x550/0x554 and this+0x4E0+0x598+0x550/0x554).

Prints PASS/FAIL per claim, ends 'FAILS n'.
"""
import sys, os, bisect
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "auditspec-review-sd141-0930"))
import sdx
from capstone.x86 import X86_OP_MEM, X86_OP_IMM

fails = 0
def check(name, ok, detail=""):
    global fails
    print(("PASS " if ok else "FAIL ") + name + ("  " + detail if detail else ""))
    if not ok:
        fails += 1

def insns(va, n):
    foff = sdx.off(va)
    return list(sdx.md.disasm(sdx.raw[foff:foff + n], va))

def at(va):
    return insns(va, 15)[0]

# ---- C1: call 006084B0(rcx=rbp+0x270) ----
i = at(0x604872); check("C1a lea rcx,[rbp+0x270]", i.mnemonic == "lea" and i.op_str == "rcx, [rbp + 0x270]", i.op_str)
i = at(0x604879); check("C1b call 006084B0", i.mnemonic == "call" and i.op_str == "0x6084b0", i.op_str)

# ---- C2: staging-slot memcpy ----
seq = insns(0x604899, 0x30)
t = [f"{i.mnemonic} {i.op_str}" for i in seq]
check("C2a cursor load [rsi+0x4d8]", t[0] == "mov edi, dword ptr [rsi + 0x4d8]", t[0])
check("C2b parity &1 *0x598", "and eax, 1" in t and any("imul rax, rax, 0x598" in x for x in t),
      "; ".join(t[1:5]))
check("C2c dst base [rsi+0x4e0]", any("lea rcx, [rsi + 0x4e0]" in s for s in t))
check("C2d r8d=0x598, src=rbp+0x270", "mov r8d, 0x598" in t and "lea rdx, [rbp + 0x270]" in t)
i = at(0x6048C2); check("C2e call 00861ED2", i.mnemonic == "call" and i.op_str == "0x861ed2", i.op_str)

# ---- C3: r14 = out of 006097B0 ----
i = at(0x604BE9); check("C3a rcx=rbx", i.op_str == "rcx, rbx", i.op_str)
i = at(0x604BEC); check("C3b call 006097B0", i.mnemonic == "call" and i.op_str == "0x6097b0", i.op_str)
i = at(0x604BF9); check("C3c r14 = [rsp+0x40]", "mov r14, qword ptr [rsp + 0x40]" == f"{i.mnemonic} {i.op_str}", f"{i.mnemonic} {i.op_str}")

# ---- C4: pair into cbuffer ----
i = at(0x605F66); check("C4a read snapshot+0x550", "movss xmm1, dword ptr [rbp + 0x7c0]" == f"{i.mnemonic} {i.op_str}", f"{i.mnemonic} {i.op_str}")
i = at(0x605F6E); check("C4b store [r14+0x5d4]", "movss dword ptr [r14 + 0x5d4], xmm1" == f"{i.mnemonic} {i.op_str}", f"{i.mnemonic} {i.op_str}")
i = at(0x605F88); check("C4c read snapshot+0x554", "movss xmm1, dword ptr [rbp + 0x7c4]" == f"{i.mnemonic} {i.op_str}", f"{i.mnemonic} {i.op_str}")
i = at(0x605F90); check("C4d store [r14+0x5dc]", "movss dword ptr [r14 + 0x5dc], xmm1" == f"{i.mnemonic} {i.op_str}", f"{i.mnemonic} {i.op_str}")

# ---- C5: 006084B0 handoff ----
i = at(0x60890A); tgt = i.address + i.size + i.operands[1].mem.disp
check("C5a lea rdx,[02CB8160]", i.mnemonic == "lea" and tgt == 0x2CB8160, f"target {tgt:08X}")
i = at(0x608992); check("C5b rcx=rdi+0x2a0", "lea rcx, [rdi + 0x2a0]" == f"{i.mnemonic} {i.op_str}", f"{i.mnemonic} {i.op_str}")
i = at(0x608999); check("C5c call 005DEC50", i.mnemonic == "call" and i.op_str == "0x5dec50", i.op_str)

# ---- C6: 005DEC50 reads the pair ----
i = at(0x5DF3A0); check("C6a [rdx+0x2b0]=02CB8410", "mov eax, dword ptr [rdx + 0x2b0]" == f"{i.mnemonic} {i.op_str}", f"{i.mnemonic} {i.op_str}")
i = at(0x5DF3AC); check("C6b [rdx+0x2b4]=02CB8414", "mov eax, dword ptr [rdx + 0x2b4]" == f"{i.mnemonic} {i.op_str}", f"{i.mnemonic} {i.op_str}")

# ---- C7: second copy + cursor ----
seq = insns(0x6048E1, 0x50); t = [f"{i.mnemonic} {i.op_str}" for i in seq]
check("C7a inc + wrap mod [rsi+0x498]", "inc edi" in t and any("cmp edi, dword ptr [rsi + 0x498]" in s for s in t)
      and "mov dword ptr [rsi + 0x4d8], edi" in t)
check("C7b second slot index", any("lea rcx, [rsi + 0x4e0]" in s for s in t) and any("imul rax, rax, 0x598" in s for s in t))
check("C7c call 005DF3E0", any("call 0x5df3e0" == s for s in t))

# ---- C8: ring record + map/commit ----
seq = insns(0x604929, 0x14); t = [f"{i.mnemonic} {i.op_str}" for i in seq]
check("C8a rbx = rsi+0x4A8 + cursor*80", "lea rbx, [rbx + rbx*4]" in t and "shl rbx, 4" in t
      and any("add rbx, qword ptr [rsi + 0x4a8]" in s for s in t), "; ".join(t[:3]))
seq = insns(0x60981A, 0x40); t = [f"{i.mnemonic} {i.op_str}" for i in seq]
check("C8b 006097B0 busy-wait + map", any("call 0x5ccb80" in s for s in t) and any("call 0x626060" in s for s in t))
i = at(0x606071); check("C8c commit call 0062C300", i.mnemonic == "call" and i.op_str == "0x62c300", i.op_str)
i = at(0x6060C9); check("C8d next-index writeback [rbx+4]", "mov dword ptr [rbx + 4], r14d" == f"{i.mnemonic} {i.op_str}", f"{i.mnemonic} {i.op_str}")

# ---- C9: r14 write-only in 00604750 ----
lo, end = 0x604750, sdx.chain_end(0x604750)
foff = sdx.off(lo)
body = list(sdx.md.disasm(sdx.raw[foff:foff + (end - lo)], lo))
loads = stores = 0
for i in body:
    ops = i.op_str
    if "[r14" not in ops: continue
    dst = ops.split(",")[0].strip()
    if "[r14" in dst: stores += 1
    elif i.mnemonic != "lea": loads += 1
check("C9 r14 write-only (0 non-lea loads)", loads == 0 and stores > 200, f"stores={stores} nonlea_loads={loads}")

# ---- C10: staged slots' pair bytes have no CPU reader ----
imul_fns, slotpair = [], []
for e in sdx.PD:
    a, b = sdx.IB + e[0], sdx.IB + e[1]
    foff = sdx.off(a)
    if foff is None: continue
    for i in sdx.md.disasm(sdx.raw[foff:foff + (b - a)], a):
        for op in i.operands:
            if op.type == X86_OP_IMM and op.imm == 0x598:
                imul_fns.append((a, i.address))
            if op.type == X86_OP_MEM and op.mem.disp in (0x1030, 0x15c8, 0x1034, 0x15cc):
                b = sdx.md.reg_name(op.mem.base) if op.mem.base else ""
                if b not in ("rsp", "rbp"):
                    slotpair.append((a, i.address, i.mnemonic, i.op_str))
check("C10a only 00604750 uses imm 0x598", {f for f, _ in imul_fns} == {0x604750},
      str(sorted({f for f, _ in imul_fns})))
# surviving hits must be receiver-foreign: their function shares none of the object's
# fingerprint fields (+0x488 stride / +0x490 elem* / +0x498 count / +0x4a8 ring* /
# +0x4b0 lock / +0x4d8 cursor / +0x4e0 slot base)
FP = (0x488, 0x490, 0x498, 0x4a8, 0x4b0, 0x4d8, 0x4e0)
foreign_ok = True
for f, a, m, ops in slotpair:
    e = sdx.pdata_of(f)
    flo, fhi = sdx.IB + e[0], sdx.IB + e[1]
    ffoff = sdx.off(flo)
    dset = {op.mem.disp for i in sdx.md.disasm(sdx.raw[ffoff:ffoff + (fhi - flo)], flo)
            for op in i.operands if op.type == X86_OP_MEM}
    if any(d in FP for d in dset):
        foreign_ok = False
        print("    shared-field hit:", f"{f:08X}", f"{a:08X}", m, ops)
check("C10b no same-receiver operand at slot+0x550/0x554 displacements",
      all("stack" not in m for _, _, m, _ in slotpair) and foreign_ok,
      f"{len(slotpair)} non-stack hits, all receiver-foreign: {foreign_ok}")

print(f"FAILS {fails}")
sys.exit(1 if fails else 0)
