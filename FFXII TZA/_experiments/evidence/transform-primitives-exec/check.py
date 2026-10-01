# EXP-115 transform-primitives-exec
#
# Executes the SHIPPED bytes of the two transform primitives named in
# CONTRACT-transform-primitives (section 13 "any runtime observation
# of either function EXECUTING: none | UNKNOWN"):
#
#   00398F90  TPT   TransformPointByWorkbenchMatrix(in=rcx, out=rdx).
#                   377 B, zero calls — true leaf. out[j] =
#                   i0*M[0*4+j] + i1*M[4+j] + i2*M[8+j] + leaf3*M[12+j]
#                   over the workbench matrix M = vec4[0x22D91B0..0xEF];
#                   the w operand is NOT in[3] — it is the fourth lane
#                   of the leaf global f[0x1EF93FC] (same global the
#                   EXP-114 LEAF resets to shipped [0,0,0,1]).
#                   Side writes: scratch partials -> vec4[0x22D91A0]
#                   (the i0/i1/i2 sums WITHOUT the M[12+] term), input
#                   copy -> vec4[0x22D9300], result -> vec4[0x22D9310]
#                   and -> vec4[0x22D8F90] and -> [rdx].
#
#   00397910  CT    ComposeTransforms(a=rcx, b=rdx, out=r8).
#                   567 B, sole callee 00808C40 __security_check_cookie
#                   (executed real — the shipped cookie lives in image
#                   data at q[0x1F44830]; a mismatch would tail-call
#                   __report_gsfailure and fault on the unmapped CRT
#                   path, which is itself observable).
#                   out = B * A (row-major): out[4r+j] =
#                   a[j]*b[4r] + a[4+j]*b[4r+1] + a[8+j]*b[4r+2]
#                   + a[12+j]*b[4r+3], each lane accumulated left to
#                   right. a staged at [rsp+0x40..0x7F], b staged at
#                   [rsp+0x00..0x3F] BEFORE any multiply -> aliasing
#                   safe (out == a / out == b / out == a == b all
#                   produce the distinct-buffer result). b rows 2/3
#                   held in xmm8..15 across the 4-pass column loop;
#                   b rows 0/1 re-read from the staged copy per pass.
#
# Scripted boundaries: none. 00808C40 runs real (EXP-100 already
# executed it); the GS-failure path is reached only by mutants and
# faults into the unmapped CRT tail, recorded as a fault.
#
# Trace tokens: ck<match> = 00808C40 reached with rcx==cookie.
#
# BSS globals (image-mapped; the matrix and leaf are fixture inputs):
#   M      = vec4[0x22D91B0..0x22D91EF]  workbench matrix
#   LEAF_G = vec4[0x1EF93F0]             element 3 = the w operand
#   COOKIE = q[0x1F44830]                shipped 0x00002B992DDFA232
#   scratch windows: 0x22D91A0, 0x22D9300..0x22D931F, 0x22D8F90

import ctypes, hashlib, json, math, os, struct, sys

from unicorn import UC_ARCH_X86, UC_HOOK_CODE, UC_HOOK_MEM_UNMAPPED, \
    UC_MODE_64, UC_PROT_ALL, Uc
from unicorn.x86_const import UC_X86_REG_R8, UC_X86_REG_RCX, \
    UC_X86_REG_RDX, UC_X86_REG_RIP, UC_X86_REG_RSP

EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
IMG_LO, IMG_HI = 0x120000, 0x2F800000
RESULT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "result.json")

HEAP   = 0x40000000
STACK  = 0x61000000
RETQ   = 0x62000000

TPT    = 0x00398F90
CT     = 0x00397910
CHKCK  = 0x00808C40      # __security_check_cookie (real)
GSFAIL = 0x00809654      # __report_gsfailure — abort path, fault token

# globals (image region)
M      = 0x022D91B0      # 4x4 workbench matrix (TPT input)
SCR    = 0x022D91A0      # scratch partials vec4
INCPY  = 0x022D9300      # TPT input copy
OUTCPY = 0x022D9310      # TPT assembled result vec4
OUTG   = 0x022D8F90      # TPT result global copy
LEAF_G = 0x01EF93F0      # vec4 — element 3 is TPT's w operand
COOKIE = 0x01F44830      # __security_cookie global
OBS_LO = 0x022D8F80      # observed globals window
OBS_HI = 0x022D9330

# heap layout
INBUF  = HEAP + 0x00000  # TPT in vec4
OUTBUF = HEAP + 0x01000  # TPT out vec4
MA     = HEAP + 0x10000  # CT matrix a (64 B)
MB     = HEAP + 0x20000  # CT matrix b (64 B)
MO     = HEAP + 0x30000  # CT out (64 B)


def qw(v): return struct.pack("<Q", v & 0xFFFFFFFFFFFFFFFF)
def dw(v): return struct.pack("<I", v & 0xFFFFFFFF)
def f32(x):
    return struct.unpack("<f", struct.pack("<f", x))[0]
def fbits(x):
    return struct.unpack("<I", struct.pack("<f", x))[0]
def bits2f(b):
    return struct.unpack("<f", struct.pack("<I", b & 0xFFFFFFFF))[0]
def fm(a, b): return f32(f32(a) * f32(b))
def fa(a, b): return f32(f32(a) + f32(b))


def load_image():
    raw = open(EXE, "rb").read()
    assert hashlib.sha256(raw).hexdigest() == SHA, "EXE hash mismatch"
    pe = struct.unpack_from("<I", raw, 0x3C)[0]
    nsec = struct.unpack_from("<H", raw, pe + 6)[0]
    optsz = struct.unpack_from("<H", raw, pe + 20)[0]
    secs, off = [], pe + 24 + optsz
    for _ in range(nsec):
        vs, va, rs, ra = struct.unpack_from("<IIII", raw, off + 8)
        secs.append((va, vs, ra, rs))
        off += 40
    return raw, secs


def img_rd(raw, secs, va, n):
    rva = va - IMG_LO
    for sva, vs, ra, rs in secs:
        if sva <= rva and rva + n <= sva + rs:
            return raw[ra + (rva - sva): ra + (rva - sva) + n]
    raise KeyError("image read outside shipped bytes: %x" % va)


def img_dw(raw, secs, va):
    return struct.unpack("<I", img_rd(raw, secs, va, 4))[0]


def img_f(raw, secs, va):
    return bits2f(img_dw(raw, secs, va))


def img_qw(raw, secs, va):
    return struct.unpack("<Q", img_rd(raw, secs, va, 8))[0]


def img_rd_or_zero(raw, secs, va, n):
    try:
        return img_rd(raw, secs, va, n)
    except KeyError:
        return b"\0" * n


class GuestMem:
    def __init__(self, uc):
        self.uc, self.bufs, self.regions = uc, [], []
    def map(self, addr, size, init=b""):
        buf = ctypes.create_string_buffer(size)
        if init:
            ctypes.memmove(buf, init, min(len(init), size))
        self.bufs.append(buf)
        self.uc.mem_map_ptr(addr, size, UC_PROT_ALL, ctypes.addressof(buf))
        self.regions.append((addr, size, ctypes.addressof(buf)))
    def _ptr(self, addr, n):
        for base, size, ptr in self.regions:
            if base <= addr and addr + n <= base + size:
                return ptr + (addr - base)
        raise KeyError("fixture access to unmapped guest addr %x" % addr)
    def w(self, addr, data):
        ctypes.memmove(self._ptr(addr, len(data)), bytes(data), len(data))
    def r(self, addr, n):
        return ctypes.string_at(self._ptr(addr, n), n)


# ---------------- fixture shapes ----------------

def default_matrix():
    """A general 4x4 with distinct, non-round entries (row-major)."""
    return [1.25, -0.5, 0.75, 2.0,
            0.5, 1.5, -1.0, 0.25,
            -0.75, 0.125, 2.5, 1.0,
            10.0, 20.0, 30.0, 1.0]


def default_invec():
    return [3.0, -2.0, 0.5, 7.0]   # element 3 deliberately != 1


def default_mata():
    return [float((i * 37) % 11) - 5.0 + i * 0.25 for i in range(16)]


def default_matb():
    return [float((i * 23) % 13) - 6.0 + i * 0.125 for i in range(16)]


def vec_w(gm, addr, vals):
    for k, fv in enumerate(vals):
        gm.w(addr + k * 4, struct.pack("<f", fv))


def vec_r(gm, addr, n=4):
    return list(struct.unpack("<%df" % n, gm.r(addr, n * 4)))


class World:
    def __init__(self, case, raw, secs):
        self.case = case
        self.raw, self.secs = raw, secs
        self.uc = Uc(UC_ARCH_X86, UC_MODE_64)
        gm = self.gm = GuestMem(self.uc)
        gm.map(IMG_LO, IMG_HI - IMG_LO)
        for sva, vs, ra, rs in secs:
            if vs and rs:
                gm.w(IMG_LO + sva, raw[ra:ra + min(rs, vs)])
        gm.map(HEAP, 0x1000000)
        gm.map(STACK, 0x100000)
        gm.map(RETQ, 0x1000)

        # ---- TPT fixture ----
        vec_w(gm, M, case.get("mat", default_matrix()))
        vec_w(gm, LEAF_G, case.get("leaf", [0.0, 0.0, 0.0, 1.0]))
        vec_w(gm, INBUF, case.get("invec", default_invec()))
        vec_w(gm, OUTBUF, case.get("outinit", [-9.0] * 4))
        vec_w(gm, SCR, [-7.0] * 4)
        vec_w(gm, INCPY, [-7.0] * 4)
        vec_w(gm, OUTCPY, [-7.0] * 4)
        vec_w(gm, OUTG, [-7.0] * 4)

        # ---- CT fixture ----
        for k, fv in enumerate(case.get("mata", default_mata())):
            gm.w(MA + k * 4, struct.pack("<f", fv))
        for k, fv in enumerate(case.get("matb", default_matb())):
            gm.w(MB + k * 4, struct.pack("<f", fv))
        for k, fv in enumerate(case.get("moinit", [-8.0] * 16)):
            gm.w(MO + k * 4, struct.pack("<f", fv))

        for addr, dat in case.get("patch_bytes", []):
            gm.w(addr, dat)

        self.trace, self.faults = [], []
        self.uc.hook_add(UC_HOOK_CODE, self.on_code)
        self.uc.hook_add(UC_HOOK_MEM_UNMAPPED, self.on_bad)

    def on_code(self, uc, addr, size, _):
        if addr == CHKCK:
            rcx = uc.reg_read(UC_X86_REG_RCX)
            ck = img_qw(self.raw, self.secs, COOKIE)
            self.trace.append("ck" + ("ok" if rcx == ck else
                                      "BAD:%x" % rcx))
        elif addr == GSFAIL:
            # reached __report_gsfailure — the process would abort;
            # record the divergent observable and stop
            self.trace.append("gsfail")
            self.faults.append(("gsfail", addr, 0))
            uc.reg_write(UC_X86_REG_RIP, RETQ)

    def on_bad(self, uc, access, addr, size, value, _):
        self.faults.append((access, addr, size))
        uc.reg_write(UC_X86_REG_RIP, RETQ)
        return True

    # ---- run ----
    def run(self, case):
        uc = self.uc
        entry = case["entry"]
        self.gm.w(RETQ, b"\xc3" * 0x100)
        rsp = STACK + 0x80000
        self.gm.w(rsp, qw(RETQ))
        uc.reg_write(UC_X86_REG_RSP, rsp)
        if entry == TPT:
            uc.reg_write(UC_X86_REG_RCX, case.get("rcx", INBUF))
            uc.reg_write(UC_X86_REG_RDX, case.get("rdx", OUTBUF))
        else:
            uc.reg_write(UC_X86_REG_RCX, case.get("rcx", MA))
            uc.reg_write(UC_X86_REG_RDX, case.get("rdx", MB))
            uc.reg_write(UC_X86_REG_R8, case.get("r8", MO))
        uc.emu_start(entry, RETQ, count=4000)

    # ---- observation ----
    def obs(self):
        gm = self.gm
        o = {"trace": self.trace, "faults": self.faults,
             "globs": gm.r(OBS_LO, OBS_HI - OBS_LO).hex()}
        if self.case["entry"] == TPT:
            o["out"] = gm.r(self.case.get("rdx", OUTBUF), 16).hex()
        else:
            o["out"] = gm.r(self.case.get("r8", MO), 64).hex()
        return o


# ---------------- Python model ----------------

def tpt_model(mat, invec, leaf3):
    """out[j] = i0*M[j] + i1*M[4+j] + i2*M[8+j] + leaf3*M[12+j],
    accumulated in the body's own left-to-right order; the M[12+]
    term is added last (addss xmm1, xmmN — commutative)."""
    i0, i1, i2 = invec[0], invec[1], invec[2]
    out = []
    for j in range(4):
        p = fm(i0, mat[j])
        p = fa(p, fm(i1, mat[4 + j]))
        p = fa(p, fm(i2, mat[8 + j]))
        out.append(fa(fm(leaf3, mat[12 + j]), p))
    return out


def ct_model(a, b):
    """out[4r+j] = a[j]*b[4r] + a[4+j]*b[4r+1] + a[8+j]*b[4r+2] +
    a[12+j]*b[4r+3] — sequential f32 adds in the body's order."""
    out = [0.0] * 16
    for j in range(4):
        for r in range(4):
            p = fm(a[j], b[4 * r])
            p = fa(p, fm(a[4 + j], b[4 * r + 1]))
            p = fa(p, fm(a[8 + j], b[4 * r + 2]))
            p = fa(p, fm(a[12 + j], b[4 * r + 3]))
            out[4 * r + j] = p
    return out


def run_model(case):
    """Expected observables for a case dict."""
    raw, secs = load_image()
    entry = case["entry"]
    o = {"trace": ["ckok"] if entry == CT else [],
         "faults": []}
    globs = bytearray(img_rd_or_zero(raw, secs, OBS_LO, OBS_HI - OBS_LO))
    if entry == TPT:
        mat = case.get("mat", default_matrix())
        invec = case.get("invec", default_invec())
        leaf3 = case.get("leaf", [0.0, 0.0, 0.0, 1.0])[3]
        out = tpt_model(mat, invec, leaf3)
        i0 = invec[0]
        part = [fa(fa(fm(i0, mat[j]), fm(invec[1], mat[4 + j])),
                   fm(invec[2], mat[8 + j])) for j in range(4)]
        struct.pack_into("<4f", globs, SCR - OBS_LO, *part)
        struct.pack_into("<4f", globs, INCPY - OBS_LO, *invec)
        struct.pack_into("<4f", globs, OUTCPY - OBS_LO, *out)
        struct.pack_into("<4f", globs, OUTG - OBS_LO, *out)
        # the matrix + leaf inputs the body reads are inside the window
        struct.pack_into("<4f", globs, M - OBS_LO, *mat[:4])
        struct.pack_into("<4f", globs, M + 16 - OBS_LO, *mat[4:8])
        struct.pack_into("<4f", globs, M + 32 - OBS_LO, *mat[8:12])
        struct.pack_into("<4f", globs, M + 48 - OBS_LO, *mat[12:16])
        # the [rdx] store lands inside the window when rdx = M
        rdx = case.get("rdx", OUTBUF)
        if OBS_LO <= rdx <= OBS_HI - 16:
            struct.pack_into("<4f", globs, rdx - OBS_LO, *out)
        o["out"] = b"".join(struct.pack("<f", v) for v in out).hex()
    else:
        mata = case.get("mata", default_mata())
        matb = case.get("matb", default_matb())
        # resolve b through rdx (the register the body actually reads);
        # rcx is always MA in these cases so a == mata
        b = mata if case.get("rdx", MB) == MA else matb
        out = ct_model(mata, b)
        struct.pack_into("<4f", globs, M - OBS_LO,
                         *case.get("mat", default_matrix())[:4])
        struct.pack_into("<4f", globs, M + 16 - OBS_LO,
                         *case.get("mat", default_matrix())[4:8])
        struct.pack_into("<4f", globs, M + 32 - OBS_LO,
                         *case.get("mat", default_matrix())[8:12])
        struct.pack_into("<4f", globs, M + 48 - OBS_LO,
                         *case.get("mat", default_matrix())[12:16])
        # CT touches no globals — scratch keeps fixture init
        struct.pack_into("<4f", globs, SCR - OBS_LO, *([-7.0] * 4))
        struct.pack_into("<4f", globs, INCPY - OBS_LO, *([-7.0] * 4))
        struct.pack_into("<4f", globs, OUTCPY - OBS_LO, *([-7.0] * 4))
        struct.pack_into("<4f", globs, OUTG - OBS_LO, *([-7.0] * 4))
        o["out"] = b"".join(struct.pack("<f", v) for v in out).hex()
    o["globs"] = bytes(globs).hex()
    return o


# ---------------- cases ----------------

def build_cases():
    C = {}
    ident = [1.0, 0, 0, 0, 0, 1.0, 0, 0, 0, 0, 1.0, 0, 0, 0, 0, 1.0]
    tran = [1.0, 0, 0, 0, 0, 1.0, 0, 0, 0, 0, 1.0, 0,
            10.0, 20.0, 30.0, 1.0]
    scal = [2.0, 0, 0, 0, 0, 3.0, 0, 0, 0, 0, 4.0, 0, 0, 0, 0, 1.0]

    C["tpt-ident"] = {"entry": TPT, "mat": ident}
    C["tpt-scale"] = {"entry": TPT, "mat": scal}
    C["tpt-tran"] = {"entry": TPT, "mat": tran}
    C["tpt-general"] = {"entry": TPT}
    C["tpt-w-ignored"] = {"entry": TPT,
                          "invec": [3.0, -2.0, 0.5, 99.0]}
    C["tpt-w-zero"] = {"entry": TPT,
                       "invec": [3.0, -2.0, 0.5, 0.0]}
    C["tpt-leaf2"] = {"entry": TPT,
                      "leaf": [0.0, 0.0, 0.0, 2.0]}
    C["tpt-leaf0"] = {"entry": TPT,
                      "leaf": [0.0, 0.0, 0.0, 0.0]}
    C["tpt-zero-in"] = {"entry": TPT, "invec": [0.0] * 4}
    C["tpt-neg"] = {"entry": TPT, "invec": [-1.5, -2.5, -3.5, 1.0]}
    C["tpt-inf"] = {"entry": TPT,
                    "invec": [float("inf"), 1.0, 2.0, 1.0]}
    C["tpt-nan"] = {"entry": TPT,
                    "invec": [float("nan"), 1.0, 2.0, 1.0]}
    C["tpt-alias"] = {"entry": TPT, "rdx": INBUF}  # out == in
    C["tpt-out-mat"] = {"entry": TPT, "rdx": M}    # out over matrix

    # CT
    C["ct-ident-a"] = {"entry": CT, "mata": ident}
    C["ct-ident-b"] = {"entry": CT, "matb": ident}
    C["ct-ident-both"] = {"entry": CT, "mata": ident, "matb": ident}
    C["ct-general"] = {"entry": CT}
    C["ct-scal"] = {"entry": CT, "mata": scal, "matb": scal}
    C["ct-zero-a"] = {"entry": CT, "mata": [0.0] * 16}
    C["ct-alias-a"] = {"entry": CT, "r8": MA}      # out == a
    C["ct-alias-b"] = {"entry": CT, "r8": MB}      # out == b
    C["ct-alias-ab"] = {"entry": CT, "r8": MA, "rdx": MA}  # a==b==out
    C["ct-neg"] = {"entry": CT,
                   "mata": [-v for v in default_mata()],
                   "matb": [-v for v in default_matb()]}
    return C


# ---------------- mutations (verified byte-precise) ----------------

def B(x): return bytes([x])

MUTS = [
    # TPT — shuffle immediates broadcast the wrong input lane
    ("m-t-sh55",   0x398FB8, B(0x55), B(0x54), "tpt-general"),
    ("m-t-sh00",   0x398FC0, B(0x00), B(0x01), "tpt-general"),
    ("m-t-shaa",   0x399019, B(0xAA), B(0xA9), "tpt-general"),
    # TPT — muls/adds swapped
    ("m-t-mul1",   0x398FBB, B(0x59), B(0x58), "tpt-general"),
    ("m-t-mulp",   0x398FC2, B(0x59), B(0x58), "tpt-general"),
    ("m-t-add1",   0x398FE1, B(0x58), B(0x5C), "tpt-general"),
    ("m-t-mulm",   0x399030, B(0x59), B(0x58), "tpt-general"),
    # TPT — matrix/w operand displacement errors
    ("m-t-matd",   0x398F97, B(0x15), B(0x25), "tpt-general"),
    ("m-t-leafd",  0x39902A, B(0xCE), B(0xCA), "tpt-general"),
    ("m-t-stored", 0x3990FD, B(0x8F), B(0x90), "tpt-general"),
    # CT — loop structure
    ("m-c-r10",    0x397985, B(0x04), B(0x03), "ct-general"),
    ("m-c-stride", 0x397AE8, B(0x04), B(0x08), "ct-general"),
    ("m-c-jne",    0x397AEE, B(0x85), B(0x84), "ct-general"),
    # CT — wrong b element / a row
    ("m-c-bdisp",  0x397A24, B(0x04), B(0x08), "ct-general"),
    ("m-c-b10",    0x397A4D, B(0x10), B(0x14), "ct-general"),
    ("m-c-arow",   0x397A15, B(0xE0), B(0xF0), "ct-general"),
    ("m-c-x15d",   0x3979BA, B(0x2C), B(0x30), "ct-general"),
    # CT — arithmetic
    ("m-c-mul",    0x397A21, B(0x59), B(0x58), "ct-general"),
    ("m-c-add",    0x397A46, B(0x58), B(0x5C), "ct-general"),
    # CT — store row displacement
    ("m-c-strow",  0x397A79, B(0xE0), B(0xF0), "ct-general"),
    # CT — cookie integrity (stored=0 -> gsfailure fault)
    ("m-c-cookie", 0x397961, B(0xC4), B(0xC0), "ct-general"),
]


def run_native(case):
    raw, secs = load_image()
    w = World(case, raw, secs)
    w.run(case)
    return w.obs()


def main():
    cases = build_cases()
    keys = ("trace", "out", "globs", "faults")
    results = {"cases": {}, "mutants": {}, "bad_sites": []}
    fails = 0
    for name, case in cases.items():
        nat = run_native(case)
        mod = run_model(case)
        d = [k for k in keys if k in nat and nat[k] != mod.get(k)]
        results["cases"][name] = "ok" if not d else {"diff": d}
        if d:
            fails += 1
            print("CASE", name, "DIFF", d)
            for k in d:
                print("  nat:", str(nat.get(k))[:170])
                print("  mod:", str(mod.get(k))[:170])
    print("functional: %d/%d" % (len(cases) - fails, len(cases)))

    raw, secs = load_image()
    for mid, va, orig, mut, cname in MUTS:
        got = img_rd(raw, secs, va, len(orig))
        if got != orig:
            results["bad_sites"].append((mid, hex(va), got.hex()))
            print("BAD SITE", mid, hex(va), "want", orig.hex(),
                  "got", got.hex())
    if results["bad_sites"]:
        print("aborting mutant run — fix sites first")
        json.dump(results, open(RESULT, "w"), indent=1)
        return

    alive = 0
    for mid, va, orig, mut, cname in MUTS:
        case = dict(cases[cname])
        case["patch_bytes"] = list(case.get("patch_bytes", [])) + [(va, mut)]
        try:
            nat = run_native(case)
        except Exception as e:
            print("MUTANT CRASH", mid, repr(e), flush=True)
            results["mutants"][mid] = "crash: %r" % e
            continue
        mod = run_model(case)
        if [k for k in keys if k in nat and nat[k] != mod.get(k)]:
            results["mutants"][mid] = "killed"
        else:
            results["mutants"][mid] = "ALIVE"
            alive += 1
            print("MUTANT ALIVE", mid, flush=True)
    print("mutants: %d/%d killed" % (len(MUTS) - alive, len(MUTS)))
    json.dump(results, open(RESULT, "w"), indent=1)


if __name__ == "__main__":
    main()
