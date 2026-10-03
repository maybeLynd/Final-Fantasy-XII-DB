"""k54_light.py - OPUS, 2026-10-02. What the five kind-0x54 lighting routines write into the lit per-normal table
(the residue on effect-mesh-records-kind-54.md: 003962F0 / 00396A30 / 00396560 / 00395CF0 / 00395780).

The routines are PS2 VU0 microcode translated to x86: 022D8F10.. is the emulated register file (022D8F90 = the
current input vector, 022D91B0 / 91C0 / 91D0 the three matrix columns the caller loads, 01EF93F0 = vf00 = (0,0,0,1)).
Each is executed to its own ret over the certified image with FABLE's SD-140 Unicorn harness (imported, not copied).
The only bridge is the CRT import sqrtf (IAT thunk 00861F14 -> api-ms-win-crt-math sqrtf), computed in float32.
E-checks compare native output with a float32 model (the model is the claim); N-checks score a deliberately wrong model
and pass only if it is rejected. Last line: 'FAILS n'.
"""
import os
import random
import struct
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SD140 = os.path.abspath(os.path.join(HERE, "..", "sd140-vertex-prep-kernel-0930"))
sys.path.insert(0, SD140)
import sd140_emu as U  # noqa: E402
from unicorn import UC_HOOK_CODE  # noqa: E402
from unicorn.x86_const import (UC_X86_REG_RSP, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9,  # noqa: E402
                               UC_X86_REG_RIP, UC_X86_REG_XMM0)

f32 = np.float32
fails = checks = 0
E = U.Emu()
mu = E.mu
S = U.SCR
REG = 0x022D8F10


def check(tag, ok, text):
    global fails, checks
    checks += 1
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def _sqrtf(mu_, a, size, ud):
    x = struct.unpack("<f", struct.pack("<I", mu_.reg_read(UC_X86_REG_XMM0) & 0xFFFFFFFF))[0]
    r = f32(np.sqrt(f32(x))) if x >= 0 else f32("nan")
    mu_.reg_write(UC_X86_REG_XMM0, struct.unpack("<I", struct.pack("<f", float(r)))[0])
    rsp = mu_.reg_read(UC_X86_REG_RSP)
    mu_.reg_write(UC_X86_REG_RIP, struct.unpack("<Q", mu_.mem_read(rsp, 8))[0])
    mu_.reg_write(UC_X86_REG_RSP, rsp + 8)


mu.hook_add(UC_HOOK_CODE, _sqrtf, begin=0x00861F14, end=0x00861F14)


def call(fn, rcx=0, rdx=0, r8=0, r9=0, count=5_000_000):
    rsp = U.STACK + 0xF0000 - 8
    mu.mem_write(rsp, struct.pack("<Q", U.RET) + b"\0" * 64)
    mu.reg_write(UC_X86_REG_RSP, rsp)
    for r, v in ((UC_X86_REG_RCX, rcx), (UC_X86_REG_RDX, rdx), (UC_X86_REG_R8, r8), (UC_X86_REG_R9, r9)):
        mu.reg_write(r, v)
    E.fault = None
    try:
        mu.emu_start(fn, U.RET, count=count)
    except Exception as e:  # noqa: BLE001
        E.fault = E.fault or ("exception", str(e))
    return E.fault is None and mu.reg_read(UC_X86_REG_RIP) == U.RET


def wf(a, xs):
    E.w(a, struct.pack("<%df" % len(xs), *[float(x) for x in xs]))


def rf(a, n):
    return np.array(struct.unpack("<%df" % n, E.r(a, 4 * n)), dtype=f32)


def close(a, b, tol=2e-5):
    a, b = np.asarray(a, dtype=np.float64), np.asarray(b, dtype=np.float64)
    return bool(np.all(np.abs(a - b) <= tol * np.maximum(1.0, np.abs(b))))


def rnd(n, lo=-1.0, hi=1.0):
    return [f32(random.uniform(lo, hi)) for _ in range(n)]


random.seed(54)
IN, OUT, SC = S + 0x1000, S + 0x8000, S + 0x100


def setup(n_list, C, carry=None, V=None):
    for i, v in enumerate(list(n_list) + [(0, 0, 0, 0)]):
        wf(IN + 16 * i, v)
    for i, c in enumerate(C):
        wf(REG + 0x2A0 + 16 * i, c)          # 022D91B0 / 022D91C0 / 022D91D0: the caller's three matrix columns
    if carry is not None:
        wf(0x022D9310, carry)
    if V is not None:
        wf(SC, V)
    E.w(0x022D8F10, b"\0" * 16)              # vi00
    E.w(OUT, b"\0" * 16 * (len(n_list) + 2))


def mvec(n, C):
    C = np.array(C, dtype=np.float64)
    return C[0] * n[0] + C[1] * n[1] + C[2] * n[2]


def unit_half(f):
    l = np.linalg.norm(f)
    return 0.5 + 0.5 * (f / l if l > 0 else f)


def m_planar(n, C, s):                        # 003962F0 (s > 0)
    m = mvec(n, C)
    return np.array([-s * m[0], s * m[1], 0.0, m[3]])


def m_matcap(n, C, axis):                     # 00396560 (z) / 00396A30 (y); lane 3 is the carried 022D9310.w
    m = mvec(n, C)[:3]
    f = np.array([m[0], -m[1], m[2] + 1]) if axis == "z" else np.array([m[0], m[2], m[1] + 1])
    return unit_half(f)


def m_reflect(n, C, V, axis):                 # 00395780 (z) / 00395CF0 (y); lane 3 = (M n).w, as in 003962F0
    m = mvec(n, C)[:3]
    v = np.array(V[:3], dtype=np.float64)
    r = 2 * np.dot(m, v) * m - v
    f = np.array([r[0], -r[1], r[2] + 1]) if axis == "z" else np.array([r[0], r[2], r[1] + 1])
    return unit_half(f)


# ------------------------------------------------------------------------------------------------- A static anchors
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))


TRIALS, NROW = 150, 4
miss = {k: 0 for k in ("planar", "matcap-z", "matcap-y", "carry-w", "reflect-z", "reflect-y", "reflect-w")}
wrong = {k: 0 for k in ("planar-no-neg", "matcap-z-as-y", "reflect-no-flip", "reflect-raw-n")}
for t in range(TRIALS):
    N = [rnd(4) for _ in range(NROW)]
    C = [rnd(4) for _ in range(3)]
    s = f32(random.uniform(0.05, 2.0))
    setup(N, C)
    E.w(SC, struct.pack("<f", float(s)))
    ok = call(0x003962F0, rcx=IN, rdx=OUT, r8=SC, r9=NROW)
    for i in range(NROW):
        o = rf(OUT + 16 * i, 4)
        miss["planar"] += 0 if ok and close(o, m_planar(N[i], C, s)) else 1
        bad = m_planar(N[i], C, s); bad[0] = -bad[0]
        wrong["planar-no-neg"] += 0 if close(o, bad) else 1
    for fn, axis in ((0x00396560, "z"), (0x00396A30, "y")):
        carry = rnd(4)
        setup(N, C, carry=carry)
        ok = call(fn, rcx=IN, rdx=OUT, r8=NROW)
        for i in range(NROW):
            o = rf(OUT + 16 * i, 4)
            miss["matcap-" + axis] += 0 if ok and close(o[:3], m_matcap(N[i], C, axis)) else 1
            miss["carry-w"] += 0 if o[3] == f32(carry[3]) else 1
            if axis == "z":
                wrong["matcap-z-as-y"] += 0 if close(o[:3], m_matcap(N[i], C, "y")) else 1
    for fn, axis in ((0x00395780, "z"), (0x00395CF0, "y")):
        V = rnd(4)
        setup(N, C, V=V)
        ok = call(fn, rcx=IN, rdx=OUT, r8=SC, r9=NROW)
        for i in range(NROW):
            o = rf(OUT + 16 * i, 4)
            miss["reflect-" + axis] += 0 if ok and close(o[:3], m_reflect(N[i], C, V, axis)) else 1
            miss["reflect-w"] += 0 if close([o[3]], [mvec(N[i], C)[3]]) else 1
            if axis == "z":
                m = mvec(N[i], C)[:3]; v = np.array(V[:3], float); r = 2 * np.dot(m, v) * m - v
                wrong["reflect-no-flip"] += 0 if close(o[:3], unit_half(np.array([r[0], r[1], r[2] + 1]))) else 1
                nn = np.array(N[i][:3], float); r2 = 2 * np.dot(nn, v) * nn - v
                wrong["reflect-raw-n"] += 0 if close(o[:3], unit_half(np.array([r2[0], -r2[1], r2[2] + 1]))) else 1
total = TRIALS * NROW

for k, v in miss.items():
    check("E-" + k, v == 0, "%d / %d rows off the model" % (v, 2 * total if k in ("carry-w", "reflect-w") else total))
for k, v in wrong.items():
    check("N-" + k, v > 0, "wrong model rejected on %d / %d rows" % (v, total))

# static anchors: the selector in the draw path 004355D0 (the other four draw paths call the same five routines)
import subprocess as _sp
_d = _sp.run([sys.executable, "-B", os.path.join(os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools",
             "analysis-kit", "gfz-scripts")), "retool.py"), "dis", "004355D0", "--n", "2000"], capture_output=True,
             text=True).stdout
_ins = {l.split(None, 1)[0]: " ".join(l.split(None, 1)[1].split(";")[0].split()) for l in _d.splitlines()
        if len(l) > 9 and l[8] == " "}
for a, want, what in (("004359E5", "movzx ecx, byte ptr [r15 + rdi + 0x1b0]", "the mode byte +0x1B0 + p"),
                      ("00435A75", "cmp byte ptr [r15 + rax + 0x1b4], 0", "+0x1B4 picks the matcap axis"),
                      ("00435A80", "call 0x396a30", "+0x1B4 == 0: y-axis matcap 00396A30"),
                      ("00435A8A", "call 0x396560", "+0x1B4 != 0: z-axis matcap 00396560"),
                      ("00435AE8", "lea r8, [r15 + r8*4]", "planar scalar at param + 0x1D8 + 4k, k from rbx (not shown equal to the pass index)"),
                      ("00435AF1", "call 0x3962f0", "mode 2: planar 003962F0"),
                      ("00435BBE", "cmp byte ptr [r15 + rax + 0x1b4], 0", "+0x1B4 picks the reflection axis"),
                      ("00435BC9", "call 0x395cf0", "+0x1B4 == 0: y-axis reflection 00395CF0"),
                      ("00435BD0", "call 0x395780", "+0x1B4 != 0: z-axis reflection 00395780")):
    check("A-" + a, _ins.get(a) == want, "%s (%s)" % (what, _ins.get(a)))
check("K-008C5FB0", struct.unpack("<4f", E.r(0x008C5FB0, 16)) == (0.0, 0.0, 1.0, 0.0),
      "the reflection path's V is (0, 0, 1, 0) before 00394DA0 transforms it")

# zero vector: the FLT_MAX guard leaves the centre 0.5
setup([(0, 0, -1, 0)], [(1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0)], carry=(0, 0, 0, 0))
call(0x00396560, rcx=IN, rdx=OUT, r8=1)
check("E-zero-guard", close(rf(OUT, 4)[:3], [0.5, 0.5, 0.5]), "matcap of n = (0,0,-1) is the centre (0.5, 0.5, 0.5)")
print("FAILS %d" % fails)
