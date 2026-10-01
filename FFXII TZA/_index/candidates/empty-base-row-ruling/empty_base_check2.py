"""empty_base_check2.py - (v2: variants built from the current store, on OPUS-NOTICE-FABLE-EMPTY-BASE-CHECK-C-STATE) OPUS-REQ-FABLE-EMPTY-BASE-ROW: how the store writes an empty base that takes zero bytes
(FABLE, Claude Opus 5.5, 2026-09-28). The live store is read, never written; the trial rows go into a scratch copy.

  E1 the premise, from the certified image's bytes: 00616880, 00616900 and 0062BAB0 each load the qword at [rbx+0],
     test it, call [its vtable + 0x10] (IUnknown::Release, slot 2) and store 0 there - so +0x00..+0x07 is a COM pointer
     member of PShaderProgramD3D11, not a vptr, and the empty base PShaderProgramBase (instance size 1) takes no bytes
  E2 the ruled rows - base row size 0 with ctype 'PShaderProgramBase[0]' and a meaning opening 'EMPTY BASE', then the
     8-byte member at +0x000 - add no error to types_index --validate and no size disagreement to
     check_embed_parent_fields PASS 2, against the live store's own counts
  C  controls on the same scratch copy: size 0 with the bare ctype 'PShaderProgramBase' is flagged by PASS 2 (delta);
     keeping the 1-byte base row with the 8-byte member at +0x000 is flagged by types_index as an overlap
"""
import hashlib, os, re, shutil, struct, subprocess, sys, tempfile
import capstone
HERE = os.path.dirname(os.path.abspath(__file__)); DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
KIT = os.path.join(DB, "..", "Tools", "analysis-kit", "gfz-scripts")
EXE = os.environ.get("FFXII_EXE", os.path.join(DB, "..", "Tools", "work", "exe", "FFXII_TZA.exe"))
d = open(EXE, "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8": print("REFUSED  not the certified image"); sys.exit(2)
pe = struct.unpack_from("<I", d, 0x3c)[0]; ns = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + 40 * i + 8) for i in range(ns)]
off = lambda v: next(ra + v - 0x120000 - va for vs, va, rs, ra in SECS if va <= v - 0x120000 < va + rs)
MD = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
fails = 0
def ok(tag, cond, msg):
    global fails
    print(("PASS " if cond else "FAIL ") + tag + "  " + msg); fails += (not cond)
def releases_plus0(a):
    ins = [(i.mnemonic + " " + i.op_str).strip() for i in MD.disasm(d[off(a):off(a) + 0xC0], a)]
    for k, s in enumerate(ins):
        m = re.match(r"mov (r\w+), qword ptr \[(r\w+)\]$", s)
        if m and m.group(2) != "rsp":
            rc, base = m.groups(); w = ins[k + 1:k + 7]
            if ("test %s, %s" % (rc, rc)) in w and "call qword ptr [rax + 0x10]" in w and any(re.match(r"mov qword ptr \[%s\], (r\w+|0)$" % base, x) for x in w):
                return True
    return False
E1 = {"%08X" % a: releases_plus0(a) for a in (0x616880, 0x616900, 0x62BAB0)}
ok("E1", all(E1.values()), "each destructor releases the qword at +0 through slot +0x10 and zeroes it: %s" % E1)

src = os.environ.get("TYPES_DIR", os.path.join(DB, "_types"))   # a store from another revision, for replay
def trial(edit):
    t = tempfile.mkdtemp(prefix="emptybase_")
    os.makedirs(os.path.join(t, "_types"))
    for f in ("types.tsv", "fields.tsv"): shutil.copyfile(os.path.join(src, f), os.path.join(t, "_types", f))
    p = os.path.join(t, "_types", "fields.tsv"); rows = open(p, encoding="utf-8", newline="").read().split("\n")
    rows = edit(rows); open(p, "w", encoding="utf-8", newline="").write("\n".join(rows))
    v = subprocess.run([sys.executable, os.path.join(KIT, "types_index.py"), "--store", os.path.join(t, "_types"), "--validate"], capture_output=True, text=True, encoding="utf-8", errors="replace").stdout
    e = subprocess.run([sys.executable, os.path.join(KIT, "check_embed_parent_fields.py"), "--types", os.path.join(t, "_types", "types.tsv"), "--fields", p], capture_output=True, text=True, encoding="utf-8", errors="replace").stdout
    shutil.rmtree(t)
    errs = [l for l in v.splitlines() if "PShaderProgramD3D11 " in l and ("overlap" in l or "overrun" in l or "gap" in l)]
    mism = [l for l in e.splitlines() if "PShaderProgramD3D11" in l and "ctype" in l]
    return errs, mism
BASE = ("PShaderProgramD3D11", "baseClass_PShaderProgramBase")
def variant(base_size, base_ctype):
    """Build the variant from whatever the store holds: the base row found by type and name, the member normalised to one
    8-byte row at +0x0000 (a pre-ruling +0x0001 7-byte span is widened), so the trial is the same before and after OPUS applies."""
    def edit(rows):
        out = []
        for r in rows:
            c = r.split("	")
            if len(c) > 5 and c[0] == BASE[0] and c[3] == BASE[1]:
                c[2] = base_size; c[4] = base_ctype
                if base_size == "0" and not c[5].startswith("EMPTY BASE"): c[5] = "EMPTY BASE (zero bytes here by the MSVC empty-base optimization). " + c[5]
                out.append("	".join(c))
            elif len(c) > 5 and c[0] == BASE[0] and c[1] == "0x0001" and c[2] == "7":
                c[1], c[2] = "0x0000", "8"; out.append("	".join(c))
            else: out.append(r)
        return out
    return edit
ruled = trial(variant("0", "PShaderProgramBase[0]"))
ok("E2", ruled == ([], []), "the ruled rows, built from the current store: types_index errors %d, PASS 2 disagreements %d" % (len(ruled[0]), len(ruled[1])))
bare = trial(variant("0", "PShaderProgramBase"))
keep1 = trial(variant("1", "PShaderProgramBase"))
ok("C", len(bare[1]) > len(ruled[1]) and len(keep1[0]) > len(ruled[0]),
   "bare ctype at size 0 adds %d PASS-2 disagreement(s); a 1-byte base under the 8-byte member adds %d types_index error(s)"
   % (len(bare[1]) - len(ruled[1]), len(keep1[0]) - len(ruled[0])))
print("FAILS", fails); sys.exit(1 if fails else 0)
