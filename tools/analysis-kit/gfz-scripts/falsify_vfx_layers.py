"""Falsification pass 1 on the-six-vfx-display-layers (OPUS, 2026-09-29), from the shipping image.
Each row states what the bytes show; a row marked REFUTES is a clause of the page they break.

  V0  sizes: the nineteen bodies the page and its notes cite
  V1  section 1: 00258EE0 opens with 00862C10(0, layer); layer 3 branches first; the six-entry table at 00259014 sends layers
      1, 2, 4, 5, 6 to the five marker strings; layers 1, 2, 4 end in the follow-up 0024C640; layer 4 brackets with 0039CFF0
      (0, 0x3C00) / (0, 0x3700) and an extra 0036F550 unless 00181DD0 answers non-zero; layer 5 makes 0036F9F0 the same way
      before its marker; 6 shares 5's text; every path closes through 00862C30
  V2  section 1: 00259030 draws groups 2, 3, 5, 6, 9, 1, 7, 4 through 0024D370, then 003A3740; its two waits on 02EAF6D8 bit 8
      jump back to the test, not the load
  V3  section 1a: 0024D370 heads at 020910F0, gates through 0024D4E0, publishes 02092700 (-1 at the end), walks +0x348,
      compares +0x3A8 with 00181DD0 and +0x378 >> 12 with the layer, calls 0024D770(container, 1), then 0024ED80;
      flag +0x36A bit 0 runs 003AA2E0 and skips on zero, bit 1 raises bit 0 of 02F8F310
  V4  section 1a: 0024D4E0 refuses 8, tests bit (group - 1) of the AND of 02092162/4/6 for 1-4 and 7, 02F8F29E bit 0 for 2,
      02EBEF68 bit 0 for 5
  V5  section 1a: 0024ED80 publishes the nine globals and tail-jumps
  V6  section 1b: 0024D770: +0x364 refuses; table 0024D920 sends kind 2 to the two byte tables, 3 to the 02EBD480 handle
      entry (0x38 stride, six bits), 4 to an object's +0x20 bit 0, 5 / 6 / 9 to the enable bit or +0x13, 7 / 8 to "draw"
  V7  section 2: layer 3 tests bit 2 of 02F8F310, never calls 00259030, and calls 003A3990, not 003A3740
  V8  the notes that survive: 00862C30 / 00862C10, 0024C640's body, 00183060, 00376320, 0036F550's submit, 0036F9F0's
      records, 001B2530's stores
  V9  SWE2-EC7-99 note (REFUTES "0209F6C0" and "(ecx, 0, 0)"): 002D7E00 zeroes 0209E6C0 + id * 48 and calls 002D7E30 with
      its caller's rdx and r8 and r9 = 0
  V10 001B2530 note (REFUTES "picks 0017FEE0/0017FE60 on edi > 5"): the pick is 0017D980's answer; edi > 5 is the argument;
      the second emit always calls 0017FEE0, the third 0017FDE0
  V11 0039CFF0 note (REFUTES "runs per layer record" and "0xE0 + [rsp+0x20] entries"): 00258EE0 calls it only in layer 4,
      twice, with ids 0x3C00 and 0x3700; the reallocation passes the fixed pair 0x100 / 0xE0 and a fifth argument
  V12 SWE2-EC7-106 note (REFUTES "run on reload"): 00258EE0 calls 0024C640 on its shared tail after the grouped pass of
      layers 1, 2 and 4, on every such request; 002590F0 calls it too
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
txt = lambda fa: [S(x) for x in body(fa)]
rips = lambda fa: {r for x in body(fa) for r in rip(x)}
imm = lambda x: x.operands[0].imm if x.operands and x.operands[0].type == X86_OP_IMM else None
at = lambda fa: {x.address: S(x) for x in body(fa)}
cstr = lambda va: blob[OFF(va):OFF(va) + 80].split(b"\0")[0].decode("ascii", "replace")
calls = lambda fa: [(x.address, imm(x)) for x in body(fa) if x.mnemonic in ("call", "jmp") and imm(x) and not (fa <= imm(x) < fa + sizes[fa])]

SZ = {0x00258EE0: 307, 0x00259030: 179, 0x0024D370: 367, 0x0024D4E0: 94, 0x0024D770: 431, 0x0024ED80: 132, 0x00181DD0: 21,
      0x00862C30: 12, 0x00862C10: 17, 0x002D7E00: 47, 0x0024C640: 97, 0x00183060: 10, 0x0036F550: 1172, 0x003B5340: 113,
      0x0036F9F0: 438, 0x001B2530: 201, 0x0039CFF0: 198, 0x00376320: 47, 0x002590F0: 119}
bad = {("%08X" % a): sizes.get(a) for a in SZ if sizes.get(a) != SZ[a]}
check("V0", not bad, "mismatches %s" % bad if bad else "all nineteen sizes as cited")

L = at(0x00258EE0)
tab = [BASE + t for t in struct.unpack("<6I", blob[OFF(0x00259014):OFF(0x00259014) + 24])]
marker = {}
for x in body(0x00258EE0):
    for r in rip(x):
        if 0x00915600 <= r < 0x00915700:
            marker[x.address] = cstr(r)
names = sorted(set(marker.values()))
check("V1", L.get(0x00258EE8) == "cmp ecx, 3" and L.get(0x00258EFD) == "call 0x862c10" and L.get(0x00258F52) == "call 0x862c10"
      and tab == [0x00258F78, 0x00258F9F, 0x00258F9F, 0x00258FA8, 0x00258FE3, 0x00258FF1]
      and marker.get(0x00258F78) == "display VFX [layer : first]" and marker.get(0x00258F9F) == "display VFX [layer : after BG]"
      and marker.get(0x00258FA8) == "display VFX [layer : in EFF]" and marker.get(0x00258FF1) == "display VFX [layer : after EFF & MENU]"
      and marker.get(0x00258EED) == "display VFX [layer : TsEffMan_Layer_AfterOBJ]" and len(names) == 5
      and L.get(0x00258FB4) == "mov edx, 0x3c00" and L.get(0x00258FBB) == "call 0x39cff0" and L.get(0x00258FD5) == "mov edx, 0x3700"
      and L.get(0x00258FC0) == "call 0x181dd0" and L.get(0x00258FC9) == "call 0x36f550" and L.get(0x00258FE1) == "jmp 0x258f8b"
      and L.get(0x00258FE3) == "call 0x181dd0" and L.get(0x00258FEC) == "call 0x36f9f0" and L.get(0x00258F8B) == "call 0x24c640"
      and L.get(0x00258F9A) == "jmp 0x862c30" and L.get(0x0025900E) == "jmp 0x862c30" and L.get(0x00258F3F) == "call 0x862c30",
      "table %s; five marker texts; layer 4's 0x3C00 / 0x3700 bracket and extra call; layer 5's extra call before its marker" % ["%08X" % t for t in tab])

G = at(0x00259030)
order = [int(G[a - 7].split(", ")[1]) for a, s in sorted(G.items()) if s == "call 0x24d370"]
check("V2", order == [2, 3, 5, 6, 9, 1, 7, 4] and G.get(0x002590C0) == "call 0x3a3740" and G.get(0x00259052) == "jne 0x259050"
      and G.get(0x002590D7) == "jne 0x2590d5" and 0x02EAF6D8 in rips(0x00259030),
      "group order %s; drain 003A3740; both waits loop to the test (00259052 -> 00259050, 002590D7 -> 002590D5)" % order)

D = at(0x0024D370)
check("V3", 0x020910F0 in rips(0x0024D370) and D.get(0x0024D3A8) == "call 0x24d4e0" and D.get(0x0024D3B8) == "mov dword ptr [rip + 0x1e45342], edi"
      and D.get(0x0024D4CF, "").endswith("0xffffffff") and D.get(0x0024D3C0) == "mov rdi, qword ptr [rbx + 0x348]"
      and D.get(0x0024D3CC) == "movzx ecx, word ptr [rbx + 0x3a8]" and D.get(0x0024D3E2) == "shr eax, 0xc" and D.get(0x0024D3E5) == "cmp eax, esi"
      and D.get(0x0024D3ED) == "mov edx, 1" and D.get(0x0024D3F5) == "call 0x24d770" and D.get(0x0024D405) == "call 0x24ed80"
      and D.get(0x0024D448) == "call 0x3aa2e0" and D.get(0x0024D476) == "or word ptr [rip + 0x2d41e92], 1",
      "020910F0 heads, the group gate, 02092700 published and reset to -1, +0x348 / +0x3A8 / +0x378 >> 12, gate(container, 1), make current")

Q = at(0x0024D4E0)
check("V4", Q.get(0x0024D4E3) == "cmp ecx, 8" and Q.get(0x0024D4E6) == "je 0x24d523" and Q.get(0x0024D4ED) == "lea eax, [rcx - 7]"
      and {0x02092162, 0x02092164, 0x02092166, 0x02F8F29E, 0x02EBEF68} == rips(0x0024D4E0) and Q.get(0x0024D50C) == "shr dx, cl",
      "8 refused; bit (group - 1) for 1-4 and 7; 02F8F29E for 2; 02EBEF68 for 5")

pub = {r for x in body(0x0024ED80) for r in rip(x) if x.operands[0].type == X86_OP_MEM}
check("V5", pub == {0x02F97340, 0x02F97348, 0x02EBEF70, 0x02EBEFA8, 0x02EBEFA0, 0x02EBEF90, 0x02EBEF78, 0x02EBEF98, 0x02EBEFB0, 0x02EBEF88}
      and at(0x0024ED80).get(0x0024EDB9) == "lea rax, [rdx + 0x848]" and at(0x0024ED80).get(0x0024EDF1) == "lea rax, [rcx + 0x1b8]"
      and txt(0x0024ED80)[-1] == "jmp 0x24fcf0",
      "ten stores (container, resource, eight pointers); +0x848 -> 02EBEF90, +0x1B8 -> 02EBEF88; tail-jump 0024FCF0")

K = at(0x0024D770)
kt = [BASE + t for t in struct.unpack("<8I", blob[OFF(0x0024D920):OFF(0x0024D920) + 32])]
check("V6", K.get(0x0024D799) == "cmp word ptr [rbx + 0x364], 0" and K.get(0x0024D7A3) == "or word ptr [rbx + 0x36a], 1"
      and kt == [0x0024D7CD, 0x0024D87B, 0x0024D8F4, 0x0024D7FC, 0x0024D7FC, 0x0024D90F, 0x0024D90F, 0x0024D7FC]
      and K.get(0x0024D7D1, "").endswith("+ 0x2e6f23c], 2") and K.get(0x0024D7E0, "").endswith("+ 0x2e6f27c], 2")
      and K.get(0x0024D87E) == "and eax, 0x3f" and K.get(0x0024D881) == "imul rcx, rax, 0x38" and 0x02EBD480 in rips(0x0024D770)
      and K.get(0x0024D8A0) == "and al, 0xfb" and K.get(0x0024D8B5) == "and byte ptr [rcx + 0x30], 0xfd" and K.get(0x0024D8D7) == "cmp byte ptr [rbx + 0x39b], 0"
      and K.get(0x0024D905) == "test byte ptr [rax + 0x20], 1" and K.get(0x0024D817) == "and al, 6" and K.get(0x0024D824) == "test al, 0x10"
      and K.get(0x0024D84E) == "test word ptr [rip + 0x1e44e8f], ax" and K.get(0x0024D849) == "mov eax, 0x800",
      "kinds 2..9 -> %s" % ["%08X" % t for t in kt])

lay3 = [t for a, t in calls(0x00258EE0) if 0x00258EED <= a < 0x00258F4E]
check("V7", L.get(0x00258F0E) == "test byte ptr [rip + 0x2d363fb], 4" and 0x02F8F310 in rips(0x00258EE0)
      and 0x00259030 not in lay3 and 0x003A3990 in lay3 and 0x003A3740 not in lay3,
      "layer 3 calls %s" % ["%08X" % t for t in lay3])

B = at(0x001B2530)
check("V8", txt(0x00862C30) == ["mov rcx, qword ptr [rip + 0x171c8a1]", "jmp 0x1b2600"] and rips(0x00862C30) == {0x01F7F4D8}
      and txt(0x00862C10) == ["mov r8d, edx", "mov edx, ecx", "mov rcx, qword ptr [rip + 0x171c8bc]", "jmp 0x1b2530"]
      and at(0x0024C640).get(0x0024C652) == "cmp rcx, 8" and at(0x0024C640).get(0x0024C661) == "mov word ptr [rax + 0x32], dx"
      and {0x020910A0, 0x02F8DA00, 0x02F8C200} == rips(0x0024C640)
      and txt(0x00183060) == ["test ecx, ecx", "setne byte ptr [rip + 0x1dfc4a5]", "ret"]
      and at(0x0036F550).get(0x0036F9CB) == "lea r8, [rip + 0x105f0e]" and at(0x0036F550).get(0x0036F9D2) == "mov dword ptr [rsp + 0x20], 0x438"
      and at(0x0036F550).get(0x0036F554) == "call 0x3b5340" and at(0x0036F550).get(0x0036F576) == "mov eax, 0x55555556"
      and 0x02AD9B60 in rips(0x0036F9F0) and at(0x0036F9F0).get(0x0036F9F4) == "call 0x3b5340"
      and B.get(0x001B2556) == "mov byte ptr [rsi + 0x98], al" and B.get(0x001B25CC) == "and edi, 0xffffffef"
      and B.get(0x001B25CF) == "mov dword ptr [rsi + 0x90], ebp" and B.get(0x001B25F4) == "jmp 0x1fbd80" and B.get(0x001B257C) == "call 0x17d980",
      "forwarders, the row reset, the latch, the submit (004758E0, 0x438), the reseed, and 001B2530's stores")

E = at(0x002D7E00)
check("V9", E.get(0x002D7E1A) == "lea rax, [rip + 0x1dc689f]" and 0x0209E6C0 in rips(0x002D7E00) and 0x0209F6C0 not in rips(0x002D7E00)
      and E.get(0x002D7E09) == "xor r9d, r9d" and not any(s.startswith(("xor edx", "mov edx", "xor r8d", "mov r8d")) for s in txt(0x002D7E00))
      and E.get(0x002D7E0E) == "call 0x2d7e30" and E.get(0x002D7E21) == "mov qword ptr [rax + rcx*8], 0",
      "(REFUTES) the zeroed table is 0209E6C0 + id * 48; the notify gets the caller's rdx / r8 and r9 = 0")
check("V10", B.get(0x001B2579) == "setg bl" and B.get(0x001B2583) == "test eax, eax" and B.get(0x001B2585) == "je 0x1b258e"
      and B.get(0x001B2587) == "call 0x17fee0" and B.get(0x001B258E) == "call 0x17fe60" and B.get(0x001B25A5) == "call 0x17fee0"
      and B.get(0x001B25BA) == "call 0x17fde0" and [B.get(a) for a in (0x001B2599, 0x001B25B0, 0x001B25C5)] == ["mov ecx, 0xe00", "mov ecx, 0xdff", "xor ecx, ecx"],
      "(REFUTES) 0017FEE0 vs 0017FE60 is chosen by 0017D980's answer (001B2583); edi > 5 (setg) is the argument; emit 2 always "
      "0017FEE0, emit 3 0017FDE0")
C = at(0x0039CFF0)
sites = [a for a, t in calls(0x00258EE0) if t == 0x0039CFF0]
check("V11", sites == [0x00258FBB, 0x00258FDC] and all(0x00258FA8 <= a < 0x00258FE3 for a in sites)
      and C.get(0x0039D07F) == "mov r9d, 0xe0" and C.get(0x0039D092) == "lea r8d, [r9 + 0x20]" and C.get(0x0039D085) == "mov dword ptr [rsp + 0x20], 1",
      "(REFUTES) 00258EE0 calls 0039CFF0 at %s only, inside layer 4's arm; 002D7D90 gets r8 = 0x100, r9 = 0xE0, fifth argument 1"
      % ["%08X" % a for a in sites])
rs = [a for a, t in calls(0x00258EE0) if t == 0x0024C640]
arms = {0x00258F78: "1", 0x00258F9F: "2", 0x00258FA8: "4"}
check("V12", rs == [0x00258F8B] and L.get(0x00258F86) == "call 0x259030" and L.get(0x00258FA6) == "jmp 0x258f7f"
      and L.get(0x00258FE1) == "jmp 0x258f8b" and any(t == 0x0024C640 for a, t in calls(0x002590F0)),
      "(REFUTES 'on reload') 0024C640's one call site in 00258EE0 is %s, the shared tail after the grouped pass that layers %s "
      "reach on every request; 002590F0 also calls it" % (["%08X" % a for a in rs], sorted(arms.values())))
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)
