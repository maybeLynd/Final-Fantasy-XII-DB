"""Falsification pass 1 on the-indexed-source-request-from-arm-to-terminal-pump (OPUS, 2026-09-30), from the shipping
image. SECTION-09's executions are carried, not re-run; these checks pin the static clauses the page rests on.

  I1  sections 1-2: the armer 003DDA20 indexes owners at 02B581A0 + (g*16 + i) * 0x1C, accepts only state 0, stores the
      annotation at +8, writes state 2, ORs 1 << i into the mask at 02B58A60 + 4g, returns 1, else 0
  I2  section 3: 0032F240 reads the enable byte 022C6D18 + g and the selector dword 022C6D28 + 4g (-1 when disabled);
      0032F170 maps group 0 (and below) to kind 5 / 3 * sel, groups 1-3 to kind 8 / 4 * sel, group 4 to kind 1 / sel + 0x6B;
      0032F290 / 0032F260 refuse g > 3 with -1, test the metadata pointer's first byte at 022C6E70 + 8g, and read the
      length at +0xC + 8i and the offset at +8 + 8i
  I3  section 4: 00263FF0 is 02098E10 + g * 0x288; 0037B330 returns 4 when 02ADD931 is set, else the byte 02ADD930;
      00267310 reads slot + 0x201
  I4  sections 2-5, the producer 003DD4C0: groups 0-4 x slots 0-15; a record needs its mask bit AND state 2; a negative
      selector or a nonpositive length writes state 0 and keeps the bit; mode 2 with slot +0x17 bit 0x40 tries arena 11
      class 5 first (route 1 on success), otherwise or on failure arena 6 class 5; both failing writes state 0 and keeps the
      bit; success pins (0036A000), reclassifies (0036C620 with 1), stores kind as low16 and index as low16 + 1, then hold
      -> state 1, else 003DDA70; both clear the bit; the route byte +0xD is written at the common tail, state 2 or not
  I5  section 4: 003DDA70 sign-extends the kind and index words, submits through 0032E620 and writes state 3 without
      testing the result
"""
import io, os, re
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
EXE = os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe")
FUNCS = os.path.join(ROOT, "Tools", "work", "graph", "functions.tsv")
blob = io.open(EXE, "rb").read()
pe = pefile.PE(EXE, fast_load=True); BASE = pe.OPTIONAL_HEADER.ImageBase
SECS = [(s.Name.rstrip(b"\0").decode(), BASE + s.VirtualAddress, max(s.Misc_VirtualSize, s.SizeOfRawData), s.PointerToRawData, s.SizeOfRawData)
        for s in pe.sections]
md = Cs(CS_ARCH_X86, CS_MODE_64)
fails = 0


def OFF(va):
    for _n, start, size, raw, rawsz in SECS:
        if start <= va < start + min(size, rawsz):
            return raw + (va - start)
    raise ValueError("VA %08X in no raw section" % va)


def check(tag, ok, text):
    global fails
    fails += not ok
    print("%s  %s  %s" % ("SURVIVES" if ok else "BROKEN  ", tag, text))


sizes = {}
for i, line in enumerate(io.open(FUNCS, encoding="utf-8", errors="replace")):
    p = line.rstrip("\n").split("\t")
    if i and len(p) > 2:
        try:
            sizes[int(p[0], 16)] = int(p[2])
        except ValueError:
            pass


def body(fa):
    return {x.address: ("%s %s" % (x.mnemonic, x.op_str)).strip() for x in md.disasm(blob[OFF(fa):OFF(fa) + sizes[fa]], fa)}


def rip_to(a, target):
    x = next(md.disasm(blob[OFF(a):OFF(a) + 16], a))
    m = re.search(r"rip ([+-]) 0x([0-9a-f]+)", x.op_str)
    return m is not None and x.address + x.size + (1 if m.group(1) == "+" else -1) * int(m.group(2), 16) == target


A = body(0x003DDA20)
check("I1", A.get(0x003DDA29) == "shl rcx, 4" and A.get(0x003DDA30) == "imul rax, rcx, 0x1c" and rip_to(0x003DDA34, 0x02B581A0)
      and A.get(0x003DDA3B) == "cmp dword ptr [rax + rcx + 4], 0" and A.get(0x003DDA42) == "mov dword ptr [rax + rcx + 8], r8d"
      and rip_to(0x003DDA47, 0x02B58A60) and A.get(0x003DDA4E) == "mov dword ptr [rax + rcx + 4], 2"
      and A.get(0x003DDA5F) == "or dword ptr [r8 + r9*4], eax" and A.get(0x003DDA63) == "mov eax, 1" and A.get(0x003DDA69) == "xor eax, eax",
      "owners 02B581A0 + (16g + i) * 0x1C; state 0 only; annotation +8; state 2; mask 02B58A60 + 4g |= 1 << i")
S, K, L, O = body(0x0032F240), body(0x0032F170), body(0x0032F290), body(0x0032F260)
check("I2", S.get(0x0032F243) == "lea rcx, [rip - 0x20f24a]" and 0x0032F24A - 0x20F24A == BASE
      and S.get(0x0032F24A) == "cmp byte ptr [rax + rcx + 0x21a6d18], 0" and BASE + 0x21A6D18 == 0x022C6D18
      and S.get(0x0032F254) == "mov eax, dword ptr [rcx + rax*4 + 0x21a6d28]" and S.get(0x0032F25C) == "or eax, 0xffffffff"
      and K.get(0x0032F172) == "jle 0x32f19e" and K.get(0x0032F17E) == "lea eax, [rdx + 0x6b]" and K.get(0x0032F181) == "mov dword ptr [r8], 1"
      and K.get(0x0032F18C) == "lea eax, [rdx*4]" and K.get(0x0032F193) == "mov dword ptr [r8], 8"
      and K.get(0x0032F19E) == "lea eax, [rdx + rdx*2]" and K.get(0x0032F1A1) == "mov dword ptr [r8], 5"
      and L.get(0x0032F290) == "cmp ecx, 3" and L.get(0x0032F293) == "jg 0x32f2b0" and rip_to(0x0032F298, 0x022C6E70)
      and L.get(0x0032F2A3) == "cmp byte ptr [rcx], 0" and L.get(0x0032F2AB) == "mov eax, dword ptr [rcx + rax*8 + 0xc]"
      and O.get(0x0032F263) == "jg 0x32f280" and rip_to(0x0032F268, 0x022C6E70) and O.get(0x0032F27B) == "mov eax, dword ptr [rcx + rax*8 + 8]",
      "enable 022C6D18 + g, selector 022C6D28 + 4g; kinds 5 / 8 / 1; group 4 refused by the length and offset providers")
T, M, H = body(0x00263FF0), body(0x0037B330), body(0x00267310)
check("I3", rip_to(0x00263FF3, 0x02098E10) and T.get(0x00263FFA) == "imul rax, rax, 0x288" and rip_to(0x0037B330, 0x02ADD931)
      and rip_to(0x0037B337, 0x02ADD930) and M.get(0x0037B340) == "mov eax, 4" and rip_to(0x0026731A, 0x02098E10 + 0x201)
      and H.get(0x00267313) == "imul rcx, rax, 0x288",
      "slot 02098E10 + 0x288 g; mode 02ADD930 (4 when 02ADD931 is set); hold byte slot + 0x201")
P = body(0x003DD4C0)
ok = (P.get(0x003DD510) == "test dword ptr [r15], edi" and P.get(0x003DD513) == "je 0x3dd67a" and P.get(0x003DD52F) == "cmp dword ptr [rbx + 4], 2"
      and P.get(0x003DD533) == "jne 0x3dd665" and P.get(0x003DD543) == "jns 0x3dd54d" and P.get(0x003DD545) == "mov dword ptr [rbx + 4], esi"
      and P.get(0x003DD576) == "jg 0x3dd580" and P.get(0x003DD578) == "mov dword ptr [rbx + 4], esi"
      and P.get(0x003DD590) == "cmp eax, 2" and P.get(0x003DD595) == "test byte ptr [rsi + 0x17], 0x40"
      and P.get(0x003DD59B) == "lea edx, [rax + 3]" and P.get(0x003DD59E) == "lea ecx, [rax + 9]" and P.get(0x003DD5A1) == "call 0x36c1d0"
      and P.get(0x003DD5B3) == "call 0x36c140" and P.get(0x003DD5B8) == "mov edx, 5" and P.get(0x003DD5BD) == "lea ecx, [rdx + 1]"
      and P.get(0x003DD5D7) == "mov dword ptr [rbx + 4], r13d" and P.get(0x003DD5DD) == "mov dword ptr [rsp + 0x80], 1"
      and P.get(0x003DD5EC) == "call 0x36a000" and P.get(0x003DD5F1) == "mov edx, 1" and P.get(0x003DD5F9) == "call 0x36c620"
      and P.get(0x003DD609) == "mov word ptr [rbx + 0x10], ax" and P.get(0x003DD618) == "inc ax" and P.get(0x003DD61D) == "mov word ptr [rbx + 0x12], ax"
      and P.get(0x003DD62F) == "call 0x267310" and P.get(0x003DD638) == "mov dword ptr [rbx + 4], 1" and P.get(0x003DD644) == "call 0x3dda70"
      and P.get(0x003DD649) == "mov r13d, 1" and P.get(0x003DD665) == "mov byte ptr [rbx + 0xd], sil" and P.get(0x003DD672) == "and dword ptr [r15], eax"
      and P.get(0x003DD68A) == "cmp r14d, 0x10" and P.get(0x003DD6A4) == "cmp r12d, 5")
check("I4", ok, "mask bit AND state 2; failures -> state 0 with the bit kept; arena 11 (mode 2, +0x17 & 0x40) then 6, class 5; "
      "pin, reclassify, low16 kind / low16 index + 1; hold -> 1 else submit; bit cleared; route byte at the common tail")
Q = body(0x003DDA70)
check("I5", Q.get(0x003DDA98) == "movsx ecx, word ptr [rbx + 0x10]" and Q.get(0x003DDAA8) == "movsx edx, word ptr [rbx + 0x12]"
      and Q.get(0x003DDAB9) == "call 0x32e620" and Q.get(0x003DDABE) == "mov dword ptr [rbx + 4], 3",
      "kind and index sign-extended; submit 0032E620; state 3 written without testing the result")
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)
