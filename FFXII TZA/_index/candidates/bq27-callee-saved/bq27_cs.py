"""bq27_cs.py - BQ-27: the 61-site residue of ../bq27-arg-width/, followed through callee-saved registers and one level of
direct callers (FABLE, Claude Opus 5.5, 2026-09-28). Static.

bq27_width.py's reaching-definition pass (F) followed rdx only and treated every call as a clobber. Its residue:
27 sites whose edx is a computed 32-bit value (mostly a copy of esi / edi / ebx) and 34 that pass the enclosing
function's incoming rdx through. This pass:
  V1  follows a copy into edx back through the source register. Under the Windows x64 ABI, rbx, rbp, rsi, rdi and
      r12-r15 survive a call, so a call does not end the search for them (it still ends it for volatile registers).
      A definition is: a literal, a 64-bit write, the function's incoming rcx/rdx/r8/r9 (an argument), or "opaque"
      (a load, arithmetic, or a callee-saved register at entry)
  V2  a site whose every definition is a literal without bits 0 and 2 both set is settled. A site that passes an
      incoming argument other than the second (rcx / r8 / r9) into edx is also listed, because that value is not the
      caller's flag
  V3  for a residue function with direct callers, the value of rdx at every direct call site is taken with the same
      pass. If every caller passes a settled value, the site is settled
  C1  control: V1 reproduces the settled verdict at all 499 sites bq27_width.py's F settles
  C2  control: V1 reproduces "passthrough" (incoming rdx) at every one of the 34 passthrough sites
Writes bq27-cs-sites.tsv.
"""
import os, re, sys, collections
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "../bq27-arg-width/bq27_width.py")
_t = open(SRC, encoding="utf-8").read()
_t = _t.split('with open(os.path.join(HERE, "bq27-sites.tsv")')[0]
_saved = sys.stdout; sys.stdout = open(os.devnull, "w")
_g = {"__file__": SRC, "__name__": "bq27_width_import"}
exec(compile(_t, SRC, "exec"), _g)
sys.stdout.close(); sys.stdout = _saved
body, rows, flows, fam, NOWRITE, IMM = _g["body"], _g["rows"], _g["flows"], _g["fam"], _g["NOWRITE"], _g["IMM"]
fails = 0
def ok(tag, cond, msg):
    global fails
    print(("PASS " if cond else "FAIL ") + tag + "  " + msg); fails += (not cond)
SAVED = {"rbx", "rbp", "rsi", "rdi", "r12", "r13", "r14", "r15"}
ARGS = {"rcx": "arg1", "rdx": "arg2", "r8": "arg3", "r9": "arg4"}
CFG = {}
def cfg(f):
    if f in CFG: return CFG[f]
    ins = sorted((int(a, 16), s) for a, s in body[f]); idx = {a: i for i, (a, s) in enumerate(ins)}
    preds = collections.defaultdict(set)
    for i, (a, s) in enumerate(ins):
        mn = s.split()[0]; m = re.match(r"j\w+ 0x([0-9a-f]+)$", s)
        if m and int(m.group(1), 16) in idx: preds[idx[int(m.group(1), 16)]].add(i)
        if mn not in ("jmp", "ret") and i + 1 < len(ins): preds[i + 1].add(i)
    CFG[f] = (ins, idx, preds); return CFG[f]
def defs_at(f, i0, reg, depth=0):
    """Reaching definitions of register family `reg` just before instruction index i0 of f."""
    ins, idx, preds = cfg(f); out = set(); seen = set(); stack = [(k, reg) for k in preds[i0]]
    if not preds[i0]: out.add(ARGS.get(reg, "opaque-entry") if i0 == 0 else "opaque-pred")
    while stack:
        k, r = stack.pop()
        if (k, r) in seen: continue
        seen.add((k, r)); s = ins[k][1]; mn, ops = (s.split(None, 1) + [""])[:2]
        parts = [x.strip() for x in ops.split(";")[0].split(",")]
        if s.startswith("call"):
            if r not in SAVED: out.add("call-clobber"); continue
        elif mn not in NOWRITE and parts and fam(parts[0]) == r and "[" not in parts[0]:
            src = parts[1] if len(parts) > 1 else ""
            if mn == "xor" and fam(src) == r: out.add(("lit", 0))
            elif mn == "mov" and IMM.fullmatch(src): out.add(("lit", int(src, 0) & 0xFFFFFFFF))
            elif mn == "mov" and fam(src) and depth < 6 and "[" not in src:
                if parts[0] == r and fam(src) == src: out.add("w64")          # a 64-bit copy: pointer-sized
                else: out |= defs_at(f, k, fam(src), depth + 1)
            elif parts[0] == r: out.add("w64")
            else: out.add("opaque")
            continue
        if k == 0: out.add(ARGS.get(r, "opaque-entry")); continue
        if not preds[k]: out.add("opaque-pred"); continue
        stack.extend((p, r) for p in preds[k])
    return out
def safe(ds): return bool(ds) and all(d == "w64" or (isinstance(d, tuple) and (d[1] & 5) != 5) for d in ds)
def verdict(ds):
    if safe(ds): return "settled"
    if ds == {"arg2"} or (ds and ds <= {"arg2", "w64"} | {d for d in ds if isinstance(d, tuple) and (d[1] & 5) != 5} and "arg2" in ds): return "passthrough"
    if "call-clobber" in ds: return "no-second-argument"
    if ds & {"arg1", "arg3", "arg4"} and not ds - ({"arg1", "arg3", "arg4", "w64"} | {d for d in ds if isinstance(d, tuple)}): return "other-argument"
    return "open"
res = {}
for r in rows:
    f, a = r[0], r[1]; ins, idx, preds = cfg(f)
    res[(f, a)] = defs_at(f, idx[int(a, 16)], "rdx")
v = {k: verdict(ds) for k, ds in res.items()}
settledF = [k for k, fl in flows.items() if fl == "flow-settled"]
ok("C1", all(v[k] == "settled" for k in settledF), "the %d sites F settles are settled here too (%s)" % (len(settledF), collections.Counter(v[k] for k in settledF)))
pt = [k for k, fl in flows.items() if fl == "residue-passthrough"]
ok("C2", all(v[k] in ("passthrough", "settled") for k in pt), "the %d passthrough sites: %s" % (len(pt), collections.Counter(v[k] for k in pt)))
resid = [k for k, fl in flows.items() if fl in ("residue-passthrough", "residue-computed")]
vc = collections.Counter(v[k] for k in resid)
ok("V1", len(resid) == 61, "the 61 residue sites, followed through callee-saved registers: %s" % dict(vc))
# V3: one level of direct callers for passthrough sites
callers = collections.defaultdict(list)
for f, ins in body.items():
    for a, s in ins:
        m = re.match(r"(call|jmp) 0x([0-9a-f]+)$", s)
        if m: callers["%08X" % int(m.group(2), 16)].append((f, a))
up = {}
for k in resid:
    if v[k] != "passthrough": continue
    cs = callers.get(k[0], [])
    if not cs: up[k] = "no-direct-caller"; continue
    vs = []
    for cf, ca in cs:
        ins, idx, preds = cfg(cf); vs.append(verdict(defs_at(cf, idx[int(ca, 16)], "rdx")))
    up[k] = "settled-by-callers" if all(x == "settled" for x in vs) else "callers:" + ",".join(sorted(set(vs)))
uc = collections.Counter(up.values())
ok("V3", sum(uc.values()) == vc["passthrough"], "passthrough sites by their direct callers: %s" % dict(uc))
final = {}
for k in resid:
    final[k] = "settled" if v[k] == "settled" or up.get(k) == "settled-by-callers" else (up.get(k) or v[k])
THIRD = {}
# V4: a third argument written in the call's own block and not read again before the call. r8 / r9 are volatile, so
# such a write is dead unless it is an argument: the slot's method takes three or more parameters, so it is not a
# deleting destructor (this, unsigned flags)
last_write = _g["last_write"]
R89 = re.compile(r"\b(r8|r8d|r8w|r8b|r9|r9d|r9w|r9b)\b")
def third_arg(f, a):
    ins = sorted(body[f]); i = next(k for k, (x, y) in enumerate(ins) if x == a)
    for reg in ("r8", "r9"):
        k = last_write(ins, i, reg)
        if k is not None and not any(R89.search(y.split(";")[0]) for x, y in ins[k + 1:i]): return reg + ": " + ins[k][1]
    return None
# controls: the deleting-destructor bodies (bit-0 test, bit-4 test and the 0016D6A0 call in their head) never read r8 / r9
# before writing them, and no direct call to one writes r8 / r9 in its block
dd = [f for f, ins in body.items() if any(re.match(r"test (dil|bl|sil|bpl|r1[2-5]b), 1$", y) for x, y in sorted(ins)[:40])
      and any(re.match(r"test (dil|bl|sil|bpl|r1[2-5]b), 4$", y) for x, y in sorted(ins)[:60]) and any(y == "call 0x16d6a0" for x, y in ins)]
def reads_r89_first(f):
    for x, y in sorted(body[f]):
        ops = (y.split(None, 1) + [""])[1].split(";")[0]; parts = [q.strip() for q in ops.split(",")]
        if R89.search(",".join(parts[1:])) or (parts and "[" in parts[0] and R89.search(parts[0])): return True
        if parts and R89.fullmatch(parts[0] or "") : return False
        if y.startswith(("call", "ret", "jmp")): return False
    return False
dset = set(dd); ddc = [(f, a) for f, ins in body.items() for a, y in ins if re.match(r"(call|jmp) 0x([0-9a-f]+)$", y) and "%08X" % int(y.split("0x")[1], 16) in dset]
ok("C3", reads_r89_first("00623C10") and len(dd) > 1000 and not [f for f in dd if reads_r89_first(f)] and ddc and not [k for k in ddc if third_arg(*k)],
   "control: the check flags 00623C10 (reads r8 at 00623C23); %d deleting-destructor bodies, none reads r8/r9 before writing it; %d direct calls to them, none writes r8/r9 in its block"
   % (len(dd), len(ddc)))
for k in resid:
    if final[k] != "settled":
        t = third_arg(*k)
        if t: final[k] = "three-parameter-method"; THIRD[k] = t
fc = collections.Counter(final.values())
settled_now = sum(n for k2, n in fc.items() if k2 in ("settled", "three-parameter-method"))
print("V2  residue after this pass: %s" % dict(fc))
print("T   settled: 546 (bq27_width.py) + %d here = %d of 607; residue %d" % (settled_now, 546 + settled_now, 61 - settled_now))
with open(os.path.join(HERE, "bq27-cs-sites.tsv"), "w", encoding="utf-8", newline="\n") as h:
    h.write("function\tsite\tslot\tfirst_pass\tdefinitions\tthis_pass\tthird_argument\n")
    for r in rows:
        k = (r[0], r[1])
        if k in final:
            ds = ";".join(sorted(str(d) if not isinstance(d, tuple) else "lit%#x" % d[1] for d in res[k]))
            h.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (r[0], r[1], r[2], flows[k], ds, final[k], THIRD.get(k, "-")))
print("FAILS", fails); sys.exit(1 if fails else 0)
