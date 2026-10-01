"""Re-seed the MovementContext census from bases another census already proved.

WHY IT NEEDED RE-SEEDING. 719 of the 1,029 rows in movement-context-accesses.tsv carry route
`chain:0xB8`, produced by record_field_scan.py, whose first hop matches ANY `mov RD, [RB+0xB8]`
in ANY function with no constraint on RB. Measured on 2026-09-19: 410 functions in the image
perform that load, the scan admitted 181, and only 68 were in Actor- or Movement-owned code -
the rest included Audio, Presentation and the script-VM bridge. Two Presentation functions,
004640A0 and 004017D0, are why four declared `float` rows appeared to contain byte-level
bitfield inserts.

THE REPAIR IS A COMPOSITION, NOT A NEW GUESS. MovementContext is reached as `actor -> [+0xB8]`.
The store already has an ACTOR census whose rows carry `arg0+0x0` and `arg1+0x0` - functions
whose first or second argument it holds to be an ActorStorageRecord. Take that as the input and
the rest follows without inference: in such a function, taint the argument register, find the
load at +0xB8 through it, and census the displacements off the result. The base is then as
proven as the actor census's own claim, AND NO MORE THAN THAT - which is the dependency, stated
plainly: if the actor census is wrong about a function's argument, this census is wrong about
the same function. That is a real dependency and it is a far smaller one than "any register in
the image that happens to hold a pointer at +0xB8".

WHAT IS KEPT FROM THE OLD FILE. Every row whose route is NOT `chain:0xB8` and not this
generator's own `actorarg:` - the `ctxarg*`, `arg*` and `seed` routes - is argument-proven
already and is carried over verbatim. The repair replaces the chain rows and nothing else, so
the diff is reviewable and the parts that were never in doubt are not disturbed.

RECOGNISING ITS OWN OUTPUT IS NOT A DETAIL, and the first version did not. It replaced only
`chain:0xB8`, so a second run read its own `actorarg:` rows back as "argument-proven, carry
over verbatim" and then emitted them again: 546 rows became 783 with 237 duplicates, silently.
A GENERATOR THAT REWRITES A FILE IN PLACE MUST RECOGNISE ITS OWN WORK, or the second run
corrupts what the first one fixed. Two consecutive runs now produce the same 546 rows.

IT ALSO PUBLISHES WHAT IT PROVED. Alongside the census it writes
movement-context-proven-bases.tsv: the functions and registers that provably held a context.
The next record down the chain - SteeringRecord is `context -> [+0xF0]` - needs exactly that,
and if it is not written down the next generator has no choice but to guess a base again, which
is the mistake this repair exists to undo. COMPOSITION COMPOUNDS SOUNDNESS ONLY IF EACH STEP
PUBLISHES WHAT IT PROVED.

TWO CONTROLS, AND THE SECOND IS THE ONE THAT WAS MISSING BEFORE.

  SENSITIVITY: the re-seeded census must still reach the displacements the old chain rows
  reached FROM FUNCTIONS THAT ARE ACTOR-OWNED. A repair that throws away the contamination and
  the signal together is not a repair, and this is what would catch it.

  SPECIFICITY: 004640A0 and 004017D0 - the two Presentation functions - MUST NOT APPEAR. They
  are the reason the old census was doubted, and a re-seed that still admits them has not
  fixed anything. The generator refuses to write if either is present.

    gen_movement_context_census.py [--out PATH] [--dry-run]
"""
import argparse
import collections
import io
import os
import struct
import sys

from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_OP_REG, X86_REG_RIP
import reg_tracking as RT  # noqa: E402  (access direction: op_kind)

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
EXE = os.path.join(ROOT, "Database", "Tools", "work", "exe", "FFXII_TZA.exe")
FUNCS = os.path.join(ROOT, "Database", "Tools", "work", "graph", "functions.tsv")
DB = os.path.join(ROOT, "Database", "FFXII TZA")
ACTOR = os.path.join(DB, "04-Actor-Entity", "Actor-Storage-Record",
                     "actor-storage-record-accesses.tsv")
OUT = os.path.join(DB, "04-Actor-Entity", "Actor-Contexts", "movement-context-accesses.tsv")
CLOSURE = os.path.join(DB, "04-Actor-Entity", "Actor-Storage-Record",
                       "actor-arg-proven-closure.tsv")
HOP = 0xB8
ARGREG = {"arg0+0x0": "rcx", "arg1+0x0": "rdx", "arg2+0x0": "r8", "arg3+0x0": "r9"}
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
    off, secs = pe + 24 + struct.unpack_from("<H", raw, pe + 20)[0], []
    ib = struct.unpack_from("<Q", raw, pe + 24 + 24)[0]
    off = pe + 24 + opt
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

    # ---- the input: functions another census holds to take an actor in a named argument -----
    # PREFER THE CLOSURE when it exists. gen_actor_arg_closure.py iterates the census's own
    # step - "F holds an actor in R, F calls G passing R in an argument register, so G's
    # argument is an actor" - to a fixed point, and publishes the result with the caller and
    # site behind every admission. Nothing new in kind, only in reach: 193 -> 249 functions.
    # Falling back to the raw census keeps this generator runnable on its own.
    actor_arg = {}
    if os.path.exists(CLOSURE):
        with io.open(CLOSURE, encoding="utf-8") as fh:
            h = next(fh).rstrip("\n").split("\t")
            cf, cr = h.index("function"), h.index("argreg")
            for ln in fh:
                c = ln.rstrip("\n").split("\t")
                if len(c) > max(cf, cr):
                    actor_arg[int(c[cf], 16)] = c[cr]
        print("INPUT   %d functions from the actor argument CLOSURE" % len(actor_arg))
    with io.open(ACTOR, encoding="utf-8") as fh:
        head = next(fh).rstrip("\n").split("\t")
        fi, ri = head.index("function"), head.index("route")
        for ln in fh:
            c = ln.rstrip("\n").split("\t")
            if len(c) <= max(fi, ri):
                continue
            # the actor census writes `arg0+0x0<CALLER@SITE` - the argument claim, then the
            # caller that proves it. Only the claim is needed here; the caller is what makes
            # the claim worth borrowing.
            head_route = c[ri].split("<")[0]
            if head_route in ARGREG:
                actor_arg.setdefault(int(c[fi], 16), ARGREG[head_route])
    if not os.path.exists(CLOSURE):
        print("INPUT   %d functions the actor census holds to take an actor in arg0..arg3"
              % len(actor_arg))

    # ---- the scan: taint the actor argument, take the +0xB8 hop, census off the result ------
    rows = []
    admitted = {}
    holders = {}   # function -> registers that provably held the context
    for entry, reg in sorted(actor_arg.items()):
        ins = body(entry)
        if not ins:
            continue
        idx = {i.address: k for k, i in enumerate(ins)}
        succ = collections.defaultdict(set)
        for k, i in enumerate(ins):
            m = i.mnemonic
            tgt = i.operands[0].imm if (i.operands and i.operands[0].type == 2) else None
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

        # state = (registers holding the ACTOR, registers holding the CONTEXT)
        state = [None] * len(ins)
        state[0] = (frozenset([reg]), frozenset())
        work, seen = [0], set()
        while work:
            k = work.pop()
            st = state[k]
            if st is None:
                continue
            act, ctx = st
            i = ins[k]
            o = i.operands
            if not i.mnemonic.startswith("nop"):
                for n_, op in enumerate(o):
                    if (op.type == X86_OP_MEM and op.mem.index == 0 and op.mem.base
                            and op.mem.base != X86_REG_RIP and norm(op.mem.base) in ctx):
                        sig = (i.address, op.mem.disp, op.size)
                        if sig not in seen:
                            seen.add(sig)
                            kind = RT.op_kind(i, op, n_)
                            kind = "a" if kind == "addr" else kind
                            rows.append((entry, fname.get(entry, ""), i.address, op.mem.disp,
                                         kind, "%s %s" % (i.mnemonic, i.op_str),
                                         "actorarg:%s+0xB8" % reg, ""))
                            admitted[entry] = fowner.get(entry, "")
                            holders.setdefault(entry, set()).add(norm(op.mem.base))
            na, nc = set(act), set(ctx)
            m = i.mnemonic
            if m == "call":
                na -= CALLER_SAVED
                nc -= CALLER_SAVED
            elif m == "mov" and len(o) == 2 and o[0].type == X86_OP_REG:
                d = norm(o[0].reg)
                s = o[1]
                na.discard(d)
                nc.discard(d)
                if s.type == X86_OP_REG:
                    if norm(s.reg) in act:
                        na.add(d)
                    if norm(s.reg) in nc or norm(s.reg) in ctx:
                        nc.add(d)
                elif (s.type == X86_OP_MEM and s.size == 8 and s.mem.index == 0 and s.mem.base
                        and s.mem.base != X86_REG_RIP and norm(s.mem.base) in act
                        and s.mem.disp == HOP):
                    nc.add(d)
            elif o and o[0].type == X86_OP_REG and m not in ("cmp", "test", "push"):
                d = norm(o[0].reg)
                na.discard(d)
                nc.discard(d)
            new = (frozenset(na), frozenset(nc))
            for s2 in succ[k]:
                old = state[s2]
                if old is None:
                    state[s2] = new
                    work.append(s2)
                else:
                    merged = (old[0] | new[0], old[1] | new[1])
                    if merged != old:
                        state[s2] = merged
                        work.append(s2)

    print("SCAN    %d functions reach a context through a PROVEN actor argument; %d accesses"
          % (len(admitted), len(rows)))
    spread = collections.Counter(v or "(none)" for v in admitted.values())
    print("        admission spread: %s"
          % ", ".join("%s %d" % (k, v) for k, v in spread.most_common()))

    # ---- what is kept from the old file -----------------------------------------------------
    kept, old_chain = [], []
    with io.open(a.out, encoding="utf-8") as fh:
        head = next(fh).rstrip("\n").split("\t")
        ri = head.index("route")
        for ln in fh:
            c = ln.rstrip("\n").split("\t")
            if len(c) <= ri:
                continue
            # REPLACEABLE: the old unconstrained chain rows AND THIS GENERATOR'S OWN OUTPUT.
            # The second half was missing on the first version and the tool was not idempotent:
            # a re-run read its own `actorarg:` rows back as "argument-proven, carry over
            # verbatim" and then emitted them again, taking the file from 546 rows to 783 with
            # 237 duplicates. A generator that rewrites a file in place must recognise its own
            # work, or the second run silently corrupts what the first one fixed.
            repl = c[ri] == "chain:0xB8" or c[ri].startswith("actorarg:")
            (old_chain if repl else kept).append(c)
    print("KEEP    %d argument-proven rows carried over verbatim; %d chain rows replaced"
          % (len(kept), len(old_chain)))

    # ---- controls ---------------------------------------------------------------------------
    fi = head.index("function")
    di = head.index("disp")
    actor_owned_chain = set()
    for c in old_chain:
        e = int(c[fi], 16)
        if (fowner.get(e) or "") in ("ActorEntity", "Movement"):
            actor_owned_chain.add(int(c[di], 16))
    new_disps = {d for _, _, _, d, _, _, _, _ in rows} | {int(c[di], 16) for c in kept}
    lost = sorted(actor_owned_chain - new_disps)
    print()
    print("CONTROL sensitivity - displacements the OLD chain rows reached from Actor- or")
    print("        Movement-owned functions must still be reached")
    print("          old actor/movement chain displacements : %d" % len(actor_owned_chain))
    print("          still reached                          : %d"
          % (len(actor_owned_chain) - len(lost)))
    print("          LOST                                   : %d%s"
          % (len(lost), ("  " + ", ".join("+0x%X" % d for d in lost[:20])) if lost else ""))
    print()
    print("CONTROL specificity - the two Presentation functions must NOT be admitted")
    bad = [r for r in REJECT if r in admitted]
    for r in REJECT:
        print("          %08X  %s" % (r, "ADMITTED - the re-seed failed" if r in admitted
                                      else "absent, as required"))
    if bad:
        print("\nSPECIFICITY CONTROL FAILED - refusing to write.")
        return 1
    if a.dry_run:
        print("\ndry run, nothing written")
        return 0

    with io.open(a.out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\t".join(head) + "\n")
        for c in kept:
            fh.write("\t".join(c) + "\n")
        for e, nm, site, disp, kind, instr, route, note in sorted(rows, key=lambda r: (r[0], r[2])):
            fh.write("%08X\t%s\t%08X\t0x%x\t%s\t%s\t%s\t%s\n"
                     % (e, nm, site, disp, kind, instr, route, note))
    # THE PROVEN-BASE MANIFEST. This scan knows something the census file cannot carry: WHICH
    # REGISTERS, IN WHICH FUNCTIONS, PROVABLY HELD THE CONTEXT. The next record down the chain -
    # SteeringRecord is `context -> [+0xF0]` - needs exactly that, and if it is not written
    # down the next generator has no choice but to guess a base again, which is the mistake
    # this whole repair exists to undo. Composition compounds soundness only if each step
    # publishes what it proved.
    man = os.path.join(os.path.dirname(a.out), "movement-context-proven-bases.tsv")
    with io.open(man, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("function\tname\towner\tregisters\tvia\n")
        for e in sorted(holders):
            fh.write("%08X\t%s\t%s\t%s\tactorarg:%s+0xB8\n"
                     % (e, fname.get(e, ""), fowner.get(e, ""),
                        ",".join(sorted(holders[e])), actor_arg[e]))
    print("\nwrote %s  (%d rows)" % (a.out, len(kept) + len(rows)))
    print("wrote %s  (%d functions with a proven context base)" % (man, len(holders)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
