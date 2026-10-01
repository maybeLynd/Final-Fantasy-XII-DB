"""gen_static_census.py - build a per-access census for a record that lives at a STATIC address.

`record_field_scan.py` censuses records reached through a pointer chain. It cannot see the other
large class of uncensused record: the ones that sit at a fixed address, where every access is
RIP-relative and there is no base register to track. `BattleFormulaScratch` is at 0x02AEDFB8,
`ImageAddressArenaRecord` at 0x022D7FD0 + id*0xA8, and neither has ever had a census.

The references already exist - `Tools/work/h78/rip_data_refs.tsv`, 164,489 resolved RIP targets -
and what they lack is the one thing that turned out to matter: the INSTRUCTION TEXT. A census row
that says `mov` and `4` cannot tell `movss` from a copy from arithmetic, which is the distinction
`check_float_typed_as_int` rests on and the distinction that produced three separate false readings
in this kit on 2026-09-13. So each site is decoded here, and the emitted format is the same
`*-accesses.tsv` every other census uses.

THE CONTROL IS A COUNT, NOT A SITE
----------------------------------
`--control 0x0=77,0x4=43` requires the scan to find exactly that many accesses at those offsets, and
REFUSES TO WRITE otherwise. Counts are available because the field store's evidence column already
records them for hand-censused types - `BattleFormulaScratch +0x000` says *"77 access(es), all
4-byte"* - so the control is an independent figure recorded by somebody else from different work,
rather than a site read out of the same file this scan reads. A single site would only prove the
decoder runs; a count proves the population matches.

WHAT IT DOES NOT DO
-------------------
- **It does not find accesses that are not RIP-relative.** A function that loads the record's address
  into a register and indexes off it is invisible here, exactly as the chain scanner is blind to a
  record passed across a call. The count is a floor.
- **It does not infer types.** It records the instruction; every downstream judgement is somebody
  else's.

LOCATED STATICALLY IS NOT ACCESSED STATICALLY, AND THAT IS THE REAL LIMIT
------------------------------------------------------------------------
`_types/types.tsv`'s `instance` column names a static address for nine uncensused types, and that
column answers *where the record is*, not *how it is reached*. Most of them are reached through a
register and this tool is blind to every one of those accesses:

  PersistentFlagPayload   `SaveImage_GetActiveBuffer() + 0x200 (= 0x02164280 + 0x200)`
                          Run on 2026-09-13: all four controls wanted 1, 5, 4 and 3 accesses and
                          got ZERO. The buffer sits at a static address; the code reaches it through
                          the pointer the getter returns. REFUSED, correctly.
  AuthoredTableHeader     evidence cites `mov eax, dword ptr [r8 + 0x10]` - a registry slot pointer
                          in a register. The 132 RIP references in its band are references to the
                          BAND as data, not to a header's fields.

`BattleFormulaScratch` works because it is a scratch GLOBAL that the formula code references
directly. Before running this on a new type, check whether the field store's evidence quotes
`[rip + ...]` or `[reg + ...]`; if it quotes a register, use `record_field_scan.py` with the chain
instead.

**The count control is what makes that mistake safe.** Without it this tool would have written an
empty census for `PersistentFlagPayload` and registered it in `CENSUS`, and an empty census is
indistinguishable from a record nobody touches - the exact failure `record_field_scan`'s docstring
was already written to prevent, arrived at from the other direction.
"""
import argparse
import collections
import io
import os
import re
import sys

from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_REG_RIP

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import reg_tracking as RT  # noqa: E402  (access direction: op_kind)

ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
EXE = os.path.join(ROOT, 'Database', 'Tools', 'work', 'exe', 'FFXII_TZA.exe')
REFS = os.path.join(ROOT, 'Database', 'Tools', 'work', 'h78', 'rip_data_refs.tsv')
FUNCS = os.path.join(ROOT, 'Database', 'Tools', 'work', 'graph', 'functions.tsv')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--base', required=True, help='record base VA, e.g. 0x02AEDFB8')
    ap.add_argument('--size', required=True, help='record size, e.g. 0xA8')
    ap.add_argument('--control', default=None,
                    help='offset=count[,offset=count...] that MUST reproduce exactly')
    ap.add_argument('--control-sites', default=None,
                    help='instruction addresses the store already cites that MUST appear - '
                         'non-circular where an independent count is not available')
    ap.add_argument('--out', required=True)
    ap.add_argument('--exe', default=EXE)
    ap.add_argument('--refs', default=REFS)
    ap.add_argument('--funcs', default=FUNCS)
    a = ap.parse_args()

    base = int(a.base, 16 if a.base.lower().startswith('0x') else 16)
    size = int(a.size, 16 if a.size.lower().startswith('0x') else 16)

    names = {}
    for ln in io.open(a.funcs, encoding='utf-8', errors='replace'):
        p = ln.rstrip('\n').split('\t')
        if len(p) >= 2 and re.match(r'^[0-9A-F]{8}$', p[0]):
            names[int(p[0], 16)] = p[1]

    blob = io.open(a.exe, 'rb').read()
    import pefile
    pe = pefile.PE(a.exe, fast_load=True)
    secs = [(s.VirtualAddress + pe.OPTIONAL_HEADER.ImageBase,
             s.Misc_VirtualSize or s.SizeOfRawData, s.PointerToRawData) for s in pe.sections]

    def off(va):
        for st, sz, raw in secs:
            if st <= va < st + sz:
                return raw + (va - st)
        return None

    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True

    rows = []
    for ln in io.open(a.refs, encoding='utf-8', errors='replace'):
        p = ln.rstrip('\n').split('\t')
        if len(p) < 4 or not re.match(r'^[0-9A-F]{8}$', p[1]):
            continue
        addr = int(p[1], 16)
        if not (base <= addr < base + size):
            continue
        site = int(p[3], 16)
        fo = off(site)
        if fo is None:
            continue
        text = kind = None
        for i in md.disasm(blob[fo:fo + 16], site):
            text = ('%s %s' % (i.mnemonic, i.op_str)).strip()
            # DIRECTION FROM THE INSTRUCTION, not from the refs file. `p[2][:1]` turned the
            # refs file's `addr` into `a` and then the writer below printed every non-`w` as
            # `r`, so a `lea` of the record was censused as a READ and a read-modify-write
            # lost its write; and the refs file itself calls movups/movq stores `read`
            # (4,040 sites, riprefs_vs_iced.py). op_kind is the kit's controlled
            # classifier; the operand is the rip-relative one that addresses this cell.
            for oi, op in enumerate(i.operands):
                if (op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP
                        and i.address + i.size + op.mem.disp == addr):
                    kind = RT.op_kind(i, op, oi)
                    break
            break
        if text is None or kind is None:
            continue
        entry = int(p[0], 16)
        rows.append((site, entry, names.get(entry, 'FUN_%08x' % entry),
                     addr - base, kind, text))

    per = collections.Counter(r[3] for r in rows)

    ok = True

    # A SITE CONTROL, because a COUNT control is often circular and sometimes unavailable.
    # `--control 0x0=77` needs a number somebody measured independently. For a type nobody has
    # counted, the only place to get one is THIS VERY SCAN, and a control derived from the scan
    # it is checking cannot fail. `Mt19937State` is exactly that case and it went uncensused
    # for it. A site control asks a different question with the same force: these INSTRUCTION
    # ADDRESSES, cited by the store's own field rows from work that predates this tool, must
    # appear in the output. The addresses are not the scan's to invent, so the control is
    # non-circular - and it is the shape most of this store's evidence already has; the Widget
    # census uses it as "every declared row must have a reachable cited address".
    if not a.control and not a.control_sites:
        print('REFUSING - one of --control or --control-sites is required. An uncontrolled '
              'census is a file nobody can trust, and this tool has always said so.')
        return 2

    if a.control_sites:
        found = {r[0] for r in rows}
        print('CONTROL - every cited site must appear, or nothing is written')
        for item in a.control_sites.split(','):
            want = int(item, 16)
            hit = want in found
            print('  %08X  %s' % (want, 'found' if hit else 'ABSENT   MISMATCH'))
            if not hit:
                ok = False
        if not ok:
            print('\nCONTROL FAILED - refusing to write. A site the store cites and this scan '
                  'cannot see means the scan is not looking where the evidence came from.')
            return 1
        print('  all cited sites reproduce\n')

    if not a.control:
        return write_out(a, rows, base)

    print('CONTROL - each offset must show exactly the declared count, or nothing is written')
    for item in a.control.split(','):
        o, _, c = item.partition('=')
        o, c = int(o, 16), int(c)
        got = per.get(o, 0)
        print('  +0x%03X  want %3d  got %3d%s' % (o, c, got, '' if got == c else '   MISMATCH'))
        if got != c:
            ok = False
    if not ok:
        print('\nCONTROL FAILED - refusing to write. The population this scan sees is not the '
              'population the store was built from, and a census that disagrees with its own '
              'record without explanation is worse than no census.')
        return 1
    print('  all controls reproduce\n')

    return write_out(a, rows, base)


def write_out(a, rows, base):
    """The emit, factored out so the site control can return through it without duplicating
    the writer or falling through into the count control it was chosen instead of."""
    import collections as _c
    per = _c.Counter(r[3] for r in rows)
    with io.open(a.out, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('function\tname\tsite\tdisp\tkind\tinstruction\troute\tnote\n')
        for site, entry, name, disp, kind, text in sorted(rows):
            fh.write('%08X\t%s\t%08X\t0x%X\t%s\t%s\tstatic:0x%08X\t-\n'
                     % (entry, name, site, disp, kind, text, base))

    print('%d access row(s) over %d distinct offset(s), base 0x%08X'
          % (len(rows), len(per), base))
    print('wrote %s' % a.out)
    return 0


if __name__ == '__main__':
    sys.exit(main())
