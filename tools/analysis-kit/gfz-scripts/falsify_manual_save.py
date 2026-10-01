"""Falsification pass 1 on how-a-manual-save-is-committed (OPUS, 2026-09-29), from the shipping image. Rows check the page as
corrected by this pass (CON-191 corrects the appended SWE2-EC7-113 note, not the page's own sections).

  M0  sizes 00581DA0 640, 00581B70 514, 00582730 94, 005826D0 83, 005837F0 304, 00862130 167
  M1  section 1 and CON-191: 00582730 and 005826D0 build a stack packet {kind, path, ...} and hand it to the storage
      queue's enqueue 00582540 when the queue 02CA99C0 exists. 00582730 is kind 7 with (rdx, r8d) = (buffer, size); every
      call in the transaction passes (path, image, 8). 005826D0 is kind 0x0B with the path only. They are not a
      diagnostic sink, and rdx/r8d are not a slot/error pair
  M2  section 1: the file names: icon.sys (00D23EC8), static.ico (00D23ED8), the slot pattern "%s%03d" (009153E4); state 1
      and state 3 name kind 1 (the data file), state 2 kind 0 (icon.sys)
  M3  section 2: the weights - state 1 (flag << 6) | 0x10, state 2 ((flag | 4) << 2), state 3/4 0x10, state 7 0x168 or
      0xE6, state 8 0x32 - and the totals 0x1DA / 0x17C from 005819F0 (00581AF0..00581B01) agree only on the corrected order
  M4  section 2: the callback accepts kind 0xB at 00581BE5 and branches on +0xC8 bit 0 at 00581BFD: 7 (00581C06) or 3
      (00581C20); the flag is the request's +0x18 bit 0 (00581AB7..00581AC4)
  M5  section 2: state 7 writes 0x56690 bytes (00581F2F); state 8 stores 1 at image +4 (00581FBA) and writes 8 bytes
  M6  section 1: 00862130 opens "rb", closes, then removes
  M7  CON-192 (a consumer): the state table 00582020 - 4, 5, 6 share one arm; 7 is the submission, 8 the stamp
"""
import io, os, struct
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_REG_RIP

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
A = lambda fa: {x.address: (S(x), rip(x)) for x in body(fa)}
cstr = lambda va: blob[OFF(va):OFF(va) + 32].split(b"\0")[0].decode("latin-1")


def eq(m, a, text, target=None):
    g = m.get(a)
    return g is not None and g[0] == text and (target is None or target in g[1])


SZ = {0x00581DA0: 640, 0x00581B70: 514, 0x00582730: 94, 0x005826D0: 83, 0x005837F0: 304, 0x00862130: 167}
bad = {("%08X" % a): sizes.get(a) for a in SZ if sizes.get(a) != SZ[a]}
check("M0", not bad, "sizes %s" % (bad or "all six as cited"))
R7, RB, T = A(0x00582730), A(0x005826D0), A(0x00581DA0)
Tb = body(0x00581DA0)
sites7 = [x.address for x in Tb if S(x) == "call 0x582730"]
ok_args = all(T.get(a - 9, ("",))[0] == "mov r8d, 8" and T.get(a - 3, ("",))[0] == "mov rdx, rdi" for a in sites7)
check("M1", eq(R7, 0x00582737, "mov r10, qword ptr [rip + 0x2727282]", 0x02CA99C0) and eq(R7, 0x00582748, "mov dword ptr [rsp + 0x20], 7")
      and eq(R7, 0x0058276F, "mov qword ptr [rsp + 0x68], rdx") and eq(R7, 0x0058277C, "mov dword ptr [rsp + 0x70], r8d")
      and eq(R7, 0x00582781, "call 0x582540") and eq(RB, 0x005826E8, "mov dword ptr [rsp + 0x20], 0xb") and eq(RB, 0x00582716, "call 0x582540")
      and sites7 == [0x00581E2D, 0x00581FD9] and ok_args,
      "CON-191: kind-7 and kind-0xB packets into the storage queue; both kind-7 calls pass (path, image, 8)")
check("M2", cstr(0x00D23EC8) == "icon.sys" and cstr(0x00D23ED8) == "static.ico" and cstr(0x009153E4) == "%s%03d"
      and eq(T, 0x00581E4D, "mov r8d, 1") and eq(T, 0x00581E53, "xor ecx, ecx") and eq(T, 0x00581E5D, "call 0x5826d0")
      and eq(T, 0x00581E7C, "movzx ecx, r8b") and eq(T, 0x00581E8F, "call 0x5826d0"),
      "icon.sys / static.ico / %s%03d; state 2 deletes kind 0, state 3 kind 1")
I = A(0x005819F0)
w = {"s1": eq(T, 0x00581E3B, "shl edx, 6") and eq(T, 0x00581E3E, "or edx, 0x10"),
     "s2": eq(T, 0x00581E6B, "or edx, 4") and eq(T, 0x00581E6E, "shl edx, 2"),
     "s34": eq(T, 0x00581E94, "mov edx, 0x10"),
     "s7": eq(T, 0x00581F95, "mov edx, 0x168") and eq(T, 0x00581F9A, "mov eax, 0xe6") and eq(T, 0x00581F9F, "cmovne edx, eax"),
     "s8": eq(T, 0x00581FDE, "mov edx, 0x32"),
     "tot": eq(I, 0x00581AF7, "mov ecx, 0x17c") and eq(I, 0x00581AFC, "mov eax, 0x1da") and eq(I, 0x00581B01, "cmove ecx, eax")}
full = 0x10 + (4 << 2) + 0x10 + 0x10 + 0x168 + 0x32
short = ((1 << 6) | 0x10) + ((1 | 4) << 2) + 0xE6 + 0x32
check("M3", all(w.values()) and full == 0x1DA and short == 0x17C,
      "weights %s; full %X, short %X (states 1, 2, 7, 8)" % ("ok" if all(w.values()) else w, full, short))
C = A(0x00581B70)
check("M4", eq(C, 0x00581BE5, "cmp ecx, 0xb") and eq(C, 0x00581BFD, "test byte ptr [rbx + 0xc8], 1") and eq(C, 0x00581C06, "mov dl, 7")
      and eq(C, 0x00581C20, "mov dl, 3") and eq(I, 0x00581AB7, "mov eax, dword ptr [rbx + 0x18]") and eq(I, 0x00581AC4, "mov dword ptr [rdi + 0xc8], eax"),
      "the short variant branches inside state 2's completion; the flag is the request's +0x18 bit 0")
check("M5", eq(T, 0x00581F2F, "mov qword ptr [rsp + 0xc0], 0x56690") and eq(T, 0x00581FBA, "mov dword ptr [rdi + 4], 1"),
      "state 7 writes 0x56690 bytes; state 8 stamps {checksum, 1}")
D = body(0x00862130)
imp = [t for x in D if x.mnemonic == "call" for t in rip(x)]
order = [t for t in imp if t in (0x008C2E00, 0x008C2F00, 0x008C2B08)]
MODES = ("rb".encode("utf-16le") + b"\x00\x00", b"rb\x00")
def at_is(va, m):
    try:
        return blob[OFF(va):OFF(va) + len(m)] == m
    except ValueError:  # uninitialised data holds no string
        return False


rb = [x for x in D if rip(x) and any(at_is(rip(x)[0], m) for m in MODES)]
check("M6", order == [0x008C2E00, 0x008C2F00, 0x008C2B08] and len(rb) >= 1,
      "00862130 calls _wfopen_s (mode 'rb'), fclose, _wremove in that order")
jt = [0x00120000 + struct.unpack("<I", blob[OFF(0x00582020) + 4 * i:OFF(0x00582020) + 4 * i + 4])[0] for i in range(8)]
check("M7", eq(T, 0x00581DFA, "mov edx, dword ptr [rax + rcx*4 + 0x462020]")
      and jt == [0x00581E06, 0x00581E46, 0x00581E76, 0x00581E9E, 0x00581E9E, 0x00581E9E, 0x00581EB0, 0x00581FA8]
      and eq(T, 0x00581ED2, "call 0x5832b0") and eq(T, 0x00581FB4, "mov dword ptr [rdi], eax"),
      "CON-192: the state table sends 4, 5, 6 to one arm, 7 to the submission (00581EB0) and 8 to the stamp (00581FA8)")
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)
