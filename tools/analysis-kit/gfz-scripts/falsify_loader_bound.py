"""Falsification pass 1 on loader-bound-bin-families.md (OPUS, 2026-09-29), from the shipping image. Killers first.

  B0  (REFUTES section 1's texpack example) the texpack loader 002467A0's idempotence check is `cmp qword [0208EA88], 0` -
      the cell it stores its 7/0xD6 request into; `[*(0209AC30) + 0x3D8]` is tested by the tex2pack binder 00280670, which
      reads its directory from that pointer
  B1  section 1: fontpack_it's loader 0039C3F0 checks and fills 02AEE868 (request 7/0xD5); mrppack/clutpack's 002808D0
      checks and fills *(0209AC30) + 0x3D0 (7/0xD3) and + 0x3C8 (7/0xD4) - lazy and idempotent
  B2  (REFUTES the fontpack_it summary row "binder walks 6") the callback 0039C150 reads all eight directory dwords
      (+0x00..+0x1C); dir 6 binds 02AEE848 only when 00254A10() == 0, the slot is not 0xFFFFFFFF and the cell is empty; dir 7
      overwrites 02AEE880 whenever 02AEE848 is set
  B3  (REFUTES the fontpack_fs slot-0 row "+0x08 and +0x190") the callback 003643A0 binds dir 0 to +0x08 only and dir 1 to
      +0x190; dirs 2, 4, 5, 6 -> +0x110 / +0x120 / +0x128 / +0x130, each only when that field is still null, with flags
      1 / 4 / 8 / 0x10 and faces 0xB / 0xD / 0xE / 0xF; dir 3 (+0x0C) is never read
  B4  section 2: the tex2pack binder walks +0x338..+0x380 (ten slots, step 8, offset step 4) through 0024A1D0 and stores
      dir 10 (+0x28) raw at +0x388; the clutpack binder 00280AD0 fills +0x390 / +0x398 / +0x3A0 / +0x3A8
  B5  section 2: the 23-entry MRP relocation loop (`cmp rdi, 0x5c`, 002A00F0) is 00280980, not the loader 002808D0
  B6  (REFUTES "the preset index is player-authored through the settings data, not per-area") the selector setter 0025A160
      has three calling functions - 00304060 (call site 003040B7), 00304140 and 00356CB0, the native of script verb
      setbehindcameratype (0x01CB); its bound is `cmp ecx, [blob + 4] / jge` only, signed, so a negative index is stored
  B7  section 3: 00259370 takes the blob in ECX (`mov eax, ecx`, zero-extended), rejects null and a count <= 0, zeros
      02098DF8 and tail-jumps 00259FE0
  B8  section 4: fontcolor's accessor 002DD840 stores dword[blob] -> 0215E6B8 and blob + 4 -> 0215E6C8; monotone_chr's
      loader 002C8EE0 requests subtypes 0x74 (and 0x75), adds 0x880, and copies from *(0209AC30) + 0x390 into + 0x1DC0
"""
import collections, io, os, struct
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_REG_RIP

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
EXE = os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe")
FUNCS = os.path.join(ROOT, "Tools", "work", "graph", "functions.tsv")
VERBS = os.path.join(ROOT, "FFXII TZA", "01-Script-VM-Native-Bridge", "Verb-Dispatch", "scriptvm-dispatch.tsv")
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

refs = collections.defaultdict(list)          # target -> [(function, insn)]
calls_to = collections.defaultdict(list)      # target -> [(function, address, mnemonic)]
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
        for t in rip(x):
            refs[t].append((fa, x))
        if x.mnemonic in ("call", "jmp") and T(x) is not None:
            calls_to[T(x)].append((fa, x.address, x.mnemonic))


def ins_at(fa, va):
    return next(x for x in bodies[fa] if x.address == va)


def at(fa, va):
    return S(ins_at(fa, va))


def cell(fa, va):
    return rip(ins_at(fa, va))[0]


# B0 the texpack loader's own idempotence cell, and whose +0x3D8 test it really is
tex_chk, tex_store = cell(0x002467A0, 0x002467A6), cell(0x002467A0, 0x0024688C)
b670 = [S(x) for x in bodies[0x00280670]]
check("B0", at(0x002467A0, 0x002467A6).startswith("cmp qword ptr [rip") and tex_chk == tex_store == 0x0208EA88
      and not any("0x3d8]" in S(x) for x in bodies[0x002467A0]) and at(0x002467A0, 0x00246872) == "mov r8d, 0xd6"
      and cell(0x00280670, 0x00280674) == 0x0209AC30 and "cmp qword ptr [rdx + 0x3d8], 0" in b670 and "mov edx, dword ptr [rdi + rax]" in b670,
      "texpack 002467A0 tests and stores %08X (request 7/0xD6) and never touches +0x3D8; [*(0209AC30)+0x3D8] is the tex2pack blob, tested and read by 00280670" % tex_chk)
# B1 the other lazy loaders
check("B1", cell(0x0039C3F0, 0x0039C3F4) == cell(0x0039C3F0, 0x0039C467) == 0x02AEE868 and at(0x0039C3F0, 0x0039C411) == "mov edx, 0xd5"
      and at(0x002808D0, 0x002808E0) == "cmp qword ptr [rax + 0x3d0], 0" and at(0x002808D0, 0x002808F8) == "mov r8d, 0xd3"
      and at(0x002808D0, 0x00280924) == "cmp qword ptr [rax + 0x3c8], 0" and at(0x002808D0, 0x0028093C) == "mov r8d, 0xd4",
      "fontpack_it 0039C3F0: 02AEE868 / 7/0xD5; 002808D0: +0x3D0 / 7/0xD3 and +0x3C8 / 7/0xD4")
# B2 fontpack_it: eight directory dwords
cb = bodies[0x0039C150]
dir_reads = set({o.mem.disp for x in cb for o in x.operands if o.type == X86_OP_MEM and o.mem.base != X86_REG_RIP
                    and x.reg_name(o.mem.base) == "rcx" and x.mnemonic == "mov" and x.op_str.startswith("eax") and o.mem.disp <= 0x1C})
dir_reads |= {0} if "mov eax, dword ptr [rcx]" in [S(x) for x in cb] else set()
dests = {d: None for d in range(0, 0x20, 4)}
for i, x in enumerate(cb):
    if x.mnemonic == "mov" and x.op_str.startswith("eax, dword ptr [rcx") and i + 2 < len(cb):
        d = 0 if x.op_str == "eax, dword ptr [rcx]" else x.operands[1].mem.disp
        st = next((y for y in cb[i + 1:i + 8] if y.mnemonic == "mov" and rip(y) and y.op_str.startswith("qword ptr [rip")), None)
        dests[d] = "%08X" % rip(st)[0] if st else None
check("B2", sorted(dir_reads) == [0, 4, 8, 0xC, 0x10, 0x14, 0x18, 0x1C] and dests[0] == "02AEE810" and dests[0x18] == "02AEE848" and dests[0x1C] == "02AEE880"
      and dests[0x10] == "02AEE880" and dests[0x14] == "02AEE888" and at(0x0039C150, 0x0039C19C) == "cmp eax, -1"
      and cell(0x0039C150, 0x0039C244) == 0x02AEE848 and at(0x0039C150, 0x0039C24C) == "je 0x39c25b",
      "0039C150 reads directory dwords %s; bindings %s" % (["+0x%02X" % d for d in sorted(dir_reads)], {("+0x%02X" % k): v for k, v in dests.items()}))
# B3 fontpack_fs: dir 0 -> +0x08 only
fs = [S(x) for x in bodies[0x003643A0]]
check("B3", fs[4:10] == ["mov rcx, qword ptr [r11]", "mov eax, dword ptr [rcx]", "add rax, rcx", "mov qword ptr [r11 + 8], rax",
                        "mov eax, dword ptr [rcx + 4]", "add rax, rcx"] and "mov qword ptr [r11 + 0x190], rax" in fs
      and "or dword ptr [r11 + 0x240], 0xc0000000" in fs and not any("+ 0xc]" in s and "dword ptr [rax" in s for s in fs)
      and [s for s in fs if s.startswith("mov ecx, dword ptr [rax + ")] == ["mov ecx, dword ptr [rax + 8]", "mov ecx, dword ptr [rax + 0x10]",
                                                                           "mov ecx, dword ptr [rax + 0x14]", "mov ecx, dword ptr [rax + 0x18]"]
      and [s for s in fs if s.startswith("mov ecx, 0x")] == ["mov ecx, 0xb", "mov ecx, 0xd", "mov ecx, 0xe", "mov ecx, 0xf"]
      and sum(1 for s in fs if s.startswith("cmp qword ptr [r") and s.endswith(", 0")) == 4,
      "dir 0 -> +0x08, dir 1 -> +0x190; dirs 2/4/5/6 bound only into null fields; dir 3 never read; faces 0xB/0xD/0xE/0xF")
# B4 tex2pack and clutpack binders
b_ad0 = [S(x) for x in bodies[0x00280AD0]]
check("B4", b670[b670.index("mov ebx, 0x338")] and "add rbx, 8" in b670 and "add rdi, 4" in b670 and "cmp rbx, 0x388" in b670 and "call 0x24a1d0" in b670
      and "mov ecx, dword ptr [rax + 0x28]" in b670 and "mov qword ptr [rdx + 0x388], rcx" in b670
      and all(("mov qword ptr [rdx + 0x%x], " % o) in " ".join(b_ad0) for o in (0x390, 0x398, 0x3A0, 0x3A8)),
      "tex2pack: +0x338..+0x380 step 8 with offsets step 4 via 0024A1D0, dir 10 raw at +0x388; clutpack: +0x390..+0x3A8")
# B5 the MRP relocation loop
mrp = sorted({f for f, _a, _m in calls_to[0x002A00F0]} - {0x00249660})
check("B5", mrp == [0x00280980] and "cmp rdi, 0x5c" in [S(x) for x in bodies[0x00280980]] and not any(T(x) == 0x002A00F0 for x in bodies[0x002808D0]),
      "002A00F0 is called by %s (loop bound 0x5C = 23 dwords); 002808D0 only requests" % ["%08X" % f for f in mrp])
# B6 the preset setter's callers, including a script verb
setter = [("%08X" % f, "%08X" % a, m) for f, a, m in calls_to[0x0025A160]]
verb = [l.split("\t") for l in io.open(VERBS, encoding="utf-8") if "\t00356CB0\t" in l]
check("B6", setter == [("00304060", "003040B7", "call"), ("00304140", "00304152", "call"), ("00356CB0", "00356CC2", "jmp")]
      and verb and verb[0][1] == "setbehindcameratype" and verb[0][0] == "01CB"
      and [S(x) for x in bodies[0x0025A160]][3:5] == ["cmp ecx, dword ptr [rax + 4]", "jge 0x25a17c"],
      "0025A160 <- %s; 00356CB0 is verb %s %s; bound: %s (signed, upper only)"
      % (setter, verb[0][0] if verb else "?", verb[0][1] if verb else "?", [S(x) for x in bodies[0x0025A160]][3:5]))
# B7 the behindcamera bind
b370 = [S(x) for x in bodies[0x00259370]]
check("B7", b370[0] == "mov eax, ecx" and cell(0x00259370, 0x00259372) == 0x02098DF0 and "cmp dword ptr [rax + 4], 0" in b370 and "jle 0x259392" in b370
      and cell(0x00259370, 0x00259383) == 0x02098DF8 and b370[-2] == "jmp 0x259fe0",
      "00259370: %s -> [02098DF0]; null and count <= 0 rejected; selector 02098DF8 zeroed; tail 00259FE0" % b370[0])
# B8 fontcolor and monotone_chr
fc = [S(x) for x in bodies[0x002DD840]]
mono = [S(x) for x in bodies[0x002C8EE0]]
check("B8", cell(0x002DD840, 0x002DD849) == 0x0215E6B8 and cell(0x002DD840, 0x002DD853) == 0x0215E6C8 and "lea rax, [rcx + 4]" in fc
      and "lea edx, [rdi + 0x74]" in mono and "add ebx, 0x880" in mono and "add rax, 0x1dc0" in mono and "mov r8, qword ptr [rcx + 0x390]" in mono,
      "fontcolor count -> 0215E6B8, pairs -> 0215E6C8; monotone_chr 0x74 + edi, +0x880, clutpack +0x390 -> alloc + 0x1DC0")
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)   # a BROKEN row must fail the process, not only the text (ASTRA feb631dd4, 2026-09-29)
