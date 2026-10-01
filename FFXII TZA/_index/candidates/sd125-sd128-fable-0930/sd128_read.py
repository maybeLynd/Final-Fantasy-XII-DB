"""sd128_read.py - SD-128: 002C7660 read whole (FABLE helper, Claude Opus 5.5, 2026-09-30). Static, read-only.

Every claim in README.md section SD-128 is an instruction-level check here. The function is 1,190 bytes, ends in one
ret at 002C7B05, and contains no indirect jump (so no jump-table slots to read; checked).

  R0 extent: functions.tsv size 1190; decoded to the ret; no `jmp reg` and no `jmp [mem]` in the body.
  R1 callers: raw rel32 index (E8/E9/0F8x) over all of .text, rip-relative lea of the entry from every listed
     function, and DIR64 relocations -> one caller, 002C632F in 002C62B0's walk of the [hud+0x1D70] list.
     Control: the same index finds 002C62B0's own caller 0028EDAD (the menu draw 0028EAB0).
  R2 the argument map (what each register / stack slot is, from 002C62B0's call).
  R3..R9 the per-node computation, in execution order.
Exit 1 on any FAIL.
"""
import os, sys, struct
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "Tools", "work", "FABLE", "takebacks"))
import tk
from capstone.x86 import X86_OP_MEM, X86_OP_REG, X86_OP_IMM

FAILS = 0
def check(name, ok, detail=""):
    global FAILS
    if not ok: FAILS += 1
    print("%s  %s%s" % ("PASS" if ok else "FAIL", name, ("  " + detail) if detail else ""))

F = 0x002C7660
body = tk.fdis(F); by = {x.address: x for x in body}
def op(a): x = by.get(a); return None if x is None else (x.mnemonic, x.op_str)
def is_(a, mn, ops): return op(a) == (mn, ops)
def f32(a): return struct.unpack_from("<f", tk.d, tk.off(a))[0]

# ---------------------------------------------------------------- R0
rets = [x.address for x in body if x.mnemonic == "ret"]
ind = [x.address for x in body if x.mnemonic == "jmp" and not x.op_str.startswith("0x")]
check("R0 002C7660 is 1,190 B, decodes to a single ret at 002C7B05, and has no indirect jmp (no jump table to read)",
      tk.fsize(F) == 1190 and rets == [0x002C7B05] and body[-1].address == 0x002C7B05 and not ind, "rets %s indirect %s" % (rets, ind))

# ---------------------------------------------------------------- R1 callers
TXT = tk.d[tk.TRO:tk.TRO + min(tk.TVS, tk.TRS)]
def raw_calls(targets):
    out = []
    for i in range(len(TXT) - 5):
        b = TXT[i]
        if b in (0xE8, 0xE9): ln, k = 5, 1
        elif b == 0x0F and 0x80 <= TXT[i + 1] <= 0x8F: ln, k = 6, 2
        else: continue
        rel = struct.unpack_from("<i", TXT, i + k)[0]; va = tk.TVA + i; t = va + ln + rel
        if t in targets:
            bb = tk.boundaries(va)
            out.append((va, t, bb is not None and va in bb))
    return out
rc = raw_calls({F, 0x002C62B0})
to_f = [(a, ok) for a, t, ok in rc if t == F]
to_c = [(a, ok) for a, t, ok in rc if t == 0x002C62B0]
lea_refs = []
for e, sz in tk.flist:
    if sz <= 0 or sz > 0x40000 or tk.sec_of(e) != ".text": continue
    try: ins = tk.dis(e, e + sz)
    except Exception: continue
    for y in ins:
        for o in y.operands:
            if o.type == X86_OP_MEM and o.mem.base != 0 and y.reg_name(o.mem.base) == "rip" and y.address + y.size + o.mem.disp == F:
                lea_refs.append(y.address)
        if y.mnemonic in ("mov", "lea") and any(o.type == X86_OP_IMM and o.imm == F for o in y.operands):
            lea_refs.append(y.address)
rel = tk.reloc_ptrs(F, F + 1)
print("R1 raw rel32 hits on 002C7660: %s ; on 002C62B0: %s ; rip/imm references: %s ; relocations: %s" % (
    ["%08X%s" % (a, "" if ok else " (off-boundary)") for a, ok in to_f], ["%08X" % a for a, ok in to_c], ["%08X" % a for a in lea_refs], rel))
check("R1 control: the index finds 0028EDAD -> 002C62B0 (in the menu draw 0028EAB0)", (0x0028EDAD, True) in to_c)
check("R1 002C7660 has one caller, 002C632F in 002C62B0, and its address is taken nowhere (no rip/imm reference, no relocation)",
      [a for a, ok in to_f if ok] == [0x002C632F] and not lea_refs and not rel)
cb = {x.address: x for x in tk.fdis(0x002C62B0)}
check("R1 002C62B0 calls it once per node of the list at [hud+0x1D70] (002C62F1 load, 002C6334 next = [node+0x18], 002C633B loop)",
      cb[0x002C62F1].op_str == "rbx, qword ptr [rsi + 0x1d70]" and cb[0x002C6334].op_str == "rbx, qword ptr [rbx + 0x18]" and cb[0x002C633B].op_str == "0x2c6310")
mb = {x.address: x for x in tk.dis(0x0028ED7E, 0x0028EDB2)}
check("R1 hud = [[0209BE80]+0x10F80], drawn under menu-draw layer bit 2 (0028ED7E test dil, 4; 0028ED84/0028ED8B)",
      mb[0x0028ED7E].op_str == "dil, 4" and mb[0x0028ED84].operands[1].mem.disp + 0x0028ED8B == 0x0209BE80 and mb[0x0028ED8B].op_str == "rcx, qword ptr [rax + 0x10f80]")

# ---------------------------------------------------------------- R2 arguments
check("R2 args: rcx -> r14 (hud, 002C7696); rdx -> rdi (node, 002C76AC); r8 -> [rbp-0x51] (002C76BA); r9 -> r12 (002C76A5); arg5 [rbp+0x6f] -> r13; arg8 [rbp+0x87] -> [rbp-0x69]; arg7 [rbp+0x7f] is the HUD-path gate",
      is_(0x002C7696, "mov", "r14, rcx") and is_(0x002C76AC, "mov", "rdi, rdx") and is_(0x002C76BA, "mov", "qword ptr [rbp - 0x51], r8")
      and is_(0x002C76A5, "mov", "r12, r9") and is_(0x002C76A8, "mov", "r13, qword ptr [rbp + 0x6f]") and is_(0x002C768F, "mov", "rax, qword ptr [rbp + 0x87]")
      and is_(0x002C76AF, "mov", "qword ptr [rbp - 0x69], rax") and is_(0x002C783C, "cmp", "dword ptr [rbp + 0x7f], esi"))
check("R2 arg6 ([rbp+0x77]) is never read in the body", not any("rbp + 0x77" in x.op_str for x in body))
check("R2 from the caller: arg7 = (002E0FA0() >> 10) & 1 (002C62D8-002C62E2, passed 002C6318); arg8 = 003588B0(003590D0()), the focus unit (002C62E5-002C62F8, passed 002C6310)",
      cb[0x002C62D8].op_str == "0x2e0fa0" and cb[0x002C62DF].op_str == "edi, 0xa" and cb[0x002C62E2].op_str == "edi, 1"
      and cb[0x002C62E5].op_str == "0x3590d0" and cb[0x002C62EC].op_str == "0x3588b0" and cb[0x002C6318].op_str == "dword ptr [rsp + 0x30], edi"
      and cb[0x002C6310].op_str == "qword ptr [rsp + 0x38], r13")

# ---------------------------------------------------------------- R3 level
check("R3 level = (int)(00272DE0(node+0x10) * ((word hud+0x1D78 * byte node+0x14) >> 7)) -> [rbp-0x79]",
      is_(0x002C7699, "movsx", "ebx, word ptr [rcx + 0x1d78]") and is_(0x002C76B3, "movzx", "eax, byte ptr [rdx + 0x14]")
      and is_(0x002C76B7, "imul", "ebx, eax") and is_(0x002C76C1, "sar", "ebx, 7") and is_(0x002C76A2, "mov", "ecx, dword ptr [rdx + 0x10]")
      and is_(0x002C76C4, "call", "0x272de0") and is_(0x002C76D3, "mulss", "xmm0, xmm1") and is_(0x002C76DB, "mov", "dword ptr [rbp - 0x79], eax"))
d = {x.address: x for x in tk.fdis(0x00272DE0)}
check("R3 00272DE0(handle) = 0.0 when 003588B0 resolves no unit, else 002E7E90(unit) (tail jump 00272DFD)",
      d[0x00272DE4].op_str == "0x3588b0" and d[0x00272DEE].op_str == "xmm0, xmm0" and d[0x00272DFD].op_str == "0x2e7e90")

# ---------------------------------------------------------------- R4 unit and class
t = tk.dis(0x0035D4F0, 0x0035D4F8)[0]
check("R4 unit = 0035D4F0()[node+0x2E] with 0035D4F0 returning the table 022C8700 (002C76DE-002C76E8); class = 00263C20(unit) -> r15d",
      t.address + t.size + t.operands[1].mem.disp == 0x022C8700 and is_(0x002C76E3, "movsx", "rcx, word ptr [rdi + 0x2e]")
      and is_(0x002C76E8, "mov", "rbx, qword ptr [rax + rcx*8]") and is_(0x002C76F3, "call", "0x263c20") and is_(0x002C7704, "mov", "r15d, eax"))

# ---------------------------------------------------------------- R5 mode
t = tk.dis(0x0035BAD0, 0x0035BAD7)[0]
check("R5 mode [rsp+0x50] and float [rbp-0x75] come from 002ED0B0(handle) (mode 1 / 0.0 when the unit or its model is absent, 002ED116), and 0035BAD0 returns dword 022C806C, the battle-menu selection state's current focus handle",
      is_(0x002C7707, "call", "0x2ed0b0") and t.address + t.size + t.operands[1].mem.disp == 0x022C806C
      and tk.dis(0x002ED116, 0x002ED11C)[0].op_str == "dword ptr [rdi], 1")
check("R5 when 0037C8F0() (-> 003135C0) is non-zero: class != 8 and focus == handle -> mode 1, and then 00273460() != 0 -> init flag [rbp-0x7d] = 1 (002C770C-002C773E); otherwise focus == handle -> mode 1 (002C7743-002C7757)",
      is_(0x002C770C, "call", "0x37c8f0") and is_(0x002C771D, "cmp", "eax, 8") and is_(0x002C7727, "cmp", "eax, dword ptr [rdi + 0x10]")
      and is_(0x002C7731, "mov", "dword ptr [rsp + 0x50], ebx") and is_(0x002C7735, "call", "0x273460") and is_(0x002C773E, "mov", "dword ptr [rbp - 0x7d], ebx")
      and is_(0x002C7754, "cmove", "ecx, ebx") and tk.dis(0x0037C8F0, 0x0037C8F5)[0].op_str == "0x3135c0")
a4 = {x.address: x for x in tk.fdis(0x00273460)}
check("R5 00273460 returns the handle (+4) of the first accepted battle-menu member slot (0035BB20) whose flags byte has bit 2, else 0",
      a4[0x00273473].op_str == "0x35bb20" and a4[0x00273478].op_str == "byte ptr [rax], 4" and a4[0x0027349C].op_str == "eax, dword ptr [rax + 4]")

# ---------------------------------------------------------------- R6 the mode-2 vector
check("R6 V [rbp-0x61] = the zero vector 01EF93F0, and when mode == 2: V = 002708B0(00202DE0(02AED5F0 - node.xyzw), f) - (002C775B-002C77C1)",
      is_(0x002C775B, "cmp", "dword ptr [rsp + 0x50], 2") and by[0x002C7763].address + by[0x002C7763].size + by[0x002C7763].operands[1].mem.disp == 0x01EF93F0
      and is_(0x002C7798, "call", "0x203080") and is_(0x002C77A8, "call", "0x202de0") and is_(0x002C77AD, "movss", "xmm2, dword ptr [rbp - 0x75]")
      and is_(0x002C77C1, "call", "0x2708b0") and by[0x002C777C].address + by[0x002C777C].size + by[0x002C777C].operands[1].mem.disp == 0x02AED5F0)
s3 = {x.address: x for x in tk.fdis(0x00203080)}; s8 = {x.address: x for x in tk.fdis(0x002708B0)}
check("R6 helper semantics: 00203080(dst, a, b) = a - b per component (00203088 subss xmm0, [r8]); 002708B0(dst, v, s) = v.xyz * s, w copied",
      s3[0x00203088].op_str == "xmm0, dword ptr [r8]" and s8[0x002708B6].op_str == "xmm0, dword ptr [rdx]" and s8[0x002708D5].op_str == "dword ptr [rcx + 0xc], eax")

# ---------------------------------------------------------------- R7 gauge kind
check("R7 kind ebx: 0 when 00273320(handle) >= 0 (the unit is an accepted battle-menu member); else by class: 1, 2, 7 -> 1 + (00322950(handle) == 1); 3, 8 -> 2 if 003229A0(handle) == 1 else 0; any other class -> -1",
      is_(0x002C77C9, "call", "0x273320") and is_(0x002C77D0, "js", "0x2c77d6") and is_(0x002C77D2, "mov", "ebx, esi")
      and is_(0x002C77DB, "cmp", "r15d, 2") and is_(0x002C77E1, "cmp", "r15d, 3") and is_(0x002C77E7, "cmp", "r15d, 7") and is_(0x002C77ED, "cmp", "r15d, 8")
      and is_(0x002C77F6, "call", "0x3229a0") and is_(0x002C7805, "cmove", "ebx, ecx") and is_(0x002C780D, "call", "0x322950")
      and is_(0x002C7817, "sete", "bl") and is_(0x002C781A, "inc", "ebx") and is_(0x002C781E, "or", "ebx, 0xffffffff") and is_(0x002C77D9, "jle", "0x2c781e"))
a3 = {x.address: x for x in tk.fdis(0x00273320)}
check("R7 00273320(handle) = index k of the accepted member slot whose 0035BB00(k) equals the handle, else -1 (and -1 for handle 0)",
      a3[0x00273347].op_str == "0x35bb00" and a3[0x0027334C].op_str == "edi, eax" and a3[0x0027332C].op_str == "eax, 0xffffffff")

# ---------------------------------------------------------------- R8 the four element calls and their gates
check("R8 002C8920(node, level, r12, r13) runs when the init flag [rbp-0x7d] is set (002C7825-002C7837)",
      is_(0x002C7825, "cmp", "dword ptr [rbp - 0x7d], esi") and is_(0x002C7837, "call", "0x2c8920") and is_(0x002C7830, "movzx", "edx, r15w"))
check("R8 the gauge/status pair runs only when arg7 == 0, kind >= 0 and node+0x17 bit 1: 002C8310 (HP gauge) additionally needs hud+0x1D7A bit 0 and takes kind as its 7th arg; 002C7B10 (overhead status) always runs inside the gate and takes hud+0x1D7A & 1 as its 7th arg; both take unit, level, r8-arg, r12, r13, mode and &V",
      is_(0x002C783F, "jne", "0x2c78dc") and is_(0x002C7847, "js", "0x2c78dc") and is_(0x002C784D, "test", "byte ptr [rdi + 0x17], 2")
      and is_(0x002C7857, "test", "byte ptr [r14 + 0x1d7a], 1") and is_(0x002C787D, "mov", "dword ptr [rsp + 0x30], ebx") and is_(0x002C7892, "call", "0x2c8310")
      and is_(0x002C78AD, "and", "ecx, 1") and is_(0x002C78C4, "mov", "dword ptr [rsp + 0x30], ecx") and is_(0x002C78D5, "call", "0x2c7b10")
      and is_(0x002C7879, "mov", "dword ptr [rsp + 0x38], eax") and is_(0x002C7869, "mov", "qword ptr [rsp + 0x40], rax"))
check("R8 002C8820(node, level, r8-arg, r12, r13) runs when byte node+0x2C != 0 (002C78E0-002C78F8)",
      is_(0x002C78E0, "cmp", "byte ptr [rdi + 0x2c], sil") and is_(0x002C78F8, "call", "0x2c8820"))

# ---------------------------------------------------------------- R9 the label slots
check("R9 then it looks for this unit among two 0x1C0-byte slots (hud+0x19B0 + i*0x1C0): flags +4 bit 0 set and handle [slot] == node+0x10; none -> return (002C78FD-002C791F)",
      is_(0x002C78FD, "lea", "rcx, [r14 + 0x19b0]") and is_(0x002C7904, "test", "byte ptr [rcx + 4], 1") and is_(0x002C790D, "cmp", "dword ptr [rcx], eax")
      and is_(0x002C7913, "add", "rcx, 0x1c0") and is_(0x002C791A, "cmp", "esi, 2") and is_(0x002C791F, "jmp", "0x2c7ade"))
check("R9 positions: P = focus unit's 002E9CA0 point (or 02AED5F0 when there is no focus handle), Q = this unit's 002E9CA0 point; slot +0x18D0 = 002E9A90(handle) when flag bit 3 else a copy of the node's vec4; slot +0x19B8 = node+0x14",
      is_(0x002C7924, "call", "0x3590d0") and is_(0x002C7947, "call", "0x2e9ca0") and is_(0x002C7954, "call", "0x2e9ca0")
      and is_(0x002C7963, "test", "byte ptr [rsi + r14 + 0x19b4], 8") and is_(0x002C797B, "call", "0x2e9a90") and is_(0x002C798F, "call", "0x202c90")
      and is_(0x002C79A0, "mov", "dword ptr [rsi + r14 + 0x19b8], eax"))
c3, c08, c02, c1 = f32(0x008F311C), f32(0x008F3108), f32(0x00916F24), f32(0x01CEBBA8)
check("R9 distance scale: d = |Q - P| (00203080, 00270550 = sqrt of the xyz dot), R = hud+0x1D7C; scale = 1.0 when d <= R/3 (or R <= 0), 0.8 when d >= R, else 0.8 + 0.2 * (R - d) / (2R/3); stored to slot +0x1834",
      (c3, round(c08, 6), round(c02, 6), c1) == (3.0, 0.8, 0.2, 1.0) and is_(0x002C79AC, "call", "0x203080") and is_(0x002C79B5, "call", "0x270550")
      and is_(0x002C79BA, "movss", "xmm2, dword ptr [r14 + 0x1d7c]") and is_(0x002C79C9, "divss", "xmm1, dword ptr [rip + 0x62b74b]")
      and is_(0x002C79EE, "subss", "xmm2, xmm0") and is_(0x002C79F2, "divss", "xmm2, xmm3") and is_(0x002C7A14, "movss", "dword ptr [rsi + r14 + 0x1834], xmm2"),
      "constants 3.0=%r 0.8=%r 0.2=%r 1.0=%r; continuity at d = R/3: %.4f, at d = R: %.4f" % (c3, c08, c02, c1, c08 + c02 * (1 - 1 / 3) / (2 / 3), c08 + c02 * 0))
cd = {x.address: x for x in tk.fdis(0x0029CD00)}
check("R9 extent: 0029CD00(slot+0x1930, 0, scale) = 002B3050's text width/height times the scale -> slot +0x18F4 = w, +0x18F6 = h, +0x18F0 = -(w >> 1), +0x18F2 = -(h >> 1); slot +0x19B8 is then overwritten with the level",
      is_(0x002C7A1E, "lea", "rcx, [r14 + 0x1930]") and is_(0x002C7A33, "call", "0x29cd00") and cd[0x0029CD24].op_str == "0x2b3050" and cd[0x0029CD3D].op_str == "xmm0, xmm6"
      and is_(0x002C7A3E, "mov", "word ptr [rsi + r14 + 0x18f4], ax") and is_(0x002C7A4C, "mov", "word ptr [rsi + r14 + 0x18f6], cx")
      and is_(0x002C7A5A, "mov", "word ptr [rsi + r14 + 0x18f0], ax") and is_(0x002C7A78, "mov", "word ptr [rsi + r14 + 0x18f2], cx")
      and is_(0x002C7A70, "mov", "dword ptr [rsi + r14 + 0x19b8], eax") and is_(0x002C7A6C, "movsx", "eax, r15w"))
check("R9 flag bit 2: +0x18F2 -= 0024ABA0() * ((glyph entry [+4] >> 12) & 0xFFF) from 0035D3D0's font table (002C7A63-002C7AD5)",
      is_(0x002C7A63, "test", "byte ptr [rsi + r14 + 0x19b4], 4") and is_(0x002C7A83, "call", "0x35d3d0") and is_(0x002C7AB0, "call", "0x24aba0")
      and is_(0x002C7AB9, "shr", "eax, 0xc") and is_(0x002C7ACD, "subss", "xmm6, xmm0") and is_(0x002C7AD5, "mov", "word ptr [rsi + r14 + 0x18f2], ax"))
pb = {x.address: x for x in tk.fdis(0x002C62B0)}
check("R9 the slot is a 0x1C0-byte draw record at hud+0x1800 + i*0x1C0: 002C62B0 appends each active one to its 5th argument's list through 003F14D0 (002C6381 lea rdx, [rbx-0x1b6] with rbx = hud+0x19B6; 002C6391)",
      pb[0x002C6359].op_str == "rbx, [rsi + 0x19b6]" and pb[0x002C6381].op_str == "rdx, [rbx - 0x1b6]" and pb[0x002C6391].op_str == "0x3f14d0")

# ---------------------------------------------------------------- R10 what it reads (and does not)
callees = sorted(set(int(x.op_str, 16) for x in body if x.mnemonic == "call" and x.op_str.startswith("0x")))
print("R10 direct callees (%d): %s" % (len(callees), " ".join("%08X" % c for c in callees)))
SV = {0x00329220, 0x0031FE70, 0x00320040, 0x0031FEC0, 0x0031FF70}
node_reads = sorted(set(x.op_str.split("[rdi + ")[1].split("]")[0] for x in body if "[rdi + " in x.op_str))
print("    node (rdi) displacements read: %s" % node_reads)
check("R10 no indirect call, and none of the StatusView builder 00329220 or its four callers (0031FE70, 00320040, 0031FEC0, 0031FF70) is called: the node it evaluates is the hud list node (+0x10 dword handle, +0x14, +0x17, +0x2C, +0x2E), not the 0xC0 StatusView record (whose +0x10 is the name pointer)",
      not (SV & set(callees)) and not any(x.mnemonic == "call" and not x.op_str.startswith("0x") for x in body)
      and set(node_reads) == {"0x10", "0x14", "0x17", "0x2c", "0x2e"} and is_(0x002C76A2, "mov", "ecx, dword ptr [rdx + 0x10]"))
print("FAILS %d" % FAILS)
sys.exit(1 if FAILS else 0)
