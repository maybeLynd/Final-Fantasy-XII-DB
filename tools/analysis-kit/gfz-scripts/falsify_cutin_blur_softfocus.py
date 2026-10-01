"""Falsification pass 1 on cut-in-motion-blur-and-soft-focus (OPUS, 2026-09-29), from the shipping image.
Each row states what the bytes show; a row marked REFUTES is a clause of the page they break. The us-script census
(members/screen_effect_census.py) is carried, not re-run.

  Z0  the 35 cited sizes; 003DE3E0 is not a listed start
  Z1  callers: 0024D540 from the three frame bodies; its per-frame calls; 0036E810 from the verb and the area unload twice;
      003DE210 three callers; 003DF900 from the area unload, the area initialiser and the verb
  Z2  section 2: the driver gates on frame mode 2 or 6 ((mode - 2) & ~4 == 0) and soft focus on bit 0 and draw 0
  Z3  section 2: the late-release list 02091950 / count 0209216A with release at once when full; the allocator 00182B40 never
      reads xmm0 / xmm1 before overwriting xmm0 and sizes by device width and height x 512 / 448; soft focus asks for 0.125
  Z4  section 2: the one-shot returns - kind 4 on bit 3, the other three handlers on bit 6 of byte +0x1C - and the walker
      releasing on 0 at 00375633
  Z5  sections 3-4: the verb setters' mappings (cutintype, presettype, cluttype, noisetype, screentype)
  Z6  section 4: blur play's dead test (bit 4 cleared in dx, then `test dl, 0x10` at 0024EC34) and the clear's inverted handle
      test (0024EBD0..0024EBD6); the capture-once skip dword 01FD4A70 written by 003AAA50 and answered at 0022B196
  Z7  section 5: the soft-focus service's parameter block, play's bit-0 drop on failure and the forced byte +2 = 4
  Z8  section 5a: the teardown's bit-6 target 020926D0 and its tail - blur clear, then the cut-in clear by tail-jump;
      the fade poll 00345100 busy while 02B58C48 is non-zero; the cut-in builder's 0.875, +-73 and three line textures
  Z9  the notes that hold: 003B3B50 (32 x 0x38 from 02EBD480, empty tags skipped), 00182B20, 001830C0, 0026FF50, 003B2F90
  Z10 SWE2-EC7-90 note (REFUTES "36 0x18-stride slots are checked"): 003B1130 returns at the first slot whose key is zero
      (003B1144 `je 0x3b1173` to the ret), so slots after an empty one are not reached
  Z11 SWE2-EC7-112 note (REFUTES "a non-null rdx gets 00186AA0(obj) and a non-null rcx gets 00186A90(obj)"): 00182490 stores
      00186AA0 through rcx and 00186A90 through rdx - the reverse
"""
import io, os, struct
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_REG_RIP

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
EXE = os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe")
FUNCS = os.path.join(ROOT, "Tools", "work", "graph", "functions.tsv")
blob = io.open(EXE, "rb").read()
pe = pefile.PE(EXE, fast_load=True); BASE = pe.OPTIONAL_HEADER.ImageBase
SECS = [(s.Name.rstrip(b"\0").decode(), BASE + s.VirtualAddress, max(s.Misc_VirtualSize, s.SizeOfRawData), s.PointerToRawData, s.SizeOfRawData)
        for s in pe.sections]
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True
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
S = lambda x: ("%s %s" % (x.mnemonic, x.op_str)).strip()
rip = lambda x: [x.address + x.size + o.mem.disp for o in x.operands if o.type == X86_OP_MEM and o.mem.base == X86_REG_RIP]
body = lambda fa: [x for x in md.disasm(blob[OFF(fa):OFF(fa) + sizes[fa]], fa)]
at = lambda fa: {x.address: S(x) for x in body(fa)}
txt = lambda fa: [S(x) for x in body(fa)]
rips = lambda fa: {r for x in body(fa) for r in rip(x)}
f32 = lambda va: struct.unpack("<f", blob[OFF(va):OFF(va) + 4])[0]
text = next(x for x in SECS if x[0] == ".text")
raw = blob[text[3]:text[3] + text[4]]


def callers(t):
    return sorted(text[1] + k for k in range(len(raw) - 5)
                  if raw[k] in (0xE8, 0xE9) and text[1] + k + 5 + struct.unpack_from("<i", raw, k + 1)[0] == t)


SZ = {0x0024CF50: 158, 0x0024EC00: 329, 0x0024FAE0: 175, 0x0024CEB0: 160, 0x0024EB20: 219, 0x0024FA40: 155, 0x0024CBE0: 715,
      0x003AA6B0: 927, 0x0024EA10: 270, 0x003AAA50: 2736, 0x003AB500: 698, 0x0024C7C0: 172, 0x00375B90: 500, 0x003DF9F0: 64,
      0x003DF900: 79, 0x003DE360: 51, 0x003DE3A0: 51, 0x003DE2A0: 98, 0x003DE240: 91, 0x003DE160: 129, 0x003DE1F0: 22,
      0x00345100: 31, 0x0034FA00: 97, 0x0036E810: 104, 0x003DE210: 40, 0x0024E910: 256, 0x0024D540: 551, 0x003B3D20: 225,
      0x00182B20: 18, 0x003B3B50: 70, 0x003B1130: 68, 0x001830C0: 52, 0x00182490: 77, 0x0026FF50: 54, 0x003B2F90: 225}
bad = {("%08X" % a): sizes.get(a) for a in SZ if sizes.get(a) != SZ[a]}
check("Z0", not bad and 0x003DE3E0 not in sizes, "mismatches %s; 003DE3E0 unlisted: %s" % (bad or "none", 0x003DE3E0 not in sizes))

CW = {0x0024D540: [0x0022B191, 0x0022B927, 0x0022BC6F], 0x0024CBE0: [0x0024D6EE], 0x0024EA10: [0x0024D6F6], 0x003AB500: [0x0024D6DE],
      0x0036E810: [0x00262ACE, 0x00262CBE, 0x0034FA5C], 0x003DE210: [0x00262B7B, 0x003600EB, 0x003602D3],
      0x003DF900: [0x00262976, 0x00266ECF, 0x00354080], 0x0024FAE0: [0x0036E84A], 0x0024FA40: [0x0036E861]}
cbad = {("%08X" % t): ["%08X" % c for c in callers(t)] for t, w in CW.items() if callers(t) != w}
check("Z1", not cbad, "caller sets %s" % (cbad or "as stated"))
D = at(0x0024D540)
check("Z2", D.get(0x0024D6AF) == "add eax, -2" and D.get(0x0024D6B2) == "test eax, 0xfffffffb" and D.get(0x0024D6C9) == "test byte ptr [rip + 0x1e45014], 1"
      and D.get(0x0024D6D2) == "test r14d, r14d", "(mode - 2) & ~4 == 0 admits 2 and 6; soft focus behind bit 0 and draw 0")
P = at(0x0024FAE0)
A = txt(0x00182B40)
first_xmm = next((s for s in A if "xmm" in s), "")
check("Z3", P.get(0x0024FB1F) == "mov edx, 0x100" and P.get(0x0024FB29) == "call 0x182ca0" and {0x02091950, 0x0209216A} <= rips(0x0024FAE0)
      and A[1] == "call 0x1b6c40" and first_xmm == "xorps xmm0, xmm0" and not any("xmm1" in s for s in A)
      and f32(0x008C5B48) == 512.0 and f32(0x008C5B44) == 448.0 and f32(0x00915508) == 0.125,
      "the 256-entry late list; the allocator's first act is a call, xmm0 is overwritten first (%s) and xmm1 never read; x 512 / 448; soft focus 1/8" % first_xmm)
rets = {fa: txt(fa) for fa in (0x00375B90, 0x003745C0, 0x00374280)}
R4 = at(0x00375280)
check("Z4", rets[0x00375B90][-5:-3] == ["shr eax, 3", "and eax, 1"] and all(r[-5:-3] == ["shr eax, 6", "and eax, 1"] for fa, r in rets.items() if fa != 0x00375B90)
      and R4.get(0x00375446) == "shr eax, 6" and R4.get(0x00375449) == "and eax, 1"
      and at(0x00375500).get(0x00375631) == "jne 0x37563d" and at(0x00375500).get(0x00375636) == "call 0x375470",
      "kind 4 returns !bit 3, the other three !bit 6; the walker releases on 0 at 00375633")


def mapping(fa):
    """emulate a byte-setter's branch ladder for n = 0..6 by walking the listing"""
    ins = body(fa)
    out = {}
    for n in range(7):
        ecx, i, seen = n, 0, 0
        while i < len(ins) and seen < 40:
            seen += 1
            x = ins[i]; s = S(x)
            if s == "test ecx, ecx":
                zf = ecx == 0
            elif s.startswith("sub ecx, "):
                ecx -= int(s.split(", ")[1], 0); zf = ecx == 0
            elif s.startswith("cmp ecx, "):
                zf = ecx == int(s.split(", ")[1], 0)
            elif x.mnemonic in ("je", "jne"):
                if (x.mnemonic == "je") == zf:
                    i = next(k for k, y in enumerate(ins) if y.address == x.operands[0].imm); continue
            elif s.startswith("mov byte ptr [rip"):
                out[n] = int(s.split(", ")[1], 0)
            elif s == "ret":
                break
            i += 1
    return out


M = {name: mapping(fa) for name, fa in (("cutintype", 0x003DF9F0), ("presettype", 0x003DE400), ("cluttype", 0x003DE360),
                                          ("noisetype", 0x003DE3A0), ("screentype", 0x003DE430)) if fa in sizes or True}
want = {"cutintype": {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 2, 6: 2}, "presettype": {0: 1, 1: 2, 2: 3, 3: 1, 4: 1, 5: 1, 6: 1},
        "cluttype": {0: 1, 1: 2, 2: 3, 3: 0, 4: 1, 5: 1, 6: 1}, "noisetype": {0: 0, 1: 1, 2: 2, 3: 3, 4: 0, 5: 0, 6: 0},
        "screentype": {0: 1, 1: 2, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}}
check("Z5", M == want, "setter mappings n=0..6: %s" % M)
E, C = at(0x0024EC00), at(0x0024EB20)
check("Z6", E.get(0x0024EC0D) == "mov eax, 0xffef" and E.get(0x0024EC12) == "and dx, ax" and E.get(0x0024EC34) == "test dl, 0x10"
      and C.get(0x0024EBD0) == "cmp dword ptr [rbx], esi" and C.get(0x0024EBD2) == "jne 0x24ebdd" and C.get(0x0024EBD4) == "xor ecx, ecx" and C.get(0x0024EBD6) == "call 0x375470"
      and at(0x003AAA50).get(0x003AAAA6, "").endswith(", 1") and 0x01FD4A70 in rips(0x003AAA50)
      and at(0x0022B0B0).get(0x0022B196, "").startswith("cmp dword ptr [rip") and at(0x0022B0B0).get(0x0022B1A4, "").endswith(", 1"),
      "the dead bit-4 test; the release called only with a zero handle; 01FD4A70 set by the builder and answered by MainLoop_Draw")
V = at(0x0036E810)
check("Z7", V.get(0x0036E82C) == "cmp edx, 1" and V.get(0x0036E831) == "mov eax, 2" and V.get(0x0036E845) == "mov byte ptr [rsp + 0x21], r8b"
      and V.get(0x0036E83B) == "movss dword ptr [rsp + 0x24], xmm3" and V.get(0x0036E861) == "call 0x24fa40"
      and P.get(0x0024FB61) == "mov ecx, 0xfffe" and P.get(0x0024FB83) == "mov byte ptr [rip + 0x1e42a68], 4",
      "byte +0 = 2 on mode 1 else 1, +1 = b, +4 = amount; clear on 0; play drops bit 0 on failure and forces +2 = 4")
T = at(0x0024E910)
cut = set(rips(0x003AA6B0))
check("Z8", T.get(0x0024E9A9) == "test byte ptr [rip + 0x1e43d34], 0x40" and 0x020926D0 in rips(0x0024E910) and T.get(0x0024EA02) == "call 0x24eb20"
      and T.get(0x0024EA0B) == "jmp 0x24ceb0" and txt(0x003DE150)[0] == "mov eax, dword ptr [rip + 0x277aaf2]" and rips(0x003DE150) == {0x02B58C48}
      and at(0x00345100).get(0x00345108) == "call 0x3de150" and {0x01EFD4A0, 0x01EFD930, 0x01EFDDC0} <= cut
      and f32(0x00D11108) == 0.875 and f32(0x00D1147C) == 73.0 and f32(0x00D11484) == -73.0,
      "bit 6 / 020926D0; blur clear then the cut-in clear by tail-jump; the poll on 02B58C48; 0.875, +-73, the three line textures")
N = at(0x003B3B50)
check("Z9", N.get(0x003B3B57) == "mov r8d, 0x20" and N.get(0x003B3B63) == "test dword ptr [rax - 0x10], 0xfffffc0" and N.get(0x003B3B6A) == "je 0x3b3b8b"
      and N.get(0x003B3B8B) == "add rax, 0x38" and N.get(0x003B3B80) == "and dx, r9w" and 0x02EBD490 in rips(0x003B3B50)
      and txt(0x00182B20)[:4] == ["test rcx, rcx", "je 0x182b2f", "cmp byte ptr [rcx + 8], 0", "jne 0x182b2f"]
      and at(0x001830C0).get(0x001830DD) == "mov dword ptr [rax + 0x490], edi" and at(0x001830C0).get(0x001830E3) == "mov dword ptr [rax + 0x494], ebx"
      and at(0x0026FF50).get(0x0026FF7A, "").endswith(", 1") and at(0x003B2F90).get(0x003B303A) == "and dword ptr [rbx], 0xf000003f",
      "003B3B50 skips empty tags over 32 x 0x38; the flagged getter; the +0x490 / +0x494 pair; the latch; the bucket reap")
O = at(0x003B1130)
check("Z10", O.get(0x003B1140) == "cmp dword ptr [rax - 8], 0" and O.get(0x003B1144) == "je 0x3b1173" and O.get(0x003B1173) == "ret"
      and O.get(0x003B116E) == "cmp ecx, 0x24",
      "(REFUTES) a zero key jumps to the ret (003B1144 -> 003B1173): the sweep ends at the first empty slot of the 36")
G = at(0x00182490)
check("Z11", G.get(0x0018249A) == "mov rbx, rdx" and G.get(0x0018249D) == "mov rdi, rcx" and G.get(0x001824B7) == "call 0x186aa0"
      and G.get(0x001824BC) == "mov dword ptr [rdi], eax" and G.get(0x001824CB) == "call 0x186a90" and G.get(0x001824D0) == "mov dword ptr [rbx], eax",
      "(REFUTES) rcx receives 00186AA0 (the width the allocator reads first) and rdx receives 00186A90 - the note has them reversed")
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)
