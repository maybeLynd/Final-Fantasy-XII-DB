"""atl_filter.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only; nothing executed.
The ABI and receiver identity behind the crash filter's text, for ASTRA-REQ-OPUS-NATIVE-FILTER-TAIL (ASTRA 81) and
ASTRA-REQ-OPUS-NATIVE-FILTER-RESOURCE (ASTRA 82). Written from the bytes; ASTRA's records are static (method A) evidence.

  M  THE RECEIVER 02EAF320 IS ATL's _AtlBaseModule (CAtlBaseModule, 0x60 bytes): its constructor 0080C440, called with
     rcx = 02EAF320 at 0016A2A0, zeroes +0x28..+0x4F (memset 0x28) and +0x50 / +0x58 / +0x5C, stores +0x08 and +0x10 =
     the image base 00120000, +0x20 = 01CC7308, +0x00 = 0x60 (cbSize, the extent), +0x18 = 0xE00, then initialises the
     critical section at +0x28 (0019A650); on failure it prints "ERROR : Unable to initialize critical section in
     CAtlBaseModule" and sets the byte 01F81108. The destructor 0080C4E8 (reached from 008B9088 with rcx = 02EAF320)
     deletes the critical section, frees +0x50 and zeroes +0x50 / +0x58 / +0x5C
  G  0080C51C = CAtlBaseModule::GetHInstanceAt(this, int i): EnterCriticalSection(this + 0x28); i > [+0x58] or i < 0
     gives null; i == [+0x58] gives [+0x10]; otherwise [[+0x50] + 8i]; LeaveCriticalSection. The RaiseException
     (0xC000008C, array bounds exceeded) + int3 at 0080C582..0080C597 is unreachable from that order of tests
  L  0019A510 = AtlGetStringResourceImage(UINT id): for i = 0, 1, ... while GetHInstanceAt(&02EAF320, i) is non-null and
     nothing is found: FindResourceW(h, (id >> 4) + 1, RT_STRING = 6), and when found 0019A5B0(h, hrsrc, id); returns
     the first non-null result
  S  0019A5B0 = AtlGetStringResourceImage(HINSTANCE, HRSRC, UINT id): LoadResource, LockResource, SizeofResource; skips
     id & 15 counted strings ({u16 n; u16 text[n]}) while inside the block; returns the counted string's address, or null
     when the walk leaves the block or the selected string is empty. The caller gets the length prefix, not text + 2
  F  0079AD50, the unhandled-exception filter (LONG WINAPI (EXCEPTION_POINTERS *)): rcx is kept in rbx and written into a
     packed MINIDUMP_EXCEPTION_INFORMATION at [rsp+0x40] {ThreadId +0, ExceptionPointers +4, ClientPointers +0xC = 1};
     when the dword 01F40128 is 0 it returns at once. Otherwise: MiniDumpWriteDump (thunk 0080F2BC, type 0x1826), CloseHandle,
     SysFreeString(null), text = 0019A510(0x7837); a non-null image becomes SysAllocStringLen(image + 2, image[0]),
     otherwise the text stays null; ShowCursor(1); MessageBoxW(null, text, L"error" (008F3DC0), 0x10 = MB_OK | MB_ICONHAND);
     SysFreeString(text). Every path ends `mov eax, 1 / ret` - EXCEPTION_EXECUTE_HANDLER
  R  THE TEXT: RT_STRING block 0x784 (= (0x7837 >> 4) + 1), entry 7 (= 0x7837 & 15), language 0x409 is "Fatal error
     encountered." (24 UTF-16 units); nine languages carry the entry
  C  CONTROLS: every import named here is resolved from the import table, not assumed (the two OLEAUT32 slots are
     imported by ordinal, 6 and 4; SysFreeString / SysAllocStringLen are pefile's names for those ordinals); the neighbouring entries 6 and 8
     of block 0x784 differ from entry 7; an `id & 15` off by one (entry 8) is rejected
  N  WHICH MODULE: the object's address is formed only at 0016A2A0, 0019A528, 0019A576 and 008B9088, and GetHInstanceAt's only
     callers are in 0019A510, so nothing but the constructor and destructor writes +0x50 / +0x58: the count stays 0 and the
     lookup searches the game image's own resources only - conditionally: the constructor ran and no computed write fills
     the array (no static writer; a computed-pointer write and actual initialisation are not established)
  W  REGRESSION (FAILS before --patch): CAtlBaseModule (0x60) and its fields are in the store and tile
Not claimed: which HMODULEs the array holds at run time, the language Windows selects, that the message is shown,
what the process does after EXCEPTION_EXECUTE_HANDLER, or how the #DE of an OPDIV (script-divide-opus) reaches here.
Usage: python atl_filter.py [--patch]
"""
import hashlib, os, re, struct, sys
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__)); DB = os.path.abspath(os.path.join(HERE, "..", "..", "..")); ROOT = os.path.dirname(DB)
EXEP = os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe")
d = open(EXEP, "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
B = 0x120000
pe = pefile.PE(EXEP)
off = lambda v: pe.get_offset_from_rva(v - B)
IMP, ORD = {}, {}
for e in pe.DIRECTORY_ENTRY_IMPORT:
    for i in e.imports:
        IMP[i.address] = i.name.decode() if i.name else "ord%d" % i.ordinal
        if i.ordinal is not None: ORD[i.address] = i.ordinal
cs = Cs(CS_ARCH_X86, CS_MODE_64)
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
def dis(lo, hi):
    out = {}
    for x in cs.disasm(d[off(lo):off(hi)], lo):
        o = x.op_str; m = re.search(r"\[rip ([+-]) (0x[0-9a-f]+)\]", o)
        if m:
            t = x.address + x.size + (1 if m.group(1) == "+" else -1) * int(m.group(2), 16)
            o = re.sub(r"\[rip [+-] 0x[0-9a-f]+\]", "[%08X%s]" % (t, ("=" + IMP[t]) if t in IMP else ""), o)
        out[x.address] = (x.mnemonic, o)
    return out
def has(A, pairs):
    miss = [("%08X" % a, A.get(a), v) for a, v in pairs if A.get(a) != v]
    if miss: print("   missing", miss[:4])
    return not miss
K = dis(0x80C440, 0x80C51C)
check("M", has(K, [(0x80C44F, ("lea", "r8d, [rdx + 0x28]")), (0x80C453, ("add", "rcx, r8")), (0x80C456, ("call", "0x861ec0")),
                   (0x80C45B, ("and", "qword ptr [rdi + 0x50], 0")), (0x80C460, ("lea", "rax, [00120000]")), (0x80C467, ("and", "dword ptr [rdi + 0x58], 0")),
                   (0x80C46F, ("and", "dword ptr [rdi + 0x5c], 0")), (0x80C476, ("mov", "qword ptr [rdi + 0x10], rax")), (0x80C47C, ("mov", "qword ptr [rdi + 8], rax")),
                   (0x80C480, ("lea", "rax, [01CC7308]")), (0x80C487, ("mov", "qword ptr [rdi + 0x20], rax")), (0x80C48B, ("mov", "dword ptr [rdi], 0x60")),
                   (0x80C491, ("mov", "dword ptr [rdi + 0x18], 0xe00")), (0x80C498, ("call", "0x19a650")), (0x80C4C3, ("lea", "rcx, [01CC7320]")),
                   (0x80C4CA, ("call", "qword ptr [008C2388=OutputDebugStringW]")), (0x80C4D0, ("mov", "byte ptr [01F81108], 1")),
                   (0x80C4F5, ("call", "qword ptr [008C20D0=DeleteCriticalSection]")), (0x80C4FB, ("mov", "rcx, qword ptr [rbx + 0x50]")), (0x80C504, ("call", "0x861f26")),
                   (0x80C50E, ("and", "dword ptr [rbx + 0x58], 0")), (0x80C512, ("and", "dword ptr [rbx + 0x5c], 0"))])
      and d[off(0x1CC7320):off(0x1CC7320) + 130].decode("utf-16-le").startswith("ERROR : Unable to initialize critical section in CAtlBaseModule")
      and dis(0x16A2A0, 0x16A2AC).get(0x16A2A0) == ("lea", "rcx, [02EAF320]") and dis(0x16A2A0, 0x16A2AC).get(0x16A2A7) == ("call", "0x80c440")
      and dis(0x8B9088, 0x8B9094).get(0x8B9088) == ("lea", "rcx, [02EAF320]") and dis(0x8B9088, 0x8B9094).get(0x8B908F) == ("jmp", "0x80c4e8"),
      "02EAF320 is CAtlBaseModule: ctor 0080C440 (called 0016A2A0) stores cbSize 0x60, image base at +0x08/+0x10, 0xE00 at +0x18, 01CC7308 at +0x20, zeroes +0x28 (0x28 B) and +0x50..+0x5F; dtor 0080C4E8 (from 008B9088)")
G = dis(0x80C51C, 0x80C598)
check("G", has(G, [(0x80C533, ("movsxd", "rbx, edx")), (0x80C536, ("add", "rcx, 0x28")), (0x80C53A, ("call", "qword ptr [008C20B8=EnterCriticalSection]")),
                   (0x80C542, ("cmp", "ebx, dword ptr [rsi + 0x58]")), (0x80C545, ("jg", "0x80c554")), (0x80C549, ("js", "0x80c554")), (0x80C54E, ("jne", "0x80c576")),
                   (0x80C550, ("mov", "rdi, qword ptr [rsi + 0x10]")), (0x80C558, ("call", "qword ptr [008C20C0=LeaveCriticalSection]")),
                   (0x80C576, ("jge", "0x80c582")), (0x80C578, ("mov", "rax, qword ptr [rsi + 0x50]")), (0x80C57C, ("mov", "rdi, qword ptr [rax + rbx*8]")),
                   (0x80C588, ("mov", "ecx, 0xc000008c")), (0x80C591, ("call", "qword ptr [008C22B8=RaiseException]")), (0x80C597, ("int3", ""))]),
      "GetHInstanceAt: lock +0x28; i > count(+0x58) or i < 0 -> null; i == count -> +0x10; else (+0x50)[i]; the bounds raise is unreachable")
L = dis(0x19A510, 0x19A5A4)
check("L", has(L, [(0x19A524, ("mov", "ebp, ecx")), (0x19A528, ("lea", "rcx, [02EAF320]")), (0x19A531, ("call", "0x80c51c")), (0x19A548, ("lea", "r8d, [rbx + 6]")),
                   (0x19A54C, ("shr", "eax, 4")), (0x19A552, ("inc", "ax")), (0x19A558, ("call", "qword ptr [008C2108=FindResourceW]")), (0x19A563, ("mov", "r8d, ebp")),
                   (0x19A566, ("mov", "rdx, rax")), (0x19A569, ("mov", "rcx, rdi")), (0x19A56C, ("call", "0x19a5b0")), (0x19A576, ("lea", "rcx, [02EAF320]")),
                   (0x19A57D, ("call", "0x80c51c")), (0x19A58A, ("jne", "0x19a541")), (0x19A591, ("mov", "rax, rbx"))]),
      "0019A510(id): per module from GetHInstanceAt(02EAF320, i): FindResourceW(h, (id >> 4) + 1, 6) then 0019A5B0(h, hrsrc, id)")
S = dis(0x19A5B0, 0x19A64F)
check("S", has(S, [(0x19A5BF, ("mov", "edi, r8d")), (0x19A5C8, ("call", "qword ptr [008C20E8=LoadResource]")), (0x19A5EB, ("call", "qword ptr [008C20F0=LockResource]")),
                   (0x19A5FF, ("call", "qword ptr [008C20F8=SizeofResource]")), (0x19A607, ("add", "rcx, rbx")), (0x19A60A, ("and", "edi, 0xf")),
                   (0x19A615, ("movzx", "eax, word ptr [rbx]")), (0x19A618, ("lea", "rbx, [rbx + rax*2]")), (0x19A61C, ("add", "rbx, 2")),
                   (0x19A625, ("cmp", "rbx, rcx")), (0x19A628, ("jb", "0x19a62e")), (0x19A630, ("cmp", "word ptr [rbx], ax")), (0x19A633, ("cmove", "rbx, rax")),
                   (0x19A637, ("mov", "rax, rbx"))]),
      "0019A5B0(h, hrsrc, id): load/lock/size; skip id & 15 counted strings; the counted string's address, or null (out of block or empty)")
F = dis(0x79AD50, 0x79AE40)
rets = [a for a, (m, o) in F.items() if m == "ret"]
check("F", has(F, [(0x79AD56, ("mov", "rbx, rcx")), (0x79AD59, ("call", "qword ptr [008C21D8=GetCurrentThreadId]")), (0x79AD5F, ("cmp", "dword ptr [01F40128], 0")),
                   (0x79AD66, ("mov", "dword ptr [rsp + 0x40], eax")), (0x79AD6A, ("mov", "dword ptr [rsp + 0x4c], 1")), (0x79AD72, ("mov", "qword ptr [rsp + 0x44], rbx")),
                   (0x79AD77, ("je", "0x79ae35")), (0x79ADA8, ("mov", "r9d, 0x1826")), (0x79ADB6, ("lea", "rax, [rsp + 0x40]")), (0x79ADC3, ("mov", "qword ptr [rsp + 0x20], rax")),
                   (0x79ADCA, ("call", "0x80f2bc")), (0x79ADD2, ("call", "qword ptr [008C23E0=CloseHandle]")), (0x79ADD8, ("xor", "ecx, ecx")),
                   (0x79ADDA, ("call", "qword ptr [008C27C8=SysFreeString]")), (0x79ADE0, ("mov", "ecx, 0x7837")), (0x79ADE5, ("call", "0x19a510")),
                   (0x79ADF9, ("movzx", "edx, word ptr [rax]")), (0x79ADFC, ("lea", "rcx, [rax + 2]")), (0x79AE00, ("call", "qword ptr [008C27D0=SysAllocStringLen]")),
                   (0x79AE09, ("mov", "ecx, 1")), (0x79AE0E, ("call", "qword ptr [008C28C0=ShowCursor]")), (0x79AE14, ("mov", "r9d, 0x10")),
                   (0x79AE1A, ("lea", "r8, [008F3DC0]")), (0x79AE21, ("mov", "rdx, rbx")), (0x79AE24, ("xor", "ecx, ecx")),
                   (0x79AE26, ("call", "qword ptr [008C29C0=MessageBoxW]")), (0x79AE2F, ("call", "qword ptr [008C27C8=SysFreeString]")), (0x79AE35, ("mov", "eax, 1"))])
      and rets == [0x79AE3F] and d[off(0x8F3DC0):off(0x8F3DC0) + 12] == "error\0".encode("utf-16-le"),
      "the filter: EXCEPTION_POINTERS* -> packed MINIDUMP_EXCEPTION_INFORMATION {tid, ptrs@+4, client=1}; gate 01F40128; MessageBoxW(0, text, L\"error\", 0x10); one ret, eax = 1")
# R and C: the resource entry
def rt_string_block(block):
    for t in pe.DIRECTORY_ENTRY_RESOURCE.entries:
        if t.id == 6:
            for n in t.directory.entries:
                if n.id == block:
                    return {l.id: pe.get_data(l.data.struct.OffsetToData, l.data.struct.Size) for l in n.directory.entries}
    return {}
def entry(blob, k):
    p = 0
    for _ in range(k):
        p += 2 + 2 * struct.unpack_from("<H", blob, p)[0]
    n = struct.unpack_from("<H", blob, p)[0]
    return blob[p + 2:p + 2 + 2 * n].decode("utf-16-le")
blk = rt_string_block((0x7837 >> 4) + 1)
en = blk.get(0x409, b"")
check("R", (0x7837 >> 4) + 1 == 0x784 and 0x7837 & 15 == 7 and len(blk) == 9 and en and entry(en, 7) == "Fatal error encountered." and len(entry(en, 7)) == 24,
      "RT_STRING block 0x784 entry 7, language 0409: %r (%d units); %d languages" % (entry(en, 7) if en else None, len(entry(en, 7)) if en else 0, len(blk)))
# B (2026-09-28, ASTRA-REQ-OPUS-RESOURCE-PREFIX-BOUNDARY): the selector's only bound tests compare the walking pointer with
# the block end (0019A610, 0019A625); nothing tests prefix + 2 + 2n against it. Every entry of all nine shipped block-0x784
# variants fits its block, so the shipped data meets the span precondition that the selector does not enforce.
cmps = [(a, v) for a, v in S.items() if v[0] == "cmp"]
def fits(blob):
    p = 0
    for _ in range(16):
        if p + 2 > len(blob): return False
        n = struct.unpack_from("<H", blob, p)[0]; p += 2 + 2 * n
        if p > len(blob): return False
    return True
check("B", cmps == [(0x19A610, ("cmp", "rbx, rcx")), (0x19A625, ("cmp", "rbx, rcx")), (0x19A630, ("cmp", "word ptr [rbx], ax"))]
      and not any("rbx + rax*2 + 2" in v[1] or ("lea" == v[0] and "rax*2 + 2" in v[1]) for v in S.values())
      and len(blk) == 9 and all(fits(b) for b in blk.values()),
      "0019A5B0 bounds only the walking pointer (cmp rbx, rcx at 0019A610 / 0019A625) - no test of prefix + 2 + 2n; all 16 entries of "
      "all %d shipped block-0x784 variants fit their block" % len(blk))
check("C", en and entry(en, 6) != entry(en, 7) and entry(en, 8) != entry(en, 7) and all(v in IMP for v in (0x8C2108, 0x8C20E8, 0x8C20F0, 0x8C20F8, 0x8C29C0, 0x8C27D0, 0x8C27C8, 0x8C20B8, 0x8C20C0)) and ORD.get(0x8C27C8) == 6 and ORD.get(0x8C27D0) == 4,
      "entries 6 / 8 differ from 7 (%r / %r); every import named is resolved from the import table" % (entry(en, 6) if en else None, entry(en, 8) if en else None))
# N: who forms the object's address, and who calls its users
tb_sec = [s for s in pe.sections if s.Name.startswith(b".text")][0]; ts, tb = tb_sec.VirtualAddress, tb_sec.get_data()
lea = sorted({B + ts + i - 3 for i in range(3, len(tb) - 4) if tb[i - 3:i] == b"\x48\x8d\x0d" and B + ts + i + 4 + struct.unpack_from("<i", tb, i)[0] == 0x2EAF320})
def rip_ref(i, k):   # a disp32 at i, instruction ending k bytes after it, decoded from each possible start
    for st in range(max(0, i - 4), i):
        x = next(cs.disasm(tb[st:st + 16], B + ts + st), None)
        if x is not None and x.address + x.size == B + ts + i + 4 + k and "rip" in x.op_str: return True
    return False
anyref = sorted({B + ts + i for i in range(len(tb) - 4) for k in range(0, 6)
                 if 0x2EAF320 <= B + ts + i + 4 + k + struct.unpack_from("<i", tb, i)[0] < 0x2EAF380 and rip_ref(i, k)})
def callers(t): return [B + ts + i for i in range(len(tb) - 5) if tb[i] in (0xE8, 0xE9) and B + ts + i + 5 + struct.unpack_from("<i", tb, i + 1)[0] == t]
qref = [i for i in range(0, len(d) - 8, 8) if 0x2EAF320 <= struct.unpack_from("<Q", d, i)[0] < 0x2EAF380 or struct.unpack_from("<Q", d, i)[0] in (0x80C51C, 0x80C440, 0x80C4E8)]
check("N", lea == [0x16A2A0, 0x19A528, 0x19A576, 0x8B9088] and len(anyref) == 4 and callers(0x80C51C) == [0x19A531, 0x19A57D] and callers(0x80C440) == [0x16A2A7]
      and callers(0x80C4E8) == [0x8B908F] and not qref,
      "the object's address is formed only at %s; GetHInstanceAt's only callers are 0019A531 / 0019A57D; no absolute pointer to the object or its three methods. "
      "So nothing but the constructor and destructor writes +0x50 / +0x58: the count stays 0, GetHInstanceAt(0) returns hInstResource (the image base) "
      "and GetHInstanceAt(1) null - the lookup searches the game image's own resources only (no static writer; a computed-pointer write is not excluded)"
      % ["%08X" % a for a in lea])
REC = "_index/candidates/native-filter-abi-opus/atl_filter.py"; EXE = "exe 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
T = "CAtlBaseModule"
PV, PB, DU = ("TYPE RESOLVED", "PROVEN"), ("TYPE RESOLVED", "PROBABLE"), ("DISCOVERED", "UNKNOWN")
ROWS = [(0x00, 4, "cbSize", "uint32", "0x60, stored by the constructor (0080C48B): the structure's own size, its extent", PV),
        (0x04, 4, "unobservedSpan0004", "u8[4]", "declared gap - the constructor's cbSize store is a dword; no access read here", DU),
        (0x08, 8, "hInst", "void*", "the image base 00120000, stored by the constructor (0080C47C)", PV),
        (0x10, 8, "hInstResource", "void*", "the image base, stored by the constructor (0080C476); GetHInstanceAt 0080C51C returns it when the index equals the count at +0x58", PV),
        (0x18, 4, "atlBuildVer", "uint32", "0xE00, stored by the constructor (0080C491); no reader found here", PB),
        (0x1C, 4, "unobservedSpan001C", "u8[4]", "declared gap - no access read here", DU),
        (0x20, 8, "guidVer", "void*", "01CC7308, a 16-byte GUID in .rdata, stored by the constructor (0080C487); no reader found here", PB),
        (0x28, 40, "resourceLock", "u8[40]", "a Win64 CRITICAL_SECTION: zeroed by the constructor's memset (0080C456) and initialised by 0019A650; GetHInstanceAt enters and leaves it; the destructor deletes it", PV),
        (0x50, 8, "resourceInstances", "void*", "the HINSTANCE array GetHInstanceAt indexes at stride 8 (0080C578 / 0080C57C); the destructor frees it (00861F26) and nulls it", PV),
        (0x58, 4, "resourceInstanceCount", "int32", "the array's count: GetHInstanceAt compares its signed index against it (0080C542, 0080C54B); zeroed by the constructor and destructor", PV),
        (0x5C, 4, "resourceInstanceCapacity", "int32", "zeroed by the constructor and destructor with the count; no other access read here (ATL's CSimpleArray keeps its allocated size here)", PB)]
TROW = [T, "0x60", "24-Compiler-And-CRT-Runtime", "one static object at 02EAF320 (ATL's _AtlBaseModule); GetHInstanceAt 0080C51C and the string-resource lookup 0019A510 take it",
        "IMAGE - static at 02EAF320, constructed by 0080C440 from 0016A2A0", "0080C440 (cbSize 0x60; prints 'Unable to initialize critical section in CAtlBaseModule' on failure)",
        "0080C4E8, reached from 008B9088", PV[0], PV[1], "L1",
        "CARVED 2026-09-28 (OPUS, %s M G L S). The constructor's cbSize store gives the extent; the class name is the constructor's own debug string. %s" % (REC, EXE),
        "23-Third-Party-Libraries/third-party-middleware-inventory.md", "STATIC - 02EAF320"]
FI = os.path.join(DB, "_types", "fields.tsv"); TY = os.path.join(DB, "_types", "types.tsv")
def cells(l): return l.rstrip("\r\n").split("\t")
if "--patch" in sys.argv:
    fl = open(FI, "rb").read().decode("utf-8").splitlines(keepends=True); e = fl[1][len(fl[1].rstrip("\r\n")):]
    if not any(cells(l)[0] == T for l in fl):
        fl += ["\t".join([T, "0x%02X" % o, str(n), nm, ct, m, rd[0], rd[1], "CARVED 2026-09-28 (OPUS, %s M G). %s" % (REC, EXE)]) + e for o, n, nm, ct, m, rd in ROWS]
        open(FI, "wb").write("".join(fl).encode("utf-8"))
    tl = open(TY, "rb").read().decode("utf-8").splitlines(keepends=True); te = tl[1][len(tl[1].rstrip("\r\n")):]
    if not any(cells(l)[0] == T for l in tl):
        tl.append("\t".join(TROW) + te); open(TY, "wb").write("".join(tl).encode("utf-8"))
    print("patched"); sys.exit(0)
FR = [cells(l) for l in open(FI, "rb").read().decode("utf-8").splitlines() if cells(l)[0] == T]
TR = [cells(l) for l in open(TY, "rb").read().decode("utf-8").splitlines() if cells(l)[0] == T]
pos = 0; tiled = True
for c in FR:
    tiled &= int(c[1], 16) == pos; pos += int(c[2])
check("W", len(TR) == 1 and TR[0][1] == "0x60" and tiled and pos == 0x60 and [c[3] for c in FR if c[1] in ("0x10", "0x50", "0x58")] == ["hInstResource", "resourceInstances", "resourceInstanceCount"],
      "CAtlBaseModule (0x60) is in the store and its %d rows tile to 0x%X" % (len(FR), pos))
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
