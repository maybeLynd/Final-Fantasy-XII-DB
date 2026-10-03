"""apply.py [--apply] - FABLE, 2026-10-03: home no-reference bodies on the page that documents the table or function
that reaches them.

Rows are in rows.json beside this file. Each body is one that no document cites and that no census-listed instruction
calls or jumps to; SWE2-EC7 handed it to FABLE (Database/Tools/work/SWE2-EC7/handoff_noref_to_fable_1003.tsv, rows
without the rtti column). FABLE swept the image for every reference to the entry (absolute qwords and 32-bit
image-relative values outside .text and .pdata, rip-relative operands in .text, [reg+RVA] forms), grouped the bodies by
the table or function that holds the reference, read every listing whole and wrote one sentence per body.

Checks, all before anything is written:
  1. the page is clean in git (`git status --short -- <page>` prints nothing);
  2. there is at least one row;
  3. every function is an entry in the certified function list, is not already cited on the page outside this block,
     and its sentence has no pipe and is under 1,200 characters;
  4. every anchor is an instruction boundary strictly inside its function and decodes to the recorded mnemonic
     (linear decode of the whole extent from the certified image);
  5. the reference the sentence names really reaches the body, at the bytes (see ref kinds below);
  6. the page cites, outside this block, every token in the row's `cites` list - the referencing table or function.
Reference kinds (rows.json `ref`):
  code      - `site` is an instruction boundary in the linear decode of census function `container` and an operand of
              it (rip-relative displacement or immediate target) forms the body's address; optional `store_site` /
              `store_target` (or `store_op`): the store at `store_site` writes that register to the rip-relative cell
              `store_target` (or has exactly the operand text `store_op`).
  registrar - a `code` reference whose store target is qword +0x28 of the registrar's node, and whose registrar row in
              the page's members/guard-adapter-registrars.tsv carries the body as stored_code_pointer and that node
              as static.
  funclet   - the cleanup/catch funclet starting at `funclet` reaches the body at instruction boundary `site` (linear
              decode from the funclet entry); the dword at `slot` is the funclet's image-relative address; and `slot`
              is an action field of the unwind map (or a catch handler field of the try-block map) of the FuncInfo
              (magic 0x1993052x) that `parent`'s own .pdata unwind record names.
  slot      - the `width`-byte cell `site` holds the body's address (8: absolute; 4: image-relative), and `site` =
              `table` + `field` + `stride` * `index`; with `counted`, `index` is below the dword at `table`; with
              `via`, the qword `via.site` holds `via.value` (the pointer that names the table).
  catchable - `throw_site` in census function `thrower` forms the ThrowInfo `throwinfo`; its catchable-type array
              (dword +0xC) lists `catchable`; that CatchableType's copy-function dword (+0x18) is the body.
Without --apply it only verifies (DRY / ALREADY). With --apply it appends ONE section at the end of the page
(byte-preserving, CRLF kept, idempotent: an identical block prints ALREADY, a differing block is re-rendered).
Prints FAILS n as its last line and exits non-zero on any failure.
--test-copy FILE runs the same checks and writes against FILE (a copy of the page) instead of the page, skipping only the
git-clean check."""
import json, os, re, struct, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.normpath(os.path.join(DB, "..", "Tools", "analysis-kit", "gfz-scripts")))
import check_dispositions as cd  # noqa: E402
import family_prover as fp  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64  # noqa: E402
from capstone.x86 import X86_OP_MEM, X86_OP_IMM, X86_OP_REG  # noqa: E402

CFG = json.load(open(os.path.join(HERE, "rows.json"), encoding="utf-8"))
REL = CFG["page"]
P = os.path.join(DB, *REL.split("/"))
TEST = sys.argv[sys.argv.index("--test-copy") + 1] if "--test-copy" in sys.argv else None
ROWS = CFG["rows"]
REC = os.path.basename(HERE)
ME = os.path.basename(__file__)
DEPTH = "../" * REL.count("/")
HEADING = "## No-reference bodies homed by the table that reaches them (FABLE, %s)" % CFG["date"]
NOTE = ("*No page cited these functions and no census-listed instruction calls or jumps to them: each is reached "
        "through data or through code this page documents. Each sentence states what the body does (access and "
        "representation, not purpose) and ends with the reference that reaches it; the anchors are instructions inside "
        "the body that do it. %sHanded over by SWE2-EC7 and read whole by FABLE against the certified image; verified "
        "by [`%s`](%s_index/candidates/%s/%s): every anchor is an instruction boundary inside its function and decodes "
        "to the recorded mnemonic, and every named reference holds or forms the body's address at the bytes.*"
        % ((CFG.get("note_extra") + " ") if CFG.get("note_extra") else "", ME, DEPTH, REC, ME))

fails = 0


def fail(msg):
    global fails
    print("VERIFY FAIL " + msg)
    fails += 1


def H(x):
    return int(x, 16)


# 1. clean page
if TEST:
    print("TEST COPY %s (git-clean check skipped)" % TEST)
    P = TEST
else:
    try:
        st = subprocess.run(["git", "status", "--short", "--", P], cwd=DB, capture_output=True, text=True,
                            check=True).stdout
    except Exception as e:  # noqa: BLE001
        st = None
        fail("git status failed: %s" % e)
    if st:
        fail("page is dirty in the working tree: %s" % st.strip())
if not os.path.exists(P):
    fail("page missing: %s" % REL)
    print("FAILS", fails)
    sys.exit(1)

raw = open(P, "rb").read()
crlf = b"\r\n" in raw[:4000]
text = raw.decode("utf-8")
cut = text.find(HEADING)
outside = text if cut < 0 else text[:cut]

# 2. rows
if not ROWS:
    fail("rows.json has zero rows")

sizes = cd.load_functions()
d, off = fp.load_image()
md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True
pe = struct.unpack_from("<I", d, 0x3C)[0]
BASE = struct.unpack_from("<Q", d, pe + 24 + 24)[0]
EXC_RVA, EXC_SIZE = struct.unpack_from("<II", d, pe + 24 + 112 + 3 * 8)


def u32(va):
    o = off(va)
    if o is None:
        raise ValueError("%08X not file-backed" % va)
    return struct.unpack_from("<I", d, o)[0]


def u64(va):
    o = off(va)
    if o is None:
        raise ValueError("%08X not file-backed" % va)
    return struct.unpack_from("<Q", d, o)[0]


_dec = {}


def decode(start, n):
    k = (start, n)
    if k not in _dec:
        o = off(start)
        _dec[k] = {i.address: i for i in md.disasm(d[o:o + n], start)}
    return _dec[k]


def forms(ins, tgt):
    for op in ins.operands:
        if op.type == X86_OP_MEM and op.mem.base and ins.reg_name(op.mem.base) == "rip" \
                and ins.address + ins.size + op.mem.disp == tgt:
            return True
        if op.type == X86_OP_IMM and op.imm == tgt:
            return True
    return False


def rip_target(ins):
    for op in ins.operands:
        if op.type == X86_OP_MEM and op.mem.base and ins.reg_name(op.mem.base) == "rip":
            return ins.address + ins.size + op.mem.disp
    return None


def pdata_entry(va):
    n = EXC_SIZE // 12
    po = off(BASE + EXC_RVA)
    lo, hi = 0, n - 1
    while lo <= hi:
        m = (lo + hi) // 2
        b, e, u = struct.unpack_from("<III", d, po + m * 12)
        if va - BASE < b:
            hi = m - 1
        elif va - BASE >= e:
            lo = m + 1
        else:
            return BASE + b, BASE + e, BASE + u
    return None


def check_code(fn, r, what="code"):
    f = H(r["container"])
    n = sizes.get(f)
    if not n:
        fail("%s: %s container %s is not a census function entry" % (fn, what, r["container"]))
        return None
    dec = decode(f, n)
    ins = dec.get(H(r["site"]))
    if ins is None:
        fail("%s: %s site %s is not an instruction boundary of %s" % (fn, what, r["site"], r["container"]))
        return None
    if not forms(ins, H(fn)):
        fail("%s: %s site %s (%s %s) does not form the body address" % (fn, what, r["site"], ins.mnemonic, ins.op_str))
        return None
    if r.get("store_site"):
        st_ = dec.get(H(r["store_site"]))
        dst = ins.operands[0].reg if ins.operands and ins.operands[0].type == X86_OP_REG else None
        bad = st_ is None or st_.mnemonic != "mov" or len(st_.operands) < 2 \
            or st_.operands[1].type != X86_OP_REG or st_.operands[1].reg != dst
        if not bad and r.get("store_target"):
            bad = rip_target(st_) != H(r["store_target"])
        if not bad and r.get("store_op"):
            bad = st_.op_str != r["store_op"]
        if bad:
            fail("%s: %s store %s does not write the formed register to %s" % (
                fn, what, r.get("store_site"), r.get("store_target") or r.get("store_op")))
            return None
    return ins


_tsv = {}


def registrar_rows():
    if not _tsv:
        tp = os.path.join(os.path.dirname(os.path.join(DB, *REL.split("/"))), "members", "guard-adapter-registrars.tsv")
        lines = [l.rstrip("\n").split("\t") for l in open(tp, encoding="utf-8") if not l.startswith("#")]
        h = lines[0]
        for l in lines[1:]:
            row = dict(zip(h, l))
            _tsv[row["registrar"]] = row
    return _tsv


def check_ref(fn, r):
    k = r["kind"]
    try:
        if k == "code":
            check_code(fn, r)
        elif k == "registrar":
            if check_code(fn, r, "registrar") is None:
                return
            row = registrar_rows().get(r["container"])
            if not row:
                fail("%s: registrar %s not in members/guard-adapter-registrars.tsv" % (fn, r["container"]))
            elif row["stored_code_pointer"] != fn:
                fail("%s: registrar %s stores %s per the members file" % (fn, r["container"], row["stored_code_pointer"]))
            elif H(row["static"]) + 0x28 != H(r["store_target"]):
                fail("%s: registrar %s store target is not node %s + 0x28" % (fn, r["container"], row["static"]))
        elif k == "funclet":
            s, site, slot, parent = H(r["funclet"]), H(r["site"]), H(r["slot"]), H(r["parent"])
            ins = decode(s, 0x60).get(site)
            if ins is None or not forms(ins, H(fn)) or ins.mnemonic not in ("jmp", "call"):
                fail("%s: funclet %s does not jump to or call the body at %s" % (fn, r["funclet"], r["site"]))
                return
            if u32(slot) + BASE != s:
                fail("%s: slot %s does not hold funclet %s" % (fn, r["slot"], r["funclet"]))
                return
            pdx = pdata_entry(parent)
            if not pdx or pdx[0] != parent:
                fail("%s: parent %s has no .pdata entry of its own" % (fn, r["parent"]))
                return
            u = pdx[2]
            o = off(u)
            flags, cnt = d[o] >> 3, d[o + 2]
            if not flags & 3:
                fail("%s: parent %s unwind record has no handler" % (fn, r["parent"]))
                return
            fi = u32(u + 4 + ((cnt + 1) & ~1) * 2 + 4) + BASE
            if u32(fi) & 0xFFFFFFF0 != 0x19930520:
                fail("%s: parent %s handler data is not a FuncInfo" % (fn, r["parent"]))
                return
            ms, um, ntb, tbm = u32(fi + 4), u32(fi + 8) + BASE, u32(fi + 12), u32(fi + 16) + BASE
            ok = any(um + 8 * i + 4 == slot for i in range(ms))
            for t in range(ntb):
                te = tbm + 20 * t
                nc, ha = u32(te + 12), u32(te + 16) + BASE
                ok = ok or any(ha + 20 * c + 12 == slot for c in range(nc))
            if not ok:
                fail("%s: slot %s is not an action/handler field of %s's FuncInfo %08X" % (fn, r["slot"], r["parent"], fi))
        elif k == "slot":
            site = H(r["site"])
            if site != H(r["table"]) + int(r.get("field", "0"), 16) + int(r.get("stride", "0"), 16) * r.get("index", 0):
                fail("%s: site %s is not table %s + field + stride * index" % (fn, r["site"], r["table"]))
            v = u64(site) if r["width"] == 8 else u32(site) + BASE
            if v != H(fn):
                fail("%s: cell %s holds %08X, not the body" % (fn, r["site"], v))
            if r.get("counted") and not u32(H(r["table"])) > r.get("index", 0):
                fail("%s: index %d is not below the count dword at %s" % (fn, r.get("index", 0), r["table"]))
            if r.get("via"):
                vs, vv = H(r["via"]["site"]), H(r["via"]["value"])
                if u64(vs) != vv:
                    fail("%s: qword %s does not hold %s" % (fn, r["via"]["site"], r["via"]["value"]))
        elif k == "catchable":
            f = H(r["thrower"])
            n = sizes.get(f)
            ti, ct = H(r["throwinfo"]), H(r["catchable"])
            i2 = decode(f, n).get(H(r["throw_site"])) if n else None
            if i2 is None or not forms(i2, ti):
                fail("%s: %s does not form ThrowInfo %s" % (fn, r["throw_site"], r["throwinfo"]))
                return
            cta = u32(ti + 0xC) + BASE
            cts = [u32(cta + 4 + 4 * i) + BASE for i in range(u32(cta))]
            if ct not in cts:
                fail("%s: CatchableType %s not in array %08X" % (fn, r["catchable"], cta))
            elif u32(ct + 0x18) + BASE != H(fn):
                fail("%s: CatchableType %s copy function is not the body" % (fn, r["catchable"]))
        else:
            fail("%s: unknown ref kind %s" % (fn, k))
    except Exception as e:  # noqa: BLE001
        fail("%s: reference check raised %s" % (fn, e))


seen = set()
for r in ROWS:
    fn, t, anchors = r["fn"], r["text"], r["anchors"]
    f = int(fn, 16)
    n = sizes.get(f)
    if fn in seen:
        fail("%s: duplicate row" % fn)
    seen.add(fn)
    if not n:
        fail("%s: not a function entry" % fn)
        continue
    if "|" in t:
        fail("%s: pipe in text" % fn)
    if not t.strip() or len(t) >= 1200:
        fail("%s: text length %d" % (fn, len(t)))
    if not (1 <= len(anchors) <= 5):
        fail("%s: %d anchors (want 1-5)" % (fn, len(anchors)))
    if re.search(r"`%s`" % fn, outside):
        fail("%s: already cited on the page outside this block" % fn)
    ins = {i.address: i.mnemonic for i in md.disasm(d[off(f):off(f) + n], f)}
    for a, mn in anchors:
        av = int(a, 16)
        if not (f < av < f + n):
            fail("%s: anchor %s outside the body (or at its entry)" % (fn, a))
        elif ins.get(av) != mn:
            fail("%s: %s decodes to %r, recorded %r" % (fn, a, ins.get(av), mn))
    check_ref(fn, r["ref"])
    for tok in r.get("cites", []):
        if not re.search(r"(?<![0-9A-Za-z_])(0x)?%s(?![0-9A-Za-z_])" % re.escape(tok), outside):
            fail("%s: page does not cite %s" % (fn, tok))
print("VERIFY %d functions, %d anchors, %d references, page %s (%s)" % (
    len(ROWS), sum(len(r["anchors"]) for r in ROWS), len(ROWS), REL, "CRLF" if crlf else "LF"))

if not fails:
    body = (HEADING + "\n\n" + NOTE + "\n\n| function | size | what the body does | interior anchors |\n|---|---|---|---|\n"
            + "".join("| `%s` | %d B | %s | %s |\n" % (r["fn"], sizes[int(r["fn"], 16)], r["text"],
                                                       "; ".join("Interior anchor `%s`" % a for a, _m in r["anchors"]))
                      for r in ROWS))
    s = body.encode("utf-8")
    if crlf:
        s = s.replace(b"\n", b"\r\n")
    key = HEADING.encode("utf-8")
    if key in raw:
        i = raw.index(key)
        old = raw[i:]
        if old.rstrip(b"\r\n") == s.rstrip(b"\r\n"):
            print("ALREADY")
        elif raw.count(key) != 1 or not old.rstrip(b"\r\n").endswith(b"|"):
            fail("existing block is not the last section of the page; refusing to re-render")
        elif "--apply" not in sys.argv:
            print("DRY (block differs from rows.json; --apply re-renders it)")
        else:
            open(P, "wb").write(raw[:i] + s)
            print("REWRITTEN")
    elif "--apply" not in sys.argv:
        print("DRY (verified; --apply appends %d rows)" % len(ROWS))
    else:
        nl = b"\r\n" if crlf else b"\n"
        open(P, "wb").write(raw.rstrip(b"\r\n") + nl + nl + s)
        print("PATCHED")
print("FAILS", fails)
sys.exit(1 if fails else 0)
