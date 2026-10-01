"""Falsification pass 1 on the-source-block-mover-and-separate-consumer-refresh (OPUS, 2026-09-30), from the shipping
image. SECTION-07's executions are carried, not re-run; these checks pin the static clauses the page rests on.

  S1  section 3: 0036A2A0's order - the slot's +8 takes the destination header (0036A364), the old allocation is released
      (00369860 at 0036A397), the payload is copied from old +0x40 to new +0x40 (004746F0 at 0036A3A7), the destination
      is claimed (0036BC60 at 0036A3BB), and the slot generation word is stored (0036A461)
  S2  section 2: the equal-size selector starts at arena +0x90 and compares the signed +0x18 extent, testing inhibit bit
      0x04 of +0x15; the adjacent selector tests (+0x15 & 6) == 2
  S3  section 2: 00369C60 runs the exact pass (0036AAD0) once and the adjacent pass (0036ABE0), repeating only the adjacent
      pass while it succeeds and the repeat flag is set; a nonzero count sets +2 and the +0x62 latch; zero leaves them
  S4  section 5: 00369CF0 reads and 003697C0 clears arena +0x62 (arena stride 0xA8); 003E6AA0 sets +0x294 bit 27 and
      replaces +0x304[31:27] keeping the low 27 bits
  S5  section 5: the delivery in 00427DE0 runs only with bit 27 set and +0x288 != -1, calls 003B3C00(+0x288, +0x304 >> 27)
      and clears bit 27 whatever it returns; 003B3C00 refuses a negative index or one >= 0xB, checks the ticket's
      generation in 02EBD480, needs a container, returns 1 for index 0 without refresh, and otherwise refreshes (003B3480)
      before the child start (0024FE70)
  S6  section 4: 002E65A0 compacts arenas 6 and 10 with repeat 1; the script adapter 0050E300 passes its two operands
      to 00369C60
  S7  section 7: 0024D540 makes five service calls, skips the window when its argument is nonzero, walks 02091108 through
      +0x348, repairs the context against +0x858 (003A9BA0 among the repairs) and each container against +0x390 separately
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


M = body(0x0036A2A0)
order = [0x0036A364, 0x0036A397, 0x0036A3A7, 0x0036A3BB, 0x0036A461]
check("S1", M.get(0x0036A364) == "mov qword ptr [rax + 8], rbx" and M.get(0x0036A393) == "lea rcx, [rbp + 0x40]" and M.get(0x0036A397) == "call 0x369860"
      and M.get(0x0036A39C) == "lea rcx, [rbx + 0x40]" and M.get(0x0036A3A3) == "lea rdx, [rbp + 0x40]" and M.get(0x0036A3A7) == "call 0x4746f0"
      and M.get(0x0036A3BB) == "call 0x36bc60" and M.get(0x0036A461) == "mov word ptr [rsi + 6], ax" and order == sorted(order),
      "slot +8 = destination header, release old, copy old +0x40 -> new +0x40, claim destination, store the generation word")
E, A = body(0x0036AAD0), body(0x0036ABE0)
check("S2", E.get(0x0036AADC) == "mov rsi, qword ptr [rcx + 0x90]" and E.get(0x0036AB16) == "mov r14d, dword ptr [rsi + 0x18]"
      and E.get(0x0036AB4C) == "test byte ptr [rbx + 0x15], 4"
      and A.get(0x0036AC24) == "movzx eax, byte ptr [rax + 0x15]" and A.get(0x0036AC28) == "and al, 6" and A.get(0x0036AC2A) == "cmp al, 2",
      "exact: free head arena +0x90, extent +0x18, inhibit +0x15 bit 4; adjacent: (+0x15 & 6) == 2")
C = body(0x00369C60)
check("S3", C.get(0x00369C6C) == "mov esi, edx" and C.get(0x00369CAE) == "call 0x36aad0" and C.get(0x00369CB3) == "mov ebx, eax"
      and C.get(0x00369CB8) == "call 0x36abe0" and C.get(0x00369CC1) == "inc ebx" and C.get(0x00369CC5) == "jne 0x369cb5"
      and C.get(0x00369CC9) == "je 0x369cd3" and C.get(0x00369CCB) == "mov byte ptr [rdi + 2], 1" and C.get(0x00369CCF) == "mov byte ptr [rdi + 0x62], 1"
      and C.get(0x00369C8F) == "imul rdi, rax, 0xa8",
      "exact pass once, adjacent pass repeated only while it moves and repeat != 0; a nonzero count sets +2 and +0x62")
R, L, Q = body(0x00369CF0), body(0x003697C0), body(0x003E6AA0)
check("S4", R.get(0x00369D06) == "imul rcx, rax, 0xa8" and R.get(0x00369D17) == "movzx eax, byte ptr [rcx + 0x62]"
      and L.get(0x003697D3) == "imul rcx, rax, 0xa8" and L.get(0x003697E4) == "mov byte ptr [rcx + 0x62], 0"
      and Q.get(0x003E6AA0) == "or dword ptr [rcx + 0x294], 0x8000000" and Q.get(0x003E6AAA) == "and dword ptr [rcx + 0x304], 0x7ffffff"
      and Q.get(0x003E6AB4) == "shl edx, 0x1b" and Q.get(0x003E6AB7) == "or dword ptr [rcx + 0x304], edx",
      "latch +0x62 read / cleared; request: bit 27 of +0x294, index in +0x304[31:27], low 27 bits kept")
D, T = body(0x00427DE0), body(0x003B3C00)
check("S5", D.get(0x0042863B) == "test dword ptr [rbx + 0x294], 0x8000000" and D.get(0x00428647) == "mov ecx, dword ptr [rbx + 0x288]"
      and D.get(0x0042864D) == "cmp ecx, -1" and D.get(0x00428650) == "je 0x42866a" and D.get(0x00428658) == "shr edx, 0x1b"
      and D.get(0x0042865B) == "call 0x3b3c00" and D.get(0x00428660) == "and dword ptr [rbx + 0x294], 0xf7ffffff"
      and T.get(0x003B3C0C) == "jns 0x3b3c16" and T.get(0x003B3C16) == "cmp ebx, 0xb" and T.get(0x003B3C19) == "jge 0x3b3c0e"
      and rip_to(0x003B3C24, 0x02EBD480) and T.get(0x003B3C2B) == "cmp dword ptr [rcx + rax], edx" and T.get(0x003B3C3D) == "je 0x3b3c72"
      and T.get(0x003B3C41) == "je 0x3b3c84" and T.get(0x003B3C84) == "mov eax, 1" and T.get(0x003B3C4D) == "call 0x3b3480"
      and T.get(0x003B3C64) == "call 0x24fe70",
      "delivery only with bit 27 and +0x288 != -1, bit cleared regardless; index <0 / >=0xB refused, 0 -> 1 unrefreshed, else refresh then start")
X, Y = body(0x002E65A0), body(0x0050E300)
pairs = [(a, t) for a, t in X.items() if t == "call 0x369c60"]
arenas = sorted({X[a - 3] for a, _ in pairs if (a - 3) in X})
check("S6", len(pairs) == 4 and arenas == ["lea ecx, [rdx + 5]", "lea ecx, [rdx + 9]"] and all(X.get(a - 8) == "mov edx, 1" for a, _ in pairs)
      and Y.get(0x0050E327) == "mov edx, ebx" and Y.get(0x0050E329) == "mov ecx, eax" and Y.get(0x0050E32B) == "call 0x369c60",
      "maintenance compacts arenas 6 and 10 with repeat 1 (twice each); the script adapter passes its two operands")
W = body(0x0024D540)
calls5 = [a for a, t in W.items() if a < 0x0024D565 and t.startswith("call ")]
check("S7", len(calls5) == 5 and W.get(0x0024D568) == "jne 0x24d6aa" and rip_to(0x0024D573, 0x02091108)
      and W.get(0x0024D63C) == "cmp rsi, qword ptr [rbp + 0x858]" and W.get(0x0024D656) == "call 0x3a9ba0"
      and W.get(0x0024D662) == "mov qword ptr [rbp + 0x858], rsi" and W.get(0x0024D669) == "cmp rsi, qword ptr [rdi + 0x390]"
      and W.get(0x0024D67F) == "mov qword ptr [rdi + 0x390], rsi" and W.get(0x0024D686) == "mov rdi, qword ptr [rdi + 0x348]",
      "five service calls; window skipped for a nonzero argument; 02091108 -> +0x348 walk; context +0x858 and container +0x390 apart")
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)
