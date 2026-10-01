# ctx_indexed.py : find INDEXED accesses through the shared drawing context pointer 0209CC40.
#
# The page's field map was built by tracking the loaded pointer and recording fixed displacements,
# so it can only see `[ctx + const]`. That is why it reports 24 offsets, all in the last sixty bytes
# of a 4,360-byte object, and why the head 0x1060 bytes look untouched - a whole-image sweep of the
# object's OWN address range finds exactly one reference, the initialiser's `lea`. So the head is
# reached neither by a fixed displacement nor by its address: if it is used at all, it is used
# through a SCALED INDEX off the pointer, which is precisely the shape a displacement census cannot
# see.
#
# This tracks the register a load of [0209CC40] lands in, propagates it through reg-to-reg moves and
# `add reg, const`, kills it on a write or a volatile-clobbering call, and reports every memory
# operand that uses it as a BASE WITH AN INDEX REGISTER.
#
# Control: 002B3550 must NOT appear (it only takes the address and memsets), and at least one of the
# ten functions the page names as touching +0x10FC must appear in the tracked population, or the
# tracker is not reaching the bodies the page already read.
import collections
import re
import sys

exec(open('disw.py').read().split("fn = int")[0])

CELL = 0x0209CC40
NONVOL = {"rbx", "rbp", "rdi", "rsi", "r12", "r13", "r14", "r15"}
WRITE = ("mov", "or", "and", "add", "sub", "xor", "inc", "dec", "lea", "movzx", "movsx",
         "pop", "imul", "shl", "shr", "sar", "cmpxchg", "xchg")
# [base + index*scale ( + disp )]
IDX = re.compile(r"\[(r[a-z0-9]+) \+ (r[a-z0-9]+)\*(\d)(?: \+ (0x[0-9a-f]+))?\]")

tracked = collections.Counter()
hits = []
for fn in sorted(funcs):
    o = off(fn)
    if o is None:
        continue
    try:
        ins = list(md.disasm(d[o:o + funcs[fn]], fn))
    except Exception:
        continue
    live = set()
    for x in ins:
        ops = x.op_str
        dest = ops.split(",")[0].strip()
        # a load of the cell starts tracking
        if x.mnemonic == "mov" and ("rip + " in ops or "rip - " in ops):
            sgn = 1 if "rip + " in ops else -1
            try:
                disp = int(ops.split("rip + " if sgn > 0 else "rip - ")[1].split("]")[0], 16)
            except (IndexError, ValueError):
                disp = None
            if disp is not None and x.address + x.size + sgn * disp == CELL and "[" not in dest:
                live.add(dest)
                tracked[fn] += 1
                continue
        if x.mnemonic == "call":
            live = {r for r in live if r in NONVOL}
            continue
        # propagate through reg-to-reg moves; an `add reg, const` keeps it a base into the object
        if x.mnemonic == "mov" and "[" not in ops:
            src = ops.split(",")[-1].strip()
            if src in live:
                live.add(dest)
            elif dest in live:
                live.discard(dest)
        elif x.mnemonic == "add" and dest in live and "0x" in ops.split(",")[-1]:
            pass
        elif dest in live and x.mnemonic in WRITE and "[" not in dest:
            live.discard(dest)
        m = IDX.search(ops)
        if m and m.group(1) in live:
            hits.append((fn, x.address, x.mnemonic, ops, m.group(1), m.group(2), int(m.group(3)),
                         int(m.group(4), 16) if m.group(4) else 0))

print("functions that load [%08X] : %d" % (CELL, len(tracked)))
print("INDEXED accesses through it : %d\n" % len(hits))
for fn, a, mn, ops, base, idx, scale, disp in hits:
    print("  %08X @%08X  %s %s      base=%s index=%s scale=%d disp=+0x%X"
          % (fn, a, mn, ops[:52], base, idx, scale, disp))

print("\nCONTROL initialiser 002B3550 is NOT in the tracked set:", 0x2B3550 not in tracked)
PAGE_TOUCHERS = {0x2AC5F0, 0x2AF960}
print("CONTROL at least one page-named toucher is tracked:",
      bool(PAGE_TOUCHERS & set(tracked)), sorted("%08X" % f for f in (PAGE_TOUCHERS & set(tracked))))
