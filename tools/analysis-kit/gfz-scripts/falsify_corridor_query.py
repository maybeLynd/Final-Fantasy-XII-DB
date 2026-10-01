"""Falsification pass 1 on CONTRACT-corridor-query-family (OPUS, 2026-09-29), from the shipping image. Killers first.

  K0  section 9 / section 5: the call closure of the five entries is 102 bodies; it contains no generator entry
      (00328370, 00379CD0, 00863BF0, 00863D30, 0018EE20, 0018D740) and no reference to the gameplay LCG cell 022C256C
  K1  (REFUTES section 4 "the family writes no global on any path that returns", and section 5's "nothing global on a
      returning path") RDEC 0032A6E0 stores 16 bytes to the global 022D91B0 (`movdqu` at 0032A735) and returns normally;
      BMASK 003912E0 memsets the buffer behind the global pointer 02AEE0B0 and ORs into it, then returns. The rip-relative
      write census is exactly RDEC's site plus __report_gsfailure's                    KILLER: another rip-relative write
  K2  what K1 does not change for the verdicts: no function in the closure reads 022D91B0, and BMASK clears the whole mask
      on every entry before its first OR, so no verdict carries state from one call to the next. What it does change for
      everyone else: 022D91B0 is an engine-wide 16-byte scratch with many writers and readers, some reading it at entry
  K3  section 2 return literals: BLKCHK's shared exit block 0033601C holds `mov eax, 1` (00336021); GATE's `neg esi / sbb eax, eax / and eax, 2`;
      PVAL's `cmove` at 00335E0D; PATHW's 0033A40B `mov eax, 1 / jmp`
  K4  section 4: BLKCHK loads the mode byte at 00335FB5 and RE-LOADS q[agent + 0x108] before the `mode == 3` test at 00335FEB
  K5  section 2 / 12: PATHW calls QWALK 0033D3E0 five times and VADD 00202B10 (not MXV)
  K6  section 3: GATE reads its identity through `movzx ecx, byte ptr [... + 0xea9]`; the stale-handle null is `cmovne` at
      00358925
  K7  section 10: PVAL's `ucomiss tol, 0` continues on both `jp` and `jne` (NaN proceeds); GATE's GCHK exit at 00335822
      precedes its register saves
"""
import collections, io, os, struct
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_REG_RIP

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
EXE = os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe")
FUNCS = os.path.join(ROOT, "Tools", "work", "graph", "functions.tsv")
blob = io.open(EXE, "rb").read()
pe = pefile.PE(EXE, fast_load=True); BASE = pe.OPTIONAL_HEADER.ImageBase
SECS = [(s.Name.rstrip(b"\0").decode(), BASE + s.VirtualAddress, max(s.Misc_VirtualSize, s.SizeOfRawData), s.PointerToRawData, s.SizeOfRawData)
        for s in pe.sections]
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True
fails = 0


def OFF(va):
    for _n, start, size, raw, rawsz in SECS:
        if start <= va < start + min(size, rawsz):
            return raw + (va - start)
    raise ValueError("VA %08X in no raw section" % va)


def check(tag, ok, text):
    global fails
    fails += not ok
    print("%s  %s  %s" % ("SURVIVES" if ok else "BROKEN  ", tag, text))


sizes, names = {}, {}
for i, line in enumerate(io.open(FUNCS, encoding="utf-8", errors="replace")):
    p = line.rstrip("\n").split("\t")
    if i and len(p) > 2:
        try:
            sizes[int(p[0], 16)] = int(p[2]); names[p[1]] = int(p[0], 16)
        except ValueError:
            pass
S = lambda x: ("%s %s" % (x.mnemonic, x.op_str)).strip()
rip = lambda x: [x.address + x.size + o.mem.disp for o in x.operands if o.type == X86_OP_MEM and o.mem.base == X86_REG_RIP]
T = lambda x: x.operands[0].imm if x.operands and x.operands[0].type == X86_OP_IMM else None
text = next(x for x in SECS if x[0] == ".text")

refs = collections.defaultdict(list)          # target -> [(function, insn)]
calls_to = collections.defaultdict(list)      # target -> [(function, address, mnemonic)]
bodies = {}
for fa in sorted(sizes):
    if not (text[1] <= fa < text[1] + text[2]):
        continue
    try:
        code = blob[OFF(fa):OFF(fa) + sizes[fa]]
    except ValueError:
        continue
    ins = list(md.disasm(code, fa))
    bodies[fa] = ins
    for x in ins:
        for t in rip(x):
            refs[t].append((fa, x))
        if x.mnemonic in ("call", "jmp") and T(x) is not None:
            calls_to[T(x)].append((fa, x.address, x.mnemonic))

STORES = ("mov", "movss", "movsd", "movaps", "movups", "movdqa", "movdqu", "movq", "movd", "inc", "dec", "add", "sub", "or", "and", "xor")


def is_write(x):
    return bool(x.operands) and x.operands[0].type == X86_OP_MEM and x.mnemonic in STORES


def at(fa, va):
    return next(S(x) for x in bodies[fa] if x.address == va)


def run(fa, lo, hi):
    return [S(x) for x in bodies[fa] if lo <= x.address <= hi]


PVAL, GATE, PATHW, BLKCHK, LQUERY = 0x00335B60, 0x003357B0, 0x0033A3D0, 0x00335F90, 0x00391410
RDEC, BMASK, QWALK, GSF = 0x0032A6E0, 0x003912E0, 0x0033D3E0, 0x00809654

# K0 the closure, and no generator in it
seen, st = set(), [PVAL, GATE, PATHW, BLKCHK, LQUERY]
while st:
    f = st.pop()
    if f in seen or f not in bodies:
        continue
    seen.add(f)
    for x in bodies[f]:
        t = T(x) if x.mnemonic in ("call", "jmp") else None
        if t is not None and t in bodies and not (f <= t < f + sizes[f]):
            st.append(t)
GEN = [0x00328370, 0x00379CD0, 0x00863BF0, 0x00863D30, 0x0018EE20, 0x0018D740]
lcg = [f for f, _x in refs[0x022C256C] if f in seen]
check("K0", len(seen) == 102 and not [g for g in GEN if g in seen] and not lcg,
      "closure %d bodies; generator entries in it %s; LCG-cell users in it %s" % (len(seen), [hex(g) for g in GEN if g in seen] or "none", lcg or "none"))
# K1 (REFUTES the no-global-write headline): the rip-relative write census, RDEC's returning store, BMASK's pointer-borne writes
gw = sorted({("%08X" % f, "%08X" % x.address, "%08X" % t) for f in seen for x in bodies[f] if is_write(x) for t in rip(x)})
non_gsf = [g for g in gw if g[0] != "%08X" % GSF]
rb = bodies[RDEC]
bm = bodies[BMASK]
ptr = rip(next(x for x in bm if x.address == 0x00391302))[0]
orp = rip(next(x for x in bm if x.address == 0x003913B1))[0]
retp = rip(next(x for x in bm if x.address == 0x003913E8))[0]
check("K1", non_gsf == [("0032A6E0", "0032A735", "022D91B0")] and at(RDEC, 0x0032A735).startswith("movdqu xmmword ptr [rip")
      and S(rb[-1]) == "ret" and at(BMASK, 0x0039130E) == "call 0x861ec0" and names.get("memset") == 0x00861EC0
      and at(BMASK, 0x003913C4) == "or byte ptr [rdx + rax - 1], cl" and ptr == orp == retp == 0x02AEE0B0 and S(bm[-1]) == "ret"
      and len({g[1] for g in gw if g[0] == "%08X" % GSF}) == 7,
      "rip-relative writes outside __report_gsfailure: %s (RDEC returns: %s); BMASK memsets and ORs through [%08X] and returns it; "
      "__report_gsfailure sites %d" % (non_gsf, S(rb[-1]), ptr, len({g[1] for g in gw if g[0] == "%08X" % GSF})))
# K2 no cross-call state: 022D91B0's readers in the closure, and BMASK's clear before its first OR
rd = sorted({("%08X" % f, "%08X" % x.address) for f, x in refs[0x022D91B0] if not is_write(x)})
rd_in = [r for r in rd if int(r[0], 16) in seen]
wide = [(f, x) for t in range(0x022D91B0, 0x022D91C0) for f, x in refs[t]]
w_fn = {f for f, x in wide if is_write(x)}; r_fn = {f for f, x in wide if not is_write(x)}
at_entry = sorted("%08X" % f for f, x in wide if not is_write(x) and x.address == f)
first_or = min(x.address for x in bm if x.mnemonic == "or" and x.operands[0].type == X86_OP_MEM)
size_cell = rip(next(x for x in bm if x.address == 0x003912F9))[0]
check("K2", not rd_in and first_or > 0x0039130E and len(w_fn) > 1,
      "022D91B0..+0x10 is engine-wide: %d references, %d writing functions, %d reading functions, %d of which read it at their "
      "entry (e.g. %s); none of its readers is in the closure; BMASK's memset (length [%08X]) at 0039130E precedes its first OR at %08X"
      % (len(wide), len(w_fn), len(r_fn), len(at_entry), at_entry[:3], size_cell, first_or))
# K3 literal returns
check("K3", "mov eax, 1" in run(BLKCHK, 0x0033601C, 0x00336021) and any(run(GATE, x.address, x.address + 8)[:3] == ["neg esi", "sbb eax, eax", "and eax, 2"] for x in bodies[GATE])
      and at(PVAL, 0x00335E0D).startswith("cmove") and run(PATHW, 0x0033A40B, 0x0033A410) == ["mov eax, 1", "jmp 0x33a544"],
      "BLKCHK exit 0033601C: %s; GATE neg/sbb/and 2 present; PVAL %s; PATHW %s" % (run(BLKCHK, 0x0033601C, 0x00336021), at(PVAL, 0x00335E0D), run(PATHW, 0x0033A40B, 0x0033A410)))
# K4 the mode byte is re-read
bl = bodies[BLKCHK]
reload = [S(x) for x in bl if x.address < 0x00335FEB and x.address > 0x00335FB5 and "+ 0x108]" in x.op_str]
check("K4", "0x174]" in at(BLKCHK, 0x00335FB5) and "0x174], 3" in at(BLKCHK, 0x00335FEB) and reload,
      "00335FB5 %s; re-load %s; 00335FEB %s" % (at(BLKCHK, 0x00335FB5), reload, at(BLKCHK, 0x00335FEB)))
# K5 PATHW: five QWALK calls, VADD not MXV
pw = [T(x) for x in bodies[PATHW] if x.mnemonic == "call"]
check("K5", pw.count(QWALK) == 5 and 0x00202B10 in pw,
      "QWALK calls %d; VADD 00202B10 called %s" % (pw.count(QWALK), 0x00202B10 in pw))
# K6 identity and stale handle
gi = [S(x) for x in bodies[GATE] if "+ 0xea9]" in x.op_str]
check("K6", any(s.startswith("movzx ecx, byte ptr") for s in gi) and at(0x003588B0, 0x00358925).startswith("cmovne rax"),
      "GATE identity %s; 00358925 %s" % (gi, at(0x003588B0, 0x00358925)))
# K7 NaN tolerance proceeds; GATE's GCHK exit precedes the saves
pv = [S(x) for x in bodies[PVAL]]
k = next(i for i, s in enumerate(pv) if s.startswith("ucomiss xmm7"))   # tol: xmm3 moved to xmm7 at 00335B8F
gt = bodies[GATE]
g_exit = [x for x in gt if x.address == 0x00335822]
saves = [x.address for x in gt if x.mnemonic == "mov" and x.operands[0].type == X86_OP_MEM and "rsp" in x.op_str.split(",")[0]
         and x.op_str.split(", ")[-1] in ("rbx", "rbp", "rsi", "rdi", "r12", "r13", "r14", "r15")]
check("K7", "movaps xmm7, xmm3" in pv[:k] and pv[k + 2].startswith("jp") and pv[k + 3].startswith("jne") and g_exit and (not saves or min(saves) > 0x00335822 or
      any(x.mnemonic == "ret" for x in gt if 0x00335822 <= x.address <= 0x00335830)),
      "PVAL %s / %s / %s; GATE 00335822 %s; first callee-saved spill %s"
      % (pv[k], pv[k + 2], pv[k + 3], S(g_exit[0]) if g_exit else "?", "%08X" % min(saves) if saves else "none"))
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)   # a BROKEN row must fail the process, not only the text (ASTRA feb631dd4, 2026-09-29)
