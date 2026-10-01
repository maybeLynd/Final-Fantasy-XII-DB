"""Controls for the eps field read.
(a) ctor -> installed vtable -> RTTI class name, and vft[+0x08] getter value == classId, and vft[+0x30] = applier.
(b) known answers: shipped values pushed through the arithmetic the code applies, using constants read from the exe.
(c) the build-time sample-rate assumption encoded in .data initial images."""
import sys, struct, math, re
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
from pe import d, off, u32, u64, f32, BASE
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
md = Cs(CS_ARCH_X86, CS_MODE_64)

CTORS = {1: 0x007D2150, 2: 0x007D85E0, 3: 0x007D0AC0, 4: 0x007D80E0, 5: 0x007D9530, 7: 0x007DA0A0, 10: 0x007DAFF0}
print("(a) ctor -> vtable -> RTTI; getter; applier")
for cid, ctor in CTORS.items():
    vt = None
    for x in md.disasm(d[off(ctor):off(ctor) + 0x40], ctor):
        m = re.match(r"rax, \[rip \+ (0x[0-9a-f]+)\]", x.op_str)
        if x.mnemonic == "lea" and m:
            vt = x.address + x.size + int(m.group(1), 16)
            break
    col = u64(vt - 8)
    td = u32(col + 12)
    name = d[off(BASE + td + 16):off(BASE + td + 16) + 80].split(b"\0")[0].decode()
    getter = u64(vt + 8)
    gi = list(md.disasm(d[off(getter):off(getter) + 6], getter))[0]
    applier = u64(vt + 0x30)
    print("  classId %2d ctor %08X vtable %08X %-42s getter %08X '%s %s'  vft+0x30 = %08X" % (
        cid, ctor, vt, name, getter, gi.mnemonic, gi.op_str, applier))
    assert int(gi.op_str.split(",")[1], 16) == cid

print("\n(b) known answers")
fs = 48000.0
print("  fs assumption: .data images 01F41D18=%.9g (1/fs -> %.1f), 01F41D24=%g (fs/2), 01F41D28=%g (fs/4800); runtime fs is [02EAD348] set at 007AF064" % (
    f32(0x01F41D18), 1 / f32(0x01F41D18), f32(0x01F41D24), f32(0x01F41D28)))
k_db = f32(0x01CB7780)
print("  Compressor dB->lin constant 01CB7780 = %.7f ; ln(10)/20 = %.7f ; -6 dB default -> %.4f" % (k_db, math.log(10) / 20, math.exp(-6 * k_db)))
print("  Compressor attack 10 ms example: exp(-2/(0.010*fs)) = %.6f per sample; release exp(-1/(0.010*fs)) = %.6f" % (
    math.exp(-2 / (0.010 * fs)), math.exp(-1 / (0.010 * fs))))
print("  Filter shipped f=2000 Hz -> w = 2000*%.6f*%.9g = %.5f rad (= 2pi*2000/48000 = %.5f)" % (f32(0x01CEBC78), f32(0x01F41D18),
      2000 * f32(0x01CEBC78) * f32(0x01F41D18), 2 * math.pi * 2000 / 48000))
print("  Filter shipped Q=0.707 -> stored 1/Q = %.4f ; SurroundReverb band 1/Q shipped 1.414 -> Q = %.4f (same designs 007D0EA0/007D1330/007D1080)" % (1 / 0.707, 1 / 1.414))
# SurroundReverb FDN
tbl = [f32(0x01CB7100 + 4 * i) for i in range(16)]
size, T = 20.0, 500.0
print("  SurroundReverb size=20 -> scale %.4f (x*%.7f); line0 %.2f ms * scale = %.2f ms = %d samples at 48k" % (
    size * f32(0x009171D0), f32(0x009171D0), tbl[0], tbl[0] * size * f32(0x009171D0), int(fs * tbl[0] * 0.001 * size * f32(0x009171D0))))
g = [0.25 * 10 ** (-3 * t * size * f32(0x009171D0) / T) for t in tbl]
print("  SurroundReverb RT=500 ms -> FDN feedback gains 0.25*10^(-3*len/T): min %.4f max %.4f  (10^(-3*len/T) alone: %.3f..%.3f, i.e. -60 dB after T ms)" % (
    min(g), max(g), min(x / 0.25 for x in g), max(x / 0.25 for x in g)))
print("  SurroundReverb pre-delay clamp constants 01CB75AC=%g 01CB75A8=%g ; process wrap 0x5DC0=%d frames" % (f32(0x01CB75AC), f32(0x01CB75A8), 0x5DC0))
print("  SurroundReverb damping: ln10/4 = %.7f vs 01CB7598 = %.7f (Jot absorptive-filter constant)" % (math.log(10) / 4, f32(0x01CB7598)))
# BuildReverb
d_s = [f32(0x01CB7A00 + 4 * i) for i in range(6)]
off_hz = [f32(0x01CB7A18 + 4 * i) for i in range(6)]
print("  BuildReverb comb delays (s) 01CB7A00: %s" % [round(x, 3) for x in d_s])
print("  BuildReverb RT60=2.0 s -> comb gains 10^(-3*d/2): %s" % [round(10 ** (-3 * x / 2.0), 3) for x in d_s])
print("  BuildReverb damping 2000 Hz, offsets 01CB7A18 %s -> a=exp(-2pi(f-off)/fs): %s" % (
    off_hz, [round(math.exp(-2 * math.pi * (2000 - o) / fs), 3) for o in off_hz]))
print("  BuildReverb pre-delay 0.08 s -> %d samples; buffer 0.11*fs (01CB7A34=%g) = %d; clamp 0.1 s (008C5F6C=%g)" % (
    int(0.08 * fs), f32(0x01CB7A34), int(f32(0x01CB7A34) * fs), f32(0x008C5F6C)))
print("  GranularPitchShift default grain rate 10 Hz -> period %d samples; delay buffer 0x3840 = %d frames" % (int(fs / 10), 0x3840))
