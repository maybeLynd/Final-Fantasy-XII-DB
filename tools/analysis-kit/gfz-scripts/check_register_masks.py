"""What actually BUILDS the mask, for every flag field the image masks with a register.

WHY. Addendum 2026-09-13k split the 217 masked fields three ways - 132 literal-only, 47 mixed, 38
register-only - and said the 38 could not have a bit list derived from the image. The same day, one
four-instruction trace of `ActorStorageRecord +0x110` showed the mask there is `1 << arg0`: a bitmap
indexed by an entity index, whose structure is entirely knowable. A quick grep put `shl reg, cl` in
29 of the 38 masking functions.

`shl reg, cl` in the function is a GREP, not a trace. It says the idiom occurs somewhere in the same
body; it does not say that instruction is what computed THIS mask. So this instrument does the
actual backward chase, per site, and reports what built the register.

THE CHECK THIS EXISTS TO RUN AGAINST MY OWN CLASSIFICATION. A register source is not automatically
an unknown one:

    mov  eax, 0x40
    or   dword ptr [rbx + 0x304], eax

is bit 6, written through a register. The three-way split counts that operand as "register" and
therefore the field as unenumerable, and it would be WRONG - the literal is one instruction away.
Any such site is a defect in the 2026-09-13k census and is reported as CONSTANT-IN-REGISTER, loudly,
because it means a published figure moves.

CLASSES, in the order the chase resolves them:

  BITMAP-VARIABLE   `shl r, cl` / `shl r, <non-constant>` - one bit, chosen at runtime by an index.
                    The field is a bitmap and the row should name the index, not call it unknown.
  BITMAP-CONSTANT   `shl r, imm` - one bit, chosen by a constant. Enumerable: bit imm.
  CONSTANT          `mov r, imm` / `or r, imm` against a zeroed register - a literal in disguise.
  MEMORY            the mask was loaded from memory (a table, a field, a global). Not enumerable
                    from the instruction stream, but the SOURCE is named, which is a lead.
  CALL              the mask is a return value. Names the callee.
  UNRESOLVED        the chase hit the function entry, a branch target, or its depth limit.

THE CHASE IS DELIBERATELY CONSERVATIVE. It walks backward through the linear instruction stream from
the masking site to the function entry. If it crosses a label that anything jumps to, it stops and
reports UNRESOLVED rather than reading a definition that a branch may have skipped - a mask built on
one path and used on another is exactly the case where a confident answer would be a wrong one. That
is why UNRESOLVED is a reportable answer here and not a failure.

Register aliasing is resolved to the 64-bit family (eax/ax/al/ah -> RAX), because `mov eax, 1` then
`or [x], rax` is one definition and two names for it.
"""
import argparse
import collections
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_census_widths as ccw
from disasm_fn import Image, DEFAULT_EXE

try:
    from capstone import Cs, CS_ARCH_X86, CS_MODE_64
except ImportError:
    sys.stderr.write('check_register_masks: needs capstone\n')
    raise SystemExit(2)

DB = 'Database/FFXII TZA'
FIELDS = os.path.join(DB, '_types', 'fields.tsv')

# A mask operation on MEMORY. The destination is the memory operand; the source is what follows it.
MASK = re.compile(r'^\s*(and|or|xor|test)\s+(?:[a-z]+\s+ptr\s+)?\[([^\]]+)\]\s*,\s*(\S+)', re.I)
IMMEDIATE = re.compile(r'^(0x[0-9a-fA-F]+|-?\d+)$')

R64 = ['rax', 'rcx', 'rdx', 'rbx', 'rsp', 'rbp', 'rsi', 'rdi',
       'r8', 'r9', 'r10', 'r11', 'r12', 'r13', 'r14', 'r15']
ALIAS = {}
for _i, _r in enumerate(R64):
    ALIAS[_r] = _r
    if _i < 8:
        e = 'e' + _r[1:]
        w = _r[1:]
        ALIAS[e] = _r
        ALIAS[w] = _r
        ALIAS[{'rax': 'al', 'rcx': 'cl', 'rdx': 'dl', 'rbx': 'bl',
               'rsp': 'spl', 'rbp': 'bpl', 'rsi': 'sil', 'rdi': 'dil'}[_r]] = _r
        if _r in ('rax', 'rcx', 'rdx', 'rbx'):
            ALIAS[_r[1] + 'h'] = _r
    else:
        ALIAS[_r + 'd'] = _r
        ALIAS[_r + 'w'] = _r
        ALIAS[_r + 'b'] = _r


def fam(name):
    return ALIAS.get(name.strip().lower())


def declared():
    per = collections.defaultdict(dict)
    for n, line in enumerate(io.open(FIELDS, encoding='utf-8')):
        if n == 0 or not line.strip():
            continue
        c = line.rstrip('\n').split('\t')
        if len(c) < 6:
            continue
        try:
            per[c[0]][int(c[1], 16)] = (c[3], c[4])
        except ValueError:
            continue
    return per


def decode(img, md, entry, limit=0x4000):
    """Linear decode of a function body, plus the set of addresses anything branches to."""
    b = img.read(entry, limit)
    if not b:
        return [], set()
    out = []
    targets = set()
    for ins in md.disasm(b, entry):
        text = '%s %s' % (ins.mnemonic, ins.op_str)
        out.append((ins.address, ins.mnemonic, ins.op_str, text))
        if ins.mnemonic.startswith('j') or ins.mnemonic == 'loop':
            m = re.match(r'^0x([0-9a-f]+)$', ins.op_str.strip())
            if m:
                targets.add(int(m.group(1), 16))
        if ins.mnemonic == 'int3':
            break
    return out, targets


STACK_SLOT = re.compile(r'r[sb]p\s*\+\s*(?:0x[0-9a-f]+|\d+)')


def chase_stack(body, targets, idx, slot, depth=0):
    """Walk backward for the STORE that filled this stack slot, then chase what it stored.

    Conservative in the same way as `chase`: a branch target above the read means a store found
    beyond it may not have run on this path, so it declines rather than guesses. The slot is matched
    on its rendered text, which is exact for `rsp`-relative locals in one body and would be wrong
    only if the frame pointer moved mid-function - in which case the decode would be wrong anyway.
    """
    if depth > 6:
        return 'UNRESOLVED', 'chase depth limit in a stack slot'
    i = idx - 1
    while i >= 0:
        addr, mn, ops, text = body[i]
        if addr in targets:
            return 'UNRESOLVED', 'stack slot %s: crossed branch target %08X' % (slot, addr)
        parts = [p.strip() for p in ops.split(',')]
        if mn == 'mov' and len(parts) > 1 and '[' in parts[0] and slot in parts[0]:
            if IMMEDIATE.match(parts[1]):
                return 'CONSTANT', '%08X  %s   the slot holds a literal' % (addr, text)
            src = fam(parts[1])
            if src:
                k, d = chase(body, targets, i, src, depth + 1)
                return k, '%08X  %s  <- %s' % (addr, text, d)
            return 'UNRESOLVED', '%08X  %s' % (addr, text)
        i -= 1
    return 'UNRESOLVED', 'stack slot %s: no store found above the read' % slot


def chase(body, targets, idx, reg, depth=0):
    """Walk backward from body[idx] for the definition of `reg`. -> (class, detail)."""
    if depth > 6:
        return 'UNRESOLVED', 'chase depth limit'
    i = idx - 1
    while i >= 0:
        addr, mn, ops, text = body[i]
        # A label anything jumps to: a definition above it may not have executed on this path.
        if addr in targets:
            return 'UNRESOLVED', 'crossed branch target %08X without finding a definition' % addr
        parts = [p.strip() for p in ops.split(',')]
        dst = fam(parts[0]) if parts else None
        if dst == reg:
            if mn in ('shl', 'sal') and len(parts) > 1:
                if fam(parts[1]) == 'rcx' or parts[1].strip().lower() == 'cl':
                    return 'BITMAP-VARIABLE', '%08X  %s   one bit, index in cl' % (addr, text)
                if IMMEDIATE.match(parts[1]):
                    return 'BITMAP-CONSTANT', '%08X  %s   bit %s' % (addr, text, parts[1])
                return 'BITMAP-VARIABLE', '%08X  %s' % (addr, text)
            if mn in ('mov', 'movzx', 'movsx', 'movsxd') and len(parts) > 1:
                if IMMEDIATE.match(parts[1]):
                    return 'CONSTANT', '%08X  %s' % (addr, text)
                if '[' in parts[1]:
                    # A STACK SLOT IS NOT A DATA SOURCE. `mov r15d, dword ptr [rsp + 0x3c]` reads a
                    # local the same function computed, so stopping here reports "the mask comes
                    # from memory" about a value that is sitting three instructions up. A field of
                    # a record or a global genuinely ends the chase; a spill slot does not, and
                    # lumping the two together is the same category error as counting a `mov` as
                    # type evidence - it treats WHERE THE BYTES WENT as WHAT THEY ARE.
                    m_st = STACK_SLOT.search(parts[1])
                    if m_st:
                        k, d = chase_stack(body, targets, i, m_st.group(0), depth + 1)
                        return k, '%08X  %s  <- %s' % (addr, text, d)
                    return 'MEMORY', '%08X  %s' % (addr, text)
                src = fam(parts[1])
                if src:
                    return chase(body, targets, i, src, depth + 1)
            if mn in ('not', 'neg') and len(parts) == 1:
                k, d = chase(body, targets, i, reg, depth + 1)
                return k, '%08X  %s  <- %s' % (addr, text, d)
            if mn == 'xor' and len(parts) > 1 and fam(parts[1]) == reg:
                return 'CONSTANT', '%08X  %s   zeroed' % (addr, text)
            if mn in ('and', 'or', 'add', 'sub', 'lea', 'imul', 'shr', 'sar', 'inc', 'dec'):
                return 'UNRESOLVED', '%08X  %s' % (addr, text)
            if mn in ('pop', 'call'):
                return 'UNRESOLVED', '%08X  %s' % (addr, text)
        if mn == 'call' and reg in ('rax', 'rcx', 'rdx', 'r8', 'r9', 'r10', 'r11'):
            # A call clobbers the volatile registers, so a definition above it is not this value.
            if reg == 'rax':
                return 'CALL', '%08X  %s   mask is a return value' % (addr, text)
            return 'UNRESOLVED', 'volatile %s crosses %08X %s' % (reg, addr, text)
        i -= 1
    return 'UNRESOLVED', 'reached function entry without a definition'


def _body(*rows):
    """Synthetic decode: ('addr', 'mnemonic', 'operands') triples -> the shape `chase` expects."""
    return [(int(a, 16), m, o, ('%s %s' % (m, o)).strip()) for a, m, o in rows]


def self_test():
    """The chase classes, exercised on synthetic bodies.

    WHY THIS EXISTS. The stack-slot chase fires exactly ONCE against the real image and declines
    that one. A verdict-producing code path exercised once and never seen to succeed is the same
    hazard this kit already documented from the other side: a check that prints a clean result
    without having compared anything. So the paths are exercised here, where the input is known.
    """
    cases = []

    # a bitmap: the 1 << index idiom, which is what ActorStorageRecord +0x110 does
    b = _body(('0x10', 'mov', 'edi, 1'), ('0x15', 'shl', 'edi, cl'), ('0x20', 'or', '[rbx + 8], edi'))
    cases.append(('bitmap', chase(b, set(), 2, 'rdi')[0], 'BITMAP-VARIABLE'))

    # a literal in disguise: CharacterRenderRecord +0x61C
    b = _body(('0x10', 'mov', 'eax, 0xfffe'), ('0x20', 'and', '[rdi + 0xc], ax'))
    cases.append(('literal via register', chase(b, set(), 1, 'rax')[0], 'CONSTANT'))

    # a record field: a genuine dead end for this instrument
    b = _body(('0x10', 'mov', 'ecx, dword ptr [rbx + 0x4c]'), ('0x20', 'or', '[rsi + 0x14], ecx'))
    cases.append(('record field', chase(b, set(), 1, 'rcx')[0], 'MEMORY'))

    # a STACK SLOT that resolves - the path the real image never completes
    b = _body(('0x08', 'mov', 'eax, 1'), ('0x0c', 'shl', 'eax, cl'),
              ('0x10', 'mov', 'dword ptr [rsp + 0x3c], eax'),
              ('0x18', 'mov', 'r15d, dword ptr [rsp + 0x3c]'), ('0x20', 'and', '[rbx + 0x60], r15d'))
    cases.append(('stack slot -> bitmap', chase(b, set(), 4, 'r15')[0], 'BITMAP-VARIABLE'))

    # the same, with a literal in the slot
    b = _body(('0x10', 'mov', 'dword ptr [rsp + 0x3c], 0x40'),
              ('0x18', 'mov', 'r15d, dword ptr [rsp + 0x3c]'), ('0x20', 'or', '[rbx + 0x60], r15d'))
    cases.append(('stack slot -> literal', chase(b, set(), 2, 'r15')[0], 'CONSTANT'))

    # a branch target above the definition must DECLINE, not read past it
    b = _body(('0x10', 'mov', 'edi, 1'), ('0x15', 'shl', 'edi, cl'), ('0x18', 'nop', ''),
              ('0x20', 'or', '[rbx + 8], edi'))
    cases.append(('declines past a label', chase(b, {0x18}, 3, 'rdi')[0], 'UNRESOLVED'))

    # `not` must pass THROUGH to what built the value, which is how the clear-mask half is read
    b = _body(('0x10', 'mov', 'edi, 1'), ('0x15', 'shl', 'edi, cl'), ('0x18', 'mov', 'esi, edi'),
              ('0x1c', 'not', 'esi'), ('0x20', 'and', '[rbx + 8], esi'))
    cases.append(('not passes through', chase(b, set(), 4, 'rsi')[0], 'BITMAP-VARIABLE'))

    bad = [c for c in cases if c[1] != c[2]]
    for name, got, want in bad:
        print('  FAIL %-26s want %-16s got %s' % (name, want, got))
    print('check_register_masks self-test: %d of %d' % (len(cases) - len(bad), len(cases)))
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--exe', default=DEFAULT_EXE)
    ap.add_argument('--self-test', action='store_true')
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    img = Image(a.exe)
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    decl = declared()

    # ---- pass 1: reproduce the three-way split, and keep the register sites ------------------
    lit = collections.defaultdict(set)      # (type, off) -> set of literal masks
    regsites = collections.defaultdict(list)  # (type, off) -> [(fnva, site, text)]
    total_mask = 0
    for tname, fname, _sbase, shift, extent in ccw.censused_types():
        path = None
        for root, _d, files in os.walk(DB):
            if fname in files:
                path = os.path.join(root, fname)
                break
        if path is None:
            continue
        for n, line in enumerate(io.open(path, encoding='utf-8', errors='replace')):
            if n == 0 or not line.strip():
                continue
            c = line.rstrip('\n').split('\t')
            if len(c) < 6:
                continue
            m = MASK.match(c[5])
            if not m:
                continue
            try:
                off = int(c[3], 16)
            except ValueError:
                continue
            if shift:
                off = ccw.rebase(off, shift, extent)
                if off is None:
                    continue
            total_mask += 1
            key = (tname, off)
            src = m.group(3).strip().rstrip(',')
            if IMMEDIATE.match(src):
                lit[key].add(src)
            elif fam(src):
                try:
                    regsites[key].append((int(c[0], 16), int(c[2], 16), c[5]))
                except ValueError:
                    continue

    literal_only = [k for k in lit if k not in regsites]
    mixed = [k for k in lit if k in regsites]
    register_only = sorted(k for k in regsites if k not in lit)

    print('--- control: mask operations on memory across all censuses: %d ---' % total_mask)
    print('    literal-only fields %d   mixed %d   REGISTER-ONLY %d   (2026-09-13k: 132 / 47 / 38)'
          % (len(literal_only), len(mixed), len(register_only)))
    if not total_mask:
        print('  CONTROL FAILED: no mask operation matched. Everything below is void.')
        return 2
    print()

    # ---- pass 2: chase the mask for every register-only field --------------------------------
    bodies = {}
    verdicts = collections.Counter()
    rows = []
    for key in register_only:
        tname, off = key
        per = collections.Counter()
        detail = []
        for fnva, site, text in regsites[key]:
            if fnva not in bodies:
                bodies[fnva] = decode(img, md, fnva)
            body, targets = bodies[fnva]
            idx = next((i for i, b in enumerate(body) if b[0] == site), None)
            if idx is None:
                per['UNRESOLVED'] += 1
                detail.append(('UNRESOLVED', '%08X not in a linear decode of %08X' % (site, fnva)))
                continue
            parts = [p.strip() for p in body[idx][2].split(',')]
            reg = fam(parts[-1])
            if not reg:
                per['UNRESOLVED'] += 1
                continue
            k, d = chase(body, targets, idx, reg)
            per[k] += 1
            detail.append((k, d))
        verdicts[per.most_common(1)[0][0]] += 1
        name, ctype = decl.get(tname, {}).get(off, ('(undeclared)', ''))
        # THE WEAKER OBSERVATION, KEPT AND LABELLED AS WEAKER. Where the chase declined, does the
        # `1 << reg` idiom occur anywhere in the masking body at all? That is the grep the first
        # measurement made, and on its own it is not evidence about THIS mask - a body can shift a
        # bit for one field and mask another with something else entirely. It is recorded because
        # the difference between "traced" and "not traced" is not the difference between "is a
        # bitmap" and "is not", and a floor that cannot be told from a ceiling is a bad floor.
        idiom = any(any(b[1] in ('shl', 'sal') and b[2].strip().endswith(', cl')
                        for b in bodies.get(fnva, ([], set()))[0])
                    for fnva, _s, _t in regsites[key])
        rows.append((per, tname, off, name, ctype, detail, idiom))

    order = ['BITMAP-VARIABLE', 'BITMAP-CONSTANT', 'CONSTANT', 'MEMORY', 'CALL', 'UNRESOLVED']
    rows.sort(key=lambda r: (order.index(r[0].most_common(1)[0][0]), -sum(r[0].values())))

    print('--- what builds the mask, per register-only field (%d) ---' % len(rows))
    for per, tname, off, name, ctype, detail, idiom in rows:
        verdict = per.most_common(1)[0][0]
        print('  %-14s %-22s 0x%03X  %-24s %s%s'
              % (verdict, tname[:22], off, name[:24],
                 ' '.join('%s=%d' % (k, v) for k, v in sorted(per.items())),
                 '   [1<<reg idiom present in the body]' if idiom and verdict == 'UNRESOLVED'
                 else ''))
        seen = set()
        for k, d in detail:
            if (k, d) in seen:
                continue
            seen.add((k, d))
            print('        %-16s %s' % (k, d))
    print()
    print('--- verdict census over the %d register-only fields ---' % len(rows))
    for k in order:
        if verdicts[k]:
            print('  %-16s %d' % (k, verdicts[k]))

    unres_idiom = sum(1 for r in rows
                      if r[0].most_common(1)[0][0] == 'UNRESOLVED' and r[6])
    bmp = verdicts['BITMAP-VARIABLE'] + verdicts['BITMAP-CONSTANT']
    print()
    print('  BITMAPS: a FLOOR of %d and a CEILING of %d out of %d.' % (bmp, bmp + unres_idiom, len(rows)))
    print('  %d fields are UNRESOLVED with the `1 << reg` idiom somewhere in the masking body - the'
          % unres_idiom)
    print("  weaker observation, which is not evidence about the mask at that site. The floor is what")
    print('  has been traced. Nothing between the two has been established either way.')
    print()
    print('  `ActorStorageRecord +0x110` IS ONE OF THE UNRESOLVED, and it is the field whose hand')
    print('  trace started this: its mask IS `1 << arg0`, established instruction by instruction at')
    print('  00225CE8-00225D06. The chase declines it because the definition sits above the branch')
    print('  target 00225D7A. So UNRESOLVED means THIS INSTRUMENT DID NOT ESTABLISH IT - never that')
    print('  the field is unknowable, and never that a hand trace of it would fail.')
    if verdicts['CONSTANT'] or verdicts['BITMAP-CONSTANT']:
        print()
        print('  ** %d of the fields addendum 2026-09-13k called unenumerable have a LITERAL mask'
              % (verdicts['CONSTANT'] + verdicts['BITMAP-CONSTANT']))
        print('     one instruction away. The published three-way split over-counts, and the')
        print('     figure must move. A register operand is not by itself an unknown value.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
