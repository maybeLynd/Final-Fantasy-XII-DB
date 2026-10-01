"""Widen the actor argument proof by closing it over calls, and measure what that buys.

WHY. Two censuses are blocked on the same thing. The MovementContext re-seed loses 45
displacements, and the SteeringRecord composition reaches nothing at all, because both take
their bases from the ACTOR census's argument-proven set - the functions it records as
`arg0+0x0<CALLER@SITE` - and that set is small.

WHAT IS SOUND TO ADD. If a function F is known to hold an actor in register R, and F calls G
passing R in an argument register, THEN G's CORRESPONDING ARGUMENT IS AN ACTOR. That is the
same step the census already takes once; iterating it to a fixed point adds nothing new in
kind, only in reach. Each admission names the caller and the site, so every new function is
traceable back through the chain to a function the census already vouched for.

WHAT IS NOT ADDED. A callee that receives the actor anywhere but an argument register, a call
through a register or a table, and a tail-jump - all are outside this and are counted rather
than quietly followed. The result is a floor.

THE GROUND IS WORTH STATING, because it is better than it looks. ActorManagerSlot is
`ARRAY 0x02098E10 stride=0x288 count=5` - A STATIC ADDRESS - and ActorStorageRecord is
`DYNAMIC *(*(ActorManagerSlot +0x08) + 8 + i*8)`. So the actor chain grounds out in an absolute
address rather than in an assumption, and everything this closure adds inherits that grounding
through the census it starts from.

CONTROL. The closure must reproduce its own input: every function it starts from must still be
present at the fixed point. And it reports, for each round, how many functions were added and
in which code domains - a round that suddenly admits unrelated domains is the same failure the
one-hop chain had, and would show here as a spread rather than as a number.

    gen_actor_arg_closure.py [--rounds N] [--out PATH] [--dry-run]
"""
import argparse
import collections
import io
import os
import struct
import sys

from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_OP_REG, X86_OP_IMM, X86_REG_RIP

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
EXE = os.path.join(ROOT, "Database", "Tools", "work", "exe", "FFXII_TZA.exe")
FUNCS = os.path.join(ROOT, "Database", "Tools", "work", "graph", "functions.tsv")
DB = os.path.join(ROOT, "Database", "FFXII TZA")
ACTOR = os.path.join(DB, "04-Actor-Entity", "Actor-Storage-Record",
                     "actor-storage-record-accesses.tsv")
OUT = os.path.join(DB, "04-Actor-Entity", "Actor-Storage-Record",
                   "actor-arg-proven-closure.tsv")
ARGREG = {"arg0+0x0": "rcx", "arg1+0x0": "rdx", "arg2+0x0": "r8", "arg3+0x0": "r9"}

# HAND-PROVEN SEEDS. Each is a function the actor census does not name, whose argument is an
# actor by a chain of instructions read one at a time and grounded in a row the store already
# declares. One entry per finding, with the whole chain, because a seed nobody can re-derive is
# a seed nobody should trust.
#
# 00265FF0, arg0 in RCX:
#   * 00265FF0 has ONE caller, 0026681B in 00266530, which does `mov rcx, rbx ; call 00265FF0`.
#   * In 00266530, RBX comes from 0026656A `mov rbx, qword ptr [rdx + r10*8 + 8]`, where
#     r10 = movsxd(arg2) is an index and RDX is arg1 - THE SAME `pool + 8 + i*8` INDEXING the
#     getter 00358940 performs at 00358955, and the same shape the declared DYNAMIC route
#     names: *(*(ActorManagerSlot +0x08) + 8 + i*8).
#   * 00266530 has ONE caller, 00267B79 in 002679F0, which passes `mov rdx, r14 ; mov r8d, ebp`
#     inside a loop running EBP from 0 to the record count.
#   * 002679F0 is the function the store's own ActorManagerSlot +0x08 row names -
#     ActorStorage_AllocateAndInitializeRecords, "the single block ... carves", with "the
#     pointer table starts at pool+8, so record i is ((void**)pool)[1+i]". So R14 is that pool
#     and RBX is record i.
#   Therefore 00265FF0's arg0 is an ActorStorageRecord. It carries 41 of the 45 displacements
#   the MovementContext re-seed was losing.
HAND_PROVEN = {
    0x265FF0: "rcx",
}
SLOT = ["rcx", "rdx", "r8", "r9"]
CALLER_SAVED = {"rax", "rcx", "rdx", "r8", "r9", "r10", "r11"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rounds", type=int, default=6)
    ap.add_argument("--out", default=OUT)
    ap.add_argument("--dry-run", action="store_true")
    # THE CLOSURE ITSELF WAS NEVER ACTOR-SPECIFIC. `If F holds the object in register R and
    # passes R to G in an argument register, then G's corresponding argument is that object`
    # says nothing about actors, and the census column it reads - `arg0+0x0<CALLER@SITE` - is
    # written by every census this kit produces. Only the seed FILE and the hand-proven seeds
    # were actor-only, so both are now arguments. Defaults preserve the original behaviour
    # exactly, and `--census` on any other type's accesses.tsv runs the same proof for it.
    #
    # WHY THIS MATTERS BEYOND CONVENIENCE: two major-system pages - S-01's boot singleton and
    # S-14's battle-unit pool - prove spans untouched with this method BY HAND, reaching 175
    # and 67 proved bodies. The array-seeded and rip-relative instruments elsewhere in this kit
    # are structurally blind to what it closes over, which is why the S-33 node census held two
    # functions. This is the kit's one technique that can promote an unobserved span honestly.
    ap.add_argument("--census", default=ACTOR,
                    help="the seed census (*-accesses.tsv) whose `argN+0x0` routes ground the "
                         "closure; defaults to the actor storage record")
    a = ap.parse_args()
    census = a.census
    actor_seed = os.path.abspath(census) == os.path.abspath(ACTOR)

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
    cache = {}

    def body(entry):
        if entry not in cache:
            n, f = flen.get(entry, 0), fo(entry)
            cache[entry] = [] if (f is None or n <= 0) else list(md.disasm(raw[f:f + n], entry))
        return cache[entry]

    def norm(r):
        nm = md.reg_name(r)
        m = {"eax": "rax", "ebx": "rbx", "ecx": "rcx", "edx": "rdx", "esi": "rsi", "edi": "rdi",
             "ebp": "rbp", "esp": "rsp"}
        if nm in m:
            return m[nm]
        if nm and nm.startswith("r") and nm[-1] in "dwb" and nm[1:-1].isdigit():
            return "r" + nm[1:-1]
        return nm

    # The hand-proven seeds are ACTOR findings, each justified by a chain in this file's header.
    # They are sound for the actor census and meaningless for any other, so they are applied only
    # when the actor census is the input rather than smuggled into every run.
    known = dict(HAND_PROVEN) if actor_seed else {}
    with io.open(census, encoding="utf-8") as fh:
        # THE HEADER IS NOT ALWAYS THE FIRST LINE. Censuses emitted through a wrapper open with a
        # `#` provenance comment - the resource-request slot names its emitter that way - and
        # check_census_widths already carries this same skip. Taking line 1 as the header made
        # this tool crash on those files instead of reading them.
        head = None
        for ln in fh:
            if ln.lstrip().startswith("#") or not ln.strip():
                continue
            head = ln.rstrip("\n").split("\t")
            break
        if head is None or "function" not in head or "route" not in head:
            sys.stderr.write(
                "gen_actor_arg_closure: %s has no function/route columns. 62 of the corpus's 80\n"
                "  censuses do; this is one of the 18 that do not, so the closure has nothing to\n"
                "  seed from. That is a property of the census, not a failure of the closure.\n"
                % os.path.relpath(census, DB))
            return 2
        fi, ri = head.index("function"), head.index("route")
        for ln in fh:
            c = ln.rstrip("\n").split("\t")
            if len(c) > max(fi, ri):
                hr = c[ri].split("<")[0]
                if hr in ARGREG:
                    known.setdefault(int(c[fi], 16), ARGREG[hr])
    seed_input = dict(known)
    print("SEED    %s" % os.path.relpath(census, DB))
    print("INPUT   %d functions the census proves take the object in arg0..arg3%s"
          % (len(known), "" if actor_seed else "  (hand-proven actor seeds NOT applied)"))

    def calls_passing_actor(entry, reg):
        """Calls this function makes with the actor in an argument register."""
        ins = body(entry)
        if not ins:
            return []
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
        state[0] = frozenset([reg])
        work, out = [0], []
        while work:
            k = work.pop()
            cur = state[k]
            if cur is None:
                continue
            i = ins[k]
            o = i.operands
            if (i.mnemonic == "call" and o and o[0].type == X86_OP_IMM):
                for s_i, s in enumerate(SLOT):
                    if s in cur:
                        out.append((o[0].imm, s_i, i.address))
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
        return out

    added_rows = []
    frontier = dict(known)
    for rnd in range(1, a.rounds + 1):
        new = {}
        for f, reg in sorted(frontier.items()):
            for callee, slot_i, site in calls_passing_actor(f, reg):
                if callee in known or callee in new or callee not in flen:
                    continue
                new[callee] = SLOT[slot_i]
                added_rows.append((callee, SLOT[slot_i], f, site, rnd))
        if not new:
            print("ROUND %d  fixed point reached" % rnd)
            break
        spread = collections.Counter(fowner.get(k) or "(none)" for k in new)
        print("ROUND %d  +%d functions   %s"
              % (rnd, len(new),
                 ", ".join("%s %d" % (k, v) for k, v in spread.most_common(6))))
        known.update(new)
        frontier = new
    else:
        # THE ROUND LIMIT IS NOT A FIXED POINT, AND SILENCE HERE WOULD READ AS ONE. The default 6
        # was tuned on the actor census, which closes at round 5; the battle-unit census needs 7.
        # A caller who took a truncated run for a closed one would report a floor as a complete
        # proof, which is exactly the error this file's header warns about in the other direction.
        sys.stderr.write(
            "gen_actor_arg_closure: STOPPED AT THE ROUND LIMIT (%d) WITHOUT A FIXED POINT.\n"
            "  The last round still admitted functions, so this result is TRUNCATED, not closed.\n"
            "  Re-run with a larger --rounds before treating it as a proof.\n" % a.rounds)

    print()
    print("RESULT  %d -> %d functions with a proven actor argument (+%d)"
          % (len(seed_input), len(known), len(known) - len(seed_input)))
    print()
    print("CONTROL every input function must still be present at the fixed point")
    missing = [f for f in seed_input if f not in known]
    print("          inputs: %d   missing: %d" % (len(seed_input), len(missing)))
    if missing:
        print("\nCONTROL FAILED - refusing to write.")
        return 1
    if a.dry_run:
        print("\ndry run, nothing written")
        return 0
    with io.open(a.out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("function\tname\towner\targreg\tvia_function\tvia_site\tround\n")
        for f, reg in sorted(seed_input.items()):
            fh.write("%08X\t%s\t%s\t%s\t\t\t0\n" % (f, fname.get(f, ""), fowner.get(f, ""), reg))
        for callee, reg, viaf, site, rnd in sorted(added_rows):
            fh.write("%08X\t%s\t%s\t%s\t%08X\t%08X\t%d\n"
                     % (callee, fname.get(callee, ""), fowner.get(callee, ""), reg,
                        viaf, site, rnd))
    print("\nwrote %s  (%d functions)" % (a.out, len(known)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
