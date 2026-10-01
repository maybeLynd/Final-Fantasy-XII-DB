"""sd21_mix_remainder.py - the unread remainder of the SQEX Sd mix path (OPUS, 2026-09-30; register SD-21).
Asserts over the certified image via Database/Tools/analysis-kit/gfz-scripts/retool.py and prints what it reads.
"""
import os, re, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import retool as T  # noqa: E402

R, c = T.R, T.scan()
fails = 0


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def ins(a):
    return next(R.md.disasm(R.at(a, 16), a, 1))


def txt(a):
    i = ins(a)
    return "%s %s" % (i.mnemonic, i.op_str)


def vtable(vt, n):
    return list(struct.unpack("<%dQ" % n, R.at(vt, 8 * n)))


# V1 - the three core voice classes by RTTI and their slots
VT = {0x01CB8290: ("SQEX::Sd::Driver::Core::CoreMasterVoice", 7), 0x01CB82D0: ("SQEX::Sd::Driver::Core::CoreSubmixVoice", 7),
      0x01CB8360: ("SQEX::Sd::Driver::Core::CoreSourceVoice", 17)}
ok = all(T.rtti_class(vt) == name for vt, (name, _) in VT.items())
m, s, src = vtable(0x01CB8290, 7), vtable(0x01CB82D0, 7), vtable(0x01CB8360, 17)
check("V1", ok and src[3] == 0x007E2710 and src[9] == 0x007E0A40, "RTTI classes; CoreSourceVoice slot 3 = start 007E2710, slot 9 = enqueue 007E0A40")
# V2 - slot 1 is the class's type id: Master 1, Submix 2, Source 3
check("V2", txt(m[1]) == "mov eax, 1" and txt(s[1]) == "mov eax, 2" and txt(src[1]) == "mov eax, 3", "type ids 1 / 2 / 3")
# V3 - slot 0 is the deleting destructor: calls the class destructor then the SEAD free 007AD450
dtor = all("call 0x7ad450" in " ".join("%s %s" % (i.mnemonic, i.op_str) for i in R.md.disasm(R.at(f, 0x60), f)) for f in (m[0], s[0], src[0]))
check("V3", dtor, "slot 0 of each frees through 007AD450")
# V4 - the per-class getters and setters (fields named by offset only)
check("V4", txt(m[2]) == "movsx eax, word ptr [rcx + 0x74]" and txt(s[2]) == "movsx eax, word ptr [rcx + 0xcc]"
      and txt(src[2]) == "mov eax, dword ptr [rcx + 0xb0]" and txt(s[4]) == "mov eax, dword ptr [rcx + 0x88]"
      and txt(src[10]) == "movss xmm0, dword ptr [rcx + 0x100]" and txt(src[12]) == "mov eax, dword ptr [rcx + 0xac]"
      and txt(src[13]) == "mov eax, dword ptr [rcx + 0x90]" and txt(src[14]) == "mov eax, dword ptr [rcx + 0x268]",
      "getters: Master +0x74 (s16), Submix +0xCC (s16) / +0x88 (send count), Source +0xB0 (queued buffers), +0x100 (float), "
      "+0xAC, +0x90, +0x268 (send count)")
idx = lambda f: [("%s %s" % (i.mnemonic, i.op_str)) for i in R.md.disasm(R.at(f, 0x30), f)][:10]
check("V5", "movups xmm0, xmmword ptr [rcx + rax*8 + 0x38]" in idx(s[5]) and "movups xmm0, xmmword ptr [rcx + rax*8 + 0x218]" in idx(src[15])
      and "cmp dword ptr [rcx + 0x88], r8d" in idx(s[5]) and "cmp dword ptr [rcx + 0x268], r8d" in idx(src[15]),
      "indexed 16-byte send entries: Submix +0x38 (count +0x88), Source +0x218 (count +0x268), bounds-checked")
check("V6", "movss dword ptr [rcx + 0x5c], xmm1" in idx(m[6]) and "movss dword ptr [rcx + rax*8], xmm1" in idx(s[6])
      and "movss dword ptr [rcx + 0x100], xmm1" in idx(src[6]) and "movss dword ptr [rcx + 0x104], xmm1" in idx(src[6])
      and "movss dword ptr [rcx + 0x108], xmm1" in idx(src[7]),
      "float setters: Master +0x5C (index 0 only), Submix send level, Source +0x100/+0x104 (slot 6) and +0x108 (slot 7, "
      "refused in states 0 and 4)")
b4 = " ".join("%s %s" % (i.mnemonic, i.op_str) for i in R.md.disasm(R.at(src[4], 77), src[4]))
b5 = " ".join("%s %s" % (i.mnemonic, i.op_str) for i in R.md.disasm(R.at(src[5], 101), src[5]))
check("V7", "mov dword ptr [rdi + 0x80], 2" in b4 and "mov dword ptr [rsi + 0x80], 4" in b5,
      "Source slot 4 sets state 2 under the lock (stop); slot 5 sets state 4 (flush)")
# F1 - the voice pool take 007DF750: under the pool's lock, pop [pool+0x30] (next at node+0), count [pool+0x48]
check("F1", txt(0x007DF763) == "mov rdi, qword ptr [rbx + 0x30]" and txt(0x007DF76C) == "mov rcx, qword ptr [rdi]"
      and txt(0x007DF76F) == "inc dword ptr [rbx + 0x48]" and txt(0x007DF772) == "mov qword ptr [rbx + 0x30], rcx",
      "007DF750 pops a free-list node under EnterCriticalSection / LeaveCriticalSection (imports 008C20B8 / 008C20C0)")
# F2 - the factory 007AEA20's two paths, chosen by its 10th argument (byte [rsp+0xa8])
check("F2", txt(0x007AEA3A) == "cmp byte ptr [rsp + 0xa8], 0" and txt(0x007AEA5B) == "call 0x7df750"
      and txt(0x007AEAF5) == "call 0x7af380" and txt(0x007AEB1F) == "call 0x7ad460" and txt(0x007AEB16) == "mov edx, 0x2b8"
      and txt(0x007AEBCA) == "call 0x7af490" and txt(0x007AD4AC) == "mov dword ptr [rax], 0x5ead5ead",
      "flag 0: pooled voice (pool 02EAD250), listed by 007AF380 under lock 02EAD138; flag set: 0x2B8-byte aligned "
      "allocation through the SEAD hook (007AD460, header 0x5EAD5EAD), listed by 007AF490 under lock 02EAD160")
# F3 - who starts / queues a created voice: owner code loading the voice from owner+0x68 (+0x48 for HCAMixerVoice)
starts, queues = [], []
for f, n in T.sizes().items():
    if not 0x007A0000 <= f < 0x00800000:
        continue
    d = R.at(f, n)
    if not d:
        continue
    b = list(R.md.disasm(d, f))
    for k, i in enumerate(b):
        mm = re.match(r"qword ptr \[(r\w+) \+ (0x18|0x48)\]$", i.op_str) if i.mnemonic == "call" else None
        if not mm:
            continue
        for j in range(k - 1, max(0, k - 8), -1):
            m2 = re.match(r"%s, qword ptr \[(r\w+)\]$" % mm.group(1), b[j].op_str)
            if b[j].mnemonic == "mov" and m2:
                if any(b[q].mnemonic == "mov" and re.match(r"%s, qword ptr \[r\w+ \+ (0x68|0x48)\]$" % m2.group(1), b[q].op_str)
                       for q in range(j - 1, max(0, j - 8), -1)):
                    (starts if mm.group(2) == "0x18" else queues).append((f, i.address))
                break
check("F3", sorted(starts) == [(0x007B9050, 0x007B9355), (0x007B9AF0, 0x007B9C8B), (0x007DCE20, 0x007DD011), (0x007EDA60, 0x007EDA82),
                              (0x007EDAB0, 0x007EDAD4)]
      and sorted(queues) == [(0x007B9590, 0x007B96FF), (0x007DCE20, 0x007DD007), (0x007EAA60, 0x007EB8CE)],
      "start callers %s; queue callers %s" % (["%08X" % f for f, _ in sorted(starts)], ["%08X" % f for f, _ in sorted(queues)]))
# K1 - the SIMD kernels of 007E0B60: every path specialises on the source channel count r9d (1, 2; the third path
#      also 4) before a general case, at 007E100E / 007E108D (unity rate), 007E1378 / 007E143A (resampled),
#      007E1796 / 007E1882 / 007E19CF (the other source format)
disp = [(a, txt(a)) for a in (0x007E100E, 0x007E108D, 0x007E1378, 0x007E143A, 0x007E1796, 0x007E1882, 0x007E19CF)]
check("K1", [t for _, t in disp] == ["cmp r9d, 1", "cmp r9d, 2", "cmp r9d, 1", "cmp r9d, 2", "cmp r9d, 1", "cmp r9d, 2", "cmp r9d, 4"],
      "source-channel dispatch %s" % ["%08X" % a for a, _ in disp])
# K2 - the kernel shape (the unity-rate mono 16-bit case, 007E1020-007E1086): the sample is widened and broadcast, times
#      the 8-wide per-output-channel gain vector (xmm8 / xmm7, the +0x10C table with the scale folded in, §2a) and the
#      ramped gain (xmm6, stepped by xmm12 each frame); 8 output channels are stored per frame (two movaps, 32 bytes)
#      at the output stride, and the position double +0x98 advances by the step
k2 = [txt(a) for a in (0x007E1020, 0x007E1023, 0x007E1027, 0x007E1046, 0x007E1049, 0x007E104D, 0x007E1050, 0x007E1053,
                       0x007E1056, 0x007E1059, 0x007E1064, 0x007E106C, 0x007E107B)]
check("K2", k2 == ["movaps xmm3, xmm6", "shufps xmm3, xmm3, 0", "addss xmm6, xmm12", "cvtdq2ps xmm2, xmm2", "shufps xmm2, xmm2, 0",
                   "mulps xmm0, xmm2", "mulps xmm1, xmm2", "mulps xmm0, xmm3", "mulps xmm1, xmm3", "movaps xmmword ptr [rsi], xmm0",
                   "movaps xmmword ptr [rsi + 0x10], xmm1", "addsd xmm0, qword ptr [rbx + 0x98]", "movsd qword ptr [rbx + 0x98], xmm0"],
      "sample x gain vector x ramped gain -> 8 output floats per frame; position += step")
body = [("%s %s" % (i.mnemonic, i.op_str)) for i in R.md.disasm(R.at(0x007E0B60, T.sizes()[0x007E0B60]), 0x007E0B60)]
stores = sum(1 for t in body if t.startswith("movaps xmmword ptr [rsi"))
adds = sum(1 for t in body if t.startswith("addps"))
check("K3", stores == 48 and adds >= 10, "48 paired 16-byte output stores (24 frame kernels x 8 channels) and %d addps "
      "(the general-channel accumulation)" % adds)
print("FAILS %d" % fails)
