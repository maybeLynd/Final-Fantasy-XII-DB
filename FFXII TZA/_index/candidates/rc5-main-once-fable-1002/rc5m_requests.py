"""rc5m_requests.py - RC-5 residue, part (b) (FABLE, 2026-10-02). Static; shipped bytecode only.

Question: can any shipped script request `main` of an actor again? FABLE's rc5-counter-loops record bounds six
increment-only class-1 counters only if `main` of their actor runs once per image load.

Census, over every .ebp in the shipped VBF (all language copies), of every operation that files a request or replaces
a special-function slot, and of the function each one names:
- REQ-family opcodes 0x21-0x29 (REQ FREQ TREQ REQSW FREQSW TREQSW REQEW FREQEW TREQEW). The submit 00268850 pops the
  function id first (r14d, 00268870-002688AD), then the target (edi, 002688B0-002688D6), then the channel (esi,
  002688D8-0026893F), so the push order is channel, target, function id: the kit decoder's args[0..2].
- REQCHG 0x34. The interpreter pops three values at 002615BD-002615D9 (function id -> r9d, target -> r8d,
  slot -> edx) and calls 0025AF60, which writes override slot `edx` (<= 0x11) of the target. Push order: slot, target,
  function id. NOTE: the kit decoder's NARGS table gives 0x34 seven arguments; this script uses three (the handler's).
- REQALL 0x5F / REQIALL 0x63: the 16-bit operand indexes the payload's list table (header +0x30; section-000 page,
  "REQALL, REQIALL, REQWAITALL"): list = {u32 count; {u16 ordinal; u16 functionId}[count]}. Every pair is a request.
  REQWAITALL 0x61 files nothing; its pairs are counted separately as a control population.
- the verbs sysreq 0x0AA, sysreqall 0x0AB, sysreqf 0x228 (CALL-family immediates). They pop the footer SLOT first
  (`class`, < 0x12), so the slot is the LAST pushed argument; slot 1 is `main` (RC-12 Part B).

Resolution of a target function (RC-12 Part B's method: the image's own name pool, header +0x4C):
  actor   = directory entry `ordinal` (section 000 +0x18, entries 0x30 bytes)
  name    = pool + functionTable[functionId].nameOffset   (entry +0x10: {u32 n; {u32 nameOff; u32 codeOff}[n]})
A request "targets main" when that name is `main` (and, independently, when functionId equals the target's footer
word k = 1). A target with bit 14 set names another manager (`(manager << 16) | ordinal`) and is not resolved here;
a non-constant target or function id is reported as unresolved, with the function id checked against every actor of the
file ("could be main").

Controls (all must PASS):
- R1 RC-12 Part B reproduces over the us copy: 26,390 actors in 1,114 images, footer k = 1 names `main` 6,765 times.
- R2 RC-13's REQCHG census reproduces over the us copy: 1,884 calls; slot 2: 1,804, 3: 14, 4: 8, 5: 8, 16: 24, 17: 26.
- R3 the resolver agrees with the decompiler: for the us copy, every constant (target, function) REQ / REQCHG pair is
  printed as `ACTOR::function`, and the per-file multiset is compared with the decompiled corpus's `sysReq*(.., A::f)`.
- R4 positive: the census finds requests of commonly requested named functions (`talk*` through REQCHG slot 2,
  `logic_main`, `repos_main`), so a zero for `main` is not a blind resolver.
- R5 synthetic: a constructed `PUSHII ch; PUSHII ordinal; PUSHII mainIndex; REQ` against str_z0000's director is
  classified as a request of `main`, through the same functions.

Part (c): for each of the six actors, every function entry of the actor is tested for reaching an increment of the
counter in the control-flow graph of the WHOLE actor (jump table at entry +0x14; FABLE's rc5c_loops.py CFG, copied).
If only `main`'s entry reaches the increments, a request of another function cannot run them.

Outputs: rc5m_requests.out (this report), rc5m_requests.tsv (one row per request that targets an actor of the six
files, plus every request anywhere resolved to `main`).
"""
import collections, io, os, re, struct, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
CORPUS = os.path.join(DB, "..", "Tools", "work", "FABLE", "pub140-scratch", "corpus", "us")
sys.path.insert(0, os.path.join(DB, "25-EBP-Script-Container", "Bytecode-And-Opcodes", "members"))
_cwd = os.getcwd()
os.chdir(os.path.abspath(os.path.join(DB, "..", "..")))
import gen_req_channel_census as G  # noqa: E402
U32 = lambda b, o: struct.unpack_from("<I", b, o)[0]
U16 = lambda b, o: struct.unpack_from("<H", b, o)[0]
S32 = lambda b, o: struct.unpack_from("<i", b, o)[0]
FAILS = []
OUT = []


def say(s=""):
    OUT.append(s)
    print(s)


def check(name, ok, detail=""):
    say(("PASS " if ok else "FAIL ") + name + ((" | " + detail) if detail else ""))
    if not ok:
        FAILS.append(name)


SIX = {("enw_a0580", "読込監督", "class1+0xe98"), ("mnt_c0100", "監督", "class1+0x13"),
       ("rwf_d0100", "監督", "class1+0x13"), ("rwf_d0101", "監督", "class1+0x13"),
       ("rwg_a0181", "監督", "class1+0x20"), ("str_z0000", "監督", "class1+0x2a")}
SIXF = {f for f, _a, _v in SIX}
REQOPS = {0x21: "REQ", 0x22: "FREQ", 0x23: "TREQ", 0x24: "REQSW", 0x25: "FREQSW", 0x26: "TREQSW", 0x27: "REQEW",
          0x28: "FREQEW", 0x29: "TREQEW", 0x34: "REQCHG"}
LISTOPS = {0x5F: "REQALL", 0x63: "REQIALL", 0x61: "REQWAITALL"}
VERBS = {0x0AA: "sysreq", 0x0AB: "sysreqall", 0x228: "sysreqf"}
DECOMP = {0x21: "sysReq", 0x24: "sysReqsw", 0x27: "sysReqew", 0x34: "sysReqchg"}


def cstr(sec, o):
    return sec[o:sec.find(b"\0", o)].decode("cp932", "replace")


def const_of(sec, pool, arg):
    """ORACLE's const_of (rc5b_operands.py), on a resolved producer tuple."""
    name, im, kind = arg
    if kind != "push":
        return None
    if name == "PUSHII":
        return im if im < 0x8000 else im - 0x10000
    if name.startswith("PUSHI") and name[-1].isdigit():
        return int(name[-1])
    if name == "PUSHI":
        try:
            return S32(sec, pool + im * 4 + 4)
        except struct.error:
            return None
    return None


def parse(sec):
    """directory -> list of actors (index = ordinal)."""
    diroff = U32(sec, 0x18)
    cnt = U32(sec, diroff)
    if cnt > 0x400 or diroff + 4 + cnt * 0x30 > len(sec):
        return None
    npool = U32(sec, 0x4C)
    acts = []
    for s in range(cnt):
        en = diroff + 4 + s * 0x30
        ft, lt, sepa = U32(sec, en + 0x10), U32(sec, en + 0x14), U32(sec, en + 0x18)
        nf, nj = U32(sec, ft), U32(sec, lt)
        cntf = U16(sec, sepa)
        acts.append(dict(name=cstr(sec, npool + U32(sec, en)), start=U32(sec, en + 8),
                         fnames=[cstr(sec, npool + U32(sec, ft + 4 + 8 * i)) for i in range(nf)],
                         foffs=[U32(sec, ft + 4 + 8 * i + 4) for i in range(nf)],
                         joffs=[U32(sec, lt + 4 + 4 * i) for i in range(nj)],
                         special=[U16(sec, sepa + 2 + 2 * k) for k in range(min(cntf, 18))],
                         spawn=spawn_lists(sec, sepa)))
    return acts


I16 = lambda b, o: struct.unpack_from("<h", b, o)[0]


def spawn_lists(sec, sepa):
    """00263D40's walk: from the footer {i16 n; i16 w[n]}, skip (sel + 1) count-prefixed lists, then item i.
    Only when the image's first word is above 3 (00263D65). Returns the five lists (entry, spawn, talk, touch,
    respawn) as far as they lie inside the section."""
    if U16(sec, 0) <= 3:
        return None
    out, o = [], sepa
    try:
        o += 2 * (I16(sec, o) + 1)
        for _sel in range(5):
            n = I16(sec, o)
            if n < 0 or o + 2 + 2 * n > len(sec):
                break
            out.append([I16(sec, o + 2 + 2 * i) for i in range(n)])
            o += 2 * (n + 1)
    except struct.error:
        pass
    return out


def resolve(acts, tgt, fid):
    """-> (kind, actor name, function name, main_by_name, main_by_footer)"""
    if tgt is None or fid is None:
        return ("unresolved", None, None, None, None)
    if tgt & 0x8000 or fid & 0x8000:
        return ("abort-bit15", None, None, False, False)
    if tgt & 0x4000:
        return ("other-manager", None, None, None, None)
    if not 0 <= tgt < len(acts):
        return ("ordinal-out-of-range", None, None, False, False)
    a = acts[tgt]
    if not 0 <= fid < len(a["fnames"]):
        return ("function-out-of-range", a["name"], None, False, False)
    fn = a["fnames"][fid]
    return ("resolved", a["name"], fn, fn == "main", len(a["special"]) > 1 and a["special"][1] == fid)


# ---------------------------------------------------------------- walk
verbs = G.load_verbs()
f = io.open(G.VBF, "rb")
names, blocks = G.V.load_index(f)
tot = collections.Counter()
by_kind = collections.Counter()
main_hits = []          # every request resolved to main (by name or by footer k=1)
six_rows = []           # every request whose file is one of the six
fname_tally = collections.Counter()   # resolved function names (all copies), for R4
chg_us = collections.Counter()
partB = dict(images=0, actors=0, main_k1=0)
mine_us = collections.defaultdict(collections.Counter)   # basename -> Counter("A::f" for decompiler-printed forms)
maybe_main = collections.Counter()
maybe_rows = []
d_hits, d_six, d_setup_six, d_items, d_setup = [], [], [], collections.Counter(), [0, 0]
d_names = collections.defaultdict(collections.Counter)
verb_slots = collections.Counter()
unres_all = collections.Counter()
SIXACT = {}             # file path -> (sec, acts) for part (c) and R5
files = 0
for path in sorted(p for p in names if p.lower().endswith(".ebp")):
    try:
        b = G.V.read_entry(f, names, blocks, path)
    except Exception:
        continue
    if len(b) < 0x80 or U32(b, 0x80) != 0x8000000B:
        continue
    sec = b[0x80:0x80 + U32(b, 0x84)]
    acts = parse(sec)
    if acts is None:
        continue
    files += 1
    us = "/us/" in path
    base = path.split("/")[-1][:-4]
    pool = U32(sec, 0x20)
    if us:
        partB["images"] += 1
        partB["actors"] += len(acts)
        for a in acts:
            if len(a["special"]) > 1 and a["special"][1] != 0xFFFF and a["special"][1] < len(a["fnames"]) \
                    and a["fnames"][a["special"][1]] == "main":
                partB["main_k1"] += 1
    if base in SIXF:
        SIXACT[path] = (sec, acts)
    # (d) function ids the engine takes from the image itself
    for oi, a in enumerate(acts):
        fn = a["fnames"]
        for k, w in enumerate(a["special"]):
            if w != 0xFFFF and w < len(fn) and fn[w] == "main" and k != 1:
                d_hits.append((path, a["name"], "footer word k=%d" % k, w))
        for sel, lst in enumerate(a["spawn"] or []):
            d_items[sel] += len(lst)
            for i, w in enumerate(lst):
                if us and 0 <= w < len(fn):
                    d_names[sel][fn[w]] += 1
                if 0 <= w < len(fn) and fn[w] == "main":
                    d_hits.append((path, a["name"], "spawn-table list %d item %d" % (sel, i), w))
        if base in SIXF:
            d_six.append((path, a["name"], fn, a["special"], a["spawn"]))
    so_ord = I16(sec, 0x50)
    if so_ord >= 0 and U32(sec, 0x58):
        lo = U32(sec, 0x58)
        n = U16(sec, lo)
        ids = [I16(sec, lo + 2 + 2 * i) for i in range(n)]
        d_setup[0] += 1
        d_setup[1] += len(ids)
        if so_ord < len(acts):
            for w in ids:
                if 0 <= w < len(acts[so_ord]["fnames"]) and acts[so_ord]["fnames"][w] == "main":
                    d_hits.append((path, acts[so_ord]["name"], "setup spawn-order list (header +0x58)", w))
            if base in SIXF:
                d_setup_six.append((path, acts[so_ord]["name"], [acts[so_ord]["fnames"][w] if 0 <= w < len(
                    acts[so_ord]["fnames"]) else w for w in ids]))
    mainidx = {i for a in acts for i, n in enumerate(a["fnames"]) if n == "main"}
    # list table
    lt_off = U32(sec, 0x30) if len(sec) > 0x34 else 0
    lists = []
    if 0 < lt_off < len(sec):
        nl = U32(sec, lt_off)
        for i in range(min(nl, 0x10000)):
            lo = U32(sec, lt_off + 4 + 4 * i)
            n = U32(sec, lo)
            lists.append([(U16(sec, lo + 4 + 4 * k), U16(sec, lo + 6 + 4 * k)) for k in range(n)])
    starts = sorted(set(a["start"] for a in acts))
    bounds = sorted(set(starts) | {U32(sec, 0x18), len(sec)})
    owner = {}
    for i, a in enumerate(acts):
        owner.setdefault(a["start"], i)
    for start in starts:
        end = min((x for x in bounds if x > start), default=len(sec))
        if start >= len(sec) or end <= start:
            continue
        ins, _ = G.decode(sec[start:end])
        src = acts[owner[start]]["name"]
        for j, (pc, op, imm) in enumerate(ins):
            rows = []
            if op in REQOPS:
                args, st = G.resolve_args(ins, j, 3, verbs)
                if args:
                    lead, tgt, fid = (const_of(sec, pool, x) for x in args)
                else:
                    lead = tgt = fid = None
                selfreq = bool(args) and args[1][0] == "call:getmyid"
                if selfreq:      # verb 0x072 getmyid: the issuer itself
                    tgt = owner[start]
                kind, an, fn, mn, mf = resolve(acts, tgt, fid)
                if selfreq:
                    kind = "self(getmyid)/" + kind
                rows.append((REQOPS[op], lead, tgt, fid, kind, an, fn, mn, mf, st))
                if us and op == 0x34 and args:
                    chg_us[lead] += 1
                if us and op in DECOMP and kind == "resolved":
                    mine_us[base][(DECOMP[op], an + "::" + fn)] += 1
            elif op in LISTOPS:
                for (o, fd) in (lists[imm] if imm < len(lists) else []):
                    kind, an, fn, mn, mf = resolve(acts, o, fd)
                    rows.append((LISTOPS[op], "list%d" % imm, o, fd, kind, an, fn, mn, mf, "ok"))
            elif op in (0x58, 0x59, 0x5D, 0x5E) and imm in VERBS:
                v = verbs.get(imm)
                need = (v[0] if v and v[0] is not None else 1) + (1 if op in (0x59, 0x5E) else 0)
                args, st = G.resolve_args(ins, j, need, verbs)
                slot = const_of(sec, pool, args[-1]) if args else None
                rows.append((VERBS[imm], args and const_of(sec, pool, args[0]), None, slot,
                             "slot" if slot is not None else "unresolved", None,
                             ("slot %s" % slot), slot == 1, slot == 1, st))
            for r in rows:
                form, lead, tgt, fid, kind, an, fn, mn, mf = r[:9]
                tot[form] += 1
                by_kind[(form, kind)] += 1
                if fn:
                    fname_tally[(form, fn)] += 1
                if form in VERBS.values():
                    verb_slots[(form, fid)] += 1
                row = (path, src, "%X" % (start + pc), form, str(lead), str(tgt), str(fid), kind, str(an), str(fn),
                       "1" if mn else "0", "1" if mf else "0", r[9])
                if kind == "unresolved" and form not in VERBS.values():
                    unres_all[(form, "function id constant" if fid is not None else "function id not constant",
                               "target constant" if tgt is not None else "target not constant")] += 1
                    win = ins[max(0, j - 6):j + 1]
                    wtxt = " ".join(G.OPN.get(o, "%02X" % o) + ("" if i is None else ":%X" % i) for _p, o, i in win)
                    # target = PUSHII base; PUSHV v; OPADD  ->  ordinals >= base; which of them have `main` at fid?
                    tb = None
                    if len(win) >= 5 and [o for _p, o, _i in win[-5:-2]] == [0x4F, 0x48, 0x12]:
                        tb = win[-5][2]
                    cands = ([(k, acts[k]["name"]) for k in range(tb or 0, len(acts)) if fid is not None
                              and fid < len(acts[k]["fnames"]) and acts[k]["fnames"][fid] == "main"]
                             if tb is not None else None)
                    if fid is not None and fid in mainidx:
                        maybe_main[form] += 1
                    if us:
                        maybe_rows.append(row + (wtxt, "base %s" % tb if tb is not None else "no base",
                                                 "-" if cands is None else str(cands)))
                if mn or mf:
                    main_hits.append(row)
                if base in SIXF:
                    six_rows.append(row)
os.chdir(_cwd)

say("files %d (all language copies); request-family operations by form: %s" % (files, dict(tot)))
say("sysreq-family verbs by footer slot operand (slot 1 = main): " +
    ", ".join("%s slot %s: %d" % (k[0], k[1], n) for k, n in sorted(verb_slots.items(), key=lambda kv: str(kv[0]))))
say("resolution kinds: " + ", ".join("%s/%s %d" % (k[0], k[1], n) for k, n in sorted(by_kind.items())))

# ---------------------------------------------------------------- controls
check("R1 RC-12 Part B reproduces over the us copy: images 1,114, actors 26,390, footer k=1 -> main 6,765",
      (partB["images"], partB["actors"], partB["main_k1"]) == (1114, 26390, 6765), str(partB))
want = {2: 1804, 3: 14, 4: 8, 5: 8, 16: 24, 17: 26}
check("R2 RC-13 REQCHG census reproduces over the us copy (1,884; slot 2:1804 3:14 4:8 5:8 16:24 17:26)",
      dict(chg_us) == want, "%d calls %s" % (sum(chg_us.values()), dict(sorted(chg_us.items(), key=lambda kv: str(kv[0])))))
# R3: decompiler agreement
CALL = re.compile(r"\b(sysReq(?:sw|ew|chg)?)i?\(\s*[^,()]+?\s*,\s*([^()]*?::[^()]*?)\s*\)")
agree = theirs_n = mine_n = 0
files_cmp = 0
for base, mine in mine_us.items():
    p = os.path.join(CORPUS, base + ".txt")
    if not os.path.exists(p):
        continue
    files_cmp += 1
    theirs = collections.Counter()
    for m in CALL.finditer(open(p, encoding="utf-8", errors="replace").read()):
        theirs[(m.group(1), m.group(2).strip())] += 1
    agree += sum((mine & theirs).values())
    mine_n += sum(mine.values())
    theirs_n += sum(theirs.values())
check("R3 the raw resolver's ACTOR::function agrees with the decompiler for constant REQ/REQSW/REQEW/REQCHG pairs "
      "(us copy, >= 99%)", mine_n > 0 and agree >= 0.99 * mine_n,
      "%d files; %d raw pairs, %d decompiled, %d agree (%.2f%%)" % (files_cmp, mine_n, theirs_n, agree,
                                                                   100.0 * agree / max(1, mine_n)))
talk = sum(n for (form, fn), n in fname_tally.items() if form == "REQCHG" and fn.startswith("talk"))
lm = sum(n for (form, fn), n in fname_tally.items() if fn == "logic_main")
rm = sum(n for (form, fn), n in fname_tally.items() if fn == "repos_main")
mainish = sum(n for (form, fn), n in fname_tally.items() if fn != "main" and "main" in fn)
check("R4 the census finds commonly requested named functions (REQCHG -> talk*, logic_main, repos_main)",
      talk > 0 and lm > 0 and rm > 0, "talk* via REQCHG %d, logic_main %d, repos_main %d, any name containing "
      "'main' other than main %d (all copies)" % (talk, lm, rm, mainish))
# R5 synthetic
sp = [p for p in SIXACT if "/us/" in p and p.endswith("str_z0000.ebp")][0]
ssec, sacts = SIXACT[sp]
so = [i for i, a in enumerate(sacts) if a["name"] == "監督"][0]
smi = sacts[so]["fnames"].index("main")
code = bytes([0x4F, 1, 0, 0x4F, so & 0xFF, so >> 8, 0x4F, smi & 0xFF, smi >> 8, 0x21])
sins, _ = G.decode(code)
sargs, sst = G.resolve_args(sins, 3, 3, verbs)
sres = resolve(sacts, *(const_of(ssec, 0, x) for x in sargs[1:]))
check("R5 synthetic REQ(1, director ordinal %d, function %d) in str_z0000 resolves to main" % (so, smi),
      sres[0] == "resolved" and sres[3] and sres[4], str(sres))

# ---------------------------------------------------------------- result (b)
say("")
say("RESULT (b): requests whose target function is `main` (by name, or by the target's footer word k=1), all copies:")
by_form = collections.Counter(r[3] for r in main_hits)
say("  total %d %s" % (len(main_hits), dict(by_form)))
for r in main_hits[:40]:
    say("    " + " | ".join(r))
say("  unresolved single requests (REQ family, REQCHG), by what is not constant: " +
    ", ".join("%s/%s/%s %d" % (k + (n,)) for k, n in sorted(unres_all.items())))
say("  of these, a constant function id that is the index of some `main` in the same file (could be main): %s"
    % dict(maybe_main))
say("  every unresolved single request in the us copy (file | issuer | site | form | function id | the six "
    "instructions before it | target = constant base + variable? | actors at ordinals >= base whose function at "
    "that id is `main`):")
for r in maybe_rows:
    say("    %s | %s | %s | %s fid %s | %s | %s | %s" % (r[0].split("/")[-1], r[1], r[2], r[3], r[6], r[13], r[14],
                                                      r[15]))
sixc = collections.Counter((r[0].split("/")[-1], r[3], r[7]) for r in six_rows)
say("  requests issued inside the six files, by form and resolution (all copies):")
for k, n in sorted(sixc.items()):
    say("    %-16s %-10s %-22s %d" % (k[0], k[1], k[2], n))
tgt6 = [r for r in six_rows if any(r[0].endswith(fn + ".ebp") and r[8] == an for fn, an, _v in SIX)]
tgt6c = collections.Counter((r[0].split("/")[-1], r[8], r[9]) for r in tgt6)
say("  requests inside the six files that TARGET the counter's actor, by function (all copies):")
for k, n in sorted(tgt6c.items()):
    say("    %-16s %-6s %-24s %d" % (k[0], k[1], k[2], n))
unres6 = [r for r in six_rows if r[7] in ("unresolved", "other-manager")]
say("  unresolved or other-manager requests inside the six files: %d" % len(unres6))
for r in unres6[:20]:
    say("    " + " | ".join(r))

# ---------------------------------------------------------------- part (d): function ids the engine reads from the image
say("")
say("PART (d): function ids the engine files from the image itself (all copies)")
say("  spawn-table items read (lists entry, spawn, talk, touch, respawn): %s; setup spawn-order lists %d with %d ids"
    % (dict(sorted(d_items.items())), d_setup[0], d_setup[1]))
say("  footer words k != 1, spawn-table items and setup spawn-order ids that name `main`: %d" % len(d_hits))
for h in d_hits[:30]:
    say("    %s | %s | %s | function %d" % (h[0].split("/")[-1], h[1], h[2], h[3]))
for path, an, fn, sp, spl in d_six:
    if "/us/" in path and any(path.endswith(f + ".ebp") and an == a for f, a, _v in SIX):
        say("  %-10s %-6s functions %s; footer %s; spawn table %s" % (path.split("/")[-1][:-4], an, fn,
            {k: (fn[w] if w < len(fn) else w) for k, w in enumerate(sp) if w != 0xFFFF}, spl))
for path, an, ids in d_setup_six:
    if "/us/" in path:
        say("  %-10s setup actor %s spawn-order list: %s" % (path.split("/")[-1][:-4], an, ids))
six_main0 = [(p, an) for p, an, fn, sp, spl in d_six if any(p.endswith(f + ".ebp") and an == a for f, a, _v in SIX)
             and fn and fn[0] == "main"]
check("D1 for the six actors, function 0 (filed by index at record start, 00266957) is not `main` in any copy",
      not six_main0 and len([1 for p, an, *_r in d_six if any(p.endswith(f + ".ebp") and an == a for f, a, _v in SIX)]) == 54,
      str(six_main0[:3]))
top = {sel: d_names[sel].most_common(1)[0][0] if d_names[sel] else None for sel in range(5)}
check("D2 the spawn-table walk is aligned: in the us copy the commonest item of lists 0 / 1 / 2 / 4 is entry* / "
      "spawn* / btalk* / respawn* (00263D40's selectors entry, spawn, talk, touch, respawn)",
      str(top[0]).startswith("entry") and str(top[1]).startswith("spawn") and str(top[2]).startswith("btalk")
      and str(top[4]).startswith("respawn"), str(top))

# ---------------------------------------------------------------- part (c): which function entries reach the increments
UNCOND = {0x51, 0x60, 0x5A}
COND = {0x52, 0x53, 0x54, 0x55, 0x56, 0x57, 0x5B, 0x5C}
JMPF = UNCOND | COND
STOP = {0x2D, 0x2E, 0x2F, 0x30}


def build_cfg(ins, joffs):
    """FABLE's rc5c_loops.py build_cfg, copied."""
    pcj = {pc: j for j, (pc, _o, _i) in enumerate(ins)}
    succ = []
    for j, (pc, op, imm) in enumerate(ins):
        s = []
        if op in JMPF:
            t = joffs[imm] if imm < len(joffs) else None
            if t in pcj:
                s.append(pcj[t])
            if op in COND and j + 1 < len(ins):
                s.append(j + 1)
        elif op not in STOP and j + 1 < len(ins):
            s.append(j + 1)
        succ.append(s)
    return succ, pcj


def closure(succ, src):
    seen, st = set(), [src]
    while st:
        x = st.pop()
        if x in seen:
            continue
        seen.add(x)
        st.extend(succ[x])
    return seen


INC = collections.defaultdict(set)
tsv = os.path.join(HERE, "..", "rc5-counter-loops-fable-1002", "rc5c_increments.tsv")
for ln in open(tsv, encoding="utf-8").read().splitlines()[1:]:
    c = ln.split("\t")
    if c[0] == "startscene increment-only":
        INC[(c[1], c[2])].add(int(c[4], 16))
say("")
say("PART (c): function entries of each counter actor from which an increment of the counter is reachable "
    "(whole-actor CFG, all copies)")
pc_ok = True
for path, (sec, acts) in sorted(SIXACT.items()):
    base = path.split("/")[-1][:-4]
    for fb, an, var in sorted(SIX):
        if fb != base:
            continue
        a = [x for x in acts if x["name"] == an][0]
        start = a["start"]
        ends = sorted(set(x["start"] for x in acts) | {U32(sec, 0x18), len(sec)})
        end = min(x for x in ends if x > start)
        ins, _ = G.decode(sec[start:end])
        succ, pcj = build_cfg(ins, a["joffs"])
        incs = {pcj[p] for p in INC[(path, an)] if p in pcj}
        reach = [a["fnames"][i] for i, fo in enumerate(a["foffs"]) if fo in pcj and closure(succ, pcj[fo]) & incs]
        ok = reach == ["main"] and len(incs) == len(INC[(path, an)]) and len(incs) > 0
        pc_ok &= ok
        if "/us/" in path:
            say("  %-10s %-6s %-14s increments %d; functions %d; entries reaching an increment: %s"
                % (base, an, var, len(incs), len(a["fnames"]), reach))
check("C-entry in all 54 copies only `main`'s entry reaches the counter's increments", pc_ok and len(SIXACT) == 54,
      "%d actor copies" % len(SIXACT))

with open(os.path.join(HERE, "rc5m_requests.tsv"), "w", encoding="utf-8", newline="") as w:
    w.write("file\tissuing_actor\tsite\tform\tlead_operand\ttarget\tfunction_or_slot\tresolution\ttarget_actor\t"
            "target_function\tmain_by_name\tmain_by_footer\tdecode_status\n")
    seen = set()
    for r in main_hits + six_rows:
        if r not in seen:
            seen.add(r)
            w.write("\t".join(r) + "\n")
say("")
say("FAILS %d %s" % (len(FAILS), FAILS))
with open(os.path.join(HERE, "rc5m_requests.out"), "w", encoding="utf-8") as w:
    w.write("\n".join(OUT) + "\n")
sys.exit(1 if FAILS else 0)
