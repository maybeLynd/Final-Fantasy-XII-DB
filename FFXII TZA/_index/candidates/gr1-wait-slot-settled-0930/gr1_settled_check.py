"""gr1_settled_check.py - GR-1: is the ActorWaitSlot +0x27 `settled` byte read anywhere? (OPUS, 2026-09-30)
Static, the certified image, via Database/Tools/analysis-kit/gfz-scripts/retool.py and structflow.py (the kit's
offset-keeping CFG dataflow, generalised from SWE2-STRUCT's rowflow.py).

S1  every qword load of [X + 0xA8] whose loaded register is then used as an indexed base: the ones with a 0x28 stride
    (index formed as lea i, [j + j*4], then *8) are exactly the seven wait-slot functions; the rest index a different
    stride or a stack slot.
S2  no indexed access through such a base covers +0x27.
S3  structflow from those seven functions (the +0xA8 load is the array base, stride 0x28, depth 3): the accesses whose
    width covers slot +0x27 are exactly the two sets and ten clears; no access at an unknown offset, no escape, no copy;
    the only indirect calls handed a slot pointer are the three native-command handler calls in 002621D0, each with
    r8 = slot + 0x18.
S4  those handlers come from the five static command tables 003DC2D0 installs (1,960 commands). Entered with
    r8 = slot + 0x18 (depth 2), 46 handlers touch the window covering +0x27 - a dword at r8 + 0xC (slot +0x24..+0x27) or
    a qword at r8 + 8 (slot +0x20..+0x27): handler scratch. Every read of it (22 sites, 38 command-reads, 26 commands) has a covering write
    in its command's begin handler or earlier in the same handler; no unknown offset, no escape.
S5  the four indirect calls the handlers hand r8 to are a debug printf (0017D280, r8 a variadic argument) and a widget
    callback (00244F00 -> call [rcx], which takes rcx / rdx; r8 is a stale register there).
Positive control: S3 finds the twelve known writes; S4 finds the begin/poll pairs the native-command contract names.
Prints PASS/FAIL per check and FAILS n last.
"""
import os, re, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import retool as T  # noqa: E402
import structflow as S  # noqa: E402

R, SZ, c = T.R, T.sizes(), T.scan()
fails = 0
W = {"byte": 1, "word": 2, "dword": 4, "qword": 8, "xmmword": 16}


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def txt(a):
    i = next(R.md.disasm(R.at(a, 16), a, 1))
    return ("%s %s" % (i.mnemonic, i.op_str)).strip()


def drain(g):
    while g.q:
        f = g.q.pop()
        dp, ent = g.entry[f]
        g.walk(f, ent, dp)


# S1 / S2 - the image-wide shape census
stride28, other, cover = set(), {}, []
for f in sorted(SZ):
    try:
        ins = list(R.md.disasm(R.at(f, SZ[f]), f))
    except Exception:
        continue
    for k, i in enumerate(ins):
        if not (i.mnemonic == "mov" and re.match(r"r\w+, qword ptr \[\w+ \+ 0xa8\]$", i.op_str)):
            continue
        reg = i.op_str.split(",")[0]
        five = {m.group(1) for j in ins[max(0, k - 10):k + 14]
                for m in [re.match(r"(\w+), \[(\w+) \+ \2\*4\]$", j.op_str)] if m and j.mnemonic == "lea"}
        for j in ins[k + 1:k + 25]:
            dst = j.op_str.split(",")[0]
            if re.match(r"%s\b" % reg, dst) and j.mnemonic in ("mov", "lea", "xor", "pop", "movzx", "movsxd") \
                    and "[%s" % reg not in j.op_str.split(",", 1)[-1]:
                break
            m = re.search(r"\[%s \+ (\w+)\*(\d)(?: \+ (0x[0-9a-f]+|\d+))?\]" % reg, j.op_str)
            if not m:
                continue
            if m.group(2) == "8" and m.group(1) in five:
                stride28.add(f)
            else:
                other.setdefault(f, "%08X %s %s" % (j.address, j.mnemonic, j.op_str))
            d = int(m.group(3), 0) if m.group(3) else 0
            w = re.search(r"(byte|word|dword|qword|xmmword) ptr", j.op_str)
            if w and d <= 0x27 < d + W[w.group(1)]:
                cover.append("%08X" % j.address)
WAIT_FNS = {0x0025B400, 0x0025DF00, 0x0025E4C0, 0x002651A0, 0x0026B4C0, 0x0026B4E0, 0x003DBDC0}
check("S1", stride28 == WAIT_FNS, "stride-0x28 users of a +0xA8-loaded base: %s; other indexed uses: %s"
      % (" ".join("%08X" % x for x in sorted(stride28)), "; ".join("%08X %s" % kv for kv in sorted(other.items()))))
check("S2", cover == [], "indexed accesses through a +0xA8-loaded base covering +0x27: %d" % len(cover))

# S3 - structflow from the seven functions
SETS = {0x0025E04F, 0x0025E07A}
CLEARS = {0x0025F5CC, 0x0025F92B, 0x0025FD02, 0x002600D9, 0x00260439, 0x002607FC, 0x00260BBF, 0x00260EF7, 0x00261147,
          0x00261592}
g = S.Flow([0x27], 3, stride=0x28, slot=0, seed_loads={(f, 0xA8) for f in WAIT_FNS})
g.run(sorted(WAIT_FNS))
acc = {h[1]: h for h in g.hits}
ind = sorted((f, a, t) for f, a, t, _ in g.indirect)
r8s = all("('E', 24)" in a for _, _, _, a in g.indirect)
check("S3", set(acc) == SETS | CLEARS and all(acc[a][2] == "w" for a in acc) and not g.unk and not g.esc and not g.copies
      and [(f, a) for f, a, _ in ind] == [(0x002621D0, 0x00262278), (0x002621D0, 0x002622DB), (0x002621D0, 0x002622F8)]
      and r8s and all(txt(a - 0xA) == "lea r8, [rdi + 0x18]" or txt(a - 0xF) == "lea r8, [rdi + 0x18]"
                      or txt(a - 0x12) == "lea r8, [rdi + 0x18]" for a in (0x00262278, 0x002622DB, 0x002622F8)),
      "%d functions walked; +0x27 covered only by 2 sets + 10 clears; unknown %d, escapes %d, copies %d; indirect %s"
      % (len(g.entry), len(g.unk), len(g.esc), len(g.copies), ["%08X" % a for _, a, _ in ind]))

# S4 - the native command handlers, entered with r8 = slot + 0x18
q = lambda a: struct.unpack("<Q", R.at(a, 8))[0]
d32 = lambda a: struct.unpack("<i", R.at(a, 4))[0]
TBL = {0: 0x01EED700, 3: 0x01F281B0, 5: 0x01F29418, 7: 0x01F29440, "def": 0x01F26720}
lea_tbl = {txt(0x003DC2D5).endswith("]"), txt(0x003DC2E8) == "rep stosq qword ptr [rdi], rax"}
cmds = []
for fam, tbl in TBL.items():
    for N in range(d32(tbl)):
        b, p, r = (q(tbl + 32 * N + o) for o in (8, 0x10, 0x20))
        cmds.append((fam, N, b if b in SZ else None, p if p in SZ else None, r if r in SZ else None))
H = sorted({h for cm in cmds for h in cm[2:] if h})
per, unk, esc, indirect = {}, 0, 0, set()
for h in H:
    gh = S.Flow([0x27], 2, stride=0x28, slot=0)
    gh.enqueue(h, {"r8": {("E", 0x18)}}, 2)
    drain(gh)
    per[h] = sorted(gh.hits, key=lambda x: x[1])
    unk += len(gh.unk)
    esc += len(gh.esc)
    indirect |= {(f, a) for f, a, _, _ in gh.indirect}
rd = lambda h: [x for x in per[h] if x[2] == "r"] if h else []
wr = lambda h: [x for x in per[h] if x[2] == "w"] if h else []
reads, sites, uncovered, cmdset = 0, set(), [], set()
for fam, N, b, p, r in cmds:
    for h in (b, p, r):
        for x in rd(h):
            reads += 1
            sites.add(x[1])
            cmdset.add((fam, N))
            if not (wr(b) or [y for y in wr(h) if y[1] < x[1]]):
                uncovered.append("%s/%d %08X" % (fam, N, x[1]))
touch = sum(1 for h in H if per[h])
check("S4", len(cmds) == 1960 and len(H) == 1886 and touch == 46 and len(sites) == 22 and reads == 38 and len(cmdset) == 26
      and uncovered == [] and unk == 0 and esc == 0,
      "%d commands / %d handlers; %d touch the +0x20..+0x27 scratch; %d read sites (%d command-reads) in %d commands, uncovered %s; "
      "unknown %d, escapes %d" % (len(cmds), len(H), touch, len(sites), reads, len(cmdset), uncovered or "none", unk, esc))
# S5 - the handlers' indirect calls
check("S5", indirect == {(0x0017D280, 0x0017D2A8), (0x00244F00, 0x00244F34)}
      and txt(0x0017D28A) == "mov qword ptr [rsp + 0x18], r8" and txt(0x0017D2A3) == "mov ecx, 1"
      and txt(0x00244F25) == "mov rax, qword ptr [rcx]" and txt(0x00244F2D).startswith("lea rdx, [rip"),
      "indirect calls handed r8: %s (debug printf vararg; widget callback on rcx / rdx)"
      % ["%08X@%08X" % x for x in sorted(indirect)])
print("FAILS %d" % fails)
