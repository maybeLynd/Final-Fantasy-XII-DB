"""nav_population.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only. Independent derivation for
ASTRA-REQ-OPUS-NAV-POPULATION-DOMAINS (_experiments/evidence/nav-population-id-domains/) and ASTRA-REQ-OPUS-NAV-ROOT-CALL-ORDER
(_experiments/evidence/nav-root-clear-call-order/), written without ASTRA's code; corrects three OPUS absence claims.

  G  00383840 is the root getter: mov rax, [02AEDFB0] / ret, and the only one in .text
  P  00392740 (the navigation population builder) - after the ids 0..127 of the pointer list (guard [02AEE0BC] < 0x80 before the
     store at 02AEE0C0 and the increment) - calls the getter (003928E7), keeps the root in r15, and when it is non-null takes
     count = min(unsigned [root+0x24], 0x20) (00392904 mov edx, 0x20 / 00392909 cmp / 0039290C cmovb) and walks 0x20-byte records
     at 0020E600([root+0x28]) (00392920 / 00392924): kind = word [rec+0] (00392929); kind 0: xmm3 = float [rec+0xC]; kind 1:
     xmm3 = max(float [rec+0xC], float [rec+0x10]) (0039293A / 0039293F); then xmm2 = float [rec+8], xmm1 = float [rec+4] and
     00392200(id) with ids from 0x80 (00392917 mov ebx, ebp); any other kind skips the call but the id still advances (0039295C)
  Q  a second consumer at 00391597 decodes [root+0x28] the same way (reached with the root in r13), bounds its index below 0x20,
     and reads the record's kind word and float +4
  C  the absence procedure: the tracked census seeded on the CELL 02AEDFB0 does not reach +0x24; seeded on the GETTER's return
     (census_receiver_fixpoint.py SEED=call 0x383840) it finds 00392909 / 0039290C (+0x24) and 00392920 / 00391597 (+0x28). The old
     'no access' / 'no code reads' claims came from the cell seed alone; the tool's own rule is to union every applicable seed
  O  the area-teardown battery 002341C0 calls Navigation_ClearDataset 00383A20 (mov qword [02AEDFB0], 0) at 002341C9, then the
     opaque 00306570(0) at 002341D0, then the grid teardown 00392710 at 002341D5, with no local branch between: the root clear
     precedes the grid teardown on this path; whether 00306570 rebinds the root is not established
  Not claimed: what the records describe (geometry, radius), the ids' meaning, or any native effect of 00392200.
  S  REGRESSION: the corrected rows and the retyped record are in the store as generated (FAILS before)
Usage: python nav_population.py [--patch]
"""
import hashlib, json, os, re, struct, subprocess, sys, tempfile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__)); DB = os.path.abspath(os.path.join(HERE, "..", "..", "..")); ROOT = os.path.dirname(DB)
d = open(os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe"), "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
B = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [(d[pe + 24 + opt + i * 40:pe + 24 + opt + i * 40 + 8].rstrip(b"\0"),) + struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for nm, vs, va, rs, ro in SECS:
        if B + va <= v < B + va + rs: return v - B - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def at(a):
    x = next(cs.disasm(d[off(a):off(a) + 16], a)); m = re.search(r"rip ([+-]) (0x[0-9a-f]+|\d+)", x.op_str)   # capstone prints small displacements in decimal
    return x.mnemonic, x.op_str, (x.address + x.size + (1 if m.group(1) == "+" else -1) * int(m.group(2), 0)) if m else None
A = lambda pairs: all(at(a)[:2] == v for a, v in pairs)
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
text = next(s for s in SECS if s[0] == b".text"); tlo = B + text[2]
getters = []
for i in range(off(tlo), off(tlo) + text[3] - 8):
    if d[i:i + 3] == b"\x48\x8b\x05" and d[i + 7] == 0xC3 and tlo + i - off(tlo) + 7 + struct.unpack_from("<i", d, i + 3)[0] == 0x2AEDFB0:
        getters.append(tlo + i - off(tlo))
check("G", getters == [0x383840], "root getters: %s" % ["%08X" % g for g in getters])
check("P", A([(0x3927E0, ("lea", "rcx, [rip + 0x275b8d9]")), (0x39285E, ("movsxd", "rax, dword ptr [rip + 0x275b857]")), (0x392865, ("cmp", "eax, ebp")),
              (0x392867, ("jge", "0x3928bf")), (0x39286E, ("mov", "qword ptr [rsi + rax*8], rdi")), (0x3927FF, ("mov", "ebp, 0x80")),
              (0x3928E7, ("call", "0x383840")), (0x3928F4, ("mov", "r15, rax")), (0x392904, ("mov", "edx, 0x20")), (0x392909, ("cmp", "dword ptr [rax + 0x24], edx")),
              (0x39290C, ("cmovb", "edx, dword ptr [rax + 0x24]")), (0x392917, ("mov", "ebx, ebp")), (0x392920, ("mov", "ecx, dword ptr [r15 + 0x28]")),
              (0x392924, ("call", "0x20e600")), (0x392929, ("movzx", "edx, word ptr [rdi + rax]")), (0x392935, ("cmp", "edx, 1")), (0x392938, ("jne", "0x39295c")),
              (0x39293A, ("movss", "xmm3, dword ptr [rcx + 0xc]")), (0x39293F, ("maxss", "xmm3, dword ptr [rcx + 0x10]")), (0x392946, ("movss", "xmm3, dword ptr [rcx + 0xc]")),
              (0x39294B, ("movss", "xmm2, dword ptr [rcx + 8]")), (0x392950, ("movss", "xmm1, dword ptr [rcx + 4]")), (0x392957, ("call", "0x392200")),
              (0x39295C, ("inc", "ebx")), (0x39295E, ("add", "rdi, 0x20"))]),
      "00392740: root +0x24 as an unsigned count capped at 0x20, +0x28 decoded, 0x20-byte records read (kind word, floats +4 +8 +0xC +0x10)")
check("Q", A([(0x39158D, ("cmp", "rsi, 0x20")), (0x391597, ("mov", "ecx, dword ptr [r13 + 0x28]")), (0x39159B, ("call", "0x20e600")),
              (0x3915A3, ("movzx", "edx, word ptr [rax]")), (0x3915B3, ("movss", "xmm0, dword ptr [rax + 4]"))]),
      "00391597: a second reader of +0x28's records (kind word, float +4)")
def census(seed, cell):
    fd, path = tempfile.mkstemp(suffix=".json"); os.close(fd)
    env = dict(os.environ, SEED=seed, EMIT_JSON=path)
    subprocess.run([sys.executable, os.path.join(ROOT, "Tools", "analysis-kit", "gfz-scripts", "census_receiver_fixpoint.py"), cell, "0", "0x30"],
                   env=env, capture_output=True, text=True, timeout=1800)
    j = json.load(open(path)); os.remove(path)
    return {int(k.split(":")[0]): set(v) for k, v in j["sites"].items()}
cell, call = census("cell", "0x2AEDFB0"), census("call", "0x383840")
check("C", 0x24 not in cell and {"00392909", "0039290C"} <= call.get(0x24, set()) and {"00392920", "00391597"} <= call.get(0x28, set()),
      "cell seed reaches +0x24: %s; getter seed: +0x24 %s, +0x28 %s" % (0x24 in cell, sorted(call.get(0x24, [])), sorted(call.get(0x28, []))))
check("O", A([(0x2341C9, ("call", "0x383a20")), (0x2341CE, ("xor", "ecx, ecx")), (0x2341D0, ("call", "0x306570")), (0x2341D5, ("call", "0x392710"))])
      and at(0x383A20)[0] == "mov" and at(0x383A20)[2] == 0x2AEDFB0 and at(0x383A2B)[0] == "ret",
      "002341C0: 00383A20 (root = 0), then 00306570(0), then 00392710, no local branch")
FI = os.path.join(DB, "_types", "fields.tsv"); TY = os.path.join(DB, "_types", "types.tsv")
REC = "_index/candidates/nav-population-opus/nav_population.py"; EXE = "exe 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
TAG = "(OPUS, %s; ASTRA nav-population-id-domains)" % REC
M24 = ("the number of NavTrailerRecord28 records at +0x28: the population builder 00392740 takes min(this, 0x20) as an unsigned count "
       "(00392909 cmp / 0039290C cmovb) and walks that many records. It reaches this block through the root getter 00383840, which the "
       "cell-seeded census did not follow - CORRECTED 2026-09-28 %s P C" % TAG)
TR = [["NavTrailerRecord28", "0x000", "2", "kind", "uint16", "the record's kind word: 00392740 reads it (movzx word, 00392929) and handles kind 0 and kind 1, skipping any other kind while still advancing the id; 00391597's reader also switches on it. What the kinds mean is not claimed", "TYPE RESOLVED", "PROVEN"],
      ["NavTrailerRecord28", "0x002", "2", "unobservedSpan002", "u8[2]", "the two bytes after the kind word; not read", "DISCOVERED", "UNKNOWN"],
      ["NavTrailerRecord28", "0x004", "4", "float04", "float", "passed by 00392740 as the first float argument (xmm1) of 00392200; 00391597 also reads it", "TYPE RESOLVED", "PROVEN"],
      ["NavTrailerRecord28", "0x008", "4", "float08", "float", "passed by 00392740 as the second float argument (xmm2) of 00392200", "TYPE RESOLVED", "PROVEN"],
      ["NavTrailerRecord28", "0x00C", "4", "float0C", "float", "passed by 00392740 as the third float argument (xmm3) of 00392200 for kind 0; for kind 1 the larger of this and +0x10 is passed", "TYPE RESOLVED", "PROVEN"],
      ["NavTrailerRecord28", "0x010", "4", "float10", "float", "read only for kind 1, where 00392740 passes max(+0x0C, +0x10) (maxss) as 00392200's third float argument", "TYPE RESOLVED", "PROVEN"],
      ["NavTrailerRecord28", "0x014", "12", "unobservedSpan014", "u8[12]", "not read by the two readers", "DISCOVERED", "UNKNOWN"]]
def cells(l): return l.rstrip("\r\n").split("\t")
if "--patch" in sys.argv:
    fl = open(FI, "rb").read().decode("utf-8").splitlines(keepends=True); out = []
    for l in fl:
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if c[0] == "NavRunStateBlock" and c[1] == "0x024" and c[3] == "dword0024":
            c[3] = "trailerRecordCount"; c[5] = "~~%s~~ %s" % (c[5], M24); c[6] = "TYPE RESOLVED"
            c[8] += " || CORRECTED 2026-09-28 %s: the 'no access' result was the cell-seeded census only; the getter-seeded census finds 00392909 / 0039290C" % TAG
            out.append("\t".join(c) + e); continue
        if c[0] == "NavRunStateBlock" and c[1] == "0x028" and REC not in c[5]:
            c[5] += (" || MORE CONSUMERS 2026-09-28 %s P Q: the population builder 00392740 (00392920) and the reader at 00391597 decode it through 0020E600 "
                     "after reaching the block through the root getter 00383840 - 'read by 00384160 and its caller set only' held for the cell-seeded census only" % TAG)
            out.append("\t".join(c) + e); continue
        if c[0] == "NavTrailerRecord28" and c[1] in ("0x000", "0x004") and c[3] in ("dword00", "body04"):
            was = "%s %s (%s)" % (c[3], c[4], c[5])
            for r in TR:
                if (c[1] == "0x000" and r[1] in ("0x000", "0x002")) or (c[1] == "0x004" and r[1] not in ("0x000", "0x002")):
                    out.append("\t".join(r + ["RE-CUT 2026-09-28 %s P Q; the old 'no code reads the table' held for the cell-seeded census only. was %s. %s" % (TAG, was, EXE)]) + e)
            continue
        out.append(l)
    open(FI, "wb").write("".join(out).encode("utf-8"))
    tl = open(TY, "rb").read().decode("utf-8").splitlines(keepends=True)
    for i, l in enumerate(tl):
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if c[0] == "NavRunStateBlock" and REC not in c[6]:
            c[6] += (" || CALL ORDER 2026-09-28 (OPUS, %s O; ASTRA nav-root-clear-call-order): on the area-teardown battery 002341C0 the root "
                     "clear 00383A20 (002341C9) precedes the grid teardown 00392710 (002341D5) with no local branch, but the opaque 00306570(0) "
                     "runs between them (002341D0); whether it rebinds the root, and the other callers' order, stay not established" % REC)
            tl[i] = "\t".join(c) + e
        if c[0] == "NavTrailerRecord28" and REC not in c[10]:
            c[10] += " || READ BY CODE 2026-09-28 %s: 00392740 and 00391597 read the records (kind word, floats +4 +8 +0xC +0x10); see the field rows" % TAG
            tl[i] = "\t".join(c) + e
    open(TY, "wb").write("".join(tl).encode("utf-8")); print("patched"); sys.exit(0)
F = {(cells(l)[0], cells(l)[1]): cells(l) for l in open(FI, "rb").read().decode("utf-8").splitlines() if cells(l)[0] in ("NavRunStateBlock", "NavTrailerRecord28")}
T = {cells(l)[0]: cells(l) for l in open(TY, "rb").read().decode("utf-8").splitlines()}
live = lambda s: re.sub(r"~~.*?~~", "", s)
ok = (F.get(("NavRunStateBlock", "0x024"), [0, 0, 0, ""])[3] == "trailerRecordCount" and "No access" not in live(F[("NavRunStateBlock", "0x024")][5])
      and REC in F[("NavRunStateBlock", "0x028")][5]
      and all(F.get(("NavTrailerRecord28", r[1]), [0] * 8)[2:6] == r[2:6] for r in TR)
      and not any("no code reads the table" in live(v[5]) for k, v in F.items() if k[0] == "NavTrailerRecord28")
      and sum(int(v[2]) for k, v in F.items() if k[0] == "NavTrailerRecord28") == 0x20
      and REC in T["NavRunStateBlock"][6] and REC in T["NavTrailerRecord28"][10])
check("S", ok, "the three absence claims corrected, NavTrailerRecord28 retyped from its readers (tiles 0x20), call order recorded")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
