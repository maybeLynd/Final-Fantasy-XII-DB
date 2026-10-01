"""Declared-integer fields that every censused access treats as a float.

Recovering four layout gaps in `CharacterRenderRecord` on 2026-09-13 turned up the same defect
thirteen times: a field declared `UNRESOLVED uint32`, or left `UNRESOLVED`, whose every access in the
image is a `movss`. The rows were not careless - they were filed from a read that looked integral -
but finding them one gap at a time is the wrong instrument for a defect that repeats.

A FINDING HERE IS ONLY AS GOOD AS THE CENSUS UNDER IT, AND THAT IS MEASURED, NOT ASSUMED.
On 2026-09-13 this check reported twenty MovementContext displacements as exclusively float-class.
Re-running the same classification over a MERGED census - the route-tracked one unioned with a chain
scan through `[actor + 0xB8]`, which agree on the displacement of all 221 sites they share - FIVE OF
THE TWENTY DID NOT SURVIVE:

    +0x078   the fuller census shows an INTEGER access as well
    +0x0D4   two float accesses and one integer: mixed, not exclusive
    +0x04C   no float-class access at all, only a constant store
    +0x074   every access is a move or an address computation
    +0x03C   no access at this displacement at all

The route-tracked census holds about a quarter of that type's accesses, so "every access is a float"
was true of the accesses it could see and false of the type. **This check cannot distinguish "no
integer evidence" from "no evidence the census reached", and a single-access finding is the case
where those look identical.** The disposition that follows from it: retype on two or more
float-class accesses with no integer use, hold a single-access finding, and re-test against the
fullest census available before either. Sixteen rows were retyped that way, seven held and five
flagged on their own rows as not surviving.

THE TEST. For each censused type, group the access census by displacement and classify every
instruction there as FLOAT (`movss`/`movaps`/`mulss`/`addss`/`comiss`/`cvt*`/...), CONST (an immediate
store whose value is a plausible float bit pattern), INTEGER (a `mov`/`and`/`or`/`test`/`cmp` that is
neither), or NEITHER. A declared 4-byte field whose type is integral and which has float evidence and
**no** integer evidence is reported.

WHY "NO INTEGER EVIDENCE" AND NOT "MOSTLY FLOAT". `mov dword [rdx+0xc], ecx` with `ecx` zeroed stores
a float zero, and three lanes of the matrix at `+0x180` are written exactly that way - so a genuinely
mixed displacement is evidence of nothing and is counted separately, never reported. The one-sided
rule costs recall and buys the property that a report is always right.

WHY `CONST` IS ITS OWN CLASS, added after the first version had fifteen real floats in the mixed pile.
`mov dword ptr [rbx + 0x2b0], 0xbf800000` is how a compiler writes -1.0f: no float instruction is
involved, because storing a constant needs no arithmetic. Counting that as integer evidence made every
default-initialised float look contested, which is the reverse of the truth - a float constant in the
initialiser corroborates the type, it does not dispute it. The immediate is called float-plausible
only if it is at least 0x10000 (a small integer is a small integer) and its float reading is neither
denormal nor absurd. Effect on this tree: control 36 -> 50, findings 26 -> 47, mixed 70 -> 43.

THE CONTROL RUNS FIRST AND IS PRINTED FIRST. Fields already declared `float` whose accesses are
float-class are counted: if that number is zero the classifier is broken, and every empty defect list
below it is a property of the classifier rather than of the store.
"""
import collections
import io
import os
import re
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_census_widths as ccw
import insn_class

DB = 'Database/FFXII TZA'
FIELDS = os.path.join(DB, '_types', 'fields.tsv')

# FLOAT is scalar float WORK, not any instruction that happens to use an xmm register.
#
# `movaps`, `movups`, `movdqa` and `movdqu` were in this class until 2026-09-13 and had to come out.
# A 16-byte packed move is how a compiler COPIES a block - `SaveImageHeader` is memcpy'd by an
# unrolled `movups xmm0,[rbx]` / `movups [rax-0x80],xmm0` loop - and with them included the gate
# reported `imageChecksumComplement` and `battleSystemStateMagic` as floats. A checksum is not a
# float and a magic number is not a float; the instruction was a copy.
#
# That was the THIRD time in one hour that this file treated a MOVE as evidence of a TYPE: first
# plain `mov`, then `lea`, then the packed moves. Only arithmetic and comparison say what something
# IS. Everything that merely relocates bytes says where they went.
FLOAT_OP = re.compile(r'\b(movss|mulss|addss|subss|divss|comiss|ucomiss|sqrtss|maxss|minss|'
                      r'cvtsi2ss|cvtss2si|cvttss2si|cvtss2sd|cvtsd2ss|rcpss|rsqrtss|'
                      r'unpcklps|shufps)\b')
# ARITHMETIC AND MOVES ARE NOT THE SAME EVIDENCE, and the paragraph above says why: "Only
# arithmetic and comparison say what something IS. Everything that merely relocates bytes says
# where they went." The retype policy ("two or more float-class accesses") was written against
# `movss`, where a single access can be a mis-attributed base. `addss xmm6,[rdi+0xc]` adds the
# loaded dword AS a float and relocates nothing, so one of those is not the same as one move.
# Reported apart rather than merged, with the adjudication left to a person who can see the
# difference. 2026-09-14, OPUS.
ARITH = re.compile(r'\b(mulss|addss|subss|divss|comiss|ucomiss|sqrtss|maxss|minss|'
                   r'cvtsi2ss|cvtss2si|cvttss2si|cvtss2sd|cvtsd2ss|rcpss|rsqrtss)\b')
# A plain `mov` is NOT integer evidence, and neither is `lea`.
#
# Added 2026-09-13, the same hour the reverse direction was added and immediately produced five
# findings, ALL FIVE OF THEM FALSE:
#
#   CharacterRenderRecord 0x1C0   lea rcx, [rbx + 0x1c0]        taking an address
#   CharacterRenderRecord 0x200   mov dword [rbx+0x200], esi    esi is zero
#   CharacterRenderRecord 0x614   mov dword [rdi + 4], eax      copying float bits through a GPR
#   BattleUnit            0x0F4   mov eax, [rdx + 0x74]         the same, loading
#
# A compiler moves a float through a general register whenever it is copying rather than computing,
# and `lea` says nothing about the value at all. Only ARITHMETIC and BIT MANIPULATION are evidence
# that something is being treated as an integer. Splitting the class fixed all five without a single
# special case - which is the sign it was one classification error and not five separate accidents.
NEUTRAL_OP = re.compile(r'^\s*(mov|movzx|movsx|movsxd|lea|movaps|movups|movdqa|movdqu|'
                        r'movlps|movhps|nop)\b')
INT_OP = re.compile(r'\b(and|or|xor|test|cmp|add|sub|inc|dec|bt|bts|btr|shl|shr|sar|imul|idiv|'
                    r'neg|not|adc|sbb)\b')

# An immediate store whose value is a plausible float bit pattern is NOT integer evidence.
#
# Added 2026-09-13, after the first version put fifteen real floats in the `mixed` bucket and left
# them there. `mov dword ptr [rbx + 0x2b0], 0xbf800000` is how a compiler writes -1.0f: there is no
# float instruction involved, because storing a constant needs no arithmetic. Counting that as
# integer evidence made every default-initialised float look contested, which is the opposite of the
# truth - a float CONSTANT in the initialiser is corroboration, not conflict.
IMM = re.compile(r',\s*(0x[0-9a-fA-F]+|\d+)\s*$')


def float_plausible(imm):
    """Is this immediate more plausibly a float bit pattern than an integer?"""
    try:
        v = int(imm, 16) if imm.lower().startswith('0x') else int(imm)
    except ValueError:
        return False
    if not 0 < v <= 0xFFFFFFFF:
        return False
    if v < 0x10000:
        return False                      # a small integer is a small integer
    f = struct.unpack('<f', struct.pack('<I', v))[0]
    if f != f or f in (float('inf'), float('-inf')):
        return False
    a = abs(f)
    return 1e-6 <= a <= 1e9               # denormals and absurd magnitudes are not constants


INTEGRAL = {'uint32', 'int32', 'UNRESOLVED', 'uint16', 'int16', 'uint8', 'int8', 'uint64', 'int64'}


def declared():
    """type -> {offset: (size, name, ctype, readiness)}"""
    per = collections.defaultdict(dict)
    for n, line in enumerate(io.open(FIELDS, encoding='utf-8')):
        if n == 0 or not line.strip():
            continue
        c = line.rstrip('\n').split('\t')
        if len(c) < 8:
            continue
        try:
            per[c[0]][int(c[1], 16)] = (int(c[2]), c[3], c[4], c[6])
        except ValueError:
            continue
    return per


def meanings():
    """(type, offset) -> the `meaning` cell, where a prior adjudication lives.

    Kept separate from declared() so that function's tuple shape stays what its callers expect.
    """
    out = {}
    for n, line in enumerate(io.open(FIELDS, encoding='utf-8')):
        if n == 0 or not line.strip():
            continue
        c = line.rstrip('\n').split('\t')
        if len(c) < 6:
            continue
        try:
            out[(c[0], int(c[1], 16))] = c[5]
        except ValueError:
            continue
    return out


MEANING = meanings()


def kinds(path):
    """displacement -> Counter of 'float' / 'int' / 'other'"""
    per = collections.defaultdict(collections.Counter)
    for n, line in enumerate(io.open(path, encoding='utf-8', errors='replace')):
        if n == 0 or not line.strip():
            continue
        c = line.rstrip('\n').split('\t')
        if len(c) < 6:
            continue
        try:
            off = int(c[3], 16)
        except ValueError:
            continue
        # Classified by the SHARED definition, never restated here. The rule this file spent three
        # revisions rediscovering now lives in insn_class.py, with every one of those three failures
        # written into its docstring - and a fourth from check_strided_fields, which reproduced the
        # `lea` mistake a few hours after this file was fixed.
        per[off][insn_class.classify(c[5])] += 1
        # recorded alongside, not instead: a float access that is ARITHMETIC is stronger evidence
        # than one that is a move, and the reporting splits on it
        if ARITH.search(c[5]):
            per[off]['float-arith'] += 1
    return per


decl = declared()
control = 0
findings = []
reverse = []
mixed = 0
types_seen = 0

for tname, census_file, _sbase, shift, extent in ccw.censused_types():
    path = None
    for root, _d, files in os.walk(DB):
        if census_file in files:
            path = os.path.join(root, census_file)
            break
    if path is None or tname not in decl:
        continue
    types_seen += 1
    per = kinds(path)
    if shift:
        # A sub-object shares its parent's census file at a fixed displacement - and its own
        # EXTENT bounds it from above. This clip was missing until 2026-09-13: without it a
        # SavePayload access at 0xE2D0 was presented here as a field of ImageBackedStateBlock,
        # a type whose declared rows end at 0x47E8. ccw.rebase applies both bounds, once.
        per = dict((ccw.rebase(d, shift, extent), k) for d, k in per.items()
                   if ccw.rebase(d, shift, extent) is not None)
    for off, (size, name, ctype, readiness) in sorted(decl[tname].items()):
        k = per.get(off)
        if not k:
            continue
        pure_float = k['float'] > 0 and k['int'] == 0
        pure_int = k['int'] > 0 and k['float'] == 0 and k['const'] == 0
        if ctype.startswith('float') and pure_float:
            control += 1
            continue
        if ctype.startswith('float') and pure_int:
            # THE OTHER DIRECTION. A gate that tests one way is half a gate, and this file spent
            # its first two versions being exactly that. A field declared float whose every access
            # is an integer operation is the same defect mirrored, and nothing was looking for it.
            reverse.append((tname, off, name, ctype, readiness, k['int']))
            continue
        if ctype in INTEGRAL and size == 4 and pure_float:
            findings.append((tname, off, name, ctype, readiness, k['float'],
                             k['float-arith']))
        elif ctype in INTEGRAL and size == 4 and k['float'] and k['int']:
            mixed += 1

print('--- control (printed first, because everything below is a property of the classifier) ---')
print('  fields already declared float whose accesses are float-class: %d' % control)
print('  censused types compared against the store: %d' % types_seen)
if not control:
    print('  CONTROL FAILED: the classifier finds no float field anywhere. Every result below is void.')
    sys.exit(2)

print()
# THE ADJUDICATION IS IN THE ROW AND NOTHING READ IT. Every one of these findings has already been
# considered: the `meaning` cell says "HELD, NOT RETYPED" and gives the reason, usually that a
# single float-class access can be a mis-attributed base. Reporting ten held rows as ten findings,
# run after run, is how a checker becomes wallpaper - and it hid the one row that mattered.
#
# **A HELD row is only still held while its evidence is what the hold was argued against.**
# `MovementContext+0x058` was held because the evidence was ONE access and the cell named its own
# bar - "two independent accesses with no integer use". The census grew to two, in different
# functions by different routes, and the row sat in this list looking exactly like the nine that
# had not moved. Split them, and put the ones whose evidence has outgrown their hold FIRST.
# 2026-09-14, OPUS.
# ARITH is defined beside FLOAT_OP, where the classification rules live.
HELD = re.compile(r'HELD,\s*NOT\s*RETYPED', re.I)
# WIDENED 2026-09-14 (OPUS). This matched only "SINGLE ... access" and "still a single one", so a
# row held with "read once as a float32" - SavePayload +0x4E470 and +0x4E480 - could never be
# re-raised however far its census grew. More rows under the re-raise, not fewer.
SINGLE_BASIS = re.compile(r'\bSINGLE\b.*?\baccess\b|\bstill a single one\b|'
                          r'\bread once\b|\bexactly ONE\b|\bstill one\b', re.I)
# A HOLD MUST SAY WHAT IT IS HELD AGAINST, or it cannot be re-checked and is permanent by accident.
# Either it names the bar it was argued at (SINGLE_BASIS), or it says plainly that it is held for
# some other stated reason - the two TYPE CONFLICT rows are held "for a different reason from a
# single-access threshold" and that is a bar too, just not a count.
OTHER_BASIS = re.compile(r'held for a different reason|TYPE CONFLICT|under the same threshold',
                         re.I)
held, fresh, outgrown, arith, unstated = [], [], [], [], []
for row in findings:
    tname, off, name, ctype, readiness, n, na = row
    meaning = MEANING.get((tname, off), '')
    if HELD.search(meaning) and n >= 2 and SINGLE_BASIS.search(meaning):
        outgrown.append(row)
    elif HELD.search(meaning) and not (SINGLE_BASIS.search(meaning)
                                       or OTHER_BASIS.search(meaning)):
        unstated.append(row)
    elif HELD.search(meaning):
        held.append(row)
    elif na:
        arith.append(row)
    else:
        fresh.append(row)

print('--- declared-integral 4-byte fields whose accesses are EXCLUSIVELY float-class: %d ---'
      % len(findings))
if outgrown:
    print('  EVIDENCE HAS OUTGROWN THE HOLD - the cell was held on a SINGLE access and the census')
    print('  now shows more. These are the rows to read first:')
    for tname, off, name, ctype, readiness, n, na in outgrown:
        print('    %-26s 0x%03X  %-24s %-10s %d float access(es), %d arithmetic'
              % (tname, off, name, ctype, n, na))
if arith:
    print('  FLOAT ARITHMETIC, not a move - stronger evidence about the VALUE:')
    print('    `addss xmm,[mem]` adds the loaded dword AS a float; a move only relocates bits.')
    print('    BUT IT SETTLES THE VALUE, NOT THE OFFSET - corrected 2026-09-14 (OPUS), because the')
    print('    line that stood here said arithmetic was "stronger than the hold policy was written')
    print('    for" and named the mis-attributed base as the thing it defeats. It does not.')
    print('    The two-access rule guards against an instruction being ATTRIBUTED to the wrong')
    print('    displacement through an inferred base; whether that instruction is an add or a move')
    print('    is irrelevant to which field it touched. MEASURED in the MovementContext census:')
    print('    SEVEN sites are each attributed to 4-5 different displacements at stride 0x10 -')
    print('    003DA7C1 to 0x30/0x40/0x50/0x60/0x70, 003DA7CD to 0x34/0x44/..., 003DA73E to')
    print('    0x38/0x48/..., and 003DA60F - the ARITHMETIC one - to 0x3C/0x4C/0x6C/0x7C.')
    print('    So the "1 float access" at +0x3C and at +0x4C is the SAME INSTRUCTION seen through')
    print('    two different inferred bases, not two independent observations. Do not retype on')
    print('    this alone. Routed as OPUS-REQ-SWE2-STRUCT-MOVCTX-STRIDED-ATTRIBUTION.')
    print('    THE FAMILY REACHES INTO THE LIST BELOW TOO, so read the two lists together:')
    print('    MovementContext +0x74 and +0x78 are also stride-family rows - their float access is')
    print('    003DA7CD and 003DA73E through arg0+0x70 - and +0x74 additionally has two DIRECT but')
    print('    uninformative `mov dword ptr [rax+0x74], edi` stores. MovementContext +0x0D4 is NOT')
    print('    in the family: 002E521F is `movss dword ptr [rdi + 0xd4], xmm0`, a direct write at')
    print('    its own literal displacement, so it is an ordinary single-access hold and the only')
    print('    one of the three the two-access rule was actually written for.')
    for tname, off, name, ctype, readiness, n, na in arith:
        print('    %-26s 0x%03X  %-24s %-10s %d float access(es), %d ARITHMETIC'
              % (tname, off, name, ctype, n, na))
if fresh:
    print('  NOT YET ADJUDICATED - no HELD note, and every float access is a move:')
    for tname, off, name, ctype, readiness, n, na in fresh:
        print('    %-26s 0x%03X  %-24s %-10s %d movss-class access(es)'
              % (tname, off, name, ctype, n))
if held:
    print('  ALREADY HELD, evidence unchanged - considered and deliberately not retyped: %d'
          % len(held))
    for tname, off, name, ctype, readiness, n, na in held:
        print('    %-26s 0x%03X  %-24s %-10s %d movss-class access(es)'
              % (tname, off, name, ctype, n))

print()
print('--- the other direction: declared FLOAT, every access an integer operation: %d ---'
      % len(reverse))
for tname, off, name, ctype, readiness, n in reverse:
    print('  %-28s 0x%03X  %-28s %-10s %-20s %d integer access(es)'
          % (tname, off, name, ctype, readiness, n))
if not reverse:
    print('  none. Reported even when empty, because an empty half of a symmetric test is a result')
    print('  and a missing half is a blind spot - which is what the first two versions of this file had.')

print()
print('  mixed (float AND integer accesses at the same displacement): %d - NOT reported as defects.' % mixed)
print('  `mov dword [x], ecx` with ecx zeroed stores a float zero, so a mixed displacement is')
print('  evidence of nothing on its own. Three lanes of the matrix at CharacterRenderRecord+0x180')
print('  are written exactly that way.')

if unstated:
    print('\n  HELD WITH NO STATED BAR - a hold that does not say what it is held against cannot')
    print('  be re-checked, so it never gets re-raised and is permanent by accident: %d'
          % len(unstated))
    for tname, off, name, ctype, readiness, n, na in unstated:
        print('    %-26s 0x%03X  %d float access(es)' % (tname, off, n))

# ADJUDICATED DEBT MUST NOT FAIL, AND AN UNDECIDED ROW MUST. The old line was
# `sys.exit(1 if (findings or reverse) else 0)`, which failed on the existence of any finding -
# so this file could never be green while any declared-integral field had a float-class access,
# however thoroughly each had been decided. FINAL-AUDIT-PROTOCOL records the identical defect in
# check_strided_fields and check_doc_claims, found 2026-09-14: "ACCEPTED DEBT STILL FAILS A PASS".
#
# What still fails: a FRESH finding nobody has decided; an OUTGROWN hold whose census has passed
# the bar its own note states; an UNSTATED hold that names no bar; an ARITHMETIC row with no note;
# and the reverse direction, which has no hold vocabulary at all.
owed = fresh + outgrown + unstated + arith
sys.exit(1 if (owed or reverse) else 0)
