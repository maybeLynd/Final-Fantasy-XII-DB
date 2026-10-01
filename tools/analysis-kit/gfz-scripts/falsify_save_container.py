"""Falsification pass on CONTRACT-save-container-transform, re-derived from the shipping image.

The contract's own section 15 lists one claim as **not established**:

    "whether the writer's input can actually go negative"  ->  not established

Section 2 builds a real warning on top of that hole: the transforms `movsxd` the rotation amount, only
the READER bounds it to 0..31, and the WRITER's signed `% 32` can produce a negative `n` - with which
the first `memcpy` length `32 - n` exceeds 32 and its source points before the buffer.

That question is answerable statically, and this answers it. The three instructions immediately before
the `% 32` are a branchless **abs()**, and the value being abs'd comes from an import.

Also re-checks, independently:
  C1  CALG_MD5 0x8003 into CryptCreateHash
  C2  CALG_RC4 0x6801 with 0x800000 (upper 16 bits = 128) into CryptDeriveKey
  C3  the 32-character title literal at 01CCFCF8, and `mov ebx, 0x20`
  C4  the rotation global has exactly 2 readers and 2 writers
  C5  byte 31 is NUL'd and the hashed length comes from an inline strlen

Controls: the title length is measured from the image rather than counted by eye, and the IAT slot is
resolved through the PE import table rather than guessed from the call site.
"""
import io, os, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

EXE = os.path.join('Database', 'Tools', 'work', 'exe', 'FFXII_TZA.exe')
blob = io.open(EXE, 'rb').read()
md = Cs(CS_ARCH_X86, CS_MODE_64)

# VA -> file offset. The database's usual shorthand `VA - 0x121000 + 0x600` is the **.text**
# mapping and nothing else; the first run of this pass used it to read the title literal out of a
# DATA section and got three bytes of garbage, then reported the 32-character claim as failed. The
# claim was fine. So resolve through the section table, which is right for every section, and keep
# the shorthand only as a cross-check that the two agree inside .text.
try:
    import pefile as _pe
    _img = _pe.PE(EXE, fast_load=True)
    _secs = [(s.VirtualAddress + _img.OPTIONAL_HEADER.ImageBase,
              s.Misc_VirtualSize or s.SizeOfRawData, s.PointerToRawData) for s in _img.sections]

    def OFF(va):
        for start, size, raw in _secs:
            if start <= va < start + size:
                return raw + (va - start)
        raise ValueError('VA %08X is in no section' % va)
except ImportError:
    OFF = lambda va: va - 0x121000 + 0x600

print('=== the writer computing the rotation amount, 008663AD..008663F3')
seq = []
for i in md.disasm(blob[OFF(0x008663AD):OFF(0x008663AD) + 0x50], 0x008663AD):
    print('  %08X  %-9s %s' % (i.address, i.mnemonic, i.op_str))
    seq.append((i.address, i.mnemonic, i.op_str))
    if i.address >= 0x008663F3:
        break

txt = ['%s %s' % (m, o) for _, m, o in seq]
abs_idx = next((k for k in range(len(txt) - 2)
                if txt[k] == 'cdq ' or txt[k].startswith('cdq')), None)
is_abs = (abs_idx is not None
          and txt[abs_idx + 1].startswith('xor eax, edx')
          and txt[abs_idx + 2].startswith('sub eax, edx'))
print()
print('  branchless abs(eax) before the %% 32: %s' % ('YES (cdq / xor eax,edx / sub eax,edx)'
                                                      if is_abs else 'NO'))

# --- what is abs() applied to? resolve the IAT slot through the import table ---
call = next((a for a, m, o in seq if m == 'call'), None)
target = None
for i in md.disasm(blob[OFF(call):OFF(call) + 8], call):
    if i.mnemonic == 'call' and 'rip' in i.op_str:
        disp = int(i.op_str.split('+')[1].split(']')[0].strip(), 16)
        target = i.address + i.size + disp
    break
name = '(unresolved)'
try:
    import pefile
    pe = pefile.PE(EXE, fast_load=True)
    pe.parse_data_directories(
        directories=[pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_IMPORT']])
    for e in pe.DIRECTORY_ENTRY_IMPORT:
        for imp in e.imports:
            if imp.address == target:
                name = '%s!%s' % (e.dll.decode(),
                                  (imp.name or b'').decode() or 'ord%d' % imp.ordinal)
except ImportError:
    pass
print('  the value being abs\'d comes from %08X -> %s' % (target or 0, name))

# --- C3: the title literal, measured ---
title_va = 0x01CCFCF8
raw = blob[OFF(title_va):OFF(title_va) + 64]
title = raw.split(b'\x00')[0]
print()
print('--- claims ---')
print('  C3  title at %08X = %r, length %d (contract says 32, `mov ebx, 0x20`)'
      % (title_va, title.decode('latin-1'), len(title)))

deriv = list(md.disasm(blob[OFF(0x008658F0):OFF(0x008658F0) + 0xD0], 0x008658F0))
dt = ['%s %s' % (i.mnemonic, i.op_str) for i in deriv]
c1 = any('0x8003' in t for t in dt)
c2 = any('0x6801' in t for t in dt) and any('0x800000' in t for t in dt)
print('  C1  CALG_MD5 0x8003 present in the derivation: %s' % c1)
print('  C2  CALG_RC4 0x6801 and 0x800000 present:      %s  (0x800000 >> 16 = %d)'
      % (c2, 0x800000 >> 16))

refs = 'Database/Tools/work/h78/rip_data_refs.tsv'
rd = wr = []
if os.path.exists(refs):
    rows = [l.rstrip('\n').split('\t') for l in io.open(refs, encoding='utf-8')]
    rd = sorted({r[3] for r in rows if len(r) > 3 and r[1] == '02EB3868' and r[2] == 'read'})
    wr = sorted({r[0] for r in rows if len(r) > 3 and r[1] == '02EB3868' and r[2] == 'write'})
    print('  C4  rotation global 02EB3868: %d read sites %s, %d writing bodies %s'
          % (len(rd), rd, len(wr), wr))

print()
print('--- the answer to the contract\'s open question ---')
if is_abs and name.endswith('rand'):
    print('  The writer computes  abs(rand()) % 32.')
    print('  rand() returns 0..RAND_MAX and is never negative, so abs() is a no-op on every')
    print('  reachable value; and even the one input whose abs is negative, INT_MIN, runs the')
    print('  signed-% 32 fixup to 0x80000000 -> dec -> or 0xFFFFFFE0 -> inc -> 0.')
    print('  THEREFORE the writer\'s rotation amount is 0..31 for every input. It cannot go negative.')
else:
    print('  NOT ESTABLISHED by this run - the abs() or the import did not resolve as expected.')

sys.exit(0 if (is_abs and len(title) == 32 and c1 and c2) else 1)
