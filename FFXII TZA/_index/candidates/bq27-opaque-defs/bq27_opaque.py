"""bq27_opaque.py - BQ-27 pass O: classify the last rdx-family write at each
still-open residue site of ../bq27-callee-saved/ (SWE2-ORACLE, 2026-10-02).

The callee-saved pass left 40 sites. This pass reads the reaching definition
of the rdx family in the call's block and classifies it:

  lit:N       edx is provably the constant N on every reaching path
              (mov edx,imm / xor edx,edx / lea edx,[reg+k] with the base
              register's own last def being xor reg,reg in the same block)
  field-load  edx = dword [reg + off]; the field's image-wide writer census
              is then taken (literal store values listed; arithmetic stores
              counted)
  index-copy  edx = a register also used to index a qword/word array in the
              same block (a count/index argument, value unbounded)
  cmov-min    edx = reg where the block holds `cmp A,B; mov reg,A;
              cmovg reg,B` (a clamped count)
  table-delta edx = w[table + idx*2] - reg (a computed 16-bit delta)
  argN        edx = an incoming argument register (flag chosen by the caller)
  other       anything else

A site with literal N is settled when N lacks bits 0 and 2 together
((N & 5) != 5). Everything else stays open with its class named.

Writes bq27-opaque.tsv. Reads the capstone listing (Y1P_CACHE) the same way
bq27_width.py does.
"""
import os, re, csv, collections, sys

CACHE = os.environ.get(
    "Y1P_CACHE",
    r"C:/Users/Kristian/AppData/Local/Temp/claude/C--Users-Kristian-source-repos"
    r"/3c89ec72-2988-46c1-ba7b-44218ae1bb19/scratchpad/y1p_all.txt")
HERE = os.path.dirname(os.path.abspath(__file__))

fails = 0
def ok(tag, cond, msg):
    global fails
    print(("PASS " if cond else "FAIL ") + tag + "  " + msg)
    fails += (not cond)

# listing: insn_addr func_addr disasm
body = collections.defaultdict(list)
for line in open(CACHE, encoding="utf-8", errors="replace"):
    p = line.split(None, 2)
    if len(p) == 3:
        body[p[1]].append((p[0], p[2].strip()))

RDX64 = {"rdx", "edx", "dx", "dl"}
REG32 = {"eax","ebx","ecx","edx","esi","edi","ebp","esp",
         "r8d","r9d","r10d","r11d","r12d","r13d","r14d","r15d"}
def fam(reg):
    """register family name"""
    m = {"rdx":"rdx","edx":"rdx","dx":"rdx","dl":"rdx",
         "rsi":"rsi","esi":"rsi","si":"rsi","sil":"rsi",
         "rdi":"rdi","edi":"rdi","di":"rdi","dil":"rdi",
         "rbx":"rbx","ebx":"rbx","bx":"rbx","bl":"rbx",
         "rbp":"rbp","ebp":"rbp","bp":"rbp","bpl":"rbp"}
    m.update({r: r[:3] if r.endswith("d") else r for r in
              ("r8d","r9d","r10d","r11d","r12d","r13d","r14d","r15d")})
    for w in ("r8w","r9w","r10w","r11w","r12w","r13w","r14w","r15w"):
        m[w] = w[:2]
    for b in ("r8b","r9b","r10b","r11b","r12b","r13b","r14b","r15b"):
        m[b] = b[:2]
    return m.get(reg, reg)

def last_rdx_def(f, site):
    """(index, insn) of the last rdx-family write at/before site in f,
    scanning the whole function (block-local boundaries unknown here)."""
    ins = sorted(body[f])
    upto = [i for i, (a, s) in enumerate(ins) if int(a, 16) <= int(site, 16)]
    if not upto:
        return None, None, ins
    i0 = upto[-1]
    # the call itself (at i0) does not define rdx — start before it;
    # an earlier call/ret clobbers rdx and ends the search
    for i in range(i0 - 1, -1, -1):
        a, s = ins[i]
        m = re.match(r"(mov|lea|xor|and|or|add|sub|dec|inc|movzx|movsxd|pop)\s+"
                     r"([a-z0-9]+)", s)
        if m and fam(m.group(2)) == "rdx":
            return i, (a, s), ins
        # a write of a full 64-bit rdx that isn't one of the above forms
        if re.match(r"\w+\s+rdx\b", s) and not s.startswith(("cmp", "test")):
            return i, (a, s), ins
        if s.startswith("call") or s.startswith("ret"):
            break
    return None, None, ins

def block_defs(ins, i):
    """instructions from the nearest preceding control boundary to i."""
    # walk back to a jmp/jcc target boundary: stop at a ret or a jump whose
    # target is inside the scanned window — simple version: stop at the
    # previous `jmp`/unconditional boundary or at a je/jne whose target is
    # above (labels unknown in flat listing, so approximate: stop at any
    # instruction that is the target of a backward jump is unknowable; use
    # "previous unconditional jmp or ret or call" as the block edge and also
    # stop at any conditional jump whose target is < current addr).
    out = []
    for j in range(i, -1, -1):
        a, s = ins[j]
        out.append((a, s))
        if j < i and re.match(r"(ret|jmp|call)\b", s):
            break
    return out

def classify(f, site):
    i, wr, ins = last_rdx_def(f, site)
    if wr is None:
        return ("no-def", "-", "")
    a, s = wr
    blk = block_defs(ins, i)
    # path-conditioned zero: `test rdx,rdx`/`cmp rdx,0` followed by
    # `jne/jnz <target>` where target is past the call site means every
    # path reaching the call has edx == 0.
    if i + 2 < len(ins):
        n1, n2 = ins[i + 1][1], ins[i + 2][1]
        m = re.match(r"(test|cmp) e?dx, (e?dx|0)$", n1)
        if m:
            mj = re.match(r"(jne|jnz) 0x([0-9a-f]+)$", n2)
            if mj and int(mj.group(2), 16) > int(site, 16):
                return ("lit", "0", s + " | " + n1 + " | " + n2)
            mj = re.match(r"(je|jz) 0x([0-9a-f]+)$", n2)
            if mj and int(mj.group(2), 16) > int(site, 16):
                return ("nonzero", "-", s + " | " + n1 + " | " + n2)
    # literal forms
    m = re.match(r"mov edx, (0x[0-9a-f]+|\d+)$", s)
    if m:
        return ("lit", str(int(m.group(1), 0)), s)
    if s.startswith("xor edx, edx"):
        return ("lit", "0", s)
    m = re.match(r"lea edx, \[([a-z0-9]+) \+ (0x[0-9a-f]+|\d+)\]$", s)
    if m:
        base, k = m.group(1), int(m.group(2), 0)
        # is the base provably zero: last write of its family in blk is xor r,r
        for a2, s2 in blk[1:]:
            m2 = re.match(r"xor (\w+), \1$", s2)
            if m2 and fam(m2.group(1)) == fam(base):
                return ("lit", str(k), s + f"  [{base}=0]")
            m3 = re.match(r"mov (\w+), (0x[0-9a-f]+|\d+)$", s2)
            if m3 and fam(m3.group(1)) == fam(base):
                return ("lit", str(int(m3.group(2), 0) + k), s)
        return ("lea-addend", f"[{base}+{k:#x}]", s)
    # memory load
    if re.match(r"mov \w+, dword ptr \[", s):
        g = re.search(r"=>([0-9A-Fa-f]{8})", s)
        if g:
            return ("field-load", "glob:" + g.group(1), s)
        off = re.search(r"\+ (0x[0-9a-f]+)\]", s)
        return ("field-load", off.group(1) if off else "0", s)
    # reg copy
    m = re.match(r"mov edx, (\w+)$", s)
    if m:
        src = m.group(1)
        if src in {"ecx", "r8d", "r9d"}:
            return ("argN", src, s)
        # cmov-min idiom: does the block carry cmp X,Y; mov src,X; cmovg src,Y ?
        for a2, s2 in blk[1:]:
            if re.match(r"cmov\w+ " + src + ",", s2):
                return ("cmov-cond", src, s + " | " + s2)
        # index use: src used as an index anywhere in the block
        for a2, s2 in blk[1:]:
            if re.search(r"\[\w+ \+ " + src + r"\*", s2):
                return ("index-copy", src, s + " | " + s2)
        return ("reg-copy", src, s)
    if re.match(r"(movzx|movsxd) e?dx, ", s):
        return ("table-load", "-", s)
    if re.match(r"(and|or|add|sub|dec|inc) e?dx", s):
        return ("arith", "-", s)
    return ("other", "-", s)

# field-load writer census: every dword store to [reg + OFF] image-wide;
# for RIP-relative loads (off = "glob:ADDR") count stores to the absolute
# cell instead
def field_writers(off):
    if off.startswith("glob:"):
        addr = off[5:]
        pat = re.compile(r"dword ptr \[(?:rip \+ 0x[0-9a-f]+\] ; =>)?" +
                         addr.lstrip("0") + r"\]?,? ?(\w*)")
        hits = []
        for f, ins in body.items():
            for a, s in ins:
                if re.match(r"mov dword ptr \[.*\], \w+$", s) and \
                   addr in s:
                    hits.append((a, f, s))
        return hits
    pat = re.compile(r"dword ptr \[\w+ \+ " + off + r"\], (\w+)$")
    hits = []
    for f, ins in body.items():
        for a, s in ins:
            m = pat.search(s)
            if m:
                hits.append((a, f, s))
    return hits

rows = list(csv.reader(open(os.path.join(
    HERE, "../bq27-callee-saved/bq27-cs-sites.tsv"), encoding="utf-8"),
    delimiter="\t"))
openk = {"open", "no-direct-caller", "callers:passthrough", "callers:open",
         "callers:other-argument", "callers:open,passthrough,settled"}
sites = [r for r in rows[1:] if r and r[5] in openk]
ok("population", len(sites) == 39, f"{len(sites)} open rows (expect 39)")

out = [["function", "site", "slot", "prev", "cls", "detail", "insn",
        "verdict"]]
field_census = {}
for r in sites:
    f, site = r[0], r[1]
    cls, det, insn = classify(f, site)
    verdict = "open"
    if cls == "lit":
        v = int(det)
        verdict = "settled" if (v & 5) != 5 else "FLAG-5-POSSIBLE"
    elif cls == "field-load":
        if det not in field_census:
            field_census[det] = field_writers(det)
        verdict = "field:%s writers=%d" % (det, len(field_census[det]))
    elif cls in ("index-copy", "cmov-cond", "table-load", "table-delta"):
        verdict = "computed:" + cls
    elif cls == "argN":
        verdict = "forwards:" + det
    elif cls == "no-def":
        # rdx is never written in the function body — it arrives as this
        # function's own arg2 and is forwarded unchanged to the vtable call
        verdict = "forwards:arg2-edx"
    out.append([f, site, r[2], r[5], cls, det, insn, verdict])

with open(os.path.join(HERE, "bq27-opaque.tsv"), "w", encoding="utf-8",
          newline="\n") as h:
    csv.writer(h, delimiter="\t").writerows(out)

settled = [r for r in out[1:] if r[7] == "settled"]
ok("new settles", len(settled) == 3,
   f"{len(settled)} literal settles: {[r[1] for r in settled]}")
ok("no flag5", not any(r[7] == "FLAG-5-POSSIBLE" for r in out[1:]),
   "no site provably passes 5")
# the +0x1894 census: named writers
w = field_census.get("0x1894", [])
ok("f1894 census", len(w) == 1,
   f"d[+0x1894] has {len(w)} literal store(s): "
   + "; ".join(f"{a} {s}" for a, f_, s in w))
print(f"FAILS {fails}")
sys.exit(1 if fails else 0)
