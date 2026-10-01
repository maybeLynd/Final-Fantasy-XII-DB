"""Falsification pass 1 on the-actor-request-from-arming-through-start-and-return.md (OPUS, 2026-09-29), from the image.

  A0  section 1: the state1/state2 gate at 002689F0 / 002689F7 reads byte +02 == 1 and byte +10 == 0 of r15 (= rdx, the issuer), not of the target
      003587C0 returned (rbx), and a passing test calls 003DB790 on the target
  A1  section 2: 003DBDC0 selects the wait slot [actor + 0xA8] + byte[entry + 0x11] * 0x28, resets it through 0025D460, and
      sets PC = [actor + 0x58] + the function-table offset (00358A00)
  A2  section 2: 0025D460 clears +0x00..+0x16 exactly (qword, qword, dword, word, byte) and nothing past +0x16
  A3  section 4: 003DC050 walks the detached list from byte [actor + 0x61] over 0x14-byte entries at [actor + 0xA0], matching
      dword [entry + 0xC] (the continuation offset) and sbyte [entry + 2] (the channel) - no generation token; the walk is
      also capped by byte [actor + 0x89] (not stated on the page)
  A4  section 7: 0x5F / 0x63 arm kind 7 through one `mov word ptr [rsi + 0x14], 0x107` (00261B97); 0x61 arms kind 5
      (`mov byte ptr [rsi + 0x14], 5`, 00261D24) after 002674B0
  A5  section 6: the two list helpers exist with the cited names and sizes (00267420 132 B, 002674B0 166 B)
"""
import collections, io, os
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


sizes, names = {}, {}
for i, line in enumerate(io.open(FUNCS, encoding="utf-8", errors="replace")):
    p = line.rstrip("\n").split("\t")
    if i and len(p) > 2:
        try:
            sizes[int(p[0], 16)] = int(p[2]); names[p[1]] = int(p[0], 16)
        except ValueError:
            pass
S = lambda x: ("%s %s" % (x.mnemonic, x.op_str)).strip()
bodies = {}
for fa in (0x00268850, 0x003DBDC0, 0x0025D460, 0x003DC050, 0x0025E4C0, 0x00267420, 0x002674B0):
    bodies[fa] = list(md.disasm(blob[OFF(fa):OFF(fa) + sizes[fa]], fa))


def run(fa, lo, hi):
    return [S(x) for x in bodies[fa] if lo <= x.address <= hi]


# A0
check("A0", run(0x00268850, 0x002689E3, 0x00268A06) == ["call 0x3587c0", "mov rbx, rax", "test rax, rax", "je 0x268a3b", "cmp byte ptr [r15 + 2], 1",
                                                        "jne 0x268a0d", "cmp byte ptr [r15 + 0x10], 0", "jne 0x268a0d", "lea rdx, [rsp + 0x20]",
                                                        "mov rcx, rax", "call 0x3db790"]
      and run(0x00268850, 0x00268883, 0x00268883) == ["mov r15, rdx"],
      "the gate reads r15 (= rdx, the issuer argument, 00268883) +02 / +10, not rbx, the resolved target; a pass inserts the target through 003DB790")
# A1
d = [S(x) for x in bodies[0x003DBDC0]]
check("A1", d[5:19] == ["movsx rax, byte ptr [rcx + 0x11]", "mov rsi, rdx", "movzx edx, word ptr [rdx + 4]", "mov rbp, rcx", "lea r8, [rax + rax*4]",
                        "mov rax, qword ptr [rcx + 0xa8]", "lea rdi, [rax + r8*8]", "call 0x358a00", "mov rcx, rdi", "movsxd rbx, eax", "call 0x25d460",
                        "mov rax, rbx", "add rax, qword ptr [rbp + 0x58]", "mov qword ptr [rdi], rax"],
      "slot = [+0xA8] + byte[+0x11] * 0x28; 0025D460; PC = [+0x58] + 00358A00's offset")
# A2
check("A2", [S(x) for x in bodies[0x0025D460]] == ["xor eax, eax", "mov qword ptr [rcx], rax", "mov qword ptr [rcx + 8], rax", "mov dword ptr [rcx + 0x10], eax",
                                                   "mov word ptr [rcx + 0x14], ax", "mov byte ptr [rcx + 0x16], al", "ret"],
      "0025D460 clears +0x00..+0x16 and nothing else")
# A3
n = [S(x) for x in bodies[0x003DC050]]
check("A3", "movzx r9d, byte ptr [rcx + 0x61]" in n and "movzx r11d, byte ptr [rcx + 0x89]" in n and "mov rax, qword ptr [rbx + 0xa0]" in n
      and "lea rcx, [r9 + r9*4]" in n and "cmp dword ptr [rax + rcx*4 + 0xc], r8d" in n and "movsx eax, byte ptr [rdx + 2]" in n
      and "cmp r10d, r11d" in n and "movzx r9d, byte ptr [rdx]" in n,
      "head byte +0x61; 0x14-byte entries at [+0xA0]; key dword +0xC and sbyte +2; next byte +0; walk capped by byte [+0x89]")
# A4
check("A4", run(0x0025E4C0, 0x00261B97, 0x00261B97) == ["mov word ptr [rsi + 0x14], 0x107"]
      and run(0x0025E4C0, 0x00261D17, 0x00261D24) == ["call 0x2674b0", "test eax, eax", "je 0x261610", "mov byte ptr [rsi + 0x14], 5"],
      "kind 7 via 0x107 at 00261B97; kind 5 at 00261D24 after 002674B0")
# A5
check("A5", names.get("ScriptVM_WaitList_HasAnyActorChannelActive") == 0x00267420 and sizes[0x00267420] == 132
      and names.get("ScriptVM_WaitList_HasAnyActorResourceEntryActive") == 0x002674B0 and sizes[0x002674B0] == 166,
      "00267420 132 B, 002674B0 166 B")
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)   # a BROKEN row must fail the process, not only the text (ASTRA feb631dd4, 2026-09-29)
