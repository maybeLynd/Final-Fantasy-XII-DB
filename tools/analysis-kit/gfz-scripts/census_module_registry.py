"""Enumerate the subsystem modules that register into the list at 02CACC90 before main.

Each registrar follows one shape, read from 00166210:
    cmp qword [listHead], 0 ; walk while [node+0x18] < 0xFF ; splice ; write vtable into a static
    object ; jmp atexit
so per registrar we want: the vtable it installs, the static object it installs it into, and the
class name from the vtable's RTTI complete-object-locator.
"""
import sys, struct, re, bisect
sys.path.insert(0, r"C:\Users\Kristian\AppData\Local\Temp\claude\C--Users-Kristian-source-repos-XIIOnline\862388d6-126d-4d2f-ae78-c9bed3a0394d\scratchpad")
import xdis
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
import kit_paths as KP  # noqa: E402
import os

HEAD = 0x02CACC90
TSV = os.path.join(KP.ROOT, "Database", "Tools", "work", "graph", "functions.tsv")

rows = []
for line in open(TSV, encoding='utf-8', errors='replace'):
    p = line.rstrip('\r\n').split('\t')
    if len(p) >= 3 and p[2].isdigit():
        rows.append((int(p[0], 16), int(p[2]), p[1], p[8] if len(p) > 8 else ''))
rows.sort()
starts = [r[0] for r in rows]
md = Cs(CS_ARCH_X86, CS_MODE_64)


def rip(i):
    m = re.search(r'rip ([+-]) (0x[0-9a-f]+)', i.op_str)
    if not m:
        return None
    return i.address + i.size + int(m.group(2), 16) * (1 if m.group(1) == '+' else -1)


def cstr(a):
    o = xdis.va2off(a)
    if o is None:
        return None
    return xdis.d[o:o + 200].split(b'\0')[0].decode('ascii', 'replace')


def rtti_name(vtable):
    """The COL sits one qword before the vtable; +0x0C is the type-descriptor RVA."""
    raw = xdis.rd(vtable - 8, 8)
    if raw is None or len(raw) < 8:
        return None
    col = struct.unpack('<Q', raw)[0]
    if not (0x120000 <= col < 0x3000000):
        return None
    b = xdis.rd(col, 0x14)
    if b is None:
        return None
    td = xdis.base + struct.unpack('<I', b[12:16])[0]
    n = cstr(td + 0x10)
    return n if n and n.startswith('.?A') else None


found = []
for entry, size, name, tag in rows:
    if size == 0 or size > 4000:
        continue
    b = xdis.rd(entry, size)
    if b is None:
        continue
    ins = list(md.disasm(b, entry))
    if not any(rip(i) == HEAD for i in ins if 'rip' in i.op_str):
        continue
    vt = obj = None
    for k, i in enumerate(ins):
        if i.mnemonic == 'lea' and 'rip' in i.op_str:
            t = rip(i)
            if t and rtti_name(t):
                reg = i.op_str.split(',')[0].strip()
                for j in ins[k + 1:k + 6]:
                    if j.mnemonic == 'mov' and 'rip' in j.op_str and j.op_str.endswith(reg):
                        vt, obj = t, rip(j)
                        break
        if vt:
            break
    found.append((entry, name, vt, obj, rtti_name(vt) if vt else None, tag))

print("registrars into %08X: %d" % (HEAD, len(found)))
print()
named = 0
for entry, name, vt, obj, cls, tag in sorted(found):
    if cls:
        named += 1
    print("%08X  vtable %s  object %s  %s" % (
        entry, ('%08X' % vt) if vt else '   --   ',
        ('%08X' % obj) if obj else '   --   ', cls or '(vtable/RTTI not resolved)'))
print()
print("named: %d of %d" % (named, len(found)))
