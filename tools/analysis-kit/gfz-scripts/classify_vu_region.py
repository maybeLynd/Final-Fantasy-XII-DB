"""Classify the VIF1/VU1 region's undeclared bodies by instruction mix and helper use.

WHY. The region at 00478280-004FF270 holds 210 undeclared bodies and 551,023 bytes - the heaviest
block of undeclared code in the store. `the-vif1-vu1-layer.md` identifies the region and cites
addresses in 22 of them; 188 it never mentions. 004D40E0, the largest of those, turned out to be a
recompiled VU1 microprogram identifiable from the page's OWN vocabulary rather than from new
research (8afccf85).

So the question is whether that was luck or a method. This applies the same two measurements to
every body in the region and reports the distribution. It CLASSIFIES; it does not explain - "a VU
microprogram" says what kind of thing a body is and nothing about what it draws, which is the
page's own first open item.

THE TWO SIGNALS, both taken from what the page already establishes:

  FLOAT RATIO       a VU microprogram recompiled to x64 is dominated by scalar float arithmetic.
                    004D40E0 is 62.3 %.
  VU HELPER CALLS   `0022CC20` clears a VU register; `0022CC30` and `0022CC40` set the VU sticky S
                    and sticky Z bits of the status word at `02064DEC`. The page names all three.
                    A body that calls them is operating the VU machine state.

A body is called a MICROPROGRAM only when BOTH hold - a high float ratio alone is any maths, and a
helper call alone is any caller. The conjunction is what the page's model predicts, and a
classifier that fires on either would tell us nothing we did not already assume.
"""
import collections
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_dispositions as cd
import check_frontier_shape as fs
from disasm_fn import Image, DEFAULT_EXE

try:
    from capstone import Cs, CS_ARCH_X86, CS_MODE_64
except ImportError:
    sys.stderr.write('classify_vu_region: needs capstone\n')
    raise SystemExit(2)

LO, HI = 0x478280, 0x4FF270
VU_HELPERS = {0x0022CC20: 'VU register clear', 0x0022CC30: 'VU sticky S', 0x0022CC40: 'VU sticky Z'}
FLOAT_HI = 0.40          # 004D40E0 sits at 0.62 even after the correction below

# THE FIRST VERSION OF THIS FILE COUNTED PACKED MOVES AS FLOAT WORK, and that is the rule this kit
# already carries a module for. `insn_class.py` exists because the same mistake was made four times
# on 2026-09-13 in two other instruments, and its first line is:
#
#     ONLY ARITHMETIC AND COMPARISON SAY WHAT SOMETHING IS.
#     EVERYTHING THAT RELOCATES BYTES SAYS WHERE THEY WENT.
#
# A private `re.compile(r'(ss|ps|pd|sd)$')` matches `movups`, `movaps`, `movdqa` - block copies -
# and I wrote one anyway, with the shared module sitting in the same directory. `004ADD10` is 238
# `movups` and 187 `movaps` out of 1,807 instructions: 23.5 % of it is copying, and the first
# version read that as maths. So the classifier now asks `insn_class`, which is the whole point of
# there being an `insn_class`.
import insn_class


def float_work(mnemonic, text):
    """True for scalar float ARITHMETIC, never for a move that happens to be in an xmm register."""
    return insn_class.classify(text) == 'float'


def main():
    sizes = cd.load_functions(fs.FUNCTIONS)
    meta = {e: v for e, v in fs.rows(fs.FUNCTIONS).items() if e in sizes}
    a_set, _eo, _ai, _da = cd.measure_a(fs.DB, sizes)
    claimed = set()
    for doc, parts in cd.parse_families(fs.DB):
        if len(parts) < 3:
            continue
        p = os.path.join(os.path.dirname(doc), parts[2].strip())
        if not os.path.exists(p):
            continue
        for n, line in enumerate(open(p, encoding='utf-8', errors='replace')):
            if n == 0 or line.startswith('#') or not line.strip():
                continue
            m = re.match(r'^([0-9A-Fa-f]{6,8})', line.strip())
            if m:
                claimed.add(int(m.group(1), 16))
    front = set(meta) - set(a_set) - claimed
    run = [e for e in sorted(meta) if LO <= e <= HI and e in front]

    print('--- control: undeclared bodies in %08X-%08X: %d, bytes %d ---'
          % (LO, HI, len(run), sum(meta[e][0] for e in run)))
    if not run:
        print('  CONTROL FAILED: the region is empty. Everything below is void.')
        return 2

    img = Image(DEFAULT_EXE)
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    kinds = collections.Counter()
    bytes_by = collections.Counter()
    helper_hits = collections.Counter()
    rows = []
    for e in run:
        b = img.read(e, min(meta[e][0], 0x8000))
        if not b:
            kinds['unreadable'] += 1
            continue
        ins = list(md.disasm(b, e))
        if not ins:
            kinds['undecodable'] += 1
            continue
        fl = sum(1 for i in ins if float_work(i.mnemonic, '%s %s' % (i.mnemonic, i.op_str)))
        ratio = float(fl) / len(ins)
        helpers = 0
        for i in ins:
            if i.mnemonic in ('call', 'jmp'):
                m = re.match(r'^0x([0-9a-f]+)$', i.op_str.strip())
                if m and int(m.group(1), 16) in VU_HELPERS:
                    helpers += 1
                    helper_hits[VU_HELPERS[int(m.group(1), 16)]] += 1
        if ratio >= FLOAT_HI and helpers:
            k = 'VU MICROPROGRAM (float-dominated AND drives VU state)'
        elif ratio >= FLOAT_HI:
            k = 'float-dominated, no VU helper call'
        elif helpers:
            k = 'drives VU state, not float-dominated'
        else:
            k = 'neither signal'
        kinds[k] += 1
        bytes_by[k] += meta[e][0]
        rows.append((meta[e][0], e, k, ratio, helpers))

    tot_b = sum(bytes_by.values())
    print()
    print('--- classification over %d bodies ---' % sum(kinds.values()))
    for k, v in kinds.most_common():
        print('  %-52s %4d bodies  %8d B  %5.1f%% of bytes'
              % (k, v, bytes_by[k], 100.0 * bytes_by[k] / max(1, tot_b)))
    print()
    print('  VU helper calls seen: %s'
          % ', '.join('%s x%d' % (k, v) for k, v in helper_hits.most_common()))
    print()
    rows.sort(reverse=True)
    print('--- the ten largest, with their signals ---')
    for size, e, k, ratio, helpers in rows[:10]:
        print('  %08X %7d B  float %4.1f%%  helpers %2d  %s'
              % (e, size, 100.0 * ratio, helpers, k[:44]))
    out = None
    for i, arg in enumerate(sys.argv):
        if arg == '--out' and i + 1 < len(sys.argv):
            out = sys.argv[i + 1]
    if out:
        head = [
            '# VU-region classification - generated by classify_vu_region.py --out',
            '# Bodies in %08X-%08X that no disposition claims, classified on TWO signals taken from'
            % (LO, HI),
            '# the-vif1-vu1-layer.md itself: float-dominated (>= 40%% of decoded instructions) AND',
            '# calling one of 0022CC20 (VU register clear), 0022CC30 (sticky S), 0022CC40 (sticky Z).',
            '#',
            '# float_pct counts SCALAR FLOAT ARITHMETIC via insn_class, never packed moves. An earlier',
            '# version of this file counted movaps/movups as maths and inflated every ratio in the',
            '# region - 13,470 packed moves against 18,808 scalar float ops. KNOWN RESIDUAL: packed',
            '# ARITHMETIC is not counted either (829 instructions region-wide: mulps 478, xorps 182,',
            '# andps 169), so these ratios under-count real vector work by at most about 4 per cent -',
            '# an error in the safe direction.',
            '#',
            '# The rows most worth checking are those nearest the 40 per cent threshold, where a',
            '# two-signal test is weakest. 004804A0 is a KNOWN FALSE POSITIVE of the class test: the',
            '# page explains it as the status-flag comparison routine, which calls the VU helpers',
            '# without being a microprogram. The two signals cannot tell a body that OPERATES the VU',
            '# machine from one that WATCHES it.',
            '#',
            '# A CLASS IS NOT AN EXPLANATION: "microprogram" says what kind of body this is and nothing',
            '# about what it draws, which is the page\'s open item.',
            'entry\tsize_bytes\tfloat_pct\tvu_helper_calls\tclass',
        ]
        with open(out, 'w', encoding='utf-8', newline='') as fh:
            fh.write('\n'.join(head) + '\n')
            for size, e, k, ratio, helpers in rows:
                fh.write('%08X\t%d\t%.1f\t%d\t%s\n' % (e, size, 100.0 * ratio, helpers, k))
        print('  wrote %s' % out)

    print()
    print('  A CLASS IS NOT AN EXPLANATION. "VU microprogram" says what kind of thing a body is and')
    print('  nothing about what it draws - the page\'s own first open item. What this buys is that')
    print('  the region stops being one undifferentiated 551 KB and becomes counted populations.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
