"""font-kern-writer-nested-1001 - SWE2-DATA, 2026-10-01. Static; reads only.

Checks the corrected reading of the .ker pair writer 001FDC10 against the certified image
(SHA-256 73461d08..21f8, A0): the writer builds a NESTED map keyed (outer = record +4,
the LEFT/preceding cp; inner = record +0, the RIGHT/cur cp), while the only reader
001FDDD0 queries (outer = cur/right, inner = prev/left) - the key order is transposed,
so a lookup can only ever return the adjust authored for the REVERSED pair.

Checks (each is an instruction-pattern assertion on the named bodies):
  A0  image hash is the certified shipping EXE.
  L1  the .ker loader 001B5230 calls 001FDC10 with edx=[rec+0], r8d=[rec+4], r9d=[rec+8].
  W1  001FDC10 spills r8d (record +4) to its home slot and passes &slot as the key of
      001FC420(font+0x70) - the outer key is `second`, NOT dead-dropped.
  W2  001FDC10 walks the returned object's tree comparing node+0x20 against ebx (edx =
      record +0, `first`) and stores edi (adjust) at node+0x24; on miss it inserts
      through 001FC9F0.
  W3  001FC420's returned value is the outer node's +0x28 (an embedded EASTL map):
      `lea rax,[rbx+0x28]` at 001FC55C.
  W4  the inner insert 001FC9F0 allocates 0x28-byte nodes (I19) - the inner map.
  R1  reader 001FDDD0: outer sentinel font+0x78 / root font+0x88, outer key vs r8d
      (arg3 = the caller's kern cp = the CURRENT/right glyph), inner sentinel at
      outer-node+0x30 / root +0x40, inner key vs r10d = edx (arg2 = the stored
      previous cp), result at node+0x24.
  R2  the kern arm's caller chain: 002AC52F passes ecx=[rbx+0x20] (the current glyph's
      kern cp) into 0017F8E0 -> 001E9780, which forwards it to 001FDDD0's r8d and
      supplies edx = [ [rcx+0x28] + 0x20 ] (the previous glyph's kern cp).
"""
import hashlib, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
GFZ = os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")
sys.path.insert(0, os.path.abspath(GFZ))
import retool  # noqa: E402

R = retool.R
fails = []


def insns(addr, n=0x800):
    return list(R.md.disasm(R.at(addr, n), addr))


def chk(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (" -- " + detail if detail else ""))
    if not ok:
        fails.append(name)


def find(ins, pat, lo=0, hi=0):
    """first instruction matching regex 'mnemonic op_str' within [lo, hi]"""
    rx = re.compile(pat)
    for i in ins:
        if (lo and i.address < lo) or (hi and i.address > hi):
            continue
        if rx.search(i.mnemonic + " " + i.op_str):
            return i
    return None


h = hashlib.sha256(open(R.b.EXE, "rb").read()).hexdigest().upper()
chk("A0 certified image", h == "73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8", h[:12])

# L1 - the loader's call convention into 001FDC10
ld = insns(0x001B5230, 0x120)
k = next((j for j, i in enumerate(ld) if i.mnemonic == "call" and i.operands[0].imm == 0x001FDC10), None)
win = ld[max(0, (k or 0) - 8):k or 0]
txt = "\n".join(i.mnemonic + " " + i.op_str for i in win)
chk("L1 loader passes (edx,r8d,r9d)=(rec+0,rec+4,rec+8)",
    all(s in txt for s in ("mov edx, dword ptr [rbx]",
                           "mov r8d, dword ptr [rbx + 4]",
                           "mov r9d, dword ptr [rbx + 8]")))

# W1 - the writer spills r8d and keys the outer map by it
wr = insns(0x001FDC10, 0xC0)
chk("W1a writer spills r8d (record +4) to its home slot",
    find(wr, r"mov dword ptr \[rsp \+ 0x18\], r8d") is not None)
chk("W1b outer find-or-insert keys on &second: lea rdx,[rsp+0x60]; call 001FC420",
    find(wr, r"lea rdx, \[rsp \+ 0x60\]") is not None and
    any(i.mnemonic == "call" and i.operands[0].imm == 0x001FC420 for i in wr))
chk("W1c the map object is font+0x70", find(wr, r"add rcx, 0x70") is not None)

# W2 - inner walk keys on ebx (= edx = record +0); adjust stored at node+0x24
chk("W2a ebx = edx (record +0) is the inner key", find(wr, r"mov ebx, edx") is not None)
chk("W2b inner compare: [node+0x20] vs ebx", find(wr, r"cmp dword ptr \[r8 \+ 0x20\], ebx") is not None)
chk("W2c inner hit stores adjust (edi) at node+0x24", find(wr, r"mov dword ptr \[rcx \+ 0x24\], edi") is not None)
chk("W2d inner miss inserts through 001FC9F0",
    any(i.mnemonic == "call" and i.operands[0].imm == 0x001FC9F0 for i in wr))

# W3 - 001FC420 returns the outer node's embedded map at +0x28
fo = insns(0x001FC420, 0x200)
chk("W3 find-or-insert returns lea rax,[node+0x28]",
    find(fo, r"lea rax, \[rbx \+ 0x28\]") is not None)

# W4 - inner insert allocates I19 nodes (0x28 bytes)
ins19 = insns(0x001FC9F0, 0x300)
chk("W4 inner insert requests 0x28-byte nodes",
    any(i.mnemonic == "mov" and "0x28" in i.op_str for i in ins19))

# R1 - the reader's key order is the transposed one
rd = insns(0x001FDDD0, 0x90)
chk("R1a outer tree: sentinel rcx+0x78, root [rcx+0x88]",
    find(rd, r"lea rdx, \[rcx \+ 0x78\]") is not None and
    find(rd, r"mov rax, qword ptr \[rcx \+ 0x88\]") is not None)
chk("R1b outer key compare vs r8d (the CURRENT cp)", find(rd, r"cmp dword ptr \[rax \+ 0x20\], r8d") is not None)
chk("R1c inner tree lives in the outer node: sentinel node+0x30, root [node+0x40]",
    find(rd, r"lea rdx, \[r9 \+ 0x30\]") is not None and
    find(rd, r"mov rcx, qword ptr \[r9 \+ 0x40\]") is not None)
chk("R1d inner key compare vs r10d = edx (the PREVIOUS cp)",
    find(rd, r"mov r10d, edx") is not None and
    find(rd, r"cmp dword ptr \[rcx \+ 0x20\], r10d") is not None)
chk("R1e kern value returned from inner node +0x24", find(rd, r"mov eax, dword ptr \[rax \+ 0x24\]") is not None)

# R2 - the caller chain supplies (cur -> r8d, prev -> edx)
mid = insns(0x001E9780, 0x30)
chk("R2a 001E9780 forwards its edx to r8d and takes edx from [obj+0x20]",
    find(mid, r"mov r8d, edx") is not None and find(mid, r"mov edx, dword ptr \[rax \+ 0x20\]") is not None)
arm = insns(0x002AC2F0, 0x260)
chk("R2b kern arm passes ecx = [rbx+0x20] (the current glyph's kern cp)",
    find(arm, r"mov ecx, dword ptr \[rbx \+ 0x20\]", lo=0x002AC520) is not None and
    any(i.mnemonic == "call" and i.operands[0].imm == 0x0017F8E0 for i in arm))

print("FAILS %d" % len(fails))
sys.exit(1 if fails else 0)
