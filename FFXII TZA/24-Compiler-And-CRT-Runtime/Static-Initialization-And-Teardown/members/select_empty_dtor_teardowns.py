"""select_empty_dtor_teardowns.py - the empty-destructor static-teardown wrappers.

EC-7 family C member selector, replacing the misnamed 'Control Flow Guard
static-guard adapters'. Re-derives membership from the shipping EXE:

  1. census-wide byte scan of .text for the 12-byte form
        48 8D 0D <rel32>   lea rcx,[a static]
        E9 <rel32>         jmp 0016D6A0
     where the E9 displacement resolves to 0016D6A0. That target is a
     one-instruction `ret 0` - an ICF-folded shared empty destructor, NOT a
     CFG check (all members use the direct E9 encoding; none goes through
     __guard_check_icall_fptr 008C31C0, which the loader would have to
     rewrite for a guard check to exist). Every site must be a census
     function entry - 185 sites expected, 0 interior.
  2. registration proof: each member is address-taken by a `lea rcx,[member]`
     inside a census body that then reaches the MSVC atexit wrapper 00808B90
     by EITHER spelling - `call 00808B90` or `add rsp,imm8 ; jmp 00808B90`.
     The earlier selector matched only the call spelling and missed 36.
  3. members = the 185 form sites less the bodies sibling families own on
     the same form: 36 declared by xc-registered library teardowns (the
     CRT/library statics' members of this form - their registrars sit in
     the 0015xxxx-0016xxxx CRT zone) and 4 declared by
     NativeAdapter.StaticAddressTailCall = 145 expected. OPUS's gap-40
     list is thereby fully accounted: 36 + 4, none frontier.
  4. refuses to write if the census count, the registration count, the
     exclusion count, or the A-measured exclusion move.

Semantic join (not membership): 144 of the 145 are the teardown half of the
declared 'Phyre serialization scalar-conversion initialisers' pairs
(image-hardening-cfg-aslr-dep-and-stack-cookies.md); the members file
carries the registering initialiser and lea'd static per row.

Reads: Database/Tools/work/exe/FFXII_TZA.exe, Database/Tools/work/graph/functions.tsv.
Usage: python select_empty_dtor_teardowns.py [--write]
"""
import io, os, re, struct, sys, collections

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(ROOT, "..", "..", "..", "..", ".."))
EXE = os.path.join(REPO, "Database", "Tools", "work", "exe", "FFXII_TZA.exe")
FUNCS = os.path.join(REPO, "Database", "Tools", "work", "graph", "functions.tsv")
DB = os.path.join(REPO, "Database", "FFXII TZA")
OUT = os.path.join(ROOT, "empty-dtor-teardown-wrappers.tsv")

EMPTY = 0x16D6A0          # the shared ret-0 body (ICF-folded empty dtor / guard nop)
AX = 0x808B90             # the MSVC atexit wrapper

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
_insn_cache = {}


def insns(e):
    if e not in _insn_cache:
        o = off(e); sz = sizes.get(e)
        _insn_cache[e] = [] if (o is None or sz is None) else list(md.disasm(d[o:o + sz], e))
    return _insn_cache[e]


def rip_target(i):
    m = re.search(r"rip ([+-]) 0x([0-9a-f]+)", i.op_str)
    if not m:
        return None
    disp = int(m.group(2), 16)
    return i.address + i.size + (disp if m.group(1) == "+" else -disp)


def edge_target(i):
    if i.mnemonic in ("call", "jmp") and i.op_str.startswith("0x"):
        return int(i.op_str, 16)
    return None


# --- step 1: census-wide byte-form scan over every 12-byte census entry -----
form = []
for e, sz in sizes.items():
    if sz != 12:
        continue
    o = off(e)
    if o is None:
        continue
    b = d[o:o + 12]
    if b[:3] != b"\x48\x8d\x0d" or b[7] != 0xE9:
        continue
    tgt = e + 12 + struct.unpack_from("<i", b, 8)[0]
    if tgt == EMPTY:
        form.append(e)
form.sort()
print("12-byte lea+jmp->%08X form sites: %d (expect 185)" % (EMPTY, len(form)))

# --- step 2: registration proof --------------------------------------------
# a body registers a member if it contains lea rcx,[member] and an edge to
# 00808B90 in the same body (either `call` or `add rsp,N ; jmp` spelling).
registrar = {}
spelling = collections.Counter()
for e, sz in sizes.items():
    if off(e) is None:
        continue
    body = insns(e)
    # walk the body: a lea rcx,[X] registers X if the next rcx-write or
    # call/jmp we meet is the edge to the atexit wrapper itself
    pending = None
    for i in body:
        if i.mnemonic == "lea" and i.op_str.startswith("rcx,"):
            pending = rip_target(i)
            continue
        if i.mnemonic in ("call", "jmp"):
            if pending is not None and edge_target(i) == AX and pending in form \
                    and pending not in registrar:
                registrar[pending] = e
                spelling[i.mnemonic] += 1
            pending = None
            continue
        if i.mnemonic.startswith("mov") and i.op_str.startswith("rcx,"):
            pending = None
unregistered = [e for e in form if e not in registrar]
print("registered: %d of %d (call spelling %d, jmp spelling %d); unregistered: %d"
      % (len(registrar), len(form), spelling["call"], spelling["jmp"], len(unregistered)))
for e in unregistered:
    print("   UNREGISTERED %08X" % e)

# --- step 3: exclusions ------------------------------------------------------
a_set, _eo, _ai, _da = CD.measure_a(DB, sizes)
dec = {}
for doc, parts in CD.parse_families(DB):
    if len(parts) < 5 or parts[1] not in ("B", "C", "D"):
        continue
    if parts[2] in ("members/empty-dtor-teardown-wrappers.tsv",
                    "members/cfg-static-guard-adapters.tsv"):
        continue
    try:
        for m in CD.read_members(doc, parts[2]):
            dec[m] = parts[0]
    except (IOError, OSError, ValueError):
        pass

excl_a = [e for e in form if e in a_set]
excl_dec = [(e, dec[e]) for e in form if e in dec]
print("excluded A-measured: %d" % len(excl_a))
for e, fam in excl_dec:
    print("   excluded declared: %08X  <- %s" % (e, fam))
members = sorted(set(form) - set(a_set) - set(dec))
print("members: %d (expect 145)" % len(members))


def lea_static(e):
    o = off(e)
    return struct.unpack_from("<i", d, o + 3)[0] + e + 7


ok = (len(form) == 185 and len(unregistered) == 0 and len(excl_a) == 0
      and len(excl_dec) == 40 and len(members) == 145)
print("VERDICT:", "PASS" if ok else "REFUSE - counts moved; investigate before writing")

if "--write" in sys.argv and ok:
    lines = ["# empty-destructor static-teardown wrappers - EC-7 family C",
             "#",
             "# %d members, all 12 bytes, ONE instruction form: lea rcx,[a static];" % len(members),
             "# jmp 0016D6A0. The jmp target is the image's shared ret-0 body - an ICF-folded",
             "# empty destructor (also serving as _guard_check_icall_nop), NOT a CFG check:",
             "# every member uses the direct E9 encoding; none goes through",
             "# __guard_check_icall_fptr. Every member is address-taken by a .CRT$XI",
             "# initialiser's lea rcx,[member] feeding the atexit wrapper 00808B90 in either",
             "# spelling (call, or add rsp,N ; jmp). 144 of them are the teardown half of the",
             "# declared scalar-conversion registrar pairs (see",
             "# Binary-Hardening-And-Hooking/members/guard-adapter-registrars.tsv).",
             "#",
             "# member\tstatic\tregistrar\tspelling"]
    for e in members:
        lines.append("%08X\t%08X\t%08X\t%s"
                     % (e, lea_static(e), registrar[e],
                        "jmp" if any(i.mnemonic == "jmp" and edge_target(i) == AX
                                     for i in insns(registrar[e])) else "call"))
    io.open(OUT, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")
    print("wrote", OUT)
