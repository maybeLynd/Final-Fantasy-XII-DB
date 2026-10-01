"""sd81_callers.py - SD-81: what the 99 callers of the EASTL red-black tree build with it. SWE2-ORACLE, 2026-09-30.
Static. Reads only the certified image (SHA-256 73461d08...21f8); writes nothing but stdout and, with --tsv PATH, the
per-caller table.

Question (register SD-81, page 24-Compiler-And-CRT-Runtime/Cxx-Runtime-Families/the-ordered-container-runtime.md):
which container and value type each of the 99 callers of the six EASTL rbtree bodies keeps, and which wrappers sit
between the callers and the six bodies.

Method.
  A  census: every direct call/jmp to the six bodies (retool.scan(), v4 extents), compared to the page's published
     enumeration members/ordered-container-runtime-callers.tsv (99 callers, 170 pairs, 213 sites, 6 signatures).
  B  per caller, a forward value-set dataflow over the caller's own control flow (rc9_channels' decoder and CFG; values
     are an entry register + offset, a constant address, one qword load "[x+k]", or a call result "call@site"). It
     records at each site: the insert's node (rcx) / parent (rdx) / header (r8) and the erase's header (rdx); the
     allocate virtual (call [vt+0x10], edx = size, rcx = tree+0x30) whose result reaches the insert's node; the
     deallocate virtual (call [vt+0x18], r8 = size, rcx = tree+0x30); every store into the fresh node and every call
     made on node+d (the value); every compare against [node+0x20..] with the condition that consumes it; the
     "reject" store `mov byte [ret+8], 0` into the hidden pair<iterator,bool> return (rdx at entry).
  C  node-construction helpers (a call whose result is the insert's node) are read the same way for their allocate.
  D  roles from the body, not from the name: insert-unique (dec + ins; the EASTL DoInsertValue/DoInsertKey shape: a
     descent, --position, compare with the predecessor, reject path), insert-hint (inc + ins; validates a position with
     ++, falls back to an insert-unique), insert-at (ins only; the parent is the caller's position argument r8),
     erase (inc + era, inline in the owning code), walk (inc only), member (0016DA60).
  E  where the tree header lives: the tree = header - 8 (the header, EASTL's mAnchor, is what the insert/erase receive);
     for walks, begin() = [tree + 0x10]; the allocator sits at tree + 0x30 and the size at tree + 0x28. The tree
     expression is carried up through the direct callers (at most 3 levels) to a global, to a getter's returned global,
     or to `this` of a virtual method whose vtable slot gives the RTTI class.
  F  the construction tags: every lea of the EASTL default allocator names "EASTL map" (008F4120) and "EASTL set"
     (008F3CB0) is followed to the allocator it names at tree + 0x30, which gives the container template (map / set)
     for that constructed tree; matched to callers' trees when both resolve to the same global or the same
     class + offset.
  G  instantiation groups: insert-family functions joined by their call edges (hint -> unique, hint -> insert-at) and
     shared node helpers; each group's node size, key compare and value layout; erase / walk callers joined to a group
     when they share its tree (same global / class + offset) or, as INFERENCE only, when node size and key compare
     match exactly one group.

Controls (must hold): the census reproduces the published 99 / 170 / 213 and every caller's signature and site count;
the allocate-site census reproduces OC-2's nine node sizes with their per-size site counts (80 allocating sites);
positive control: the font page's `.ker` store 001FDC10 -> 001FC9F0 is a map keyed by a signed 32-bit dword at
node+0x20 with 0x28-byte nodes at font+0x70 (font-data-kerning-and-expansion.md section 3) - the census must read the
same key width, signedness, node size and header offset without being told.

Everything labelled INFERENCE is a reading beyond the bytes (template names, map-vs-set where no tag reaches the tree).
"""
import collections, hashlib, io, os, re, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))           # .../Database
FF = os.path.join(DB, "FFXII TZA")
sys.path.insert(0, os.path.join(DB, "Tools", "analysis-kit", "gfz-scripts"))
import retool  # noqa: E402
import capstone  # noqa: E402
from capstone import x86 as X  # noqa: E402

R = retool.R
AUTH = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
M = {0x16D6D0: "inc", 0x16D720: "dec", 0x16D780: "rotL", 0x16D7E0: "rotR", 0x16D840: "ins", 0x16DA60: "era"}
ALLOC_CTOR = 0x001EDF00            # eastl::allocator_memory_log ctor (EASTL page key-address table)
MEMCMP = 0x00861ED2                # memcmp import thunk (functions.tsv name)
TAGS = {0x008F4120: "EASTL map", 0x008F3CB0: "EASTL set"}
FAILS = 0


def check(name, ok, detail=""):
    global FAILS
    print(("PASS " if ok else "FAIL ") + name + (" - " + detail if detail else ""))
    if not ok:
        FAILS += 1


def h8(a):
    return "%08X" % a


# ---------------------------------------------------------------- the tracker
# Values: frozensets of (base, offset). base None = a constant (an address when >= 0x100000); "reg@e" = that register
# at the function's entry (rsp@e is the entry stack pointer, so a stack local is rsp@e + k); "[x]" = the qword loaded
# from address x (one level, nested at most three deep); "call@SITE" = the value a call returned. Stack slots written
# at rsp@e + k are tracked as ("S", k) so a spilled register reloads as itself. UNK = not tracked.
UNK = None
GP = list(R.GP) + ["rsp"]
VOL = R.VOLATILE
MAXSET = 8


def full(rid):
    if rid == X.X86_REG_RSP:
        return "rsp", 8
    if rid == X.X86_REG_ESP:
        return "rsp", 4
    return R.full(rid)


def const_set(v):
    return v is not UNK and all(b is None for b, _ in v)


def vadd(v, k):
    return UNK if v is UNK else frozenset((b, o + k) for b, o in v)


def join(a, c):
    if a is UNK or c is UNK:
        return UNK
    u = a | c
    return UNK if len(u) > MAXSET else u


def sym(b, o):
    if b is None:
        return h8(o) if o >= 0x100000 else hex(o)
    return b if o == 0 else "%s%+#x" % (b, o)


def load_of(v):
    if v is UNK or len(v) != 1:
        return UNK
    (b, o), = v
    if b is not None and (b.count("[") >= 3 or b == "rsp@e"):
        return UNK
    return frozenset([("[%s]" % sym(b, o), 0)])


def memval(st, i, m):
    if m.index != 0:
        return UNK
    if m.base == X.X86_REG_RIP:
        return frozenset([(None, i.address + i.size + m.disp)])
    br, _ = full(m.base)
    if br is None:
        return UNK
    return vadd(st.get(br, UNK), m.disp)


def single(v):
    return next(iter(v)) if v is not UNK and len(v) == 1 else None


def slot(v):
    """the tracked stack slot a single rsp@e-relative address names."""
    if v is not UNK and len(v) == 1:
        (b, o), = v
        if b == "rsp@e":
            return ("S", o)
    return None


def step(st, i):
    st = dict(st)
    mn, ops = i.mnemonic, i.operands
    if mn == "call":
        for r in VOL:
            st[r] = UNK
        st["rax"] = frozenset([("call@%08X" % i.address, 0)])
        sp = single(st.get("rsp", UNK))
        if sp and sp[0] == "rsp@e":       # the callee owns its 0x20-byte home area above the return address
            for k in [k for k in st if isinstance(k, tuple) and sp[1] <= k[1] < sp[1] + 0x20]:
                del st[k]
        return st
    if mn == "push" and ops:
        sp = vadd(st.get("rsp", UNK), -8)
        st["rsp"] = sp
        sl = slot(sp)
        if sl:
            st[sl] = st.get(full(ops[0].reg)[0], UNK) if ops[0].type == X.X86_OP_REG else UNK
        return st
    if mn == "pop" and ops:
        sl = slot(st.get("rsp", UNK))
        r = full(ops[0].reg)[0] if ops[0].type == X.X86_OP_REG else None
        if r:
            st[r] = st.get(sl, UNK) if sl else UNK
        st["rsp"] = vadd(st.get("rsp", UNK), 8)
        return st
    if not ops:
        return st
    try:
        _, wr = i.regs_access()
    except capstone.CsError:
        wr = []
    written = {full(r)[0] for r in wr if full(r)[0]}
    d = ops[0]
    dr, dw = full(d.reg) if d.type == X.X86_OP_REG else (None, 0)
    s = ops[1] if len(ops) > 1 else None
    new = {}
    if d.type == X.X86_OP_MEM:                           # a store: track qword spills into stack slots
        sl = slot(memval(st, i, d.mem))
        if sl:
            if mn == "mov" and s is not None and s.type == X.X86_OP_REG and d.size == 8:
                st[sl] = st.get(full(s.reg)[0], UNK)
            else:
                st.pop(sl, None)
    if dr and s is not None:
        if mn == "mov" and s.type == X.X86_OP_IMM:
            new[dr] = frozenset([(None, s.imm & (0xFFFFFFFF if dw == 4 else (1 << 64) - 1))]) if dw >= 4 else UNK
        elif mn == "mov" and s.type == X.X86_OP_REG:
            v = st.get(full(s.reg)[0], UNK)
            new[dr] = v if dw == 8 or (dw == 4 and const_set(v)) else UNK
        elif mn == "mov" and s.type == X.X86_OP_MEM and dw == 8:
            a = memval(st, i, s.mem)
            sl = slot(a)
            new[dr] = st.get(sl, UNK) if sl else load_of(a)
        elif mn == "xor" and s.type == X.X86_OP_REG and full(s.reg)[0] == dr:
            new[dr] = frozenset([(None, 0)])
        elif mn == "lea" and s.type == X.X86_OP_MEM:
            v = memval(st, i, s.mem)
            new[dr] = v if dw == 8 else (frozenset((b, o & 0xFFFFFFFF) for b, o in v) if (dw == 4 and const_set(v)) else UNK)
        elif mn in ("add", "sub") and s.type == X.X86_OP_IMM and dw == 8:
            new[dr] = vadd(st.get(dr, UNK), s.imm if mn == "add" else -s.imm)
        elif mn == "imul" and len(ops) == 3 and ops[2].type == X.X86_OP_IMM and dw == 8:
            new[dr] = frozenset([("i*%#x" % ops[2].imm, 0)])        # an array index scaled by the element size
        elif mn == "add" and s.type == X.X86_OP_REG and dw == 8:
            a, c = single(st.get(dr, UNK)), single(st.get(full(s.reg)[0], UNK))
            if a and c and a[0] and a[0].startswith("i*") and c[0] and not c[0].startswith("i*"):
                new[dr] = frozenset([("%s[%s]" % (c[0], a[0]), c[1])])
            elif a and c and c[0] and c[0].startswith("i*") and a[0] and not a[0].startswith("i*"):
                new[dr] = frozenset([("%s[%s]" % (a[0], c[0]), a[1])])
            else:
                new[dr] = UNK
        elif mn.startswith("cmov") and dw == 8 and s.type == X.X86_OP_REG:
            new[dr] = join(st.get(dr, UNK), st.get(full(s.reg)[0], UNK))
    for r in written:
        if r not in new and mn not in ("cmp", "test", "bt", "push"):
            st[r] = UNK
    st.update(new)
    return st


_an = {}


def analyse(f):
    if f in _an:
        return _an[f]
    ins_state = {f: {r: frozenset([(r + "@e", 0)]) for r in GP}}
    work, cnt = [f], collections.Counter()
    while work:
        a = work.pop()
        i = R.dec(a)
        if i is None:
            continue
        cnt[a] += 1
        if cnt[a] > 64:
            continue
        imm = i.operands[0].imm if i.operands and i.operands[0].type == X.X86_OP_IMM else None
        if i.mnemonic == "jmp" and imm is not None and imm != f and imm in R.ext and not (f <= imm < f + R.ext[f]):
            continue
        st0 = step(ins_state[a], i)
        for t in R.branch_targets(i):
            if t in ins_state:
                old = ins_state[t]
                keys = set(GP) | {k for k in old if isinstance(k, tuple)} | {k for k in st0 if isinstance(k, tuple)}
                m = {r: join(old.get(r, UNK), st0.get(r, UNK)) for r in keys}
                m = {k: v for k, v in m.items() if not (isinstance(k, tuple) and v is UNK)}
                if m != old:
                    ins_state[t] = m
                    work.append(t)
            else:
                ins_state[t] = st0
                work.append(t)
    _an[f] = ins_state
    return ins_state


def insns(f):
    st = analyse(f)
    return [(a, R.dec(a), st[a]) for a in sorted(st) if R.dec(a) is not None]


def show(v):
    return "?" if v is UNK else "|".join(sorted(sym(b, o) for b, o in v))


# ---------------------------------------------------------------- A: census
image = io.open(R.b.EXE, "rb").read()
print("image sha256", hashlib.sha256(image).hexdigest())
check("A0 the image is the certified authority image", hashlib.sha256(image).hexdigest() == AUTH)
SC = retool.scan()
SIZES = retool.sizes()
callers = collections.defaultdict(list)
for m in M:
    for f, s in SC["calls"].get(m, ()):
        callers[f].append((s, m))
pairs = sum(len({m for _, m in v}) for v in callers.values())
sites = sum(len(v) for v in callers.values())
SIG = {f: "+".join(n for n in ("inc", "dec", "rotL", "rotR", "ins", "era") if n in {M[m] for _, m in v})
       for f, v in callers.items()}
sigc = collections.Counter(SIG.values())
print("census: %d callers, %d (caller, body) pairs, %d call sites; signatures %s" % (
    len(callers), pairs, sites, dict(sorted(sigc.items(), key=lambda x: -x[1]))))
pub = {}
tsvp = os.path.join(FF, "24-Compiler-And-CRT-Runtime", "Cxx-Runtime-Families", "members", "ordered-container-runtime-callers.tsv")
for line in io.open(tsvp, encoding="utf-8").read().splitlines():
    if line and not line.startswith(("#", "address")):
        c = line.split("\t")
        pub[int(c[0], 16)] = (c[3], int(c[4]), c[5] if len(c) > 5 else "")
norm = {"inc+era": "inc+era", "dec+ins": "dec+ins", "inc+ins": "inc+ins", "ins": "ins", "inc": "inc", "rotL+rotR": "rotL+rotR"}
check("A1 census = the published enumeration: 99 callers, 170 pairs, 213 sites",
      (len(callers), pairs, sites) == (99, 170, 213) and set(callers) == set(pub))
check("A2 every caller's member signature and site count equal the published TSV row",
      all(pub[f][0] == SIG[f] and pub[f][1] == len(callers[f]) for f in callers))
refs6 = [m for m in M if SC["refs"].get(m)]
check("A3 no rip-relative reference (lea / pointer load) names any of the six bodies", refs6 == [])
thunk6 = [f for f in callers if SIZES.get(f, 999) <= 16]
check("A4 no thin thunk (<= 16 bytes) in front of the six: every one of the 99 is a full body", thunk6 == [],
      "smallest caller %d bytes" % min(SIZES.get(f, 0) for f in callers))

# ---------------------------------------------------------------- B: per-function events
WIDTH = {1: "byte", 2: "word", 4: "dword", 8: "qword", 16: "xmm"}
SIGNED = {"jl", "jge", "jg", "jle", "setl", "setge", "setg", "setle", "cmovl", "cmovge", "cmovg", "cmovle"}
UNSIGNED = {"jb", "jae", "ja", "jbe", "setb", "setae", "seta", "setbe", "cmovb", "cmovae", "cmova", "cmovbe"}


def cond_after(L, k):
    for a, i, _ in L[k + 1:k + 5]:
        if i.mnemonic.startswith(("j", "set", "cmov")) and i.mnemonic != "jmp":
            return i.mnemonic
    return "-"


def entry_derived(v):
    """a value that is a function argument register plus an offset (the container object itself)."""
    return v is not UNK and all(b is not None and b.endswith("@e") for b, _ in v)


_ev = {}


def events(f):
    if f in _ev:
        return _ev[f]
    L = insns(f)
    E = collections.defaultdict(list)
    for k, (a, i, st) in enumerate(L):
        g = lambda r: st.get(r, UNK)
        mn = i.mnemonic
        if mn in ("call", "jmp") and i.operands and i.operands[0].type == X.X86_OP_IMM:
            t = i.operands[0].imm
            if t in M:
                E[M[t]].append(dict(site=a, rcx=g("rcx"), rdx=g("rdx"), r8=g("r8"), r9=g("r9")))
            else:
                E["call"].append(dict(site=a, tgt=t, rcx=g("rcx"), rdx=g("rdx"), r8=g("r8"), r9=g("r9"), jmp=mn == "jmp"))
            continue
        if mn == "call" and i.operands and i.operands[0].type == X.X86_OP_MEM and i.operands[0].mem.base != X.X86_REG_RIP:
            disp = i.operands[0].mem.disp
            if disp in (0x10, 0x18):
                E["vcall%x" % disp].append(dict(site=a, rcx=g("rcx"), rdx=g("rdx"), r8=g("r8")))
            continue
        ops = i.operands
        if mn in ("mov", "movups", "movdqu", "movaps", "movsd", "movss", "movq") and ops and ops[0].type == X.X86_OP_MEM:
            E["store"].append(dict(site=a, addr=memval(st, i, ops[0].mem), width=ops[0].size,
                                   src=(st.get(full(ops[1].reg)[0], UNK) if ops[1].type == X.X86_OP_REG and full(ops[1].reg)[0] else
                                        frozenset([(None, ops[1].imm)]) if ops[1].type == X.X86_OP_IMM else UNK), op=i.op_str))
        if mn in ("cmp", "comiss", "ucomiss", "comisd", "ucomisd"):
            for op in ops:
                if op.type == X.X86_OP_MEM and op.mem.base not in (0, X.X86_REG_RIP, X.X86_REG_RSP) and 0x20 <= op.mem.disp < 0x90:
                    base = memval(st, i, op.mem)
                    E["cmp"].append(dict(site=a, disp=op.mem.disp, width=op.size, mn=mn, cond=cond_after(L, k),
                                         container=entry_derived(vadd(base, -op.mem.disp)), op=i.op_str))
    _ev[f] = E
    return E


# ---------------------------------------------------------------- C: node allocation, value layout, helpers
def ctor_extent(t, depth=0):
    """a lower bound on the bytes a construct / copy callee writes relative to its rcx at entry: its own stores, and
    the extent of every callee it calls on rcx + d (three levels; the allocator ctor 001EDF00 writes one qword)."""
    if t == ALLOC_CTOR:
        return 8
    top = 0
    for s in events(t)["store"]:
        v = single(s["addr"]) if s["addr"] is not UNK else None
        if v and v[0] == "rcx@e":
            top = max(top, v[1] + s["width"])
    if depth < 3:
        for c in events(t)["call"]:
            v = single(c["rcx"]) if c["rcx"] is not UNK else None
            if v and v[0] == "rcx@e" and v[1] >= 0:
                top = max(top, v[1] + ctor_extent(c["tgt"], depth + 1))
    return top


def node_layout(f, alloc_site):
    """stores and constructor calls made on the node returned by the allocate at alloc_site in f."""
    tag = "call@%08X" % alloc_site
    out = []
    for s in events(f)["store"]:
        v = single(s["addr"]) if s["addr"] is not UNK else None
        if v and v[0] == tag and v[1] >= 0x20:
            out.append((v[1], "%s store" % WIDTH.get(s["width"], "%dB" % s["width"]), s["width"]))
    for c in events(f)["call"]:
        v = single(c["rcx"]) if c["rcx"] is not UNK else None
        if v and v[0] == tag and v[1] >= 0x20:
            ext = ctor_extent(c["tgt"])
            out.append((v[1], "call %s (writes %s bytes)" % (h8(c["tgt"]), hex(ext) if ext else "?"), ext))
    return sorted(set(out))


def allocs_in(f, tree):
    """allocate virtual calls in f on tree + 0x30 (tree is a (base, off) pair)."""
    out = []
    for vc in events(f)["vcall10"]:
        a = single(vc["rcx"]) if vc["rcx"] is not UNK else None
        sz = single(vc["rdx"]) if vc["rdx"] is not UNK else None
        if a and tree and a == (tree[0], tree[1] + 0x30) and sz and sz[0] is None:
            out.append((vc["site"], sz[1]))
    return out


_helper = {}


def node_helper(t):
    """a node-construction helper: its allocate on rcx@e + 0x30, and the value it builds."""
    if t not in _helper:
        al = allocs_in(t, ("rcx@e", 0))
        _helper[t] = [(s, z, node_layout(t, s)) for s, z in al]
    return _helper[t]


# ---------------------------------------------------------------- vtables, getters, object classes
VT = collections.defaultdict(list)
import pefile  # noqa: E402
_pe = pefile.PE(R.b.EXE, fast_load=True)
for s in _pe.sections:
    if s.Name.rstrip(b"\0") not in (b".rdata", b".data"):
        continue
    data = s.get_data()
    va = _pe.OPTIONAL_HEADER.ImageBase + s.VirtualAddress
    for off, (q,) in zip(range(0, len(data) - 7, 8), struct.iter_unpack("<Q", data[:len(data) // 8 * 8])):
        if 0x121000 <= q < 0x8C2000:
            VT[q].append(va + off)


def vclass(f):
    """RTTI classes of the vtables naming f as a slot."""
    out = []
    for site in VT.get(f, ()):
        vt, cls = retool.vtable_start(site)
        if cls:
            out.append((cls, (site - vt) // 8))
    return out


def rtti_of(v):
    try:
        return retool.rtti_class(v) if 0x8C2000 <= v < 0x3000000 else None
    except Exception:
        return None


_ctor = {}


def ctor_class(c):
    """the RTTI class of the last vtable c stores at [rcx+0] (a constructor's most-derived vtable)."""
    if c not in _ctor:
        cls = None
        for s in sorted(events(c)["store"], key=lambda s: s["site"]):
            if s["addr"] == frozenset([("rcx@e", 0)]) and s["width"] == 8 and const_set(s["src"]) and len(s["src"]) == 1:
                k = rtti_of(single(s["src"])[1])
                if k:
                    cls = k
        _ctor[c] = cls
    return _ctor[c]


_getter = {}


def getter(t):
    """the value t returns in rax when every ret agrees on one constant address or one load of a constant address."""
    if t in _getter:
        return _getter[t]
    res, vals = None, set()
    st = analyse(t)
    for a in st:
        i = R.dec(a)
        if i is not None and i.mnemonic == "ret":
            v = st[a].get("rax", UNK)
            vals |= {None} if v is UNK else set(v)
    if len(vals) == 1 and None not in vals:
        (b, o), = vals
        if b is None or re.fullmatch(r"\[[0-9A-F]{8}\]", b or "") or (b == "rcx@e" and o == 0):
            res = (b, o)
    _getter[t] = res
    return res


def new_object(f, site):
    """a call result used as an object in f: the classes of the constructors called on it, and the constant addresses
    the result (or a constructor's returned this) is stored to."""
    tok = ("call@%08X" % site, 0)
    E = events(f)
    stc = analyse(f).get(site, {})
    alloc = const_set(stc.get("rcx", UNK))             # an allocation call: a constant size in rcx
    ctors = [c for c in E["call"] if alloc and c["rcx"] is not UNK and tok in c["rcx"]]
    toks = {tok} | {("call@%08X" % c["site"], 0) for c in ctors}
    cls = [k for k in (ctor_class(c["tgt"]) for c in ctors) if k]
    glob = sorted({single(s["addr"])[1] for s in E["store"] if s["width"] == 8 and s["src"] is not UNK
                   and toks & set(s["src"]) and single(s["addr"]) and single(s["addr"])[0] is None})
    return cls, glob


_gcls = {}


def global_class(g):
    """the class of the object whose pointer a global holds: every store to g of a constructed object."""
    if g not in _gcls:
        cls = set()
        for f, site, kind in SC["refs"].get(g, ()):
            if kind != "W":
                continue
            st = analyse(f).get(site)
            i = R.dec(site)
            if st is None or i is None or len(i.operands) < 2 or i.operands[1].type != X.X86_OP_REG:
                continue
            v = st.get(full(i.operands[1].reg)[0], UNK)
            for b, o in (v or ()):
                m = re.fullmatch(r"call@([0-9A-F]{8})", b or "")
                if m and o == 0:
                    ci = R.dec(int(m.group(1), 16))
                    tgt = ci.operands[0].imm if ci and ci.operands and ci.operands[0].type == X.X86_OP_IMM else None
                    k = ctor_class(tgt) if tgt else None
                    if k:
                        cls.add(k)
                    c2, _ = new_object(f, int(m.group(1), 16))
                    cls |= set(c2)
        _gcls[g] = sorted(cls)
    return _gcls[g]


# ---------------------------------------------------------------- E: where the tree lives
# a leaf is (key, note): key is canonical and is what two trees are matched on; note says how it was reached.
def leaf_for(f, v, depth, seen):
    b, o = v
    if b is None:
        if o < 0x100000:
            return {("null+%#x" % o, "a constant %#x on a null-object path in %s" % (o, h8(f)))}
        return {("global %s" % h8(o), "a global object")}
    if b == "rsp@e":
        return {("stack %s%+#x" % (h8(f), o), "a local of %s" % h8(f))}
    m = re.fullmatch(r"(.+)\[i\*(0x[0-9a-f]+)\]", b)
    if m:
        return {("%s[i*%s]%+#x" % (k, m.group(2), o), n + "; element i of an array of %s-byte records" % m.group(2))
                for k, n in leaf_for(f, (m.group(1), 0), depth, seen)}
    m = re.fullmatch(r"\[([0-9A-F]{8})\]", b)
    if m:
        g = int(m.group(1), 16)
        cls = global_class(g)
        return {("*[%s]%+#x" % (m.group(1), o), "the object global %s points to%s" % (
            m.group(1), " (class %s)" % "/".join(cls) if cls else ""))}
    m = re.fullmatch(r"call@([0-9A-F]{8})", b)
    if m:
        site = int(m.group(1), 16)
        i = R.dec(site)
        tgt = i.operands[0].imm if i and i.operands and i.operands[0].type == X.X86_OP_IMM else None
        gv = getter(tgt) if tgt else None
        if gv == ("rcx@e", 0):                           # the callee returns its own this (a constructor)
            stc = analyse(f).get(site)
            v = stc.get("rcx", UNK) if stc else UNK
            if v is not UNK:
                out = set()
                for vb, vo in v:
                    out |= {(k, n + ", returned as this by %s" % h8(tgt)) for k, n in leaf_for(f, (vb, vo + o), depth, seen)}
                return out
        if gv and gv != ("rcx@e", 0):
            return {(k, n + ", returned by getter %s" % h8(tgt)) for k, n in leaf_for(tgt, (gv[0], gv[1] + o), depth, seen)}
        cls, glob = new_object(f, site)
        if glob:
            out = set()
            for g in glob:
                gc = global_class(g) or cls
                out.add(("*[%s]%+#x" % (h8(g), o), "the object %s builds at %s and stores to global %s%s" % (
                    h8(f), h8(site), h8(g), " (class %s)" % "/".join(gc) if gc else "")))
            return out
        if cls:
            return {("class %s%+#x" % ("/".join(sorted(set(cls))), o), "an object of that class built at %s in %s" % (h8(site), h8(f)))}
        stc = analyse(f).get(site, {})
        ctors = sorted({c["tgt"] for c in events(f)["call"] if c["rcx"] is not UNK and ("call@%08X" % site, 0) in c["rcx"]})
        if ctors and const_set(stc.get("rcx", UNK)):
            return {("object built by %s%+#x" % (h8(ctors[0]), o), "an object %s allocates at %s and constructs with %s" % (
                h8(f), h8(site), " ".join(h8(c) for c in ctors)))}
        return {("ret %s%+#x" % (h8(tgt) if tgt else "indirect", o), "the value %s returns (called at %s in %s)" % (
            h8(tgt) if tgt else "an indirect call", h8(site), h8(f)))}
    m = re.fullmatch(r"(r\w+)@e", b)
    if m:
        reg = m.group(1)
        who = "this" if reg == "rcx" else reg
        out = set()
        for cn, slot in (vclass(f) if reg == "rcx" else []):
            out.add(("class %s%+#x" % (cn, o), "this of %s, virtual slot %d of %s" % (h8(f), slot, cn)))
        ups = sorted(SC["calls"].get(f, ()))
        if out:
            return out
        if not ups or depth >= 4 or f in seen:
            refs = sorted(SC["refs"].get(f, ()))
            why = ("depth limit" if ups else "function pointer taken at %s" % " ".join(h8(r[1]) for r in refs) if refs
                   else "no direct caller, no vtable slot, no lea")
            return {("%s %s%+#x" % (who, h8(f), o), why)}
        for u, s in ups:
            stu = analyse(u).get(s)
            val = stu.get(reg, UNK) if stu else UNK
            if val is UNK:
                out.add(("%s %s%+#x" % (who, h8(f), o), "argument not tracked at %s in %s" % (h8(s), h8(u))))
                continue
            for vb, vo in val:
                out |= leaf_for(u, (vb, vo + o), depth + 1, seen | {f})
        return out
    m = re.fullmatch(r"\[(r\w+)@e([+-]0x[0-9a-f]+)?\]", b)
    if m:
        k = int(m.group(2), 16) if m.group(2) else 0
        who = "this" if m.group(1) == "rcx" else m.group(1)
        cls = vclass(f) if m.group(1) == "rcx" else []
        return {("*(%s %s%+#x)%+#x" % (who, h8(f), k, o), "the object a field of %s%s points to" % (
            who, " (%s)" % ", ".join("%s slot %d" % c for c in cls) if cls else " in %s" % h8(f)))}
    return {("%s%+#x in %s" % (b, o, h8(f)), "expression")}


def owners(f, tree):
    return sorted(leaf_for(f, tree, 0, frozenset()))


# ---------------------------------------------------------------- D: roles and per-caller facts
def trees_in(f, E, role):
    """(tree expression, how) pairs in f's own frame."""
    t = collections.Counter()
    for e in E["ins"]:
        v = single(e["r8"]) if e["r8"] is not UNK else None
        if v:
            t[((v[0], v[1] - 8), "insert header")] += 1
    for e in E["era"]:
        v = single(e["rdx"]) if e["rdx"] is not UNK else None
        if v:
            t[((v[0], v[1] - 8), "erase header")] += 1
    if role in ("walk", "erase"):
        for e in E["inc"] + E["dec"]:
            for b, o in (e["rcx"] or ()):
                m = re.fullmatch(r"\[(r\w+@e(?:\[i\*0x[0-9a-f]+\])?|[0-9A-F]{8})([+-]0x[0-9a-f]+)?\]", b or "")
                if m and o == 0:
                    k = int(m.group(2), 16) if m.group(2) else 0
                    base = m.group(1)
                    tv = (None, int(base, 16) + k - 0x10) if re.fullmatch(r"[0-9A-F]{8}", base) else (base, k - 0x10)
                    t[(tv, "begin() load")] += 1
    return t


rows = {}
for f in sorted(callers):
    E = events(f)
    sig = SIG[f]
    role = ("member" if f == 0x16DA60 else "insert-unique" if sig == "dec+ins" else "insert-hint" if sig == "inc+ins"
            else "insert-at" if sig == "ins" else "erase" if "era" in sig else "walk")
    tr = trees_in(f, E, role)
    tset = sorted({t for t, _ in tr}, key=lambda t: (str(t[0]), t[1]))
    how = sorted({w for _, w in tr})
    tree = tset[0] if len(tset) == 1 else None
    sizes, layouts, helpers, site_sizes = set(), [], set(), {}
    for e in E["ins"]:
        ss = set()
        for b, o in (e["rcx"] or ()):
            m = re.fullmatch(r"call@([0-9A-F]{8})", b or "")
            if not m or o != 0:
                continue
            site = int(m.group(1), 16)
            vc = [x for x in E["vcall10"] if x["site"] == site]
            if vc:
                z = single(vc[0]["rdx"])
                a = single(vc[0]["rcx"]) if vc[0]["rcx"] is not UNK else None
                if z and z[0] is None and tree and a == (tree[0], tree[1] + 0x30):
                    sizes.add(z[1])
                    ss.add(("allocate", site, z[1]))
                    layouts.append(tuple(node_layout(f, site)))
            else:
                c = [x for x in E["call"] if x["site"] == site]
                if c:
                    for hs, hz, hl in node_helper(c[0]["tgt"]):
                        sizes.add(hz)
                        layouts.append(tuple(hl))
                        helpers.add(c[0]["tgt"])
                        ss.add(("helper", c[0]["tgt"], hz))
        site_sizes[e["site"]] = ss
    dsizes = set()
    for vc in E["vcall18"]:
        a = single(vc["rcx"]) if vc["rcx"] is not UNK else None
        z = single(vc["r8"]) if vc["r8"] is not UNK else None
        if a and z and z[0] is None and any(a == (t[0], t[1] + 0x30) for t in tset):
            dsizes.add(z[1])
    reject = [s["site"] for s in E["store"] if s["width"] == 1 and s["src"] == frozenset([(None, 0)])
              and s["addr"] == frozenset([("rdx@e", 8)])]
    accept = [s["site"] for s in E["store"] if s["width"] == 1 and s["src"] == frozenset([(None, 1)])
              and s["addr"] == frozenset([("rdx@e", 8)])]
    keycmp = [c for c in E["cmp"] if not c["container"] and c["mn"] == "cmp" and c["disp"] == 0x20]
    kw = sorted({c["width"] for c in keycmp})
    ks = sorted({"signed" if c["cond"] in SIGNED else "unsigned" if c["cond"] in UNSIGNED else c["cond"] for c in keycmp})
    cmp_calls = sorted({c["tgt"] for c in E["call"] if c["tgt"] in (MEMCMP, 0x001A3100, 0x001A1990)})
    inner = sorted({c["tgt"] for c in E["call"] if c["tgt"] in callers})
    rows[f] = dict(role=role, sig=sig, trees=tset, how=how, tree=tree, sizes=sizes, dsizes=dsizes, layouts=layouts,
                   helpers=helpers, site_sizes=site_sizes, reject=reject, accept=accept, kw=kw, ks=ks,
                   cmp_calls=cmp_calls, inner=inner, E=E)

# ---------------------------------------------------------------- B: structural checks
per_site = collections.Counter()
alloc_sites = set()
multi = []
for f, r in rows.items():
    for s, ss in r["site_sizes"].items():
        al = {z for kind, _, z in ss if kind == "allocate"}
        alloc_sites |= {(a, z) for kind, a, z in ss if kind == "allocate"}
        if len({x for kind, x, _ in ss if kind == "allocate"}) > 1:
            multi.append((f, s, sorted({x for kind, x, _ in ss if kind == "allocate"})))
        for z in al:
            per_site[z] += 1
OC2 = {0x28: 16, 0x30: 15, 0x38: 10, 0x40: 5, 0x48: 10, 0x50: 4, 0x58: 5, 0x60: 10, 0x88: 5}
print("insert sites whose node comes from an inline allocate, by size:", {hex(k): v for k, v in sorted(per_site.items())})
check("B1 OC-2 reproduced per insert site: 80 of the 90 insert sites take their node from an inline allocate, nine sizes"
      " with the page's per-size counts", sum(per_site.values()) == 80 and dict(per_site) == OC2)
check("B1a one insert site is fed by two allocate sites on two branches (001FFB30: 001FFD0F from 001FFC30 and 001FFCE1),"
      " which is why the allocate SITES number 81", len(alloc_sites) == 81 and
      [(h8(f), h8(s), [h8(x) for x in a]) for f, s, a in multi] == [("001FFB30", "001FFD0F", ["001FFC30", "001FFCE1"])])
ins_sites = sum(len(r["E"]["ins"]) for r in rows.values())
helper_sites = [(f, s) for f, r in rows.items() for s, ss in r["site_sizes"].items() if any(k == "helper" for k, _, _ in ss)]
check("B1b the other 10 insert sites take their node from a node-construction helper that allocates on tree+0x30",
      ins_sites == 90 and len(helper_sites) == 10, "helpers %s" % " ".join(sorted({h8(x) for r in rows.values() for x in r["helpers"]})))
check("B2 every one of the 90 insert sites belongs to an insert-unique / insert-hint / insert-at body",
      all(r["role"].startswith("insert") for r in rows.values() if r["E"]["ins"]))
check("B3 every insert-family body keeps exactly one tree, at this+0 (the header it passes is rcx+8)",
      all(r["tree"] == ("rcx@e", 0) for r in rows.values() if r["role"].startswith("insert")))
check("B4 every insert-at body passes its own position argument (r8 at entry) as the parent at every insert site",
      all(all(e["rdx"] == frozenset([("r8@e", 0)]) for e in r["E"]["ins"]) for r in rows.values() if r["role"] == "insert-at"))
uni = [f for f, r in rows.items() if r["role"] == "insert-unique"]
check("B5 all 24 insert-unique bodies hold the reject path (byte [ret+8] = 0) beside the accept (byte [ret+8] = 1)",
      len(uni) == 24 and all(rows[f]["reject"] and rows[f]["accept"] for f in uni),
      "first reject stores " + " ".join(h8(rows[f]["reject"][0]) for f in uni[:4]) + " ...")
hint = [f for f, r in rows.items() if r["role"] == "insert-hint"]
check("B6 each of the 16 insert-hint bodies calls exactly one insert-unique (its fallback) and one insert-at",
      len(hint) == 16 and all(sum(1 for t in rows[f]["inner"] if rows[t]["role"] == "insert-unique") == 1 and
                              sum(1 for t in rows[f]["inner"] if rows[t]["role"] == "insert-at") == 1 for f in hint))
at_callers = collections.Counter()
for f in rows:
    for t in rows[f]["inner"]:
        if rows[t]["role"] == "insert-at":
            at_callers[t] += 1
ext_at = [t for t, r in rows.items() if r["role"] == "insert-at" and any(u not in rows for u, _ in SC["calls"].get(t, ()))]
check("B7 no insert-equal body: every insert body without a reject path is a hint (falls back to a rejecting insert) or an"
      " insert-at reached only from inside the 99",
      all(r["reject"] or r["role"] in ("insert-hint", "insert-at") for r in rows.values() if r["role"].startswith("insert"))
      and ext_at == [], "insert-at bodies called from outside the 99: %s" % (" ".join(h8(x) for x in ext_at) or "none"))

# ---------------------------------------------------------------- G: instantiation groups
parent = {}


def find(x):
    while parent.setdefault(x, x) != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


def union(a, b):
    parent[find(a)] = find(b)


ins_family = [f for f, r in rows.items() if r["role"].startswith("insert")]
for f in ins_family:
    find(f)
    for t in rows[f]["inner"]:
        if rows[t]["role"].startswith("insert"):
            union(f, t)
    for hlp in rows[f]["helpers"]:
        union(f, ("helper", hlp))
groups = collections.defaultdict(list)
for f in ins_family:
    groups[find(f)].append(f)
glist = sorted((sorted(v) for v in groups.values()), key=lambda v: v[0])


def gdesc(members):
    sizes = set().union(*(rows[f]["sizes"] for f in members))
    kw = sorted(set().union(*(rows[f]["kw"] for f in members if rows[f]["role"] == "insert-unique")))
    ks = sorted(set().union(*(rows[f]["ks"] for f in members if rows[f]["role"] == "insert-unique")))
    cc = sorted(set().union(*(rows[f]["cmp_calls"] for f in members)))
    lay = set()
    for f in members:
        lay |= set(rows[f]["layouts"])
    return sizes, kw, ks, cc, lay


CMPN = {MEMCMP: "memcmp", 0x001A3100: "001A3100", 0x001A1990: "001A1990"}


def key_text(kw, ks, cc):
    if cc:
        return "compare call %s" % "+".join(CMPN[c] for c in cc)
    return " / ".join("%s %s" % (WIDTH[w], s) for w in kw for s in ks) or "-"


def lay_text(lay):
    parts = []
    for L in sorted(lay):
        parts.append("; ".join("+%s %s" % (hex(d), what) for d, what, _ in L) or "(no store seen)")
    return " || ".join(sorted(set(parts)))


gid, GINFO = {}, {}
for n, members in enumerate(glist, 1):
    g = "I%02d" % n
    for f in members:
        gid[f] = g
    GINFO[g] = dict(members=members, desc=gdesc(members),
                    ext=[f for f in members if any(u not in members for u, _ in SC["calls"].get(f, ()))])
check("G1 the 56 insert-family bodies fall into 24 instantiations, each with one insert-unique, one node size and one key"
      " compare", len(glist) == 24 and all(
          sum(1 for f in GINFO[g]["members"] if rows[f]["role"] == "insert-unique") == 1 and len(GINFO[g]["desc"][0]) == 1
          and (len(GINFO[g]["desc"][1]) == 1 and len(GINFO[g]["desc"][2]) == 1 or GINFO[g]["desc"][3]) for g in GINFO))

# ---------------------------------------------------------------- E: owners
own = {}
for g, gi in GINFO.items():
    res = set()
    for e in gi["ext"]:
        res |= set(owners(e, ("rcx@e", 0)))
    gi["owners"] = sorted(res)
    for f in gi["members"]:
        own[f] = gi["owners"]
for f, r in rows.items():
    if r["role"] in ("erase", "walk"):
        own[f] = owners(f, r["tree"]) if r["tree"] is not None else []

# ---------------------------------------------------------------- F: construction tags
tagged = []
for tag, name in TAGS.items():
    for f, site, kind in sorted(SC["refs"].get(tag, ())):
        L = insns(f)
        k0 = next(k for k, (a, _, _) in enumerate(L) if a >= site)
        # the name goes into a stack allocator first, which is then copied into tree+0x30: take the first allocator
        # ctor within 40 instructions whose rcx - 0x30 is a tree this body initialises (size dword at +0x28 and the
        # anchor self-link [tree+0x10] = tree+8)
        st_ = events(f)["store"]
        tree = None
        for a, i, st in L[k0:k0 + 40]:
            if i.mnemonic == "call" and i.operands and i.operands[0].type == X.X86_OP_IMM and i.operands[0].imm == ALLOC_CTOR:
                v = single(st.get("rcx", UNK)) if st.get("rcx", UNK) is not UNK else None
                if not v:
                    continue
                t = (v[0], v[1] - 0x30)
                size_init = any(s["addr"] == frozenset([(t[0], t[1] + 0x28)]) and s["width"] == 4 for s in st_)
                anchor = any(s["addr"] == frozenset([(t[0], t[1] + 0x10)]) and s["src"] == frozenset([(t[0], t[1] + 8)])
                             for s in st_)
                if size_init and anchor:
                    tree = t
                    break
        if tree is None:
            tagged.append(dict(tag=name, f=f, site=site, tree=None, ok=False, owners=[]))
            continue
        tagged.append(dict(tag=name, f=f, site=site, tree=tree, ok=True, owners=owners(f, tree)))
def ident(k):
    """keys that name one tree: a value returned by an indirect call, a null-object path or an untyped expression does
    not identify an object and never ties two bodies together."""
    return not k.startswith(("ret indirect", "null+")) and " in " not in k


tag_by_key = collections.defaultdict(set)
for t in tagged:
    if t["ok"]:
        for k, n in t["owners"]:
            if ident(k):
                tag_by_key[k].add(t["tag"])


def tags_for(ow):
    return sorted(set().union(*[tag_by_key.get(k, set()) for k, _ in ow])) if ow else []


# erase / walk -> instantiation: PROVEN when the tree key equals one the instantiation's insert bodies were resolved to
key_to_group = collections.defaultdict(set)
for g, gi in GINFO.items():
    for k, n in gi["owners"]:
        if ident(k):
            key_to_group[k].add(g)
for f, r in rows.items():
    if r["role"] not in ("erase", "walk"):
        continue
    gs = set().union(*[key_to_group.get(k, set()) for k, _ in own[f]]) if own[f] else set()
    r["group"] = sorted(gs)
    r["link"] = "same tree" if gs else "-"
    if not gs:
        cand = [g for g, gi in GINFO.items() if r["dsizes"] and gi["desc"][0] == r["dsizes"]
                and (not r["kw"] or (gi["desc"][1] == r["kw"] and gi["desc"][2] == r["ks"]))]
        if len(cand) == 1:
            r["group"], r["link"] = cand, "INFERENCE: node size%s matches one instantiation only" % (" + key" if r["kw"] else "")
        elif cand:
            r["link"] = "ambiguous by size: %s" % " ".join(cand)
# second pass (INFERENCE): a body sharing a tree key with an erase / walk body already tied by the same tree; or a body
# that itself inserts through an instantiation of its own node size into a sibling tree of the same object
for f, r in rows.items():
    if r["role"] not in ("erase", "walk") or r["group"]:
        continue
    keys = {k for k, _ in own[f] if ident(k)}
    via = [(f2, r2["group"]) for f2, r2 in rows.items() if f2 != f and r2.get("link") == "same tree"
           and keys & {k for k, _ in own[f2]}]
    if via and len({tuple(g) for _, g in via}) == 1:
        r["group"], r["link"] = list(via[0][1]), "INFERENCE: shares a tree key with %s, which is tied by the same tree" % h8(via[0][0])
        continue
    sib = sorted({gid[t] for t in r["inner"] if t in gid and GINFO[gid[t]]["desc"][0] == r["dsizes"]})
    if r["dsizes"] and len(sib) == 1:
        r["group"], r["link"] = sib, "INFERENCE: the body inserts into a %s tree of the same node size on the same object" % sib[0]

# narrowing for the untied: a deallocate through an allocator that lives INSIDE the node (node+d) is a value
# destructor; it narrows the candidates to instantiations whose value constructs an allocator at the same node+d
for f, r in rows.items():
    if r["role"] not in ("erase", "walk") or r["group"] or not r["dsizes"]:
        continue
    inner_alloc = set()
    for vc in r["E"]["vcall18"]:
        v = vc["rcx"]
        if v is UNK or any(b is None for b, _ in v):
            continue
        offs = {o for _, o in v}
        if len(offs) == 1 and 0x20 <= min(offs) < max(r["dsizes"]) and not any(
                (b, o - 0x30) in r["trees"] for b, o in v):
            inner_alloc |= offs
    if inner_alloc:
        cand = [g for g, gi in GINFO.items() if gi["desc"][0] == r["dsizes"] and all(
            any(d == x and "001EDF00" in what for L in gi["desc"][4] for x, what, _ in L) for d in inner_alloc)]
        r["narrow"] = "value destructor frees through an allocator at node+%s: candidates %s" % (
            "/".join(hex(d) for d in sorted(inner_alloc)), " ".join(cand) or "none")

# ---------------------------------------------------------------- W: thin wrappers above the 99
WRAP = {}
for f in rows:
    for u, s_ in SC["calls"].get(f, ()):
        if u not in rows and SIZES.get(u, 999) <= 48:
            WRAP.setdefault(u, set()).add(f)

# ---------------------------------------------------------------- the container each instantiation keeps
KEYNAME = {(4, "signed"): "int32", (4, "unsigned"): "uint32", (8, "signed"): "int64", (8, "unsigned"): "uint64"}


def reading(g):
    """key bytes vs value bytes: value = key only -> set, value extends past the key -> map. The tag, where it reaches the
    tree, is the proof; otherwise this is the reading and is marked INFERENCE."""
    sizes, kw, ks, cc, lay = GINFO[g]["desc"]
    vend = max((d + w for L in lay for d, _, w in L), default=0)
    if cc:
        kname = "std::string (MSVC; compare 001A1990)" if 0x001A1990 in cc else "eastl::string (compare 001A3100)"
        kend = 0x40
    else:
        kname, kend = KEYNAME.get((kw[0], ks[0]), "?"), 0x20 + kw[0]
    kind = "set" if vend <= kend else "map"
    tg = tags_for(GINFO[g]["owners"])
    text = "set<%s>" % kname if kind == "set" else "map<%s, value to node+%s (>= %s bytes past the key)>" % (
        kname, hex(vend), hex(vend - kend))
    proof = ("tag %s" % "/".join(tg)) if tg else "INFERENCE (no allocator-name tag reaches its trees)"
    return kind, text, proof, tg


for g in GINFO:
    GINFO[g]["reading"] = reading(g)
tagged_groups = {g: gi["reading"] for g, gi in GINFO.items() if gi["reading"][3]}
check("F1 no instantiation is reached by both allocator names, and every tagged instantiation's value layout agrees with its"
      " tag (EASTL set -> the node holds the key only; EASTL map -> the value runs past the key)",
      all(len(r[3]) == 1 and r[3][0] == "EASTL " + r[0] for r in tagged_groups.values()),
      "%d tagged: %s" % (len(tagged_groups), " ".join("%s=%s" % (g, r[3][0].split()[1]) for g, r in sorted(tagged_groups.items()))))

# ---------------------------------------------------------------- report
print()
print("== G: the 24 insert instantiations, their value layout and where their trees live (SWE2-ORACLE)")
for g, gi in GINFO.items():
    sizes, kw, ks, cc, lay = gi["desc"]
    print("%s  node %s  key %s  %s" % (g, "/".join(hex(z) for z in sorted(sizes)), key_text(kw, ks, cc),
                                      " ".join("%s(%s)" % (h8(f), rows[f]["role"].replace("insert-", "")) for f in gi["members"])))
    print("     value at node: %s" % lay_text(lay))
    hl = sorted(set().union(*(rows[f]["helpers"] for f in gi["members"])))
    if hl:
        print("     node-construction helper: %s" % " ".join(h8(x) for x in hl))
    erasers = sorted(f for f, r in rows.items() if r["role"] in ("erase", "walk") and r.get("group") == [g])
    if erasers:
        print("     erase / walk bodies on the same tree: %s" % " ".join("%s(%s)" % (h8(f), rows[f]["link"][:9]) for f in erasers))
    tg = tags_for(gi["owners"])
    print("     constructed with allocator name: %s" % ("/".join(tg) if tg else "not reached"))
    print("     reading: %s  [%s]" % (gi["reading"][1], gi["reading"][2]))
    print("     entry bodies %s -> %d distinct tree(s):" % (" ".join(h8(x) for x in gi["ext"]), len({k for k, _ in gi["owners"]})))
    for k, n in gi["owners"]:
        print("       %-40s %s" % (k, n))

print()
print("== E: erase and walk bodies (SWE2-ORACLE)")
for f, r in sorted(rows.items()):
    if r["role"] in ("erase", "walk"):
        print("%s %-5s tree %-20s node %-5s key %-18s group %-4s (%s)  -> %s" % (
            h8(f), r["role"], show(frozenset(r["trees"])) if r["trees"] else "?",
            "/".join(hex(z) for z in sorted(r["dsizes"])) or "-", key_text(r["kw"], r["ks"], r["cmp_calls"]),
            "/".join(r["group"]) or "-", r["link"], "; ".join("%s [%s]" % kn for kn in own[f][:3]) +
            (" (+%d)" % (len(own[f]) - 3) if len(own[f]) > 3 else "")))

for f, r in sorted(rows.items()):
    if r.get("narrow"):
        print("   narrowing %s: %s" % (h8(f), r["narrow"]))

print()
print("== W: thin wrappers (<= 48 bytes) directly above the 99 (SWE2-ORACLE)")
for u in sorted(WRAP):
    cls = vclass(u)
    ups = sorted({x for x, _ in SC["calls"].get(u, ())})
    body = " ; ".join("%s %s" % (i.mnemonic, i.op_str) for i in R.md.disasm(R.at(u, SIZES[u]), u))
    print("  %s (%2d B) -> %s  %s  [%d direct callers%s]  %s" % (
        h8(u), SIZES[u], " ".join(h8(x) for x in sorted(WRAP[u])), "; ".join("%s slot %d" % c for c in cls) or "not a vtable slot",
        len(ups), "" if not ups else ": " + " ".join(h8(x) for x in ups[:4]) + (" ..." if len(ups) > 4 else ""), body[:110]))
print("  %d thin wrappers; %d of them are vtable slots; %d distinct functions call the 99 through them" % (
    len(WRAP), sum(1 for u in WRAP if vclass(u)), len({x for u in WRAP for x, _ in SC["calls"].get(u, ())})))

print()
ok_tags = [t for t in tagged if t["ok"]]
print("== F: %d allocator-name sites (%d EASTL map, %d EASTL set), %d followed to a constructed tree (size dword at"
      " tree+0x28 and the anchor self-link stored by the same body) (SWE2-ORACLE)" % (
          len(tagged), sum(1 for t in tagged if t["tag"] == "EASTL map"), sum(1 for t in tagged if t["tag"] == "EASTL set"), len(ok_tags)))
for t in tagged:
    print("  %-9s %s @%s tree %-14s %s" % (t["tag"], h8(t["f"]), h8(t["site"]), show(frozenset([t["tree"]])) if t["tree"] else "-",
                                          ("; ".join(k for k, _ in t["owners"][:3]) if t["ok"] else "not followed")))
matched = sorted({(k, "/".join(sorted(v))) for k, v in tag_by_key.items()
                  if any(k == kk for f in rows for kk, _ in own.get(f, []))})
print("  tags reaching a caller's tree: %d distinct trees" % len(matched))

# ---------------------------------------------------------------- per-caller table
print()
print("== the 99, one line each (SWE2-ORACLE)")
TSV = []
for f in sorted(rows):
    r = rows[f]
    if r["role"].startswith("insert"):
        g, link = gid[f], "code (call edges)"
    elif r["role"] == "member":
        g, link = "-", "-"
    else:
        g, link = "/".join(r["group"]) or "-", r["link"]
    size = "/".join(hex(z) for z in sorted(r["sizes"] | r["dsizes"])) or "-"
    src = ("allocate" if r["sizes"] and not r["helpers"] else "helper " + " ".join(h8(x) for x in sorted(r["helpers"]))
           if r["helpers"] else "deallocate" if r["dsizes"] else "-")
    if r["role"].startswith("insert"):
        sizes, kw, ks, cc, lay = GINFO[gid[f]]["desc"]
        key = key_text(kw, ks, cc)
    else:
        key = key_text(r["kw"], r["ks"], r["cmp_calls"]) if (r["kw"] or r["cmp_calls"]) else "-"
    kind = ("unique: reject %s" % h8(r["reject"][0]) if r["reject"] else "unique: falls back to %s" % h8(
        [t for t in r["inner"] if rows[t]["role"] == "insert-unique"][0]) if r["role"] == "insert-hint" else
        "tail of the unique insert" if r["role"] == "insert-at" else "-")
    tree = show(frozenset(r["trees"])) if r["trees"] else "-"
    o = own.get(f, [])
    ok_ = sorted({k for k, _ in o})
    tg = tags_for(o) if r["role"] != "member" else []
    rd = GINFO[g]["reading"] if g in GINFO else None
    cont = ("%s [%s]" % (rd[1], rd[2]) if rd else "-")
    TSV.append([h8(f), str(SIZES.get(f, 0)), r["sig"], r["role"], g, link, size, src, key, kind, cont, tree,
                "; ".join(ok_[:8]) + (" (+%d more, see sd81_callers.out)" % (len(ok_) - 8) if len(ok_) > 8 else "") if ok_ else "-",
                "/".join(tg) or "-"])
    print("%s %-13s %-4s %-6s %-26s tree %-14s %s" % (h8(f), r["role"], g, size, key, tree,
                                                      (o[0][0] + (" (+%d)" % (len(o) - 1) if len(o) > 1 else "")) if o else "-"))

typed = [f for f in rows if f != 0x16DA60 and (rows[f]["role"].startswith("insert") or rows[f]["group"])]
untyped = [f for f in rows if f != 0x16DA60 and f not in typed]
located = [f for f in rows if f != 0x16DA60 and any(not k.startswith(("this ", "rdx ", "r8 ", "r9 ")) for k, _ in own.get(f, []))]
print()
print("typed (node size + key + value tied to an instantiation): %d of 98; not tied: %d (%s)" % (
    len(typed), len(untyped), " ".join(h8(x) for x in sorted(untyped))))
print("tree located beyond the body's own this (global / singleton / class / stack / object): %d of 98" % len(located))

# ---------------------------------------------------------------- positive control + the contradiction it raised
print()
f = 0x001FC9F0
g = gid[f]
sizes, kw, ks, cc, lay = GINFO[g]["desc"]
check("P1 positive control (font page section 3): the .ker writer 001FDC10 -> 001FC9F0 keeps 0x28-byte nodes keyed by a"
      " signed dword at node+0x20 with an 8-byte value - read here without being told",
      sizes == {0x28} and kw == [4] and ks == ["signed"] and any(d == 0x20 and w == 8 for L in lay for d, _, w in L),
      "instantiation %s" % g)
E1 = events(0x001FDC10)
c420 = [c for c in E1["call"] if c["tgt"] == 0x001FC420]
c9f0 = [c for c in E1["call"] if c["tgt"] == 0x001FC9F0]
spill = [s for s in E1["store"] if s["width"] == 4 and s["addr"] == frozenset([("rsp@e", 0x18)])]
ret420 = [a for a, i, st in insns(0x001FC420) if i.mnemonic == "lea" and i.op_str == "rax, [rbx + 0x28]"]
g20 = gid[0x001FCCE0]
K1 = (len(c420) == 1 and c420[0]["rcx"] == frozenset([("rcx@e", 0x70)]) and c420[0]["rdx"] == frozenset([("rsp@e", 0x18)])
      and spill and len(c9f0) == 1 and c9f0[0]["rcx"] == frozenset([("call@%08X" % c420[0]["site"], 0)]) and ret420
      and 0x001FCCE0 in [c["tgt"] for c in events(0x001FC420)["call"]] and GINFO[g20]["desc"][0] == {0x60})
check("K1 CONTRADICTS font page section 3 ('flat map', 'r8d never read back'): 001FDC10 spills r8d (record +4) to its"
      " home slot, passes that slot's address as the key of 001FC420(font+0x70), which returns node+0x28 of a %s map"
      " (0x60-byte nodes) - and 001FC9F0 inserts into THAT: the writer builds map<i32 rec+4, map<i32 rec+0, i32 rec+8>>" % g20,
      bool(K1), "001FC420 call %s, spill %s, 001FC9F0 call %s, ret lea %s" % (
          h8(c420[0]["site"]) if c420 else "-", h8(spill[0]["site"]) if spill else "-",
          h8(c9f0[0]["site"]) if c9f0 else "-", h8(ret420[0]) if ret420 else "-"))

t420 = [t for t in tagged if t["f"] == 0x001FC420 and t["ok"]]
cp = [c for c in events(0x001FC420)["call"] if c["tgt"] == 0x001FBEF0]
check("K2 the value 001FC420 inserts is an eastl::map: it names a stack tree 'EASTL map', and that tree is the source (rdx)"
      " 001FBEF0 copies into the pair's +8 - the same 001FBEF0 the %s node runs at node+0x28" % g20,
      len(t420) == 1 and len(cp) == 1 and cp[0]["rdx"] == frozenset([t420[0]["tree"]]) and
      any(x == 0x28 and "001FBEF0" in what for L in GINFO[g20]["desc"][4] for x, what, _ in L),
      "tag site %s, tree %s, copy %s" % (h8(t420[0]["site"]) if t420 else "-", show(frozenset([t420[0]["tree"]])) if t420 else "-",
                                         h8(cp[0]["site"]) if cp else "-"))

if "--tsv" in sys.argv:
    out = sys.argv[sys.argv.index("--tsv") + 1]
    hdr = ["address", "bytes", "members", "role", "instantiation", "instantiation_link", "node_size", "node_size_source",
           "key_compare", "insert_kind", "container_reading", "tree_in_body", "header_owner", "construction_tag"]
    with io.open(out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# SD-81 (SWE2-ORACLE, 2026-09-30): the 99 callers of the EASTL rbtree runtime, one row each. Generated by\n"
                 "# sd81_callers.py --tsv from the certified image (73461d08...21f8). Columns and what each proves: README.md.\n")
        fh.write("\t".join(hdr) + "\n")
        for row in TSV:
            fh.write("\t".join(row) + "\n")
print()
print("FAILS %d" % FAILS)
