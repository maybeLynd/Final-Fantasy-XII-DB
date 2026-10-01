"""select_descriptor_pair_accessors.py - thread-safe magic-static accessors
whose lazily-built static is a 16-byte pair { tagged_record_pointer, 0 }.

The 115-byte form (accessor-family/arch_forms.txt form #10), e.g. 005C3B10:

    sub rsp,0x28
    mov rax,gs:[0x58]              ; TEB->ThreadLocalStoragePointer
    mov ecx,[_tls_index]           ; -> 02EAED3C
    mov edx,4
    mov rcx,[rax+rcx*8]            ; this module's TLS block
    mov eax,[rdx+rcx]              ; _Init_thread_epoch (block+4)
    cmp [guard],eax                ; already stamped for this epoch?
    jg slow
    lea rax,[static]               ; fast path: return &static
    add rsp,0x28
    ret
slow:
    lea rcx,[guard]
    call _Init_thread_header       ; 008092FC
    cmp [guard],-1
    jne fast                       ; another thread built it
    lea rax,[record]               ; the payload: a .data record
    mov qword [static+8],0
    or rax,1                       ; tag bit
    lea rcx,[guard]
    mov [static],rax               ; static = { record|1, 0 }
    call _Init_thread_footer       ; 0080929C
    jmp fast

Unlike the 98..474B singleton guards (magic-static-singleton-guards.tsv)
there is NO atexit registration - the pair is POD.  The records are shared
(61 accessors point at 27 distinct .data records, several already identified
as Phyre PClassDescriptorConcrete<> singletons); the constructors/records
themselves are NOT dispositioned by this family.

Verified per member, operand level: the 22-instruction sequence is fixed;
the only varying operands are the guard cell, the static pair and the
record - plus the invariant guard == static + 0x10.

Usage: python select_descriptor_pair_accessors.py [--write]
"""
import io, os, re, struct, sys, collections

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(ROOT, "..", "..", "..", "..", ".."))
EXE = os.path.join(REPO, "Database", "Tools", "work", "exe", "FFXII_TZA.exe")
FUNCS = os.path.join(REPO, "Database", "Tools", "work", "graph", "functions.tsv")
DB = os.path.join(REPO, "Database", "FFXII TZA")
OUT = os.path.join(ROOT, "descriptor-pair-accessors.tsv")

HDR, FTR = 0x8092FC, 0x80929C
TLS_INDEX = 0x2EAED3C
SELF = "members/descriptor-pair-accessors.tsv"
EXPECT = 61

sys.path.insert(0, os.path.join(REPO, "Database", "Tools", "analysis-kit", "gfz-scripts"))
import check_dispositions as CD
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

d = io.open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]
nsec = struct.unpack_from("<H", d, pe + 6)[0]
optsz = struct.unpack_from("<H", d, pe + 20)[0]
base = struct.unpack_from("<Q", d, pe + 24 + 24)[0]
secs = []
for i in range(nsec):
    o = pe + 24 + optsz + i * 40
    vsz, va, rsz, ptr = struct.unpack_from("<IIII", d, o + 8)
    secs.append((va, vsz, ptr, rsz))


def off(va):
    r = va - base
    for sva, vsz, ptr, rsz in secs:
        if sva <= r < sva + max(vsz, rsz):
            return ptr + (r - sva)
    return None


sizes = {}
for l in io.open(FUNCS, encoding="utf-8", errors="replace"):
    p = l.rstrip("\n").split("\t")
    try:
        sizes[int(p[0], 16)] = int(p[2])
    except (ValueError, IndexError):
        pass

md = Cs(CS_ARCH_X86, CS_MODE_64)


def rip(i):
    m = re.search(r"rip \+ 0x([0-9a-f]+)", i.op_str)
    return i.address + i.size + int(m.group(1), 16) if m else None


def imm_target(i):
    return int(i.op_str, 16) if i.op_str.startswith("0x") else None


MN = ["sub", "mov", "mov", "mov", "mov", "mov", "cmp", "jg",
      "lea", "add", "ret",
      "lea", "call", "cmp", "jne",
      "lea", "mov", "or", "lea", "mov", "call", "jmp"]


def verify(e):
    """Return (guard, static, record) if e is the exact 115B form, else None."""
    o = off(e)
    if o is None or sizes.get(e) != 115:
        return None
    ins = list(md.disasm(d[o:o + 115], e))
    if len(ins) != 22 or [i.mnemonic for i in ins] != MN:
        return None
    # TLS prologue
    if ins[1].op_str != "rax, qword ptr gs:[0x58]":
        return None
    if rip(ins[2]) != TLS_INDEX or ins[3].op_str != "edx, 4":
        return None
    if ins[4].op_str != "rcx, qword ptr [rax + rcx*8]" or ins[5].op_str != "eax, dword ptr [rdx + rcx]":
        return None
    guard = rip(ins[6])
    if guard is None or ins[6].op_str.split(",")[1].strip() != "eax":
        return None
    if imm_target(ins[7]) != ins[11].address:  # jg -> slow
        return None
    static = rip(ins[8])
    if static is None or ins[9].op_str != "rsp, 0x28":
        return None
    fast = ins[8].address  # lea rax,[static] is the shared return point
    if rip(ins[11]) != guard or imm_target(ins[12]) != HDR:
        return None
    if rip(ins[13]) != guard or not ins[13].op_str.rstrip().endswith(", -1"):
        return None
    if imm_target(ins[14]) != fast:
        return None
    record = rip(ins[15])
    if record is None:
        return None
    m = re.match(r"qword ptr \[rip \+ 0x[0-9a-f]+\], 0$", ins[16].op_str)
    if not m or rip(ins[16]) != static + 8:
        return None
    if ins[17].op_str != "rax, 1":
        return None
    if rip(ins[18]) != guard or rip(ins[19]) != static:
        return None
    if not ins[19].op_str.startswith("qword ptr") or not ins[19].op_str.endswith(", rax"):
        return None
    if imm_target(ins[20]) != FTR or imm_target(ins[21]) != fast:
        return None
    if guard != static + 0x10:
        return None
    return guard, static, record


a_set, _eo, _ai, _da = CD.measure_a(DB, sizes)
dec = {}
for doc, parts in CD.parse_families(DB):
    if len(parts) < 5 or parts[1] not in ("B", "C", "D"):
        continue
    if parts[2] == SELF:
        continue
    try:
        for m in CD.read_members(doc, parts[2]):
            dec[m] = parts[0]
    except (IOError, OSError, ValueError):
        pass

hits, owned = [], []
for e in sorted(sizes):
    v = verify(e)
    if v is None:
        continue
    (owned if (e in dec or e in a_set) else hits).append((e,) + v)

print("descriptor-pair accessor census hits: %d frontier + %d owned/A"
      % (len(hits), len(owned)))
if owned:
    own = collections.Counter(dec.get(e, "A") for e, *_ in owned)
    print("   owned by:", ", ".join("%s x%d" % kv for kv in own.most_common()))
records = collections.Counter(r for _, _, _, r in hits)
print("distinct payload records: %d (shared by %d accessors)"
      % (len(records), len(hits)))

if len(hits) != EXPECT:
    print("REFUSING TO WRITE: expected %d frontier members, got %d" % (EXPECT, len(hits)))
    sys.exit(1)

if "--write" in sys.argv:
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as fp:
        fp.write("# %d thread-safe magic-static accessors for 16-byte pairs\n" % len(hits))
        fp.write("# { tagged_record_pointer, 0 }.  115-byte form (arch_forms.txt #10):\n")
        fp.write("# TLS epoch gate + _Init_thread_header/footer; init is inlined\n")
        fp.write("# `static = record|1; static+8 = 0` - no atexit (POD).  The 61 accessors\n")
        fp.write("# share 27 distinct .data records (several are Phyre\n")
        fp.write("# PClassDescriptorConcrete<> singletons).  guard = static + 0x10.\n")
        fp.write("# member\tsize\tstatic\tguard\trecord\n")
        for e, g, s, r in hits:
            fp.write("%08X\t%d\t%08X\t%08X\t%08X\n" % (e, sizes[e], s, g, r))
    print("wrote", OUT, len(hits), "rows")
else:
    for e, g, s, r in hits:
        print("   %08X  static %08X  guard %08X  record %08X" % (e, s, g, r))
    print("dry run - pass --write to emit the TSV")
