"""Falsification pass on CONTRACT-efx-source-rebase, re-derived from the shipping image.

Claims under test (section 15):

  R1  the rebase delta is low32(new) - low32(old), sign-extended on use
  R2  all four repair walks sign-extend that delta
  R3  the repair is exact if and only if |newBase - oldBase| < 2 GiB
  R4  the offset round-trip is 32-bit in one direction only (0020E600 / 0020E620)

R2 is where the attack lands. "That delta" is singular, and the image computes **two**, over two
different base fields, with the four walks split between them - so a reader can satisfy R2 and still
have the family wrong.

Every VA resolves through the PE section table, not the `.text` shorthand.
"""
import io, os, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

EXE = os.path.join('Database', 'Tools', 'work', 'exe', 'FFXII_TZA.exe')
blob = io.open(EXE, 'rb').read()
md = Cs(CS_ARCH_X86, CS_MODE_64)
import pefile
_img = pefile.PE(EXE, fast_load=True)
_secs = [(s.VirtualAddress + _img.OPTIONAL_HEADER.ImageBase,
          s.Misc_VirtualSize or s.SizeOfRawData, s.PointerToRawData) for s in _img.sections]


def OFF(va):
    for start, size, raw in _secs:
        if start <= va < start + size:
            return raw + (va - start)
    raise ValueError('VA %08X is in no section' % va)


def code(va, n=0x60):
    out, pad = [], 0
    for i in md.disasm(blob[OFF(va):OFF(va) + n], va):
        if i.mnemonic == 'int3':
            pad += 1
            if pad >= 2:
                break
            continue
        pad = 0
        out.append((i.address, i.mnemonic, i.op_str))
    return out


def show(title, va, n=0x60):
    print('=== %s (%08X)' % (title, va))
    for a, m, o in code(va, n):
        print('  %08X  %-8s %s' % (a, m, o))
    print()


show('rebaser A - the +0x390 base, one walk', 0x0024D940, 0x40)
show('rebaser B - the +0x858 base, three walks', 0x0024D970, 0x40)
show('decode: offset -> pointer', 0x0020E600, 0x20)
show('encode: pointer -> offset', 0x0020E620, 0x20)

print('--- R2: how many deltas, and which walks belong to which ---')
a = ['%s %s' % (m, o) for _, m, o in code(0x0024D940, 0x40)]
b = ['%s %s' % (m, o) for _, m, o in code(0x0024D970, 0x40)]
wa = [t.split()[-1] for t in a if t.startswith('call')]
wb = [t.split()[-1] for t in b if t.startswith('call')]
print('  0024D940  delta from %s -> walks %s'
      % (next(t for t in a if t.startswith('sub ecx')), wa))
print('  0024D970  delta from %s -> walks %s'
      % (next(t for t in b if t.startswith('sub ebx')), wb))
print('  => %d delta computations over %d distinct base fields, %d + %d walks'
      % (2, 2, len(wa), len(wb)))

print()
print('--- the combined path, and the guard the contract does not mention ---')
for aa, m, o in code(0x0024D65D, 0x30):
    print('  %08X  %-8s %s' % (aa, m, o))

print()
print('--- R2: sign-extension in each named walk ---')
for va in (0x003A8FF0, 0x003A9BA0, 0x003A9860, 0x003AA3D0, 0x00501420, 0x00503F10):
    hits = [('%08X %s %s' % (x, m, o)) for x, m, o in code(va, 0x200) if m.startswith('movsxd')]
    print('  %08X  %s' % (va, hits[0] if hits else 'no movsxd in the first 0x200 bytes'))

print()
print('--- R3: the exact boundary of "exact" ---')
print('  sext32(low32(d)) == d  iff  -2**31 <= d < 2**31')
for d in (2**31 - 1, -2**31, 2**31, -2**31 - 1):
    lo = d & 0xFFFFFFFF
    sx = lo - (1 << 32) if lo >> 31 else lo
    print('    d = %-13d -> sext32(low32(d)) = %-13d %s' % (d, sx, 'exact' if sx == d else 'WRONG'))
print('  so the condition is  -2 GiB <= d < +2 GiB,  NOT  |d| < 2 GiB:')
print('    d = -2 GiB exactly is representable and round-trips; the stated "if and only if" excludes it.')

print()
print('--- R4: the round-trip condition ---')
dec = ['%s %s' % (m, o) for _, m, o in code(0x0020E600, 0x20)]
enc = ['%s %s' % (m, o) for _, m, o in code(0x0020E620, 0x20)]
zx = any(t.startswith('mov eax, ecx') for t in dec)
print('  decode zero-extends the offset (mov eax, ecx): %s' % zx)
print('  decode adds the base as a QWORD:               %s'
      % any('add rax, qword' in t for t in dec))
print('  encode subtracts the base as a DWORD:          %s'
      % any('sub ecx, dword' in t for t in enc))
print('  => round trip is exact iff  0 <= p - base < 2**32  (UNSIGNED); a pointer before the base')
print('     cannot round-trip at all, which the 2 GiB framing does not say.')

sys.exit(0)
