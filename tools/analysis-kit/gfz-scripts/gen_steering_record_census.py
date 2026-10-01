"""SteeringRecord, composed from the context bases the previous step proved.

THE CHAIN IS `actor -> [+0xB8] context -> [+0xF0] steering record`, and until today both hops
were taken by record_field_scan.py, whose first hop matches ANY `mov RD, [RB + 0xB8]` with no
constraint on RB. For the two-hop case that was measured CLEAN - 42 Movement, 11 unowned, 2
ActorEntity and nothing foreign - because the second hop filters what the first lets in. Clean
by measurement is not the same as sound by construction, and the measurement is of code-domain
OWNERSHIP, which is a classification rather than a proof.

So this composes instead. gen_movement_context_census.py publishes
movement-context-proven-bases.tsv: the functions and registers that provably held a
MovementContext, each traced back to an actor argument another census vouches for. Seed those
registers, take the +0xF0 hop, and census the displacements off the result. EVERY BASE IS THEN
PROVEN BY A CHAIN OF PUBLISHED CLAIMS - actor argument, then +0xB8, then +0xF0 - rather than by
a displacement that happened to match.

THE DEPENDENCY IS THE POINT AND IS STATED: this census is exactly as sound as the movement
census, which is exactly as sound as the actor census's argument claims. That is three links,
each written down and each auditable. The alternative was one unconstrained pattern match.

TWO CONTROLS.

  SENSITIVITY. The old census reached 33 distinct displacements from 57 functions. A
  composition that reaches far fewer has traded the contamination for the signal, and the
  displacements it loses are named rather than counted.

  SPECIFICITY. 004640A0 and 004017D0, the two Presentation functions that contaminated the
  one-hop census, must not appear. They cannot in principle - they are not in the manifest -
  and the control is kept anyway, because a control that cannot fail today is what catches the
  regression tomorrow.

    gen_steering_record_census.py [--out PATH] [--dry-run]
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
MANIFEST = os.path.join(DB, "04-Actor-Entity", "Actor-Contexts",
                        "movement-context-proven-bases.tsv")
OUT = os.path.join(DB, "06-Movement-And-Navigation", "Steering-Record",
                   "steering-record-accesses.tsv")
HOP = 0xF0
REJECT = (0x4640A0, 0x4017D0)
CALLER_SAVED = {"rax", "rcx", "rdx", "r8", "r9", "r10", "r11"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=OUT)
    ap.add_argument("--manifest", default=MANIFEST)
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

    seeds = {}
    with io.open(a.manifest, encoding="utf-8") as fh:
        head = next(fh).rstrip("\n").split("\t")
        fi, gi = head.index("function"), head.index("registers")
        for ln in fh:
            c = ln.rstrip("\n").split("\t")
            if len(c) > max(fi, gi):
                seeds[int(c[fi], 16)] = set(c[gi].split(","))
    print("INPUT   %d functions with a PROVEN MovementContext base, from the manifest"
          % len(seeds))

    rows, admitted = [], {}
    for entry, regs in sorted(seeds.items()):
        n, f = flen.get(entry, 0), fo(entry)
        if not n or f is None:
            continue
        ins = list(md.disasm(raw[f:f + n], entry))
        if not ins:
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

        # (registers holding the CONTEXT, registers holding the STEERING RECORD)
        state = [None] * len(ins)
        state[0] = (frozenset(regs), frozenset())
        work, seen = [0], set()
        while work:
            k = work.pop()
            st = state[k]
            if st is None:
                continue
            ctx, rec = st
            i = ins[k]
            o = i.operands
            if not i.mnemonic.startswith("nop"):
                for n_, op in enumerate(o):
                    if (op.type == X86_OP_MEM and op.mem.index == 0 and op.mem.base
                            and op.mem.base != X86_REG_RIP and norm(op.mem.base) in rec):
                        sig = (i.address, op.mem.disp, op.size)
                        if sig not in seen:
                            seen.add(sig)
                            kind = RT.op_kind(i, op, n_)
                            kind = "a" if kind == "addr" else kind
                            rows.append((entry, fname.get(entry, ""), i.address, op.mem.disp,
                                         kind, "%s %s" % (i.mnemonic, i.op_str),
                                         "ctxproven+0xF0", ""))
                            admitted[entry] = fowner.get(entry, "")
            nc, nr = set(ctx), set(rec)
            m = i.mnemonic
            if m == "call":
                nc -= CALLER_SAVED
                nr -= CALLER_SAVED
            elif m == "mov" and len(o) == 2 and o[0].type == X86_OP_REG:
                d = norm(o[0].reg)
                s = o[1]
                nc.discard(d)
                nr.discard(d)
                if s.type == X86_OP_REG:
                    if norm(s.reg) in ctx:
                        nc.add(d)
                    if norm(s.reg) in rec:
                        nr.add(d)
                elif (s.type == X86_OP_MEM and s.size == 8 and s.mem.index == 0 and s.mem.base
                        and s.mem.base != X86_REG_RIP and norm(s.mem.base) in ctx
                        and s.mem.disp == HOP):
                    nr.add(d)
            elif o and o[0].type == X86_OP_REG and m not in ("cmp", "test", "push"):
                d = norm(o[0].reg)
                nc.discard(d)
                nr.discard(d)
            new = (frozenset(nc), frozenset(nr))
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

    print("SCAN    %d functions reach the record through a proven context; %d accesses"
          % (len(admitted), len(rows)))
    spread = collections.Counter(v or "(none)" for v in admitted.values())
    print("        admission spread: %s"
          % ", ".join("%s %d" % (k, v) for k, v in spread.most_common()))

    old_disps, old_fns, head = set(), set(), None
    with io.open(a.out, encoding="utf-8") as fh:
        head = next(fh).rstrip("\n").split("\t")
        fi, di = head.index("function"), head.index("disp")
        for ln in fh:
            c = ln.rstrip("\n").split("\t")
            if len(c) > max(fi, di):
                old_disps.add(int(c[di], 16))
                old_fns.add(int(c[fi], 16))
    new_disps = {d for _, _, _, d, _, _, _, _ in rows}
    lost = sorted(old_disps - new_disps)
    print()
    print("CONTROL sensitivity - the old census reached %d displacements from %d functions"
          % (len(old_disps), len(old_fns)))
    print("          still reached : %d" % len(old_disps & new_disps))
    print("          NEW           : %d" % len(new_disps - old_disps))
    print("          LOST          : %d%s"
          % (len(lost), ("  " + ", ".join("+0x%X" % d for d in lost)) if lost else ""))
    # THE SENSITIVITY CONTROL HAS TEETH, and it needed them the first time it ran. The 55
    # functions holding a proven context DO NOT TAKE THE +0xF0 HOP AT ALL: the steering record
    # is reached in different functions from the ones the actor census can vouch for, so this
    # composition reaches nothing and would have written an EMPTY census over a working one.
    # A generator that can silently replace evidence with nothing is worse than no generator.
    if old_disps and not (old_disps & new_disps):
        print()
        print("SENSITIVITY CONTROL FAILED - this composition reaches NOTHING the old census")
        print("reached, so it is not a re-seed, it is a deletion. Refusing to write.")
        print()
        print("WHAT THAT MEASURES, because a failure here is a result and not an error: the")
        print("chain `actor -> [+0xB8] -> [+0xF0]` is real, but the functions that walk its")
        print("SECOND hop are not the ones the actor census vouches for on its FIRST. The")
        print("proven-base set is too small to compose this far, which is the same bottleneck")
        print("that costs the movement census 45 displacements. Widening the actor census's")
        print("argument proof is what unblocks both; nothing else here will.")
        return 1

    print()
    print("CONTROL specificity - the two Presentation functions must not appear")
    bad = [r for r in REJECT if r in admitted]
    for r in REJECT:
        print("          %08X  %s" % (r, "ADMITTED" if r in admitted else "absent, as required"))
    if bad:
        print("\nSPECIFICITY CONTROL FAILED - refusing to write.")
        return 1
    if a.dry_run:
        print("\ndry run, nothing written")
        return 0
    with io.open(a.out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\t".join(head) + "\n")
        for e, nm, site, disp, kind, instr, route, note in sorted(rows, key=lambda r: (r[0], r[2])):
            fh.write("%08X\t%s\t%08X\t0x%x\t%s\t%s\t%s\t%s\n"
                     % (e, nm, site, disp, kind, instr, route, note))
    print("\nwrote %s  (%d rows)" % (a.out, len(rows)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
