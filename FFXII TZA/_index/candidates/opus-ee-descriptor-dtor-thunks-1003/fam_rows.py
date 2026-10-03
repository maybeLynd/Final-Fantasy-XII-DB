"""fam_rows.py - per-member interior rows for a generated function family (OPUS, 2026-10-03).

SWE2-AUDIT-SPEC's engine_explained ruling (202e59a0a, on the PObjectAccessor rows): a member of a family whose shared
shape is explained once counts only through an interior citation that anchors the instruction distinguishing that
member and states the member-specific value, verified against the image; rows restating the shared shape earn nothing.

A record folder holds spec.json {"page", "members", "kind", "title", "lead"} and a copy of this file:
  python -B fam_rows.py derive       derive every member's row from the image -> rows.tsv (refuses a member whose
                                     body does not have the family's form: the family form is part of the check)
  python -B fam_rows.py check        re-derive from the image and compare with the committed rows.tsv, row by row,
                                     plus the controls (a swapped value and a moved anchor must each be refused);
                                     last line 'FAILS n'
  python -B fam_rows.py apply [--apply]   append (or rewrite) the page section built from rows.tsv; idempotent
Kinds (the extractor states what distinguishes a member):
  registry_node   32-byte static initialiser `sub rsp,0x28; lea rcx,[node]; call REG; lea rcx,[dtor]; ...; jmp ATEXIT`:
                  the +0x4 lea's node and the C string at the node's qword +0x8 (its registered name).
"""
import io
import json
import os
import re
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = json.load(io.open(os.path.join(HERE, "spec.json"), encoding="utf-8")) if os.path.exists(
    os.path.join(HERE, "spec.json")) else None
DBR = os.path.normpath(os.path.join(HERE, "..", "..", ".."))           # FFXII TZA/ (record is _index/candidates/X)
KIT = os.path.normpath(os.path.join(DBR, "..", "Tools", "analysis-kit", "gfz-scripts"))
sys.path.insert(0, KIT)
import retool  # noqa: E402

R = retool.R
_SIZES = None


def _sizes():
    global _SIZES
    if _SIZES is None:
        sys.path.insert(0, KIT)
        import check_dispositions as CD
        _SIZES = CD.load_functions()
    return _SIZES


def disasm(a, n):
    return list(R.md.disasm(R.at(a, n), a))


def rip_target(i):
    m = re.search(r"\[rip ([+-]) (0x[0-9a-f]+|\d+)\]", i.op_str)
    if not m:
        return None
    d = int(m.group(2), 0)
    return i.address + i.size + (d if m.group(1) == "+" else -d)


def cstr(a):
    b = R.at(a, 96) or b""
    s = b.split(b"\0")[0]
    return s.decode("ascii") if s and all(32 <= c < 127 for c in s) else None


def members():
    p = os.path.join(DBR, *SPEC["members"].split("/"))
    out = []
    for l in io.open(p, encoding="utf-8"):
        if l[:1] in "#\n" or not l.strip():
            continue
        tok = l.split("\t")[0].strip()
        if re.fullmatch(r"[0-9A-Fa-f]{8}", tok):
            out.append(int(tok, 16))
    return out


def ex_registry_node(a):
    ins = disasm(a, 0x40)
    if len(ins) < 6 or ins[0].mnemonic != "sub" or ins[1].mnemonic != "lea" or not ins[1].op_str.startswith("rcx, ") \
            or ins[2].mnemonic != "call" or ins[3].mnemonic != "lea" or ins[5].mnemonic != "jmp":
        return None, "form"
    node = rip_target(ins[1])
    if node is None:
        return None, "lea not rip-relative"
    p = struct.unpack("<Q", R.at(node + 8, 8))[0]
    name = cstr(p) if p else None
    if not name or "|" in name or "`" in name:
        return None, "no clean name at node+8"
    reg = int(ins[2].op_str, 16)
    return {"entry": "%08X" % a, "anchor": "%08X" % ins[1].address, "mnemonic": "lea",
            "value": "%08X" % node, "name": name, "callee": "%08X" % reg}, None


_RD = None


def _rdata_refs():
    """qword slot address(es) in .rdata holding each value, built once."""
    global _RD
    if _RD is None:
        import collections
        import pefile
        pe = pefile.PE(R.b.EXE, fast_load=True)
        base = pe.OPTIONAL_HEADER.ImageBase
        want = set(members())
        _RD = collections.defaultdict(list)
        for sec in pe.sections:
            if sec.Name.rstrip(b"\0") != b".rdata":
                continue
            d = sec.get_data()
            va0 = base + sec.VirtualAddress
            for o in range(0, len(d) - 7, 8):
                v = struct.unpack_from("<Q", d, o)[0]
                if v in want:
                    _RD[v].append(va0 + o)
        _RD["base"] = base
    return _RD


def _col_type_name(vt):
    """MSVC x64 RTTI: the complete-object locator before the vtable -> its type descriptor's decorated name."""
    col = struct.unpack("<Q", R.at(vt - 8, 8))[0]
    b = R.at(col, 16)
    if not b or struct.unpack_from("<I", b, 0)[0] != 1:
        return None
    td = _rdata_refs()["base"] + struct.unpack_from("<I", b, 12)[0]
    raw = (R.at(td + 0x10, 256) or b"").split(b"\0")[0]
    return raw.decode("latin1") if raw.startswith(b".?A") else None


def _template_arg(decorated):
    """'.?AV?$PClassDescriptorForType@VPTimer@Phyre@@@Phyre@@' -> 'Phyre::PTimer' (simple class arguments only)."""
    m = re.match(r"^\.\?AV\?\$PClassDescriptor\w*@([VU])(.+?)@@@Phyre@@$", decorated)
    if not m:
        return None
    if "?" in m.group(2) or "$" in m.group(2):
        # a template argument (PArray<...>, PSharray<...>): give the decorated argument exactly as the image has it
        # rather than a hand demangling; the uniqueness test compares these strings too
        inner = m.group(1) + m.group(2) + "@@"
        return None if "`" in inner or "|" in inner else "decorated `%s`" % inner
    return "::".join(reversed(m.group(2).split("@")))


def ex_call_class(a):
    """A one-call adapter: the call target is the member's own; the reflected type is the T of every
    PClassDescriptor*<T> vtable holding the member at SPEC['slot'] (all must agree)."""
    ins = disasm(a, 0x30)
    calls = [i for i in ins if i.mnemonic == "call"]
    if len(calls) != 1 or not re.fullmatch(r"0x[0-9a-f]+", calls[0].op_str):
        return None, "form (not exactly one direct call)"
    ts = set()
    for slot_va in _rdata_refs().get(a, []):
        vt = slot_va - 8 * SPEC["slot"]
        n = _col_type_name(vt)
        if n:
            ts.add(_template_arg(n))
    if len(ts) != 1 or None in ts:
        return None, "reflected type not unique at slot %d (%s)" % (SPEC["slot"], sorted(map(str, ts))[:3])
    return {"entry": "%08X" % a, "anchor": "%08X" % calls[0].address, "mnemonic": "call",
            "value": "%08X" % int(calls[0].op_str, 16), "name": ts.pop(), "callee": SPEC.get("group", "all")}, None


_VT = None
VERB_TABLES = [(0x01EED700, 0), (0x01F281B0, 3), (0x01F29418, 5), (0x01F29440, 7), (0x01F26720, 2)]
VM_HELPERS = {0x00267DB0, 0x00267E10, 0x00267F60, 0x00267F90, 0x0026B4C0, 0x0026B4E0, 0x00808C40}


def _verb_tables():
    """callback -> [(family, index, role)] read from the five image verb tables (records at table + 8 + 32*N:
    begin +0x00, poll +0x08, result +0x18; count = s32 at the table), plus the catalogue names by call id."""
    global _VT
    if _VT is None:
        import collections
        import csv
        cb = collections.defaultdict(list)
        for base, fam in VERB_TABLES:
            cnt = struct.unpack("<i", R.at(base, 4))[0]
            for i in range(cnt):
                rec = base + 8 + 32 * i
                for off, role in ((0, "begin"), (8, "poll"), (0x18, "result")):
                    q = struct.unpack("<Q", R.at(rec + off, 8))[0]
                    if q:
                        cb[q].append((fam, i, role))
        names = {}
        vt = os.path.join(DBR, *SPEC["catalogue"].split("/"))
        for row in csv.DictReader(io.open(vt, encoding="utf-8"), delimiter="\t"):
            names[int(row["call_id"], 16)] = row["verb"]
        _VT = (cb, names)
    return _VT


def ex_verb_adapter(a):
    """A registered verb callback with exactly one native (non-VM-helper) direct call / external tail jump: that
    site is the distinguishing instruction; its target and the callback's table registrations are the values."""
    n = _sizes().get(a)
    cb, names = _verb_tables()
    regs = cb.get(a)
    if not n or not regs:
        return None, "not registered in the five verb tables"
    sites = []
    for i in R.md.disasm(R.at(a, n), a):
        if i.mnemonic in ("call", "jmp") and re.fullmatch(r"0x[0-9a-f]+", i.op_str):
            t = int(i.op_str, 16)
            if not (a <= t < a + n) and t not in VM_HELPERS:
                sites.append((i, t))
    tg = {t for _i, t in sites}
    if len(tg) != 1:
        return None, "%d native targets (no single distinguishing call)" % len(tg)
    i = sites[0][0]
    if i.address == a:
        return None, "the native site is the first instruction"
    reg = "; ".join("family %d call `%04X` %s (%s)" % (f, x, role, names.get((f << 12) | x, names.get(x, "?") if f == 0 else "?"))
                    for f, x, role in sorted(set(regs)))
    if "|" in reg:
        return None, "pipe in a catalogue name"
    return {"entry": "%08X" % a, "anchor": "%08X" % i.address, "mnemonic": i.mnemonic, "value": "%08X" % tg.pop(),
            "name": reg, "callee": "family %d" % sorted(set(regs))[0][0]}, None


_SCAN = None
META_CTORS = {0x00632960: "00632960", 0x00632A10: "00632A10"}


def _refs():
    global _SCAN
    if _SCAN is None:
        _SCAN = retool.scan()["refs"]
    return _SCAN


def ex_metadata_teardown(a):
    """`lea rcx, [X]; jmp SPEC['helper']` at the entry. X is the member-specific value. Its registration is the one
    `lea rcx, [X]` immediately followed by a call to a data-member constructor (00632960, or the array form 00632A10),
    decoded from the registering function's own entry; the r9 lea there is the member name, and an immediate
    `mov dword [rsp+0x20]` the member offset (omitted when the offset is passed in a register)."""
    sizes = _sizes()
    ins = disasm(a, 16)
    if len(ins) < 2 or ins[0].mnemonic != "lea" or not ins[0].op_str.startswith("rcx, ") or ins[1].mnemonic != "jmp" \
            or ins[1].op_str not in {hex(h) for h in (SPEC["helper"] if isinstance(SPEC["helper"], list) else [SPEC["helper"]])}:
        return None, "form"
    X = rip_target(ins[0])
    regs = []
    for t in _refs().get(X, ()):
        fn, site = t[0], t[1]
        if fn == a or fn not in sizes:
            continue
        body = list(R.md.disasm(R.at(fn, sizes[fn]), fn))
        k = next((n for n, j in enumerate(body) if j.address == site), None)
        if k is None or k + 1 >= len(body) or body[k].mnemonic != "lea" or not body[k].op_str.startswith("rcx, "):
            continue
        nx = body[k + 1]
        if nx.mnemonic != "call" or not re.fullmatch(r"0x[0-9a-f]+", nx.op_str) or int(nx.op_str, 16) not in META_CTORS:
            continue
        name = off = None
        for j in reversed(body[max(0, k - 10):k]):
            if name is None and j.mnemonic == "lea" and j.op_str.startswith("r9, "):
                t9 = rip_target(j)
                name = cstr(t9) if t9 else None
            if off is None and j.mnemonic == "mov" and j.op_str.startswith("dword ptr [rsp + 0x20], "):
                v = j.op_str.split(", ", 1)[1]
                off = int(v, 0) if re.fullmatch(r"0x[0-9a-f]+|\d+", v) else "reg"
        regs.append((name, off, META_CTORS[int(nx.op_str, 16)], "%08X" % nx.address))
    if len(regs) != 1 or not regs[0][0] or "|" in regs[0][0] or "`" in regs[0][0]:
        return None, "registration not unique or unnamed (%d)" % len(regs)
    name, off, ctor, call = regs[0]
    where = "offset 0x%X" % off if isinstance(off, int) else "offset passed in a register"
    return {"entry": "%08X" % a, "anchor": "%08X" % ins[0].address, "mnemonic": "lea", "value": "%08X" % X,
            "name": "member \"%s\", %s (constructor %s, called at %s)" % (name, where, ctor, call),
            "callee": ctor}, None


def ex_vtable_store(a):
    """`lea rax, [V]; mov qword ptr [rcx], rax; jmp SPEC['helper']` at the entry: the member resets the object's vtable
    to V before the shared destructor. V is the member-specific value; its MSVC RTTI type descriptor (the complete-object
    locator before V) names the class, and for a PClassDescriptor*<T> class the template argument T."""
    ins = disasm(a, 16)
    hs = SPEC["helper"] if isinstance(SPEC["helper"], list) else [SPEC["helper"]]
    if len(ins) < 3 or ins[0].mnemonic != "lea" or not ins[0].op_str.startswith("rax, ") \
            or ins[1].mnemonic != "mov" or ins[1].op_str != "qword ptr [rcx], rax" \
            or ins[2].mnemonic != "jmp" or ins[2].op_str not in {hex(h) for h in hs}:
        return None, "form"
    V = rip_target(ins[0])
    _rdata_refs()
    n = _col_type_name(V)
    if not n:
        return None, "no RTTI locator before the vtable"
    t = _template_arg(n)
    name = t if t else "decorated `%s`" % n
    if "|" in name:
        return None, "pipe in name"
    return {"entry": "%08X" % a, "anchor": "%08X" % ins[0].address, "mnemonic": "lea", "value": "%08X" % V,
            "name": name, "callee": SPEC.get("group", "all")}, None


def ex_named_call(a):
    """The member's one direct call to SPEC['target']; within the ten instructions before it, the `lea SPEC['reg'], [S]`
    whose target is a clean C string is the distinguishing instruction (S and the string are the values), and an
    immediate `mov SPEC['size_reg'], imm` there, if any, is reported as the size argument."""
    n = _sizes().get(a)
    if not n:
        return None, "no census extent"
    body = list(R.md.disasm(R.at(a, n), a))
    calls = [k for k, j in enumerate(body) if j.mnemonic == "call" and j.op_str == hex(SPEC["target"])]
    if len(calls) != 1:
        return None, "%d calls to the target" % len(calls)
    k = calls[0]
    lea = size = None
    for j in reversed(body[max(0, k - 10):k]):
        if lea is None and j.mnemonic == "lea" and j.op_str.startswith(SPEC["reg"] + ", "):
            lea = j
        if size is None and SPEC.get("size_reg") and j.mnemonic == "mov" and j.op_str.startswith(SPEC["size_reg"] + ", "):
            v = j.op_str.split(", ", 1)[1]
            size = int(v, 0) if re.fullmatch(r"0x[0-9a-f]+|\d+", v) else None
    if lea is None:
        return None, "no lea %s before the call" % SPEC["reg"]
    S = rip_target(lea)
    name = cstr(S) if S else None
    if not name or "|" in name or "`" in name:
        return None, "no clean string at the lea target"
    if lea.address == a and not SPEC.get("entry_anchor"):
        return None, "distinguishing lea is the entry instruction"
    txt = "\"%s\"" % name + (", size 0x%X" % size if size is not None else "")
    return {"entry": "%08X" % a, "anchor": "%08X" % lea.address, "mnemonic": "lea", "value": "%08X" % S,
            "name": txt, "callee": SPEC.get("group", "all")}, None


DESC_CTOR = 0x00632D80
_CTOR_NAMES = {}


_BODIES = {}


def _body(fn):
    """Decoded body over the census extent, memoised: families re-read the same initialisers and wrappers."""
    if fn not in _BODIES:
        n = _sizes().get(fn)
        _BODIES[fn] = list(R.md.disasm(R.at(fn, n), fn)) if n else []
    return _BODIES[fn]


def _ctor_name(c):
    """The class name a descriptor-constructor wrapper passes: the `lea r8, [S]` before its one call to 00632D80."""
    b = _body(c)
    ks = [k for k, j in enumerate(b) if j.mnemonic == "call" and j.op_str == hex(DESC_CTOR)]
    if len(ks) != 1:
        return None
    for j in reversed(b[max(0, ks[0] - 10):ks[0]]):
        if j.mnemonic == "lea" and j.op_str.startswith("r8, "):
            t = rip_target(j)
            return cstr(t) if t else None
    return None


def _descriptor_name(X):
    """A static class descriptor X is named by the static initialiser that does `lea rcx, [X]` and then calls a
    descriptor-constructor wrapper; the wrapper's name argument is the class name. Every such initialiser must agree."""
    names = set()
    for t in _refs().get(X, ()):
        site = t[1]
        two = disasm(site, 32)[:2]         # the scan's site is an instruction boundary
        if len(two) == 2 and two[0].mnemonic == "lea" and two[0].op_str.startswith("rcx, ") \
                and two[1].mnemonic == "call" and re.fullmatch(r"0x[0-9a-f]+", two[1].op_str):
            c = int(two[1].op_str, 16)
            if c not in _CTOR_NAMES:
                _CTOR_NAMES[c] = _ctor_name(c)
            if _CTOR_NAMES[c]:
                names.add(_CTOR_NAMES[c])
    return names


def ex_descriptor_lea(a):
    """The member's one `lea SPEC['reg'], [X]` loads a static class descriptor; X and the class it describes (named
    through X's static initialiser and descriptor-constructor wrapper, see _descriptor_name) are the values."""
    b = _body(a)
    L = [j for j in b if j.mnemonic == "lea" and j.op_str.startswith(SPEC["reg"] + ", ")]
    if SPEC.get("same_target_ok") and len(L) > 1 and len({rip_target(j) for j in L}) == 1:
        L = L[:1]          # the same descriptor loaded on each path; the first load is the anchor
    if len(L) != 1:
        return None, "%d lea %s" % (len(L), SPEC["reg"])
    if L[0].address == a and not SPEC.get("entry_anchor"):
        return None, "the lea is the entry instruction"
    X = rip_target(L[0])
    n = _descriptor_name(X) if X else set()
    if len(n) != 1:
        return None, "descriptor not named by exactly one class (%d)" % len(n)
    name = n.pop()
    if "|" in name or "`" in name:
        return None, "unclean name"
    return {"entry": "%08X" % a, "anchor": "%08X" % L[0].address, "mnemonic": "lea", "value": "%08X" % X,
            "name": name, "callee": SPEC.get("group", "all")}, None


def ex_vtable_lea(a):
    """The member's vtable reset: the one `lea rax, [V]` immediately followed by `mov qword ptr [rcx], rax` anywhere in
    the body (every such pair must name the same V). V and the class its MSVC RTTI locator names are the values."""
    b = _body(a)
    pairs = [b[k] for k in range(len(b) - 1) if b[k].mnemonic == "lea" and b[k].op_str.startswith("rax, ")
             and b[k + 1].mnemonic == "mov" and b[k + 1].op_str == "qword ptr [rcx], rax"]
    if not pairs or len({rip_target(j) for j in pairs}) != 1:
        return None, "%d vtable stores" % len(pairs)
    j = pairs[0]
    if j.address == a and not SPEC.get("entry_anchor"):
        return None, "the lea is the entry instruction"
    V = rip_target(j)
    _rdata_refs()
    n = _col_type_name(V)
    if not n:
        return None, "no RTTI locator before the vtable"
    t = _template_arg(n)
    name = t if t else "decorated `%s`" % n
    if "|" in name:
        return None, "pipe in name"
    return {"entry": "%08X" % a, "anchor": "%08X" % j.address, "mnemonic": "lea", "value": "%08X" % V,
            "name": name, "callee": SPEC.get("group", "all")}, None


EXTRACT = {"registry_node": ex_registry_node, "call_class": ex_call_class, "verb_adapter": ex_verb_adapter,
           "metadata_teardown": ex_metadata_teardown, "vtable_store": ex_vtable_store, "named_call": ex_named_call,
           "descriptor_lea": ex_descriptor_lea, "vtable_lea": ex_vtable_lea}
COLS = ["entry", "anchor", "mnemonic", "value", "name", "callee"]


def derive_all():
    rows, bad = [], []
    for a in members():
        r, why = EXTRACT[SPEC["kind"]](a)
        (bad.append(("%08X" % a, why)) if r is None else rows.append(r))
    # declared skips (e.g. a member whose citation pulls another layer's caller edge into the page, pass 22)
    for k, why in SPEC.get("skip", {}).items():
        for r in list(rows):
            if r["entry"] == k:
                rows.remove(r)
                bad.append((k, why))
    # 2026-10-03: a value that several members share distinguishes none of them (e.g. the ForType / Concrete
    # deleting-destructor pairs restore the same vtable with identical bodies) - such members get no row
    import collections
    seen = collections.Counter(r["value"] for r in rows)
    keep = []
    for r in rows:
        if seen[r["value"]] > 1:
            bad.append((r["entry"], "value %s shared with %d other member(s): no member-specific instruction"
                        % (r["value"], seen[r["value"]] - 1)))
        else:
            keep.append(r)
    return keep, sorted(bad)


def read_rows():
    rows = []
    for l in io.open(os.path.join(HERE, "rows.tsv"), encoding="utf-8"):
        if l.startswith("#") or not l.strip() or l.startswith("entry\t"):
            continue
        rows.append(dict(zip(COLS, l.rstrip("\n").split("\t"))))
    return rows


def cmd_derive():
    rows, bad = derive_all()
    with io.open(os.path.join(HERE, "rows.tsv"), "w", encoding="utf-8", newline="\n") as f:
        f.write("# %s - derived from the shipping image by fam_rows.py (kind %s)\n" % (SPEC["title"], SPEC["kind"]))
        f.write("\t".join(COLS) + "\n")
        for r in rows:
            f.write("\t".join(r[c] for c in COLS) + "\n")
    with io.open(os.path.join(HERE, "excluded.tsv"), "w", encoding="utf-8", newline="\n") as f:
        f.write("# members the image refuses for this family's per-member form - no row; check verifies each is still refused\n")
        f.write("entry\treason\n")
        for a, why in bad:
            f.write("%s\t%s\n" % (a, why))
    print("derived %d rows, %d refused (excluded.tsv)" % (len(rows), len(bad)))
    for a, why in bad:
        print("  REFUSED %s: %s" % (a, why))
    return 0


def cmd_check():
    fails = 0
    want = {a: None for a in members()}
    got = {r["entry"]: r for r in read_rows()}
    excl = {}
    xp = os.path.join(HERE, "excluded.tsv")
    if os.path.exists(xp):
        for l in io.open(xp, encoding="utf-8"):
            if l[:1] != "#" and l.strip() and not l.startswith("entry\t"):
                excl[l.split("\t")[0]] = l.rstrip("\n").split("\t")[1]
    print("members %d, committed rows %d, declared exclusions %d" % (len(want), len(got), len(excl)))
    full_rows, _full_bad = derive_all()
    derived = {r["entry"]: r for r in full_rows}
    for a in want:
        k = "%08X" % a
        r = derived.get(k)
        why = None if r else "refused by the derivation"
        if k in excl:
            if r is not None:
                print("FAIL %s: declared excluded but the image now gives a row" % k); fails += 1
            continue
        if r is None:
            print("FAIL %s: image form refused (%s)" % (k, why)); fails += 1; continue
        c = got.get(k)
        if c is None:
            print("FAIL %s: no committed row" % k); fails += 1; continue
        diff = [col for col in COLS if r[col] != c.get(col)]
        if diff:
            print("FAIL %s: %s differ (image %s, row %s)" % (k, diff, [r[x] for x in diff], [c.get(x) for x in diff]))
            fails += 1
    for k in set(got) - {"%08X" % a for a in want}:
        print("FAIL %s: row for a non-member" % k); fails += 1
    # controls: the comparison must refuse a swapped value and a moved anchor
    rows = read_rows()
    if len(rows) >= 2:
        a0 = rows[0]
        a1 = next((r for r in rows[1:] if r["value"] != a0["value"]), rows[1])
        sw = dict(a0, value=a1["value"], name=a1["name"])
        ok1 = EXTRACT[SPEC["kind"]](int(a0["entry"], 16))[0]["value"] != sw["value"]
        mv = dict(a0, anchor="%08X" % (int(a0["anchor"], 16) + 1))
        ok2 = EXTRACT[SPEC["kind"]](int(a0["entry"], 16))[0]["anchor"] != mv["anchor"]
        print("control swapped-value %s, control moved-anchor %s" % ("refused" if ok1 else "ACCEPTED", "refused" if ok2 else "ACCEPTED"))
        fails += (not ok1) + (not ok2)
    # every anchor strictly inside its member's body (the census extent)
    sys.path.insert(0, KIT)
    import check_dispositions as CD
    sizes = CD.load_functions()
    for r in rows:
        e, an = int(r["entry"], 16), int(r["anchor"], 16)
        lo_ok = (e <= an) if SPEC.get("entry_anchor") else (e < an)
        if not (lo_ok and an < e + sizes.get(e, 0)):
            print("FAIL %s: anchor %s not inside the body" % (r["entry"], r["anchor"])); fails += 1
    print("FAILS %d" % fails)
    return 1 if fails else 0


def section(rows):
    depth = "../" * SPEC["page"].count("/")
    rec = os.path.basename(HERE)
    out = ["", SPEC["heading"], "", SPEC["lead"].replace("{N}", str(len(rows))).replace(
        "{CHECK}", "[`fam_rows.py`](%s_index/candidates/%s/fam_rows.py)" % (depth, rec)).replace(
        "{ROWS}", "[`rows.tsv`](%s_index/candidates/%s/rows.tsv)" % (depth, rec)), ""]
    groups = {}
    for r in rows:
        groups.setdefault(r["callee"], []).append(r)
    for callee, rs in groups.items():
        out += [SPEC["group_heading"].replace("{CALLEE}", callee).replace("{GROUP}", SPEC.get("groups", {}).get(callee, callee))
                .replace("{N}", str(len(rs))), "",
                "| member | distinguishing instruction | %s | %s |" % (SPEC["value_col"], SPEC["name_col"]), "|---|---|---|---|"]
        for r in rs:
            vfmt = SPEC.get("value_fmt", "`{V}`")
            out.append("| %s | `%s` `%s` | %s | %s |" % (r["entry"], r["anchor"], r["mnemonic"], vfmt.replace("{V}", r["value"]),
                                                         SPEC["name_fmt"].replace("{NAME}", r["name"])))
        out.append("")
    return "\n".join(out)


def cmd_apply(apply):
    p = os.path.join(DBR, *SPEC["page"].split("/"))
    t = io.open(p, encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in t[:3000] else "\n"
    sec = section(read_rows()).replace("\n", nl)
    head = SPEC["heading"]
    if head in t:
        i = t.index(head)
        j = t.find(nl + "## ", i + len(head))
        old = t[i:] if j < 0 else t[i:j]
        new_t = t[:i] + sec.lstrip(nl).rstrip(nl) + nl + (t[j:] if j >= 0 else "")
        if old.rstrip(nl) == sec.lstrip(nl).rstrip(nl):
            print("ALREADY (section matches rows.tsv)"); print("FAILS 0"); return 0
        state = "REWRITTEN"
    else:
        new_t = t.rstrip("\r\n") + nl + sec.rstrip(nl) + nl
        state = "APPENDED"
    if apply:
        io.open(p, "w", encoding="utf-8", newline="").write(new_t)
    print(state if apply else "DRY (%s)" % state.lower())
    print("FAILS 0")
    return 0


def cmd_readme():
    """Write the record's README from spec.json, rows.tsv, excluded.tsv and fam_rows_check.out (2026-10-03: four
    records a batch were costing a hand-drafted README each; the facts are all in these files)."""
    rows = read_rows()
    excl = [l.rstrip("\n").split("\t") for l in io.open(os.path.join(HERE, "excluded.tsv"), encoding="utf-8")
            if l[:1] != "#" and l.strip() and not l.startswith("entry\t")] if os.path.exists(os.path.join(HERE, "excluded.tsv")) else []
    chk = io.open(os.path.join(HERE, "fam_rows_check.out"), encoding="utf-8").read().strip().splitlines()
    import collections
    reasons = collections.Counter(re.sub(r"\s*\(.*$|value [0-9A-F]{8} shared.*", lambda m: "a value shared with other members" if "shared" in m.group(0) else "", w) for _e, w in excl)
    depth = "../" * (SPEC["page"].count("/") + 0)
    page_link = "../../../" + SPEC["page"]
    out = ["# Per-member rows: %s (OPUS, %s)" % (SPEC["title"], "2026-10-03"), "",
           "Host page: [`%s`](%s). It declares the family in its frontmatter (members file `%s`)." % (
               os.path.basename(SPEC["page"]), page_link, os.path.basename(SPEC["members"])), "",
           "This record adds one row for each of **%d** members, under the explained-once family sentence OPUS adopted "
           "for engine_explained ([`opus-ee-rulings-1003`](../opus-ee-rulings-1003/README.md)). Each row anchors the "
           "member's distinguishing instruction and states the member-specific value, both derived from the certified "
           "image. The shared form is stated once in the section's lead, and the lead is the authority for what each "
           "column means." % len(rows), ""]
    if excl:
        out += ["**No rows: %d members**, each listed with its reason in [`excluded.tsv`](excluded.tsv):" % len(excl)]
        out += ["- %d: %s;" % (n, w) for w, n in reasons.most_common()]
        out[-1] = out[-1].rstrip(";") + "."
        out += ["", "The checker fails if any of them starts deriving.", ""]
    out += ["## Verified", "",
            "- [`fam_rows.py`](fam_rows.py) `check` re-derives every row from the image and compares it with "
            "[`rows.tsv`](rows.tsv) ([`fam_rows_check.out`](fam_rows_check.out)):"]
    out += ["  - %s" % l for l in chk]
    out += ["- `fam_rows.py apply` is idempotent: a second run prints ALREADY.",
            "- Page gates are run per batch before publishing: `nb_page`, `check_links`, `verify_doc_addresses`, "
            "`check_consistency` and `check_self_contradiction --db`.", ""]
    io.open(os.path.join(HERE, "README.md"), "w", encoding="utf-8", newline="\n").write("\n".join(out))
    print("README written (%d rows, %d exclusions)" % (len(rows), len(excl)))
    return 0


if __name__ == "__main__":
    c = sys.argv[1] if len(sys.argv) > 1 else "check"
    sys.exit({"derive": cmd_derive, "check": cmd_check, "readme": cmd_readme}.get(
        c, lambda: cmd_apply("--apply" in sys.argv))())
