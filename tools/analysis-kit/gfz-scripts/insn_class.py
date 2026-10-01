"""One definition of what an instruction says about the data it touches.

WHY THIS FILE EXISTS. The rule below is four words long and I got it wrong four times on 2026-09-13,
in two different instruments:

  check_float_typed_as_int   counted a plain `mov` as integer evidence      -> 5 false findings
  check_float_typed_as_int   counted `lea` as integer evidence              -> in the same 5
  check_float_typed_as_int   counted packed `movaps`/`movups` as float work -> a checksum and a
                                                                               magic number reported
                                                                               as floats
  check_strided_fields       counted an indexed `lea` as an array access    -> a named uint64 reported
                                                                               as dword-walked

Each time the fix was the same and each time it was rediscovered from a false finding rather than
remembered. So the rule stops living in a comment in one file:

    ONLY ARITHMETIC AND COMPARISON SAY WHAT SOMETHING IS.
    EVERYTHING THAT RELOCATES BYTES SAYS WHERE THEY WENT.

CLASSES

  FLOAT     scalar float WORK - movss, mulss, addss, comiss, cvt*. NOT the packed moves: a 16-byte
            movaps/movups/movdqa is how a compiler copies a block, and SaveImageHeader is memcpy'd
            by an unrolled movups loop.
  INT       integer arithmetic and BIT MANIPULATION - and, or, xor, test, cmp, add, sub, shl, bt.
            These act on a value as a number or a bit pattern.
  CONST     an immediate store whose value is a plausible float bit pattern. `mov dword [x],
            0xBF800000` is how -1.0f is written: no float instruction is involved because storing a
            constant needs no arithmetic, so this CORROBORATES a float reading rather than disputing
            it.
  NEUTRAL   mov, movzx, movsx, lea, the packed moves, nop. A copy or an address computation. Says
            where bytes went and nothing about what they are.
  OTHER     anything unmatched, so a caller can see its own blind spots rather than having them
            silently folded into a class.

A caller that wants a different policy should compose these, not redefine them.
"""
import re
import struct

FLOAT_OP = re.compile(r'\b(movss|mulss|addss|subss|divss|comiss|ucomiss|sqrtss|maxss|minss|'
                      r'cvtsi2ss|cvtss2si|cvttss2si|cvtss2sd|cvtsd2ss|rcpss|rsqrtss|'
                      r'unpcklps|shufps)\b')
NEUTRAL_OP = re.compile(r'^\s*(mov|movzx|movsx|movsxd|lea|movaps|movups|movdqa|movdqu|'
                        r'movlps|movhps|nop)\b')
INT_OP = re.compile(r'\b(and|or|xor|test|cmp|add|sub|inc|dec|bt|bts|btr|shl|shr|sar|imul|idiv|'
                    r'neg|not|adc|sbb)\b')
IMM = re.compile(r',\s*(0x[0-9a-fA-F]+|\d+)\s*$')


def float_plausible(imm):
    """Is this immediate more plausibly a float bit pattern than an integer?

    At least 0x10000, because a small integer is a small integer - `mov dword [rbx+0x2a0], 0xf`
    must not be read as 2.1e-44 - and its float reading neither denormal nor absurd.
    """
    try:
        v = int(imm, 16) if imm.lower().startswith('0x') else int(imm)
    except (ValueError, AttributeError):
        return False
    if not 0 < v <= 0xFFFFFFFF or v < 0x10000:
        return False
    f = struct.unpack('<f', struct.pack('<I', v))[0]
    if f != f or f in (float('inf'), float('-inf')):
        return False
    return 1e-6 <= abs(f) <= 1e9


def classify(ins):
    """-> 'float' | 'const' | 'neutral' | 'int' | 'other' for one instruction's text."""
    if FLOAT_OP.search(ins):
        return 'float'
    m = IMM.search(ins)
    if m and ins.lstrip().startswith('mov') and float_plausible(m.group(1)):
        return 'const'
    if NEUTRAL_OP.match(ins):
        return 'neutral'
    if INT_OP.search(ins):
        return 'int'
    return 'other'


def is_address_only(ins):
    """True for an instruction that computes an address and touches no memory.

    `lea` is the whole of it today. Kept as a named predicate because both instruments that got this
    wrong got it wrong by not having a name for the idea.
    """
    return ins.lstrip().startswith('lea')


def self_test():
    cases = [
        ('movss dword ptr [rbx + 8], xmm0', 'float'),
        ('mulss xmm0, dword ptr [rbx]', 'float'),
        ('movaps xmm0, xmmword ptr [rbx]', 'neutral'),   # a block copy, not float work
        ('movups xmmword ptr [rax - 0x80], xmm0', 'neutral'),
        ('mov dword ptr [rbx + 0x2b0], 0xbf800000', 'const'),
        # A SMALL immediate store is NEUTRAL, not integer evidence, and this case is in the
        # self-test because the first version of this file expected 'int' and the test caught it.
        # `mov dword [x], 0` zeroes a float exactly as readily as an integer - that is the case
        # that produced three of the float gate's own false readings - so a store whose value is
        # too small to be a float bit pattern says nothing about the type in EITHER direction.
        # The asymmetry is deliberate: a large immediate that reads as a sane float corroborates
        # a float; a small one corroborates nothing.
        ('mov dword ptr [rbx + 0x2a0], 0xf', 'neutral'),
        ('mov dword ptr [rdi + 4], eax', 'neutral'),
        ('lea rcx, [rbx + 0x1c0]', 'neutral'),
        ('and byte ptr [rcx], 0xbf', 'int'),
        ('cmp dword ptr [rbx + 0x300], 0', 'int'),
    ]
    bad = [(i, want, classify(i)) for i, want in cases if classify(i) != want]
    for i, want, got in bad:
        print('  FAIL %-42s want %-8s got %s' % (i, want, got))
    print('insn_class self-test: %d of %d' % (len(cases) - len(bad), len(cases)))
    return 1 if bad else 0


if __name__ == '__main__':
    import sys
    sys.exit(self_test())
