"""rv_xfer.py - FABLE independent re-derivation for ASTRA packet ov42-interpreter-transfer (76dfc5dc6, OV-42).

Own reader (rvlib.py: struct + capstone 5, copied unchanged from the kind-row review, sha256 69f9bc40be32abcc...).
Does not import or run ASTRA's prove.py, capture.py, control.py, validation scripts or the shared role adapter.

Method:
  * image sha256; manifest + every member against the committed manifest;
  * the bridge leaf 00309C00 (no .pdata: a leaf): the queue read, the -1 test, the raw DWORD store through RDX, the
    unit DWORD through RCX, the queue reset; a raw E8/E9 census of its direct callers;
  * the native 00348330: two pops each resolved by 002650B0, the first result kept in RSI and passed as RDX;
  * the reference getter 002650B0: scope = bits 24..26, offset = low 24 bits, six bases plus a base-0 default;
  * PUSHV 00267FC0: width = bits 28..31, the six-entry jump table, the six loads, the kind-1 / kind-2 pushes and the
    depth bound; the pop 00267E10: tag 1 DWORD, tag 2 CVTTSS2SI, empty -> 0, other tags -> the error call;
    00348870: first pop -> EBX -> EDX, second pop -> ECX, then 0030EEA0; the decoder 0030EEA0: -1 -> FFFF, else BX + 0xD0;
  * unicorn emulation of the ORIGINAL PUSHV (resolver stubbed to supply the record), pop and decoder (lookup stubbed):
    the end-to-end word for every available queue word at every width/kind, the 511..534 table, the float case;
  * controls patch a private in-memory copy of the image; the exe on disk is never written; sha256 rechecked.
"""
import hashlib
import os
import struct
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from rvlib import Img, Body, Report, expect, run_control, check_manifest, find_exe, SHA256  # noqa: E402

SLUG = "ov42-interpreter-transfer"
COMMIT = "76dfc5dc6b6d37731786c805775edda59394b7cd"
BRIDGE, NATIVE, GETTER, PUSHV, POP, ARGS, DEC = 0x309C00, 0x348330, 0x2650B0, 0x267FC0, 0x267E10, 0x348870, 0x30EEA0


def git(*a):
    return subprocess.run(["git"] + list(a), capture_output=True, cwd=os.path.dirname(find_exe())).stdout


def rip_target(I):
    for m in I.mems:
        if m["base"] == "rip":
            return I.address + I.size + m["disp"]
    return None


def static_checks(img, R):
    B = Body(img, BRIDGE, BRIDGE + 0x32)
    R.check("00309C00 decodes exactly to its second `ret` (+ 0x31) and has no .pdata entry (a leaf)",
            B.exact and B[0x309C31].mnemonic == "ret" and img.pdata(BRIDGE) is None)
    R.check("+ 0 reads DWORD 022C2178 (the queue)", rip_target(B[0x309C00]) == 0x22C2178 and B[0x309C00].mems[0]["size"] == 4)
    expect(R, B, 0x309C06, "cmp eax, -1")
    expect(R, B, 0x309C0B, "xor eax, eax", "queue -1: + 0xB returns 0 with no store")
    expect(R, B, 0x309C13, "mov dword ptr [rdx], eax", "+ 0x13 stores the queue DWORD raw through RDX (when RDX != 0)")
    R.check("+ 0x1A / + 0x20 store DWORD 022C218C through RCX (when RCX != 0)", rip_target(B[0x309C1A]) == 0x22C218C
            and B[0x309C20].text == "mov dword ptr [rcx], eax")
    R.check("+ 0x22 resets the queue to -1 and + 0x2C returns 1", rip_target(B[0x309C22]) == 0x22C2178
            and B[0x309C22].imm == [0xFFFFFFFF] and B[0x309C2C].text == "mov eax, 1")
    # direct callers
    txt = [s for s in img.secs if s[0] == ".text"][0]
    _, va, vs, ra, rs = txt
    data, base = img.d[ra:ra + rs], img.base + va
    hits = [base + i for i in range(len(data) - 5) if data[i] in (0xE8, 0xE9)
            and base + i + 5 + struct.unpack_from("<i", data, i + 1)[0] == BRIDGE]
    R.check("raw E8/E9 census: two direct calls of 00309C00, at 0034838A (00348330 + 0x5A) and 002D6175 (in the "
            "function rooted at 002D5EB0, a chained record from 002D616B)", hits == [0x2D6175, 0x34838A] and
            img.pdata_cover(0x2D616B, 0x2D6620)[0][0][3] == 0x2D5EB0, str([hex(h) for h in hits]))
    N = Body(img, NATIVE, 0x3483D5)
    for a, t in ((0x348355, "call 0x267e10"), (0x34835A, "mov r8d, eax"), (0x348363, "call 0x2650b0"),
                 (0x34836B, "mov rsi, rax"), (0x34836E, "call 0x267e10"), (0x348373, "mov r8d, eax"),
                 (0x34837C, "call 0x2650b0"), (0x348381, "mov rdx, rsi"), (0x348384, "mov rcx, rax"),
                 (0x34838A, "call 0x309c00")):
        expect(R, N, a, t)
    w = [a for a in N.order if 0x34836B < a < 0x348381 and "rsi" in N[a].reg_writes]
    R.check("RSI (the first resolved pointer) is not written between + 0x3B and + 0x51", not w)
    G = Body(img, GETTER, 0x26517E)
    for a, t in ((0x2650BC, "sar eax, 0x18"), (0x2650C2, "and eax, 7"), (0x2650C8, "cmp eax, 5"),
                 (0x2650CB, "ja 0x26516c"), (0x26516E, "xor ecx, ecx")):
        expect(R, G, a, t)
    masks = [a for a in G.order if G[a].text == "and eax, 0xffffff"]
    R.check("002650B0 masks the offset to 24 bits on all seven exits (six scopes + the base-0 default for scopes 6..7)",
            len(masks) == 7, str(len(masks)))
    reads = sorted(set(a for a in G.order if "r8" in G[a].reg_reads or "rbx" in G[a].reg_reads and G[a].mnemonic == "mov"))
    R.check("the reference word is used only through `sar 0x18` / `and 7` and the 24-bit mask: bits 27..31 are never"
            " tested", not any(G[a].mnemonic in ("bt", "test", "shr") for a in G.order))
    P = Body(img, PUSHV, 0x2680E8)
    R.check("PUSHV 00267FC0 decodes exactly to + 0x128; six DWORD jump entries follow (+ 0x128)", P.exact)
    expect(R, P, 0x267FE1, "shr eax, 0x1c", "width = DWORD [rbp - 0x18] >> 28 (+ 0x21)")
    expect(R, P, 0x267FE4, "cmp eax, 5")
    tab = [img.base + img.u32(0x2680E8 + 4 * k) for k in range(6)]
    want = [(0x267FFC, "movzx ecx, byte ptr [rcx + rax]"), (0x26800D, "movsx ecx, byte ptr [rcx + rax]"),
            (0x26801E, "movzx ecx, word ptr [rax + rcx*2]"), (0x26802F, "movsx ecx, word ptr [rax + rcx*2]"),
            (0x268040, "mov ecx, dword ptr [rax + rcx*4]"), (0x268050, "movss xmm0, dword ptr [rax + rcx*4]")]
    R.check("the six jump entries resolve to the u8, s8, u16, s16, s32 and f32 loads, in that order",
            tab == [a for a, _ in want] and all(P[a + 8].text == t for a, t in want), str([hex(x) for x in tab]))
    expect(R, P, 0x268062, "movsx ecx, word ptr [rbp - 0x2c]", "kind = WORD [rbp - 0x2C] (+ 0xA2), separate from width")
    expect(R, P, 0x2680B9, "mov byte ptr [rax + rbx + 4], 1", "kind 1 tags 1 (+ 0xF9)")
    expect(R, P, 0x2680C9, "mov dword ptr [rbx + rcx*4 + 0x184], eax", "kind 1 stores the payload DWORD (+ 0x109)")
    expect(R, P, 0x268080, "mov byte ptr [rax + rbx + 4], 2", "kind 2 tags 2 (+ 0xC0)")
    expect(R, P, 0x268098, "movss dword ptr [rbx + rcx*4 + 0x184], xmm0", "kind 2 stores the same payload bits (+ 0xD8)")
    R.check("both pushes require depth < 0x3F (+ 0xB3 / + 0xF4 `cmp eax, 0x3f`, `jge` skips)",
            P[0x268073].text == "cmp eax, 0x3f" and P[0x2680B1].text == "cmp eax, 0x3f")
    Q = Body(img, POP, 0x267E5E)
    for a, t in ((0x267E18, "jle 0x267e3b"), (0x267E1A, "dec eax"), (0x267E2A, "je 0x267e51"),
                 (0x267E36, "call 0x8620c0"), (0x267E42, "cvttss2si eax, dword ptr [rcx + r8*4 + 0x184]"),
                 (0x267E51, "mov eax, dword ptr [rcx + r8*4 + 0x184]")):
        expect(R, Q, a, t)
    A = Body(img, ARGS, 0x3488AC)
    for a, t in ((0x348880, "call 0x267e10"), (0x348888, "mov ebx, eax"), (0x34888A, "call 0x267e10"),
                 (0x34888F, "mov edx, ebx"), (0x348891, "mov ecx, eax"), (0x348893, "call 0x30eea0"),
                 (0x348898, "mov ecx, 1"), (0x3488A7, "jmp 0x314d40")):
        expect(R, A, a, t)
    R.check("00348870 discards the decoder's EAX (+ 0x28 overwrites ECX, EAX is not read before the tail jump)",
            not any("rax" in A[a].reg_reads for a in A.order if 0x348898 <= a <= 0x3488A7))
    D = Body(img, DEC, 0x30EF17)
    for a, t in ((0x30EEA6, "mov ebx, edx"), (0x30EEA8, "cmp edx, -1"), (0x30EEB2, "add bx, ax"),
                 (0x30EEB7, "mov ebx, 0xffff"), (0x30EEF9, "mov word ptr [rax + 0x758], bx"), (0x30EF00, "call 0x30cfb0")):
        expect(R, D, a, t)
    R.check("the decoded word reaches unit +0x758 and 0030CFB0 only when DWORD 022C2170 is 4 (+ 0x2F), after a non-null"
            " 0031B7E0(ECX); otherwise it returns -1 or -2", rip_target(D[0x30EECF]) == 0x22C2170 and
            D[0x30EECF].imm == [4] and D[0x30EEC6].text == "or eax, 0xffffffff" and D[0x30EED8].text == "mov eax, 0xfffffffe")


# ---------------------------------------------------------------- emulation
class Emu(object):
    def __init__(self, img):
        from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE
        from unicorn import x86_const as X
        self.X = X
        u = Uc(UC_ARCH_X86, UC_MODE_64)
        for lo, hi in ((0x260000, 0x270000), (0x300000, 0x320000), (0x340000, 0x350000)):
            u.mem_map(lo, hi - lo)
            u.mem_write(lo, img.read(lo, hi - lo))
        u.mem_map(0x22C2000, 0x1000)
        u.mem_map(0x862000, 0x1000)
        u.mem_write(0x8620C0, b"\xC3")
        u.mem_map(0x7000000, 0x100000)      # VM state, variables, unit
        u.mem_map(0x8000000, 0x100000)      # stack
        for stub in (0x262440, 0x31B7E0, 0x30CFB0):
            u.mem_write(stub, b"\xC3")
        u.hook_add(UC_HOOK_CODE, self._hook)
        self.u, self.rec, self.unit = u, None, 0x7080000
        self.called = []

    def _hook(self, uc, addr, size, ud):
        X = self.X
        if addr == 0x262440 and self.rec is not None:      # resolver stub: write the record at the 5th argument
            rsp = uc.reg_read(X.UC_X86_REG_RSP)
            rp = struct.unpack("<Q", uc.mem_read(rsp + 0x28, 8))[0]
            kind, width, ptr, idx = self.rec
            uc.mem_write(rp + 0x00, bytes([0x5A]))
            uc.mem_write(rp + 0x04, struct.pack("<h", kind))
            uc.mem_write(rp + 0x10, struct.pack("<Q", ptr))
            uc.mem_write(rp + 0x18, struct.pack("<I", width << 28))
            uc.mem_write(rp + 0x1C, struct.pack("<i", idx))
            uc.mem_write(rp + 0x20, struct.pack("<I", 0xA5A5A5A5))
        elif addr == 0x31B7E0:
            uc.reg_write(X.UC_X86_REG_RAX, self.unit)
        elif addr == 0x30CFB0:
            self.called.append(uc.reg_read(X.UC_X86_REG_R8) & 0xFFFF)

    def call(self, fn, rcx=0, rdx=0, r8=0):
        X, u = self.X, self.u
        u.mem_write(0x8080000, struct.pack("<Q", 0xDEAD0000))       # return address sentinel
        u.reg_write(X.UC_X86_REG_RSP, 0x8080000)
        for r, v in ((X.UC_X86_REG_RCX, rcx), (X.UC_X86_REG_RDX, rdx), (X.UC_X86_REG_R8, r8)):
            u.reg_write(r, v)
        u.mem_map(0xDEAD0000, 0x1000) if not getattr(self, "_s", False) else None
        self._s = True
        u.emu_start(fn, 0xDEAD0000, count=400)
        return u.reg_read(X.UC_X86_REG_RAX)

    def chain(self, raw, width, kind, mode4=True):
        """raw DWORD in a script variable -> PUSHV(width, kind) -> pop -> decoder; returns the decoded word or None."""
        u, vm, var = self.u, 0x7000000, 0x7010000
        u.mem_write(vm, struct.pack("<I", 0) + b"\x00" * 0x300)
        u.mem_write(var, struct.pack("<I", raw & 0xFFFFFFFF))
        self.rec = (kind, width, var, 0)
        self.call(PUSHV, 0, 0, vm)
        v = self.call(POP, vm) & 0xFFFFFFFF
        u.mem_write(0x22C2170, struct.pack("<I", 4 if mode4 else 0))
        self.called = []
        u.mem_write(self.unit + 0x758, b"\x00\x00")
        self.call(DEC, 7, v)
        word = struct.unpack("<H", bytes(u.mem_read(self.unit + 0x758, 2)))[0]
        return v, (word if self.called else None)


def emu_checks(img, R, small=False):
    E = Emu(img)
    words = [w for w in range(0x10000) if w not in (0xCF, 0xFFFF)]
    if small:
        words = [0, 0xD0, 208, 511, 534, 0xFFFE]
    bad = []
    for w in words:
        e = (w - 0xD0) & 0xFFFFFFFF
        for width in (2, 3, 4):
            v, got = E.chain(e, width, 1)
            if got != w:
                bad.append((w, width, hex(v), got))
    R.check("emulated original PUSHV -> pop -> decoder, kind 1, u16 / s16 / s32 loads of the raw encoded DWORD w - 0xD0:"
            " the decoded word is w for every available queue word (%d words x 3 widths)" % len(words), not bad, str(bad[:4]))
    t8 = [E.chain((w - 0xD0) & 0xFFFFFFFF, wd, 1)[1] for w in range(511, 535) for wd in (0, 1)]
    R.check("words 511..534 through u8 and s8 loads decode to 255..278", t8 == [x for w in range(511, 535) for x in
            ((w - 0xD0) % 256 + 0xD0,) * 2] and min(t8) == 255 and max(t8) == 278, str(t8[:4]))
    tf = [E.chain(w - 0xD0, 5, 2) for w in (511, 534)]
    R.check("raw 303 / 326 loaded as f32 with kind 2: the pop's CVTTSS2SI gives 0 (positive subnormals), and the decoder"
            " gives 208", all(v == 0 and got == 208 for v, got in tf), str(tf))
    tk = [E.chain(w - 0xD0, wd, 2)[1] for w in (511,) for wd in (2, 4)]
    R.check("an integer load with kind 2 converts the integer's bits as a float: 303 as u16 / s32 also decodes to 208",
            tk == [208, 208], str(tk))
    m = E.chain(511 - 0xD0, 4, 1, mode4=False)
    R.check("with DWORD 022C2170 != 4 the decoder writes nothing and does not call 0030CFB0", m[1] is None)
    R.check("the -1 DWORD decodes to FFFF (the sentinel branch)", E.chain(0xFFFFFFFF, 4, 1)[1] == 0xFFFF)


def checks(img, R, small=False):
    static_checks(img, R)
    emu_checks(img, R, small)


def main():
    exe = find_exe()
    raw = open(exe, "rb").read()
    R = Report("rv_xfer")
    R.check("exe sha256 = %s..." % SHA256[:16], hashlib.sha256(raw).hexdigest() == SHA256)
    committed = hashlib.sha256(git("show", COMMIT + ":Database/FFXII TZA/_experiments/evidence/%s/manifest.json"
                                   % SLUG)).hexdigest()
    check_manifest(R, SLUG, committed)
    img = Img(raw)
    checks(img, R)
    print("== controls (each patched private image must FAIL at least one check)")
    ctl = [
        ("null control: an unchanged private copy passes", lambda: Img(raw), False),
        ("bridge + 0x13 store DWORD -> WORD (`mov word ptr [rdx], ax`)", lambda: img.patched(0x309C13, b"\x66\x89\x02"), True),
        ("native + 0x51 `mov rdx, rsi` -> `mov rdx, rax`", lambda: img.patched(0x348381, b"\x48\x89\xC2"), True),
        ("getter + 0x12 `and eax, 7` -> `and eax, 0xf`", lambda: img.patched(0x2650C2, b"\x83\xE0\x0F"), True),
        ("PUSHV u16 load -> s16 (`movsx`)", lambda: img.patched(0x268026, b"\x0F\xBF\x0C\x48"), True),
        ("pop + 0x32 CVTTSS2SI -> CVTSS2SI (rounding)", lambda: img.patched(0x267E42, b"\xF3\x42\x0F\x2D"), True),
        ("args + 0x1F `mov edx, ebx` -> `mov edx, eax` (pop order swapped)", lambda: img.patched(0x34888F, b"\x89\xC2"), True),
        ("decoder + 0x12 `add bx, ax` -> `add ebx, eax`", lambda: img.patched(0x30EEB2, b"\x01\xC3\x90"), True),
        ("decoder + 0x8 `cmp edx, -1` -> `cmp edx, -2`", lambda: img.patched(0x30EEA8, b"\x83\xFA\xFE"), True),
    ]
    for label, fac, must in ctl:
        ok = run_control(label, fac, lambda im, RR: checks(im, RR, small=True), must_fail=must)
        R.check("control: " + label, ok)
    R.check("exe on disk unchanged after the controls", hashlib.sha256(open(exe, "rb").read()).hexdigest() == SHA256)
    print("FAILS %d" % R.fails)


if __name__ == "__main__":
    main()
