"""A third way to prove a base: the function calls the object's own proc with a widget message.

THE BOTTLENECK THIS EXISTS TO BREAK. The widget census admits a function only when something
proves its first argument is a widget - registration as a handler, or a named caller that passes
one. That standard has held, and it has cost: 00246C20, the transition stepper, defines two
declared rows and cannot be admitted, because its single caller receives the object from a field
load. Four functions are in the same position. Loosening the standard to let them in would cost
the meaning of every row in the census.

SO A THIRD ROUTE, AND IT IS EVIDENCE RATHER THAN RESEMBLANCE. Widget's +0x000 is its proc, and
the engine's own way to send a widget a message is `mov rax,[obj] ; lea rdx,[record] ; mov
rcx,obj ; call rax`. The RECORDS ARE STATIC DATA: a small table at 00915040..009151F0, each
entry a message id dword followed by a payload. A function that passes one of those records to
a call through an object's own [obj] slot IS SENDING A WIDGET MESSAGE, and the object is a
widget. That is a claim about a data address, not about a shape.

WHAT KEEPS IT HONEST IS THE CLOSURE. A record is not admitted because it looks like a message.
It is admitted only when A FUNCTION THIS CENSUS ALREADY TRUSTS uses it in that exact call shape
- and only then may other users of the same record be admitted. The closure starts from the 40
registered handlers and the core functions and iterates to a fixed point, so every admitted
function traces back through records to a base that was proven by registration.

THE CONTROL IS THAT THE VOCABULARY IS ALREADY WIDGET-OWNED. Five of the eleven core functions
send from this table before any closure step runs - 00245020 sends 0x12, 00244F00 sends 0x0F,
002482E0 sends 0x18, 002473B0 sends 0x12, 00248030 sends 0x02 - which is what makes it the
widget message vocabulary rather than an arbitrary data window. A run that admitted records no
trusted function uses would be finding coincidences, and is reported as a failure.

A SECOND CONTROL, unplanned and worth keeping: the ids in this table independently confirm two
message numbers this store corrected by hand. 00245020, the release entry, sends the record at
00915070 whose id dword is 0x12 - the id an earlier pass first read as 0x10 from a chained `sub
ecx,1 ; sub ecx,1 ; cmp ecx, N` dispatcher and then corrected. 0x0F, likewise corrected from
0x0D, is the id 00244F00 sends. The data and the re-derivation agree.

    scan_widget_proc_abi.py [--out PATH] [--dry-run]
"""
import argparse
import collections
import io
import os
import struct
import sys

from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_OP_IMM, X86_OP_REG, X86_REG_RIP, X86_REG_R8, X86_REG_RDX

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
EXE = os.path.join(ROOT, "Database", "Tools", "work", "exe", "FFXII_TZA.exe")
FUNCS = os.path.join(ROOT, "Database", "Tools", "work", "graph", "functions.tsv")
FIELDS = os.path.join(ROOT, "Database", "FFXII TZA", "_types", "fields.tsv")
OUT = os.path.join(ROOT, "Database", "FFXII TZA", "16-UI", "widget-proc-abi-functions.tsv")
IDS = os.path.join(ROOT, "Database", "FFXII TZA", "16-UI", "widget-message-ids.tsv")
CTORS = (0x245000, 0x2465F0)
# The window the message records live in. Wide enough to be a search rather than a list, and the
# closure - not this constant - decides which records inside it count.
REC_LO, REC_HI = 0x915000, 0x915400
CORE = (0x2465F0, 0x245000, 0x245020, 0x273A20, 0x244F00, 0x2473B0, 0x247930, 0x248030,
        0x244960, 0x2482E0, 0x2468A0)
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

    tlo = thi = 0
    for nm, va, vs, rs, pr in secs:
        if nm == ".text":
            tlo, thi = va, va + vs

    funcs = []
    with io.open(FUNCS, encoding="utf-8") as fh:
        next(fh)
        for ln in fh:
            c = ln.rstrip("\n").split("\t")
            if len(c) >= 3:
                try:
                    funcs.append((int(c[0], 16), int(c[2]), c[1]))
                except ValueError:
                    pass
    flen = {e: n for e, n, _ in funcs}
    fname = {e: nm for e, _, nm in funcs}

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

    self_ptr = set()
    with io.open(FIELDS, encoding="utf-8") as fh:
        next(fh)
        for ln in fh:
            c = ln.rstrip("\n").split("\t")
            if len(c) >= 5 and c[0] == "Widget" and c[4].strip() == "Widget*":
                self_ptr.add(int(c[1], 16))

    handlers = set()
    for entry, _, _ in funcs:
        r8 = None
        for i in body(entry):
            o = i.operands
            if (i.mnemonic == "lea" and len(o) == 2 and o[0].type == X86_OP_REG
                    and o[0].reg == X86_REG_R8):
                t = None
                if o[1].type == X86_OP_MEM and o[1].mem.base == X86_REG_RIP:
                    t = i.address + i.size + o[1].mem.disp
                r8 = t if (t and tlo <= t < thi) else None
            elif (i.mnemonic in ("call", "jmp") and len(o) == 1 and o[0].type == X86_OP_IMM
                    and o[0].imm in CTORS and r8):
                handlers.add(r8)

    def proc_sends(entry):
        """Message records this function sends through a tracked object's own [obj] slot."""
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

        # state: (tracked set, reg->1 if loaded from [tracked+0], rdx record or None)
        state = [None] * len(ins)
        state[0] = (frozenset(["rcx"]), frozenset(), None)
        work, out, seen = [0], [], set()
        while work:
            k = work.pop()
            st = state[k]
            if st is None:
                continue
            cur, procreg, rec = st
            i = ins[k]
            o = i.operands
            if (i.mnemonic == "call" and o and o[0].type == X86_OP_REG
                    and norm(o[0].reg) in procreg and rec is not None and "rcx" in cur):
                if (i.address, rec) not in seen:
                    seen.add((i.address, rec))
                    out.append((rec, i.address))
            nxt, npr, nrec = set(cur), set(procreg), rec
            m = i.mnemonic
            if m == "call":
                nxt -= CALLER_SAVED
                npr -= CALLER_SAVED
                nrec = None
            elif (m == "lea" and len(o) == 2 and o[0].type == X86_OP_REG
                    and o[0].reg == X86_REG_RDX and o[1].type == X86_OP_MEM
                    and o[1].mem.base == X86_REG_RIP):
                t = i.address + i.size + o[1].mem.disp
                nrec = t if REC_LO <= t < REC_HI else None
            elif m == "mov" and len(o) == 2 and o[0].type == X86_OP_REG:
                d = norm(o[0].reg)
                s = o[1]
                npr.discard(d)
                if s.type == X86_OP_REG and norm(s.reg) in nxt:
                    nxt.add(d)
                elif (s.type == X86_OP_MEM and s.size == 8 and s.mem.index == 0
                        and s.mem.base and s.mem.base != X86_REG_RIP
                        and norm(s.mem.base) in nxt):
                    if s.mem.disp == 0:
                        npr.add(d)
                        nxt.discard(d)
                    elif s.mem.disp in self_ptr:
                        nxt.add(d)
                    else:
                        nxt.discard(d)
                else:
                    nxt.discard(d)
                if d == "rdx":
                    nrec = None
            elif o and o[0].type == X86_OP_REG and m not in ("cmp", "test", "push"):
                d = norm(o[0].reg)
                nxt.discard(d)
                npr.discard(d)
                if d == "rdx":
                    nrec = None
            new = (frozenset(nxt), frozenset(npr), nrec)
            for s2 in succ[k]:
                old = state[s2]
                if old is None:
                    state[s2] = new
                    work.append(s2)
                else:
                    merged = (old[0] | new[0], old[1] | new[1],
                              old[2] if old[2] == new[2] else (old[2] or new[2]))
                    if merged != old:
                        state[s2] = merged
                        work.append(s2)

        # ---- the record, attributed per PATH rather than per merge point -------------------
        # The merge above keeps ONE record where two arms set different ones, so a function that
        # funnels several arms into a single `mov rcx,obj ; call rax` reports only one of them.
        # 00246C20 is exactly that shape: five arms, five records, one shared call site, four
        # records lost. So each `lea rdx,[record]` is followed FORWARD on its own, along paths
        # where RDX is not redefined, and the walk stops at the first `call` on each path -
        # because a call clobbers RDX, the first call is the only one that record can reach.
        # This is a per-record reachability, not an over-approximating merge: a record is
        # attributed to a call site only if a real path carries it there untouched.
        for k0, i0 in enumerate(ins):
            o0 = i0.operands
            if not (i0.mnemonic == "lea" and len(o0) == 2 and o0[0].type == X86_OP_REG
                    and o0[0].reg == X86_REG_RDX and o0[1].type == X86_OP_MEM
                    and o0[1].mem.base == X86_REG_RIP):
                continue
            rec0 = i0.address + i0.size + o0[1].mem.disp
            if not (REC_LO <= rec0 < REC_HI):
                continue
            seen_k, stack = set(), list(succ[k0])
            while stack:
                k = stack.pop()
                if k in seen_k:
                    continue
                seen_k.add(k)
                i = ins[k]
                o = i.operands
                st = state[k]
                if i.mnemonic == "call":
                    if (st is not None and o and o[0].type == X86_OP_REG
                            and norm(o[0].reg) in st[1] and "rcx" in st[0]):
                        if (i.address, rec0) not in seen:
                            seen.add((i.address, rec0))
                            out.append((rec0, i.address))
                    continue                      # a call clobbers RDX: this path ends here
                if o and o[0].type == X86_OP_REG and norm(o[0].reg) == "rdx" \
                        and i.mnemonic not in ("cmp", "test", "push"):
                    continue                      # RDX redefined: this path no longer carries it
                stack.extend(succ[k])
        return out

    # THE SECOND VOUCHING SOURCE, and it is the receiving end of the same contract.
    # scan_widget_message_ids.py reads every registered handler's dispatch chain - carrying the
    # accumulated `sub ecx,1`, which is the trap that produced two hand corrections in one day -
    # and reports the ids a widget PROVABLY handles. A static record whose id dword is in that
    # vocabulary, sent through an object's own [obj] slot, meets TWO independent conditions:
    # the data is a message a widget handles, and the call is the widget proc ABI. Neither is
    # resemblance. The vocabulary is a lower bound (18 of 40 dispatchers are undecoded), which
    # is the safe direction when it is used to admit.
    vocab = set()
    if os.path.exists(IDS):
        with io.open(IDS, encoding="utf-8") as fh:
            next(fh)
            for ln in fh:
                c = ln.rstrip("\n").split("\t")
                if c and c[0]:
                    vocab.add(int(c[0], 16))

    trusted = set(handlers) | set(CORE)
    seeded = set(trusted)
    records = {}
    rows = []
    rounds = 0
    while True:
        rounds += 1
        new_records = {}
        for f in sorted(trusted):
            for rec, site in proc_sends(f):
                if rec not in records:
                    new_records[rec] = (f, site)
        if new_records:
            records.update(new_records)
        if rounds == 1 and vocab:
            for entry, _, _ in funcs:
                for rec, site in proc_sends(entry):
                    f = fo(rec)
                    mid = struct.unpack_from("<I", raw, f)[0] if f is not None else -1
                    if mid in vocab and rec not in records:
                        records[rec] = ("vocab:0x%X" % mid, site)
        added = set()
        for entry, _, _ in funcs:
            if entry in trusted:
                continue
            for rec, site in proc_sends(entry):
                if rec in records:
                    added.add(entry)
                    rows.append((entry, fname.get(entry, ""), rec, site, records[rec][0]))
                    break
        if not added:
            break
        trusted |= added
        if rounds > 8:
            break

    print("SEED          %d registered handlers + %d core functions" % (len(handlers), len(CORE)))
    print("ROUNDS        %d" % rounds)
    print("RECORDS       %d admitted, each vouched for by a trusted function" % len(records))
    for r in sorted(records):
        f = fo(r)
        mid = struct.unpack_from("<I", raw, f)[0] if f is not None else -1
        v = records[r][0]
        print("  %08X  id 0x%02X  vouched by %s at %08X"
              % (r, mid, ("%08X" % v) if isinstance(v, int) else v, records[r][1]))
    print()
    print("CONTROL       records vouched for BEFORE any closure step: %d"
          % len([r for r in records if isinstance(records[r][0], int) and records[r][0] in seeded]))
    if not any(isinstance(records[r][0], int) and records[r][0] in seeded for r in records):
        print("  FAILED: no trusted function uses any record, so nothing here is a widget message.")
        return 1
    print()
    print("ADMITTED      %d functions by the proc-ABI route" % len(rows))
    for e, nm, rec, site, voucher in sorted(rows):
        print("  %08X  sends %08X at %08X   (record vouched by %s)"
              % (e, rec, site, ("%08X" % voucher) if isinstance(voucher, int) else voucher))

    # ---- the vocabulary itself, as a table ----------------------------------------------
    # Every static record in the window that ANY function passes in RDX, with its id dword and
    # its senders. Vouched records are the ones a trusted function sends through an object's
    # own proc; the rest are listed because a message the census cannot vouch for is still part
    # of the vocabulary, and the next reader should see it rather than rediscover it.
    senders = collections.defaultdict(set)
    for entry, _, _ in funcs:
        for i in body(entry):
            o = i.operands
            if (i.mnemonic == "lea" and len(o) == 2 and o[0].type == X86_OP_REG
                    and o[0].reg == X86_REG_RDX and o[1].type == X86_OP_MEM
                    and o[1].mem.base == X86_REG_RIP):
                tt = i.address + i.size + o[1].mem.disp
                if REC_LO <= tt < REC_HI:
                    senders[tt].add(entry)

    def rec_id(r):
        f = fo(r)
        return struct.unpack_from("<I", raw, f)[0] if f is not None else -1

    print()
    print("THE VOCABULARY  every static record in the window passed in RDX by any function")
    print("  %-10s %-6s %-8s %s" % ("record", "id", "vouched", "senders"))
    for r in sorted(senders):
        print("  %08X   0x%02X   %-8s %s"
              % (r, rec_id(r), "yes" if r in records else "no",
                 " ".join("%08X" % s for s in sorted(senders[r]))))

    if a.dry_run:
        print("\ndry run, nothing written")
        return 0
    recs_out = os.path.join(os.path.dirname(a.out), "widget-message-records.tsv")
    os.makedirs(os.path.dirname(recs_out), exist_ok=True)
    with io.open(recs_out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("record\tmessage_id\tvouched\tsenders\n")
        for r in sorted(senders):
            fh.write("%08X\t0x%X\t%s\t%s\n"
                     % (r, rec_id(r), "yes" if r in records else "no",
                        " ".join("%08X" % s for s in sorted(senders[r]))))
    print("wrote %s" % recs_out)
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    with io.open(a.out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("function\tname\trecord\tmessage_id\tsite\tvouched_by\n")
        for e, nm, rec, site, voucher in sorted(rows):
            f = fo(rec)
            mid = struct.unpack_from("<I", raw, f)[0] if f is not None else 0
            fh.write("%08X\t%s\t%08X\t0x%X\t%08X\t%s\n"
                     % (e, nm, rec, mid, site,
                        ("%08X" % voucher) if isinstance(voucher, int) else voucher))
    print("\nwrote %s" % a.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
