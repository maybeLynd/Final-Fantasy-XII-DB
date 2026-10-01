"""Seed actor bases from the engine's own accessor, not from a displacement.

WHY THIS IS THE LEVER. Closing the actor argument proof over calls took 193 functions to 249
and recovered NOTHING of the 45 displacements the MovementContext re-seed loses: those
functions never receive an actor in an argument register from any proven caller, so no amount
of call-closure reaches them. Something has to ground out elsewhere.

WHAT I BUILT FIRST, AND WHY IT FOUND NOTHING. ActorManagerSlot is `ARRAY 0x02098E10
stride=0x288 count=5` and ActorStorageRecord is `DYNAMIC *(*(slot +0x08) + 8 + i*8)`, so the
obvious move is to walk that chain inline: `lea` the array, add the index, load +0x08, index
the table. It found 52 functions taking the `lea` and ZERO reaching an actor - because the
engine does not inline the walk. IT HAS A GETTER, AND EVERYONE CALLS IT:

    00358940  mov  r8, qword ptr [rcx + 8]          the record pool, from the slot in RCX
    00358944  test r8, r8 ; je  -> return 0
    00358949  test edx, edx ; js -> return 0        a negative ordinal returns null
    0035894D  cmp  edx, dword ptr [r8] ; jge -> 0   bounded against the count at pool+0
    00358952  movsxd rax, edx
    00358955  mov  rax, qword ptr [r8 + rax*8 + 8]  the record pointer table starts at pool+8
    0035895A  ret

Thirty bytes, and it is the DYNAMIC route written out. So the sound seed is not a pattern in
the caller - IT IS THE RETURN VALUE OF THIS FUNCTION. 75 functions call it at 107 sites.

That is the difference between matching a shape and using the engine's own call, and it cost
two wrong builds to see: the first accepted only a `lea` of a constant slot address and missed
`imul rsi, rax, 0x288 ; lea rax,[base] ; add rsi, rax`; the second fixed that and still found
no actors, because the walk it was looking for does not exist anywhere but inside the getter.
READING ONE FUNCTION WOULD HAVE SAVED BOTH.

WHAT THIS DOES NOT CLAIM. The getter returns an actor WHEN ITS CALLER PASSES A SLOT IN RCX -
that is the function's contract, and this census inherits it rather than re-proving it per
call site. It also returns NULL on three guarded paths, so a caller that does not null-check is
reading a field off zero; that is the caller's problem and is not filtered here, because a
null-check is not what makes the type right.

TWO CONTROLS.

  SENSITIVITY. The actor census already lists functions as `seed`. Those that call the getter
  must be rediscovered - if using the engine's own accessor cannot find functions the census
  found some other way, one of the two is wrong.

  SPECIFICITY. 004640A0 and 004017D0, the Presentation functions that contaminated the one-hop
  chain, must not appear.

    gen_actor_static_seed.py [--out PATH] [--dry-run]
"""
import argparse
import collections
import io
import os
import struct
import sys

from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_OP_REG, X86_OP_IMM, X86_REG_RIP
import reg_tracking as RT  # noqa: E402  (access direction: op_kind)

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
EXE = os.path.join(ROOT, "Database", "Tools", "work", "exe", "FFXII_TZA.exe")
FUNCS = os.path.join(ROOT, "Database", "Tools", "work", "graph", "functions.tsv")
DB = os.path.join(ROOT, "Database", "FFXII TZA")
ACTOR = os.path.join(DB, "04-Actor-Entity", "Actor-Storage-Record",
                     "actor-storage-record-accesses.tsv")
OUT = os.path.join(DB, "04-Actor-Entity", "Actor-Storage-Record",
                   "actor-static-proven-bases.tsv")
ACCESSOR = 0x358940
REJECT = (0x4640A0, 0x4017D0)
CALLER_SAVED = {"rax", "rcx", "rdx", "r8", "r9", "r10", "r11"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=OUT)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    raw = open(EXE, "rb").read()
    pe = struct.unpack_from("<I", raw, 0x3C)[0]
    ns = struct.unpack_from("<H", raw, pe + 6)[0]
    opt = struct.unpack_from("<H", raw, pe + 20)[0]
    ib = struct.unpack_from("<Q", raw, pe + 24 + 24)[0]
    off, secs = pe + 24 + opt, []
    for _ in range(ns):
        nm = raw[off:off + 8].rstrip(b"\x00").decode("latin1")
        vs, va, rs, pr = struct.unpack_from("<IIII", raw, off + 8)
        secs.append((nm, ib + va, vs, rs, pr))
        off += 40

    def fo(x):
        for nm, va, vs, rs, pr in secs:
            if va <= x < va + vs and (x - va) < rs:
                return pr + (x - va)
        return None

    flen, fowner, fname = {}, {}, {}
    with io.open(FUNCS, encoding="utf-8") as fh:
        next(fh)
        for ln in fh:
            c = ln.rstrip("\n").split("\t")
            if len(c) >= 4:
                try:
                    e = int(c[0], 16)
                except ValueError:
                    continue
                flen[e], fname[e], fowner[e] = int(c[2]), c[1], c[3]

    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True

    def norm(r):
        nm = md.reg_name(r)
        m = {"eax": "rax", "ebx": "rbx", "ecx": "rcx", "edx": "rdx", "esi": "rsi", "edi": "rdi",
             "ebp": "rbp", "esp": "rsp"}
        if nm in m:
            return m[nm]
        if nm and nm.startswith("r") and nm[-1] in "dwb" and nm[1:-1].isdigit():
            return "r" + nm[1:-1]
        return nm

    rows, holders, sites = [], {}, collections.defaultdict(list)
    for entry in sorted(flen):
        n, f = flen[entry], fo(entry)
        if not n or f is None:
            continue
        ins = list(md.disasm(raw[f:f + n], entry))
        if not ins:
            continue
        calls = [k for k, i in enumerate(ins)
                 if i.mnemonic == "call" and i.operands
                 and i.operands[0].type == X86_OP_IMM and i.operands[0].imm == ACCESSOR]
        if not calls:
            continue
        idx = {i.address: k for k, i in enumerate(ins)}
        succ = collections.defaultdict(set)
        for k, i in enumerate(ins):
            m = i.mnemonic
            tgt = i.operands[0].imm if (i.operands and i.operands[0].type == X86_OP_IMM) else None
            if m == "jmp":
                if tgt in idx:
                    succ[k].add(idx[tgt])
            elif m.startswith("j"):
                if tgt in idx:
                    succ[k].add(idx[tgt])
                if k + 1 < len(ins):
                    succ[k].add(k + 1)
            elif m != "ret" and k + 1 < len(ins):
                succ[k].add(k + 1)

        state = [None] * len(ins)
        work, seen = [], set()
        for k in calls:
            sites[entry].append(ins[k].address)
            for s in succ[k]:
                state[s] = frozenset(["rax"])
                work.append(s)
        while work:
            k = work.pop()
            cur = state[k]
            if cur is None:
                continue
            i = ins[k]
            o = i.operands
            if not i.mnemonic.startswith("nop"):
                for n_, op in enumerate(o):
                    if (op.type == X86_OP_MEM and op.mem.index == 0 and op.mem.base
                            and op.mem.base != X86_REG_RIP and norm(op.mem.base) in cur):
                        sig = (i.address, op.mem.disp, op.size)
                        if sig not in seen:
                            seen.add(sig)
                            kind = RT.op_kind(i, op, n_)
                            kind = "a" if kind == "addr" else kind
                            rows.append((entry, fname.get(entry, ""), i.address, op.mem.disp,
                                         kind, "%s %s" % (i.mnemonic, i.op_str),
                                         "getter:%08X" % ACCESSOR, ""))
                            holders.setdefault(entry, set()).add(norm(op.mem.base))
            nxt = set(cur)
            m = i.mnemonic
            if m == "call":
                nxt -= CALLER_SAVED
            elif m == "mov" and len(o) == 2 and o[0].type == X86_OP_REG:
                d = norm(o[0].reg)
                s = o[1]
                if s.type == X86_OP_REG and norm(s.reg) in nxt:
                    nxt.add(d)
                else:
                    nxt.discard(d)
            elif o and o[0].type == X86_OP_REG and m not in ("cmp", "test", "push"):
                nxt.discard(norm(o[0].reg))
            nxt = frozenset(nxt)
            for s2 in succ[k]:
                if state[s2] is None:
                    state[s2] = nxt
                    work.append(s2)
                elif not nxt <= state[s2]:
                    state[s2] = state[s2] | nxt
                    work.append(s2)

    print("GETTER  %08X, called from %d functions at %d sites"
          % (ACCESSOR, len(sites), sum(len(v) for v in sites.values())))
    print("WALK    %d of them then access the returned record; %d accesses"
          % (len(holders), len(rows)))
    spread = collections.Counter((fowner.get(e) or "(none)") for e in holders)
    print("        admission spread: %s"
          % ", ".join("%s %d" % (k, v) for k, v in spread.most_common()))

    census_seeds, census_fns = set(), set()
    with io.open(ACTOR, encoding="utf-8") as fh:
        h = next(fh).rstrip("\n").split("\t")
        fi, ri = h.index("function"), h.index("route")
        for ln in fh:
            c = ln.rstrip("\n").split("\t")
            if len(c) > max(fi, ri):
                census_fns.add(int(c[fi], 16))
                if c[ri] == "seed":
                    census_seeds.add(int(c[fi], 16))
    overlap = census_seeds & set(holders)
    print()
    print("CONTROL sensitivity - against the census's own %d `seed` functions"
          % len(census_seeds))
    print("          rediscovered here          : %d" % len(overlap))
    print("          NEW, not in the census at all : %d" % len(set(holders) - census_fns))
    if census_seeds and not overlap:
        print("\nSENSITIVITY CONTROL FAILED - the engine's own accessor finds none of the")
        print("functions the census found another way. One of the two is wrong. Refusing.")
        return 1
    print()
    print("CONTROL specificity - the two Presentation contaminators must not appear")
    bad = [r for r in REJECT if r in holders]
    for r in REJECT:
        print("          %08X  %s" % (r, "ADMITTED" if r in holders else "absent, as required"))
    if bad:
        print("\nSPECIFICITY CONTROL FAILED - refusing to write.")
        return 1
    if a.dry_run:
        print("\ndry run, nothing written")
        return 0
    with io.open(a.out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("function\tname\towner\tregisters\tgetter_sites\taccesses\tin_census\n")
        for e in sorted(holders):
            fh.write("%08X\t%s\t%s\t%s\t%s\t%d\t%s\n"
                     % (e, fname.get(e, ""), fowner.get(e, ""), ",".join(sorted(holders[e])),
                        " ".join("%08X" % s for s in sites[e]),
                        sum(1 for r in rows if r[0] == e),
                        "yes" if e in census_fns else "no"))
    print("\nwrote %s  (%d functions)" % (a.out, len(holders)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
