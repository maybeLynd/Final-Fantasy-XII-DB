"""Falsification pass 1 on the-query-record-from-initialization-to-reuse.md (OPUS, 2026-09-29), from the shipping image.

  Q0  section 1: fifteen 0x58-byte records at 01EEBCC0 whose +0x38 words are 5..19; 00309440 maps nibble 0..E through the
      pre-biased base 01EEBCF8 and returns -1 above E
  Q1  section 2: 0030B6A0 walks 01EEBCC0 .. +15 x 0x58; for 00/18/28 a nonzero QWORD selects a DWORD load plus a 32-bit add
      into 08/20/30; +40 takes the running sum of +3C; then 8 x 0x40 = 512 bytes cleared at state+57C8 through the full
      pointer, and 0x80 bytes at +59C8 ANDed with 0xF8
  Q2  section 3: 0035D330 writes tag and DWORD+4 of 022CA520, 0035D380 tag and WORD+6 of 022CA480; on a negative filler
      return both call the `ret 0` stub 0016D6A0 and memset all 0x98 bytes, and return the record
  Q3  section 3/4: the filler 0031C5D0 clears QWORD+18 before its 32-arm dispatch; class 1 derives the class through 00309440
      from WORD+6, stores it and redispatches without repacking; class 12's arm is the -2 at 0031C650
  Q4  section 5: the equipment arm replaces +54 bit 0 by `xor al, [rbx+54] / and al, 1 / xor [rbx+54], al`
  Q5  section 5: class 10 writes 0xFFFFFFFF at +38 + 8k for k = 0..11 (from rbx+0x3A, `[rbx-2]`), empty-string pointers at
      +08/+10 and zeros at +20/+28
  Q6  (context the loader-bound sheet got wrong) 0016D6A0 is `ret 0`, three bytes, with 2,868 call sites - not an allocator
"""
import collections, io, os, struct
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
rip = lambda x: [x.address + x.size + o.mem.disp for o in x.operands if o.type == X86_OP_MEM and o.mem.base == X86_REG_RIP]
T = lambda x: x.operands[0].imm if x.operands and x.operands[0].type == X86_OP_IMM else None
text = next(x for x in SECS if x[0] == ".text")

calls_to = collections.defaultdict(list)
bodies = {}
for fa in sorted(sizes):
    if not (text[1] <= fa < text[1] + text[2]):
        continue
    try:
        code = blob[OFF(fa):OFF(fa) + sizes[fa]]
    except ValueError:
        continue
    ins = list(md.disasm(code, fa))
    bodies[fa] = ins
    for x in ins:
        if x.mnemonic in ("call", "jmp") and T(x) is not None:
            calls_to[T(x)].append((fa, x.address, x.mnemonic))


def ins_at(fa, va):
    return next(x for x in bodies[fa] if x.address == va)


def run(fa, lo, hi):
    return [S(x) for x in bodies[fa] if lo <= x.address <= hi]


u32 = lambda va: struct.unpack("<I", blob[OFF(va):OFF(va) + 4])[0]
FILL = 0x0031C5D0

# Q0
words = [u32(0x01EEBCC0 + 0x58 * k + 0x38) for k in range(15)]
c440 = [S(x) for x in bodies[0x00309440]]
check("Q0", words == list(range(5, 20)) and c440[:4] == ["movzx eax, cx", "shr eax, 0xc", "cmp eax, 0xe", "ja 0x30945a"]
      and rip(ins_at(0x00309440, 0x0030944F)) == [0x01EEBCF8] and c440[-2:] == ["or eax, 0xffffffff", "ret"],
      "class words %s; 00309440: nibble <= 0xE -> [01EEBCF8 + n*0x58], else -1" % words)
# Q1
i6a = bodies[0x0030B6A0]
beg, end = rip(ins_at(0x0030B6A0, 0x0030B6A8))[0], rip(ins_at(0x0030B6A0, 0x0030B6B2))[0]
body = [S(x) for x in i6a]
check("Q1", beg == 0x01EEBCC0 and end == 0x01EEBCC0 + 15 * 0x58 and "add r8, 0x58" in body and body.count("add eax, r10d") == 3
      and "mov dword ptr [r8 + 0x40], r9d" in body and "add r9d, dword ptr [r8 + 0x3c]" in body
      and "lea rax, [rcx + 0x57c8]" in body and "mov ecx, 8" in body and "lea rax, [rax + 0x40]" in body
      and "lea rax, [r10 + 0x59c8]" in body and "mov ecx, 0x80" in body and "and byte ptr [rax], 0xf8" in body,
      "rows %08X..%08X (15 x 0x58); three 32-bit adds; +40 running sum of +3C; 512 B cleared at +57C8; 0x80 B & 0xF8 at +59C8" % (beg, end))
# Q2
def wrap(fa):
    b = bodies[fa]
    return [("%08X" % rip(x)[0], x.op_str.split(" ptr")[0]) for x in b if x.mnemonic == "mov" and rip(x) and x.operands[0].type == X86_OP_MEM]
w1, w2 = wrap(0x0035D330), wrap(0x0035D380)
fail_path = lambda fa: [s for s in (S(x) for x in bodies[fa]) if s in ("mov ecx, 0x800", "call 0x16d6a0", "mov r8d, 0x98", "call 0x861ec0")]
check("Q2", w1 == [("022CA520", "dword"), ("022CA524", "dword")] and w2 == [("022CA480", "dword"), ("022CA486", "word")]
      and fail_path(0x0035D330) == fail_path(0x0035D380) == ["mov ecx, 0x800", "call 0x16d6a0", "mov r8d, 0x98", "call 0x861ec0"],
      "0035D330 %s; 0035D380 %s; failure: stub 0016D6A0 then memset 0x98" % (w1, w2))
# Q3
tbl = BASE + 0x1FE598
jt = [BASE + u32(tbl + 4 * k) for k in range(32)]
head = run(FILL, 0x0031C5EA, 0x0031C5FA)
c1 = run(FILL, 0x0031C61F, 0x0031C639)
check("Q3", head == ["mov eax, dword ptr [rcx]", "xor esi, esi", "dec eax", "mov qword ptr [rcx + 0x18], rsi", "mov rbx, rcx", "cmp eax, 0x1f", "ja 0x31c63b"]
      and rip(ins_at(FILL, 0x0031C5FC)) == [BASE] and jt[0] == 0x0031C61F and jt[11] == 0x0031C650
      and c1[:6] == ["movzx ecx, word ptr [rbx + 6]", "call 0x309440", "test eax, eax", "js 0x31c650", "mov dword ptr [rbx], eax", "mov qword ptr [rbx + 0x18], rsi"]
      and "jbe 0x31c610" in c1 and run(FILL, 0x0031C650, 0x0031C650) == ["mov eax, 0xfffffffe"],
      "+0x18 cleared before dispatch; table at image+0x1FE598; class 1 -> %08X (redispatch, WORD+6 untouched); class 12 -> %08X (-2)" % (jt[0], jt[11]))
# Q4
check("Q4", run(FILL, 0x0031CA42, 0x0031CA47) == ["xor al, byte ptr [rbx + 0x54]", "and al, 1", "xor byte ptr [rbx + 0x54], al"],
      "%s" % run(FILL, 0x0031CA42, 0x0031CA47))
# Q5
loop = run(FILL, 0x0031CF3E, 0x0031CF6F)
check("Q5", loop == ["lea rax, [rip + 0x19ce6f3]", "mov qword ptr [rbx + 0x20], rsi", "mov qword ptr [rbx + 8], rax", "mov qword ptr [rbx + 0x10], rax",
                     "mov eax, 0xc", "mov qword ptr [rbx + 0x28], rsi", "add rbx, 0x3a", "nop", "mov dword ptr [rbx - 2], 0xffffffff",
                     "lea rbx, [rbx + 8]", "sub rax, 1", "jne 0x31cf60"],
      "class 10: 12 x FFFFFFFF at +38..+90 step 8; +08/+10 one string pointer; +20/+28 zero")
# Q6
check("Q6", [S(x) for x in bodies[0x0016D6A0]] == ["ret 0"] and sizes.get(0x0016D6A0) == 3 and len(calls_to[0x0016D6A0]) == 2868,
      "0016D6A0 = %s, %d B, %d call sites" % ([S(x) for x in bodies[0x0016D6A0]], sizes.get(0x0016D6A0), len(calls_to[0x0016D6A0])))
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)   # a BROKEN row must fail the process, not only the text (ASTRA feb631dd4, 2026-09-29)
