"""ptrtaint.py - forward taint of a structure pointer through registers, stack spills and call arguments, to list every
access at chosen displacements off it (OPUS, 2026-09-30; written for GR-1, the ActorWaitSlot +0x27 readers).

  python -B ptrtaint.py --seed-load 0xA8 --scale-lea --disp 0x27 [--width-cover] [--depth 2] [--monotone]
  python -B ptrtaint.py --seed FUNC:ADDR:REG [--seed ...] --disp 0x27 [--width-cover] [--depth 2] [--monotone]

Seeds: every `mov R, qword ptr [B + SEED]` in the image (a load of the array-base field), or typed seeds (an element
pointer in REG just after ADDR). With --scale-lea, a pointer formed from a seeded base (`lea X, [R + Y*k]`,
`add X, R` / `add R, Y`) is the element pointer the taint follows; without it, the loaded pointer itself is followed.
The seeded base carries the taint BASE, element pointers ELEM.
Propagation, per function, linear in address order:
  - mov / lea copies; any other write to a register kills its taint;
  - a store of a tainted register to [rsp + k] taints that stack slot; a later load from the same slot restores it;
    a qword store of a tainted register anywhere else is reported as an escape (kind e);
  - a call with a tainted rcx / rdx / r8 / r9 queues the callee with that argument tainted (to --depth); volatile
    registers are killed after the call; a `ret` with rax tainted is reported (kind ret);
  - an access through a tainted register at a displacement D (and, with --width-cover, any access whose width covers
    D) is reported with its kind (r / w) and taint (BASE / ELEM).
With --monotone no taint is ever killed: the walk is linear in address order, so a kill on one path (an epilogue
`pop`) would otherwise hide reads on paths that never ran it. Monotone runs are noisy; type every hit.
LIMITS (SWE2-STRUCT, GR-4/GR-5 record, 2026-09-30): the taint does not keep offsets through `lea r, [T + d]` (an access
[r + D - d] is missed), skips base+index accesses (`[T + r*s + D]`), and does not report 32-bit pointer stores as escapes.
It does not see taint through non-stack memory, returned values into callers, indirect calls' targets, or jumps into
the middle of a function. For an absence claim prefer structflow.py (offset-keeping CFG dataflow); use this as a
cross-check.
"""
import argparse, re, sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import retool as T  # noqa: E402

R, SZ, SC = T.R, T.sizes(), T.scan()
FAM = {}
for fam in (("rax", "eax", "ax", "al", "ah"), ("rbx", "ebx", "bx", "bl", "bh"), ("rcx", "ecx", "cx", "cl", "ch"),
            ("rdx", "edx", "dx", "dl", "dh"), ("rsi", "esi", "si", "sil"), ("rdi", "edi", "di", "dil"),
            ("rbp", "ebp", "bp", "bpl"), ("rsp", "esp", "sp", "spl")):
    for r in fam:
        FAM[r] = fam[0]
for n in range(8, 16):
    for suf in ("", "d", "w", "b"):
        FAM["r%d%s" % (n, suf)] = "r%d" % n
VOL = {"rax", "rcx", "rdx", "r8", "r9", "r10", "r11"}
ARGS = ["rcx", "rdx", "r8", "r9"]
MONOTONE = False   # --monotone: never kill a taint (linear walks cross branches; a kill on one path would hide reads on another)
WID = {"byte": 1, "word": 2, "dword": 4, "qword": 8, "xmmword": 16}
MEM = re.compile(r"(?:(byte|word|dword|qword|xmmword) ptr )?\[(\w+)(?: \+ (\w+)\*(\d+))?(?: ([+-]) (0x[0-9a-f]+|\d+))?\]")


def canon(r):
    return FAM.get(r)


def body(f):
    return list(R.md.disasm(R.at(f, SZ.get(f, 0x400)), f))


def walk(f, init, disps, cover, scale_lea, hits, queue, depth, seen):
    key = (f, tuple(sorted(init.items())))
    if key in seen:
        return
    seen.add(key)
    taint = dict(init)          # reg -> "BASE" / "ELEM"
    stack = {}                  # rsp displacement -> taint
    for i in body(f):
        ops = [o.strip() for o in i.op_str.split(",", 1)]
        d, s = ops[0], (ops[1] if len(ops) > 1 else "")
        m = i.mnemonic
        # accesses through a tainted base
        for side, text in (("w", d), ("r", s)):
            mm = MEM.search(text)
            if not mm:
                continue
            base, idx = canon(mm.group(2)), mm.group(3)
            if base in taint and not idx:
                off = int(mm.group(6), 0) * (1 if mm.group(5) != "-" else -1) if mm.group(6) else 0
                if mm.group(1) is None:
                    continue          # a lea operand is address arithmetic, not an access
                w = WID[mm.group(1)]
                for D in disps:
                    if off == D or (cover and off <= D < off + w):
                        kind = side if m not in ("cmp", "test") else "r"
                        hits.append((f, i.address, kind, taint[base], "%s %s" % (m, i.op_str)))
        if m == "ret" and "rax" in taint:
            hits.append((f, i.address, "ret", taint["rax"], "ret with rax tainted"))
        if m == "call":
            tgt = i.op_str
            if re.match(r"0x[0-9a-f]+$", tgt) and depth > 0:
                a = {r: taint[r] for r in ARGS if r in taint}
                if a:
                    queue.append((int(tgt, 16), a, depth - 1))
            if not MONOTONE:
                for r in list(taint):
                    if r in VOL:
                        del taint[r]
            continue
        cd = canon(d)
        # stack spill / reload; a store of a tainted register anywhere else is an escape (the taint would continue through
        # memory, which this walk does not follow - report it so the claim can name it)
        mm = MEM.search(d)
        if m == "mov" and mm and canon(mm.group(2)) == "rsp" and canon(s) in taint:
            off = int(mm.group(6), 0) if mm.group(6) else 0
            stack[off] = taint[canon(s)]
            continue
        if m == "mov" and mm and mm.group(1) == "qword" and canon(s) in taint and s == canon(s):
            hits.append((f, i.address, "e", taint[canon(s)], "%s %s" % (m, i.op_str)))
            continue
        if cd is None:
            continue
        ms = MEM.search(s)
        new = None
        if m == "mov" and canon(s) in taint:
            new = taint[canon(s)]
        elif m == "mov" and ms and canon(ms.group(2)) == "rsp" and not ms.group(3):
            off = int(ms.group(6), 0) if ms.group(6) else 0
            new = stack.get(off)
        elif m == "lea" and ms:
            b, idx = canon(ms.group(2)), ms.group(3)
            if b in taint:
                new = "ELEM" if (scale_lea and idx) else taint[b]
            elif idx and canon(idx) in taint and scale_lea:
                new = "ELEM"
        elif m == "add" and scale_lea and (cd in taint or canon(s) in taint):
            new = "ELEM"
        if new:
            taint[cd] = new
        elif cd in taint and m not in ("cmp", "test", "push") and not MONOTONE:
            del taint[cd]


def run(seed_load, disps, cover, scale_lea, depth):
    hits, queue, seen = [], [], set()
    seeds = 0
    for f in sorted(SZ):
        try:
            ins = body(f)
        except Exception:
            continue
        for i in ins:
            if i.mnemonic == "mov" and i.op_str.endswith("qword ptr [%s + 0x%x]" % (i.op_str.split(" ptr [")[-1].split(" ")[0], seed_load)) \
                    and i.op_str.startswith(("r",)):
                seeds += 1
                reg = canon(i.op_str.split(",")[0])
                queue.append(("SEED", f, i.address, reg))
    for item in list(queue):
        if item[0] != "SEED":
            continue
        _, f, at, reg = item
        ins = body(f)
        sub = [x for x in ins if x.address > at]
        walk_from(f, sub, {reg: "BASE"}, disps, cover, scale_lea, hits, queue, depth, seen)
    q = [x for x in queue if x[0] != "SEED"]
    while q:
        f, a, dd = q.pop()
        walk(f, a, disps, cover, scale_lea, hits, q, dd, seen)
    return seeds, hits, seen


def run_typed(seeds, disps, cover, depth):
    """seeds: [(func, after_address, reg)] - `reg` holds an element pointer just after `after_address` (ELEM from there)."""
    hits, queue, seen = [], [], set()
    for f, at, reg in seeds:
        walk_from(f, [x for x in body(f) if x.address > at], {canon(reg): "ELEM"}, disps, cover, False, hits, queue, depth, seen)
    while queue:
        f, a, dd = queue.pop()
        walk(f, a, disps, cover, False, hits, queue, dd, seen)
    return hits, seen


def walk_from(f, ins_list, init, disps, cover, scale_lea, hits, queue, depth, seen):
    # same as walk() but over a given instruction tail
    global body
    orig = body
    body = lambda _f, _l=ins_list: _l
    try:
        walk(f, init, disps, cover, scale_lea, hits, queue, depth, seen | set())
    finally:
        body = orig


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed-load", type=lambda x: int(x, 0))
    ap.add_argument("--seed", action="append", default=[], help="FUNC:ADDR:REG - an element pointer in REG after ADDR")
    ap.add_argument("--disp", type=lambda x: int(x, 0), action="append", required=True)
    ap.add_argument("--width-cover", action="store_true")
    ap.add_argument("--scale-lea", action="store_true")
    ap.add_argument("--depth", type=int, default=2)
    ap.add_argument("--monotone", action="store_true", help="never kill a taint - sound for absence claims, noisier")
    a = ap.parse_args()
    MONOTONE = a.monotone
    if a.seed:
        typed = [(int(f, 16), int(x, 16), r) for f, x, r in (s.split(":") for s in a.seed)]
        hits, seen = run_typed(typed, a.disp, a.width_cover, a.depth)
        seeds = len(typed)
    elif a.seed_load is None:
        ap.error("--seed-load or --seed is required")
    else:
        seeds, hits, seen = run(a.seed_load, a.disp, a.width_cover, a.scale_lea, a.depth)
    print("seeds: %d  functions walked: %d" % (seeds, len(set(k[0] for k in seen))))
    for h in sorted(set(hits)):
        print("  %08X %08X %s %-4s %s" % h)
    print("accesses: %d" % len(set(hits)))
