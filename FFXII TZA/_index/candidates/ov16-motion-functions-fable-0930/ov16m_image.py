"""ov16m_image.py - OV-16 motion route, image half (research helper for FABLE, 2026-09-30). Read-only.

Part A  what 00268EA0 reads: every call to 0020E600 in it, the footer word read after it (byte D, word k = (D-2)/2,
        the tool's tFuncFooter {u16 count; u16 special[18]}), the bound constant compared with the count word, and the
        record override word read first (O). Then every 003DBBE0 call in it with its channel (r8d), id (r9d),
        5th argument ([rsp+0x20]) and 6th argument ([rsp+0x28], the kind 003DBBF0 stores as (kind << 1) | bit0).
Part B  every raw E8/E9 site of the 003DBBE0 thunk and of 003DBBF0 image-wide, with the last straight-line store to
        [rsp+0x28] (the kind) before it: which callers file kind 4 / 5 entries.
Part C  raw store census for the override words +0xE8 (slot 16) / +0xEA (slot 17): every instruction in every .pdata
        chain root and every uncovered .text run (leaf code) whose memory operand is WRITTEN (capstone access flags) and
        whose byte range [disp, disp+size) meets the window 0xC8..0xF8 (the override array 0xC8 + 2k, k <= 0x11, plus
        the word at 0xF6), any base register; indexed forms are reported whatever the scale. Rows meeting 0xE8..0xEB are
        the candidates. Controls: the indexed writer 0025AFA1 (`mov word [rax+rbx*2+0xc8], di`) and the fixed writer
        0025AD34 (`mov word [rdx+0xf6], r9w`) must both be found.
Part D  the callers of the resolved override writer 0025AF60 and the slot each passes (edx).
"""
import collections, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "rc12-footer-channels-runstate-0930"))
import img  # noqa: E402  (ORACLE's shared helper: PE map, .pdata roots, raw rel32 index)
from capstone import CS_AC_WRITE
from capstone.x86 import X86_OP_MEM, X86_REG_INVALID

ok = True


def partA():
    global ok
    ins = img.fn_ins(0x00268EA0)
    print("PART A: 00268EA0 (%d instructions, %d fragments)" % (len(ins), len(img.fragments(0x00268EA0))))
    for k, x in enumerate(ins):
        if x.mnemonic == "call" and x.op_str == "0x20e600":
            O = C = D = site = None
            for p in ins[max(0, k - 8):k]:
                m = re.match(r"movzx eax, word ptr \[r\w+ \+ (0x[0-9a-f]+)\]$", p.mnemonic + " " + p.op_str)
                if m:
                    O, osite = int(m.group(1), 16), p.address
            for p in ins[k + 1:k + 8]:
                t = p.mnemonic + " " + p.op_str
                m = re.match(r"mov eax, (0x[0-9a-f]+)$", t)
                if m:
                    C = int(m.group(1), 16)
                m = re.match(r"movsx \w+, word ptr \[rcx \+ rbx \+ (0x[0-9a-f]+)\]$", t)
                if m:
                    D, site = int(m.group(1), 16), p.address
                    break
            print("  call %08X  override O=+0x%X (read %08X)  bound C=0x%X  footer D=+0x%X -> k=%d (read %08X)"
                  % (x.address, O, osite, C, D, (D - 2) // 2, site))
    for k, x in enumerate(ins):
        if x.mnemonic == "call" and x.op_str == "0x3dbbe0":
            a = {}
            for p in ins[max(0, k - 14):k]:
                m = re.match(r"dword ptr \[rsp \+ (0x2[08])\], (\w+)$", p.op_str) if p.mnemonic == "mov" else None
                if m:
                    a[m.group(1)] = (m.group(2), p.address)
                m = re.match(r"(r8d|r9d), (\w+)$", p.op_str) if p.mnemonic in ("mov", "lea") else None
                if m:
                    a[m.group(1)] = (p.mnemonic + " " + p.op_str, p.address)
                m = re.match(r"lea (r8d), (\[.*\])$", p.mnemonic + " " + p.op_str)
                if m:
                    a["r8d"] = (p.mnemonic + " " + p.op_str, p.address)
            print("  call %08X  r8d(channel)=%s  r9d(id)=%s  arg5[rsp+0x20]=%s  arg6[rsp+0x28](kind)=%s"
                  % (x.address, a.get("r8d"), a.get("r9d"), a.get("0x20"), a.get("0x28")))


def partB():
    print("\nPART B: every raw call/jmp to the 003DBBE0 thunk or 003DBBF0, with the kind stored at [rsp+0x28]")
    kinds = collections.Counter()
    for tgt in (0x003DBBE0, 0x003DBBF0):
        for a, kind in img.calls_to(tgt):
            f = img.owner(a)
            ins = img.fn_ins(f) if f else img.dis(a - 0x60, 0x65)
            pos = [i for i, x in enumerate(ins) if x.address == a]
            k6 = "?"
            if pos:
                for p in ins[max(0, pos[0] - 20):pos[0]]:
                    if p.mnemonic == "mov" and p.op_str.startswith("dword ptr [rsp + 0x28], "):
                        k6 = "%s @%08X" % (p.op_str.split(", ")[1], p.address)
            kinds[k6.split(" ")[0]] += 1
            print("  %08X %s -> %08X  in %s  kind(arg6)=%s" % (a, kind, tgt, "%08X" % f if f else "?", k6))
    print("  kind operands: %s" % dict(kinds))


def gap_streams():
    cov = sorted((b, e) for b, e, u in img.PDATA)
    gaps, cur = [], img.T0
    for b, e in cov:
        if b > cur:
            gaps.append((cur, b))
        cur = max(cur, e)
    if cur < img.T0 + img.TN:
        gaps.append((cur, img.T0 + img.TN))
    for b, e in gaps:
        pos = b
        while pos < e:
            got = list(img.md.disasm(img.rd(pos, e - pos), pos))
            if not got:
                pos += 1
                continue
            yield ("GAP%08X" % got[0].address, got)
            pos = got[-1].address + got[-1].size
            if pos < e:
                pos += 1


def streams():
    for root in sorted(img.ROOTS):
        try:
            yield ("%08X" % root, img.fn_ins(root))
        except Exception:
            continue
    for name, ins in gap_streams():
        yield (name, ins)


def partC():
    global ok
    print("\nPART C: written memory operands meeting 0xC8..0xF8 (any base; rsp/rbp-frame and rip excluded)")
    hits, nstreams, nins = [], 0, 0
    for name, ins in streams():
        nstreams += 1
        for x in ins:
            nins += 1
            for o in x.operands:
                if o.type != X86_OP_MEM or not (o.access & CS_AC_WRITE):
                    continue
                base = x.reg_name(o.mem.base) if o.mem.base != X86_REG_INVALID else None
                if base in ("rsp", "rip", None):
                    continue
                d, sz = o.mem.disp, max(o.size, 1)
                idx = o.mem.index != X86_REG_INVALID
                if d + sz <= 0xC8 or d > 0xF8:
                    continue
                meets = (d < 0xEC and d + sz > 0xE8) or (idx and d <= 0xEA)
                hits.append((name, x.address, x.mnemonic + " " + x.op_str, d, sz, idx, meets))
        # string stores: rep stos*/movs* whose rdi was formed by `lea rdi, [R + d]` with an `ecx` count before it
        for k, x in enumerate(ins):
            if not (x.mnemonic.startswith("rep stos") or x.mnemonic.startswith("rep movs")):
                continue
            d = n = None
            for p in ins[max(0, k - 10):k]:
                m = re.match(r"rdi, \[(r\w+) \+ (0x[0-9a-f]+)\]$", p.op_str) if p.mnemonic == "lea" else None
                if m and m.group(1) not in ("rsp", "rip"):
                    d = int(m.group(2), 16)
                m = re.match(r"ecx, (0x[0-9a-f]+|\d+)$", p.op_str) if p.mnemonic == "mov" else None
                if m:
                    n = int(m.group(1), 0)
            w = {"b": 1, "w": 2, "d": 4, "q": 8}.get(x.mnemonic[-1], 1)
            if d is not None and n is not None and d <= 0xEA and d + n * w > 0xE8:
                hits.append((name, x.address, "%s (rdi = +0x%X, count %d x %d)" % (x.mnemonic, d, n, w), d, n * w,
                             False, True))
    print("  streams %d, instructions %d, rows in window %d" % (nstreams, nins, len(hits)))
    got = set(h[1] for h in hits)
    for c in (0x0025AFA1, 0x0025AD34, 0x002668B0):
        print("  CONTROL %08X found: %s" % (c, "PASS" if c in got else "FAIL"))
        ok &= c in got
    # functions the actor-record censuses prove take an actor storage record (route-proven accesses, the argument
    # closure, the static getter bases): 04-Actor-Entity/Actor-Storage-Record/*.tsv
    AR = os.path.join(HERE, "..", "..", "..", "04-Actor-Entity", "Actor-Storage-Record")
    proven = set()
    for t in ("actor-storage-record-accesses.tsv", "actor-arg-proven-closure.tsv", "actor-static-proven-bases.tsv"):
        with open(os.path.join(AR, t), encoding="utf-8") as fh:
            next(fh)
            proven |= set(ln.split("\t")[0].upper() for ln in fh if ln.strip())
    cand = [h for h in hits if h[6]]
    print("  rows meeting +0xE8..+0xEB (fixed or string store) or an indexed store with disp <= 0xEA: %d "
          "in %d streams (all rows: ov16m_image_candidates.tsv)" % (len(cand), len(set(h[0] for h in cand))))
    print("  actor-record-proven functions (%d in the three census tables) among them:" % len(proven))
    for name, a, t, d, sz, idx, _ in cand:
        if name in proven:
            print("    %-12s %08X  %-48s disp=0x%X size=%d%s" % (name, a, t, d, sz, " INDEXED" if idx else ""))
    print("  script-VM / actor band 00250000-0026FFFF and 003D0000-003DFFFF (by-hand base verdicts in README):")
    for name, a, t, d, sz, idx, _ in cand:
        if name not in proven and (0x250000 <= a < 0x270000 or 0x3D0000 <= a < 0x3E0000):
            print("    %-12s %08X  %-48s disp=0x%X size=%d%s" % (name, a, t, d, sz, " INDEXED" if idx else ""))
    with open(os.path.join(HERE, "ov16m_image_candidates.tsv"), "w", newline="\n", encoding="utf-8") as w:
        w.write("stream\tsite\tinstruction\tdisp\tbytes\tindexed\tactor_record_proven_fn\n")
        for name, a, t, d, sz, idx, _ in cand:
            w.write("%s\t%08X\t%s\t0x%X\t%d\t%d\t%d\n" % (name, a, t, d, sz, idx, name in proven))
    bysz = collections.Counter((h[5], h[4]) for h in hits)
    print("  window rows by (indexed, bytes): %s" % dict(sorted(bysz.items())))


def partD():
    print("\nPART D: raw callers of the override writer 0025AF60 (slot in edx, value in r9d)")
    for a, kind in img.calls_to(0x0025AF60):
        f = img.owner(a)
        ins = img.fn_ins(f)
        pos = [i for i, x in enumerate(ins) if x.address == a][0]
        pre = ins[max(0, pos - 12):pos]
        print("  %08X %s in %08X:" % (a, kind, f))
        for p in pre:
            if re.match(r"(edx|r9d|r8d|ebx)\b", p.op_str) or "edx" in p.op_str.split(",")[0]:
                print("      %08X  %s %s" % (p.address, p.mnemonic, p.op_str))


if __name__ == "__main__":
    partA()
    partB()
    partC()
    partD()
    print("\nCONTROLS: %s" % ("PASS" if ok else "FAIL"))
    sys.exit(0 if ok else 1)
