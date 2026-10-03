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


EXTRACT = {"registry_node": ex_registry_node, "call_class": ex_call_class}
COLS = ["entry", "anchor", "mnemonic", "value", "name", "callee"]


def derive_all():
    rows, bad = [], []
    for a in members():
        r, why = EXTRACT[SPEC["kind"]](a)
        (bad.append(("%08X" % a, why)) if r is None else rows.append(r))
    return rows, bad


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
    for a in want:
        k = "%08X" % a
        r, why = EXTRACT[SPEC["kind"]](a)
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
        a0, a1 = rows[0], rows[1]
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
        if not (e < an < e + sizes.get(e, 0)):
            print("FAIL %s: anchor %s not strictly inside the body" % (r["entry"], r["anchor"])); fails += 1
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


if __name__ == "__main__":
    c = sys.argv[1] if len(sys.argv) > 1 else "check"
    sys.exit({"derive": cmd_derive, "check": cmd_check}.get(c, lambda: cmd_apply("--apply" in sys.argv))())
