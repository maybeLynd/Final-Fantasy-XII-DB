#!/usr/bin/env python3
"""
rtti_recover.py - recover MSVC RTTI class identity from FFXII_TZA.exe.

The shipping executable retains full MSVC RTTI. That means the binary itself names roughly
2,350 C++ classes, and for each one we can find its vtable and therefore its virtual methods.
This is the single highest-leverage naming source in the project: it turns anonymous
FUN_xxxxxxxx entries into `Class::method` slots mechanically, with tier-4 evidence, instead
of one function at a time.

MSVC x64 RTTI layout, walked backwards from the type name:

    TypeDescriptor            (in .data)
      +0x00  ptr    vfptr to type_info
      +0x08  ptr    spare
      +0x10  char[] mangled name, e.g. ".?AVPTexture2D@Phyre@@"

    RTTICompleteObjectLocator (in .rdata)   COL
      +0x00  u32    signature (1 for x64)
      +0x04  u32    offset
      +0x08  u32    cdOffset
      +0x0C  u32    RVA -> TypeDescriptor
      +0x10  u32    RVA -> ClassHierarchyDescriptor
      +0x14  u32    RVA -> self          (x64 only)

    vtable
      [-1]           ptr -> COL
      [0..n]         virtual method pointers

Usage:
  rtti_recover.py <exe> [--functions functions.tsv] [--out-classes c.tsv]
                        [--out-methods m.tsv] [--out-report r.md]

`--functions` (from DumpFullCoverageGraph) lets the tool report how many recovered methods
are still unnamed, which is the number that matters.
"""
import argparse
import collections
import io
import re
import struct
import sys

# Read to the NUL, NOT to the first '@@'.
#
# AS-9a FIXED 2026-09-02. A type name is NUL-terminated and contains '@@' INTERNALLY -
# a template argument list is itself '@@'-terminated - so a regex stopping at the first
# '@@' truncates every template name before it is ever demangled. That truncation, plus
# the naive splitter below, made every instantiation of a template collapse to one class
# string ('?$PMethodCallerConcrete' with no argument list held 16 vtables), which is what
# made this tool report 2,133 classes where vtable_map.py reports 2,248 for the SAME
# 2,286 vtables. '[\x21-\x7e]' cannot match NUL, so the scan stops at the terminator.
# The bound is 400, not 250: two real type descriptors in this image are 264 and 265
# characters (`?$PMethodCallerConcrete` on `PPhysicsWorld`), and a 250 bound silently
# drops both - the last 2 of the 2,350 names, and the last 2 vtables of the 2,286.
NAME_RE = re.compile(rb'\.\?A[VU][\x21-\x7e]{0,400}?\x00')


def parse_pe(data):
    """Minimal PE parse: image base, and section table."""
    if data[:2] != b'MZ':
        raise ValueError('not a PE (no MZ)')
    pe_off = struct.unpack_from('<I', data, 0x3C)[0]
    if data[pe_off:pe_off + 4] != b'PE\0\0':
        raise ValueError('not a PE (no PE signature)')
    coff = pe_off + 4
    n_sections = struct.unpack_from('<H', data, coff + 2)[0]
    opt_size = struct.unpack_from('<H', data, coff + 16)[0]
    opt = coff + 20
    magic = struct.unpack_from('<H', data, opt)[0]
    if magic != 0x20B:
        raise ValueError('not PE32+ (x64)')
    image_base = struct.unpack_from('<Q', data, opt + 24)[0]
    sec_off = opt + opt_size
    sections = []
    for i in range(n_sections):
        o = sec_off + i * 40
        name = data[o:o + 8].rstrip(b'\0').decode('ascii', 'replace')
        vsize, vaddr, rawsize, rawptr = struct.unpack_from('<IIII', data, o + 8)
        sections.append({'name': name, 'vaddr': vaddr, 'vsize': vsize,
                         'rawptr': rawptr, 'rawsize': rawsize})
    return image_base, sections


def make_mappers(image_base, sections):
    def rva_to_off(rva):
        for s in sections:
            if s['vaddr'] <= rva < s['vaddr'] + max(s['vsize'], s['rawsize']):
                d = rva - s['vaddr']
                if d < s['rawsize']:
                    return s['rawptr'] + d
                return None
        return None

    def off_to_rva(off):
        for s in sections:
            if s['rawptr'] <= off < s['rawptr'] + s['rawsize']:
                return s['vaddr'] + (off - s['rawptr'])
        return None

    return rva_to_off, off_to_rva


_UNDNAME = None
_RTTI_SUFFIX = re.compile(r"\s*`RTTI Type Descriptor'\s*$")
_TYPE_PREFIX = re.compile(r"^\s*(class|struct|union|enum)\s+")


def _load_undname():
    """dbghelp!UnDecorateSymbolName, or None when unavailable (non-Windows)."""
    global _UNDNAME
    if _UNDNAME is None:
        try:
            import ctypes, ctypes.wintypes as w
            fn = ctypes.WinDLL('dbghelp.dll').UnDecorateSymbolName
            fn.argtypes = [ctypes.c_char_p, ctypes.c_char_p, w.DWORD, w.DWORD]
            fn.restype = w.DWORD

            def call(sym):
                buf = ctypes.create_string_buffer(8192)
                n = fn(sym.encode('ascii', 'replace'), buf, 8192, 0)
                return buf.value.decode('ascii', 'replace') if n else None
            _UNDNAME = call
        except Exception:
            _UNDNAME = False
    return _UNDNAME or None


def demangle_naive(m):
    """The '@'-reversing splitter. Correct for non-template names ONLY - kept as the
    fallback when dbghelp is unavailable. See demangle()."""
    body = m[4:]                       # strip '.?AV' / '.?AU'
    if body.endswith('@@'):
        body = body[:-2]
    parts = [p for p in body.split('@') if p]
    if not parts:
        return m
    return '::'.join(reversed(parts))


def demangle(mangled):
    """'.?AVPTexture2D@Phyre@@' -> 'Phyre::PTexture2D', template arguments preserved.

    AS-9a FIXED 2026-09-02, lifted from vtable_map.py's AS-9 fix. The previous splitter
    reversed the mangled name on '@', which is right for a plain qualified name but
    DESTRUCTIVE for a template: it dropped the argument list, so every instantiation of
    one template collapsed to a single class string. Combined with NAME_RE truncating at
    the first '@@' (see above) this tool reported 2,133 classes for the same 2,286
    vtables that vtable_map.py resolves to 2,248 - the whole of the 25,798-vs-25,603 row
    discrepancy between the two tools.

    Rather than hand-roll an MSVC demangler this asks Windows: the real symbol for a type
    descriptor is '??_R0' + <name after the dot> + '@8', which dbghelp decodes.

    THE CHECK THAT MATTERS when re-running this: confirm the non-template names come out
    byte-identical to demangle_naive(). That is what proves only the broken half changed.

    Falls back to demangle_naive() when dbghelp is unavailable, so the tool still runs
    off-Windows with the old, template-incorrect behaviour.
    """
    m = mangled.decode('ascii', 'replace').rstrip('\x00')
    if not m.startswith('.?A'):
        return m
    und = _load_undname()
    if und is not None:
        s = und('??_R0' + m[1:] + '@8')
        if s:
            s = _TYPE_PREFIX.sub('', _RTTI_SUFFIX.sub('', s)).strip()
            if s:
                return s
    return demangle_naive(m)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('exe')
    ap.add_argument('--functions')
    ap.add_argument('--out-classes')
    ap.add_argument('--out-methods')
    ap.add_argument('--out-report')
    ap.add_argument('--ghidra-base', type=lambda x: int(x, 16), default=0x00120000,
                    help='image base Ghidra used (default 0x00120000)')
    a = ap.parse_args()

    data = io.open(a.exe, 'rb').read()
    image_base, sections = parse_pe(data)
    rva_to_off, off_to_rva = make_mappers(image_base, sections)
    print('PE image base 0x%X, %d sections' % (image_base, len(sections)), file=sys.stderr)
    for s in sections:
        print('  %-8s vaddr=%08X vsize=%08X raw=%08X' %
              (s['name'], s['vaddr'], s['vsize'], s['rawsize']), file=sys.stderr)

    # Ghidra loaded this at a different base; translate at the end.
    def to_ghidra(rva):
        return a.ghidra_base + rva

    # ---- 1. type descriptors -------------------------------------------------
    typedescs = {}          # td_rva -> (mangled, pretty)
    for m in NAME_RE.finditer(data):
        name_off = m.start()
        name_rva = off_to_rva(name_off)
        if name_rva is None:
            continue
        td_rva = name_rva - 0x10
        raw = m.group(0).rstrip(b'\x00')     # NAME_RE now matches the terminator too
        typedescs[td_rva] = (raw, demangle(raw))
    print('type descriptors: %d' % len(typedescs), file=sys.stderr)

    # ---- 2. complete object locators ----------------------------------------
    td_set = set(typedescs)
    cols = {}               # col_rva -> td_rva
    for s in sections:
        if s['name'] not in ('.rdata', '.data'):
            continue
        base, size = s['rawptr'], s['rawsize']
        blob = data[base:base + size]
        for off in range(0, len(blob) - 24, 4):
            td = struct.unpack_from('<I', blob, off + 0x0C)[0]
            if td not in td_set:
                continue
            sig = struct.unpack_from('<I', blob, off)[0]
            if sig != 1:
                continue
            col_rva = off_to_rva(base + off)
            if col_rva is None:
                continue
            self_rva = struct.unpack_from('<I', blob, off + 0x14)[0]
            if self_rva != col_rva:
                continue
            cols[col_rva] = td
    print('complete object locators: %d' % len(cols), file=sys.stderr)

    # ---- 3. vtables ----------------------------------------------------------
    col_va = {image_base + c: c for c in cols}
    vtables = []            # (vt_rva, td_rva, [method_rva...])
    for s in sections:
        if s['name'] not in ('.rdata', '.data'):
            continue
        base, size = s['rawptr'], s['rawsize']
        blob = data[base:base + size]
        for off in range(0, len(blob) - 8, 8):
            va = struct.unpack_from('<Q', blob, off)[0]
            if va not in col_va:
                continue
            vt_off = base + off + 8
            vt_rva = off_to_rva(vt_off)
            if vt_rva is None:
                continue
            methods = []
            p = vt_off
            while p + 8 <= base + size:
                mva = struct.unpack_from('<Q', data, p)[0]
                if mva == 0:
                    break
                mrva = mva - image_base
                mo = rva_to_off(mrva)
                if mo is None:
                    break
                # must land in an executable section
                in_text = any(sec['vaddr'] <= mrva < sec['vaddr'] + sec['vsize']
                              and sec['name'] in ('.text',) for sec in sections)
                if not in_text:
                    break
                methods.append(mrva)
                p += 8
                if len(methods) > 512:
                    break
            if methods:
                # col_va[va] is the COL's own RVA; cols maps that to the TypeDescriptor RVA.
                vtables.append((vt_rva, cols[col_va[va]], methods))
    print('vtables: %d' % len(vtables), file=sys.stderr)

    # ---- 4. join -------------------------------------------------------------
    known = {}
    if a.functions:
        with io.open(a.functions, encoding='utf-8') as f:
            f.readline()
            for line in f:
                p = line.rstrip('\n').split('\t')
                if len(p) > 1:
                    known[p[0].upper()] = p[1]

    class_methods = collections.defaultdict(set)
    for vt_rva, td_rva, methods in vtables:
        pretty = typedescs[td_rva][1]
        for i, mrva in enumerate(methods):
            class_methods[pretty].add((to_ghidra(mrva), i))

    all_methods = set()
    for s in class_methods.values():
        all_methods |= {m for m, _ in s}
    unnamed = sum(1 for m in all_methods
                  if known.get('%08X' % m, 'FUN_').startswith('FUN_'))

    ns = collections.Counter()
    for pretty in class_methods:
        ns[pretty.split('::')[0] if '::' in pretty else '(global)'] += 1

    # ---- 5. outputs ----------------------------------------------------------
    if a.out_classes:
        with io.open(a.out_classes, 'w', encoding='utf-8', newline='\n') as f:
            f.write('class\tmangled\tvtables\tmethods\n')
            vt_count = collections.Counter()
            for _vt, td, _m in vtables:
                vt_count[typedescs[td][1]] += 1
            # The mangled name per class. Hardcoded to '' until 2026-09-02, which made
            # the demangler's template collapse unrecoverable from this file - the
            # evidence that would have exposed it was being discarded on write.
            mangled_of = {}
            for _vt, td, _m in vtables:
                mangled_of.setdefault(typedescs[td][1],
                                      typedescs[td][0].decode('ascii', 'replace'))
            for c in sorted(class_methods):
                f.write('%s\t%s\t%d\t%d\n' %
                        (c, mangled_of.get(c, ''), vt_count[c],
                         len(class_methods[c])))
        print('wrote %s' % a.out_classes, file=sys.stderr)

    if a.out_methods:
        with io.open(a.out_methods, 'w', encoding='utf-8', newline='\n') as f:
            f.write('address\tclass\tslot\tcurrent_name\n')
            rows = []
            for c, s in class_methods.items():
                for addr, slot in s:
                    rows.append((addr, c, slot, known.get('%08X' % addr, '')))
            for addr, c, slot, nm in sorted(rows):
                f.write('%08X\t%s\t%d\t%s\n' % (addr, c, slot, nm))
        print('wrote %s' % a.out_methods, file=sys.stderr)

    if a.out_report:
        L = ['# MSVC RTTI recovery', '',
             '| Metric | Value |', '|---|---:|',
             '| Type descriptors found | %d |' % len(typedescs),
             '| Complete object locators | %d |' % len(cols),
             '| Vtables recovered | %d |' % len(vtables),
             '| Classes with a vtable | %d |' % len(class_methods),
             '| Distinct virtual methods | %d |' % len(all_methods),
             '| ...still named `FUN_*` | **%d** |' % unnamed, '',
             '## Top namespaces by class count', '',
             '| Namespace | Classes |', '|---|---:|']
        for k, v in ns.most_common(25):
            L.append('| %s | %d |' % (k, v))
        L += ['', '## Largest classes by virtual-method count', '',
              '| Class | Methods |', '|---|---:|']
        for c, s in sorted(class_methods.items(), key=lambda x: -len(x[1]))[:30]:
            L.append('| %s | %d |' % (c, len(s)))
        with io.open(a.out_report, 'w', encoding='utf-8', newline='\n') as f:
            f.write('\n'.join(L) + '\n')
        print('wrote %s' % a.out_report, file=sys.stderr)

    print('RTTI: %d classes, %d vtables, %d methods (%d still FUN_*)'
          % (len(class_methods), len(vtables), len(all_methods), unnamed), file=sys.stderr)


if __name__ == '__main__':
    main()
