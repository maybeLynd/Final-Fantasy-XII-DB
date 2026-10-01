"""Falsification pass on CONTRACT-storage-read-completion, re-derived from the shipping bytes.

The contract asserts, of `00866A00` and `00862590`:

  F1  the inner read returns 1 IFF every requested byte was copied  (cmp r11d,r8d / sete)
  F2  the wrapper returns `allBytesCopied ? requestedBytes : 0`     (imul eax, ebx)
  F3  the destination is written byte-by-byte BEFORE the shortfall is discovered
  F4  the cursor advances by the partial count                      (inc dword ptr [r9])
  F5  the tail is stale, not zeroed - nothing writes past the last byte copied
  F6  a non-zero mode stores and returns -4

Result, 2026-09-13: F1, F3, F4, F5 and F6 all confirmed, F2 confirmed once the omitted `mov ebx, r8d`
at 00862596 is read, and the pass found one gap the contract did not carry - a THIRD path returning 0,
the NULL-argument rejection at 00866A08/00866A0D, which no caller can tell from a partial read.

F2 is the one to attack. The contract's own listing multiplies by **ebx**, and its prose calls the
multiplier **elemSize (r8d)**. Those are different registers. If ebx is not r8d at that point the
stated return formula is wrong, and it is the formula every caller conclusion in section 3 rests on.

This decodes the two bodies out of the reference EXE and checks each claim against the instructions,
with a positive control: a claim the decoder should FAIL to find is asserted absent, so a silent
decoding failure cannot pass as six confirmations.
"""
import io, os, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

EXE = os.path.join('Database', 'Tools', 'work', 'exe', 'FFXII_TZA.exe')
OFF = lambda va: va - 0x121000 + 0x600
blob = io.open(EXE, 'rb').read()
md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True


def body(va, n=0x140):
    """Decode to the END of the function, not to the first `ret`.

    The first version stopped at the first `ret` and reported F6 NOT FOUND. The claim is true: the
    non-zero-mode path stores and returns -4 at 008625B8, which is PAST that `ret`, reached by the
    `jne` above it. A decoder that stops at the first return reports absence for every early-out tail
    a compiler places after it, and absence from a filter is not absence from the image.

    So: decode the whole window and stop only on the int3 padding that separates functions.
    """
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


inner = body(0x00866A00)
wrap = body(0x00862590)

print('=== 00866A00 inner read, %d instructions to ret' % len(inner))
for a, m, o in inner:
    print('  %08X  %-8s %s' % (a, m, o))
print()
print('=== 00862590 wrapper, %d instructions to ret' % len(wrap))
for a, m, o in wrap:
    print('  %08X  %-8s %s' % (a, m, o))

txt_i = ['%s %s' % (m, o) for _, m, o in inner]
txt_w = ['%s %s' % (m, o) for _, m, o in wrap]

print()
print('--- claims ---')


def check(tag, ok, detail):
    print('  %-4s %-9s %s' % (tag, 'CONFIRMED' if ok else 'NOT FOUND', detail))
    return ok


res = {}
res['F1'] = check('F1', any(t.startswith('sete') for t in txt_i)
                  and any(t.startswith('cmp r11d, r8d') for t in txt_i),
                  'cmp r11d, r8d followed by sete')
res['F3'] = check('F3', any('byte ptr' in t and t.startswith('mov') for t in txt_i),
                  'byte-granular store into the destination')
res['F4'] = check('F4', any(t.startswith('inc dword ptr') for t in txt_i),
                  'inc dword ptr [cursor] inside the loop')
res['F5'] = check('F5', not any(t.startswith('rep stos') or 'memset' in t for t in txt_i),
                  'no rep stos / memset anywhere in the body (tail left stale)')
res['F6'] = check('F6', any('0xfffffffc' in t or '-4' in t for t in txt_w),
                  '-4 stored/returned on the non-zero-mode path')

imul = [t for t in txt_w if t.startswith('imul')]
print()
print('--- F2, the one under attack: what does the wrapper multiply? ---')
print('  imul instruction(s): %s' % (imul or 'NONE'))
if imul:
    mult = imul[0].split(',')[-1].strip()
    print('  multiplier register: %s' % mult)
    # where did that register last come from, before the call?
    calls = [k for k, t in enumerate(txt_w) if t.startswith('call')]
    upto = txt_w[:calls[0]] if calls else txt_w
    writes = [t for t in upto if mult in t.split(',')[0]]
    print('  writes to %s before the call: %s' % (mult, writes or 'NONE IN THIS BODY'))

# positive control: a claim that must NOT be found. If the decoder is silently
# returning nothing, every CONFIRMED above is a property of the filter.
ctl = any('vfmadd' in t for t in txt_i + txt_w)
print()
print('--- control ---')
print('  a claim that must be absent (vfmadd in either body): %s'
      % ('FOUND - decoder or corpus is wrong' if ctl else 'absent, as required'))
print('  instructions decoded: %d inner + %d wrapper' % (len(inner), len(wrap)))
sys.exit(0 if len(inner) > 10 and len(wrap) > 5 and not ctl else 1)
