"""iat_any_reference.py - FABLE 2026-09-14 (CV-4). For every import slot in the shipped EXE, find ANY code reference to
the slot, not only `FF 15` calls: a rip-relative memory operand anywhere in .text whose target is the slot, found by a
byte-wise rel32 scan at every offset and then confirmed by decoding the instruction that contains it (call, jmp, mov,
lea, cmp ...). A slot reached only through a `FF 25` jump stub is then followed to the stub's own callers.

usage: python iat_any_reference.py EXE OUT.tsv     (EXE = Database/Tools/work/exe/FFXII_TZA.exe; ImageBase is printed)
"""
import struct, sys, collections
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_REG_RIP

exe, out = sys.argv[1], sys.argv[2]
BASE = 0x120000
pe = pefile.PE(exe, fast_load=True)
pe.parse_data_directories(directories=[pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_IMPORT"]])
IB = pe.OPTIONAL_HEADER.ImageBase
slots = {}
for e in pe.DIRECTORY_ENTRY_IMPORT:
    for imp in e.imports:
        name = imp.name.decode() if imp.name else "#%d" % imp.ordinal
        slots[imp.address - IB + BASE] = (e.dll.decode(), name)
text = [s for s in pe.sections if s.Name.rstrip(b"\0") == b".text"][0]
data = text.get_data()[:text.Misc_VirtualSize]
tva = BASE + text.VirtualAddress
md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True
lo, hi = min(slots), max(slots) + 8
refs = collections.defaultdict(list)
n = len(data)
for i in range(n - 4):
    disp = struct.unpack_from("<i", data, i)[0]
    for tail in (0, 1, 4):
        tgt = tva + i + 4 + tail + disp
        if lo <= tgt < hi and tgt in slots:
            # decode candidates that start 2..7 bytes before the displacement and contain it
            for back in range(7, 1, -1):   # longest decode first, so a REX-prefixed `48 FF 25` starts at its prefix
                s = i - back
                if s < 0:
                    continue
                ins = next(md.disasm(data[s:s + 15], tva + s), None)
                if ins is None or ins.address + ins.size <= tva + i:
                    continue
                for op in ins.operands:
                    if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP and ins.address + ins.size + op.mem.disp == tgt:
                        refs[tgt].append((ins.address, ins.mnemonic))
                        break
                else:
                    continue
                break
dedup = {k: sorted(set(v)) for k, v in refs.items()}
# FF 25 stubs: follow their callers (E8 / E9 anywhere in .text) and data pointers to the stub (vtables, tables)
stubs = {}
for tgt, lst in dedup.items():
    for a, m in lst:
        if m == "jmp":
            stubs[a] = tgt
stub_callers = collections.Counter()
if stubs:
    for i in range(n - 4):
        b = data[i]
        if b in (0xE8, 0xE9) and i + 5 <= n:
            t = tva + i + 5 + struct.unpack_from("<i", data, i + 1)[0]
            if t in stubs:
                stub_callers[t] += 1
raw = open(exe, "rb").read()
def data_refs(addr):
    k = 0
    for pat in {struct.pack("<Q", addr - BASE + IB), struct.pack("<Q", addr), struct.pack("<I", addr - BASE)}:   # a set: equal when IB == BASE
        j = raw.find(pat)
        while j >= 0:
            k += 1
            j = raw.find(pat, j + 1)
    return k
rows = []
for s, (dll, name) in sorted(slots.items()):
    lst = dedup.get(s, [])
    kinds = collections.Counter(m for _a, m in lst)
    calls = sum(stub_callers[a] for a, m in lst if m == "jmp")
    drefs = sum(data_refs(a) for a, m in lst if m == "jmp")
    if kinds.get("call"):
        status = "called"
    elif kinds.get("jmp"):
        status = "jump, %d E8/E9 callers, %d data pointers" % (calls, drefs)
    else:
        status = "other operand" if lst else "NO CODE REFERENCE"
    rows.append((s, dll, name, len(lst), ",".join("%s:%d" % kv for kv in sorted(kinds.items())), status))
with open(out, "w", encoding="utf-8", newline="\n") as f:
    f.write("slot\tdll\timport\tcode_refs\tby_mnemonic\tstatus\n")
    for r in rows:
        f.write("%08X\t%s\t%s\t%d\t%s\t%s\n" % r)
c = collections.Counter(r[5] if not r[5].startswith("jump") else ("jump, reached" if not r[5].startswith("jump, 0 E8/E9 callers, 0 data") else "jump, no caller or pointer to the jump") for r in rows)
print("ImageBase", hex(IB), "slots", len(rows), dict(c))
