"""rv_riglist.py - FABLE independent re-derivation for ASTRA packet rig-index-list-producer (f20407498).

Own reader (rvlib.py: struct + capstone 5). Does not import ASTRA's prove.py or the shared role adapter.
Each claim group is a function of the image; the controls rerun it on privately patched copies.
"""
import os
import random
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rvlib import check_manifest, Img, Body, Report, expect, run_control  # noqa: E402

POOL = 0x022C6F28
CODEC_BASE = 0x01F83530
FIX = (0x003E1C50, 0x003E2800)
RESET = (0x003E3C30, 0x003E3C9D)
LOOK = (0x00421D20, 0x00421D66)
M32 = 0xFFFFFFFF
M64 = 0xFFFFFFFFFFFFFFFF


def c_bodies(img, R):
    tot = 0
    for s, e in (FIX, RESET, LOOK):
        B = Body(img, s, e)
        ents, ok = img.pdata_cover(s, e)
        rets, tails, outs = B.exits()
        R.check("body %08X..%08X decodes exactly (%d B)" % (s, e, e - s), B.exact)
        R.check("body %08X .pdata tiles it (%d record(s))" % (s, len(ents)), ok,
                " ".join("%08X..%08X%s" % (b, en, "~chain" if fl & 4 else "") for b, en, fl, r in ents))
        R.check("body %08X: no jcc leaves; exits rets=%s tails=%s" % (s, ["%08X" % r for r in rets],
                ["%08X->%08X" % (a, t) for a, t in tails]), not outs)
        tot += e - s
    R.check("new source total 3,171 bytes (2,992 + 109 + 70)", tot == 3171, str(tot))


def c_codec(img, R):
    D = Body(img, 0x0020E600, 0x0020E60A)
    E = Body(img, 0x0020E620, 0x0020E629)
    expect(R, D, 0x0020E600, "mov eax, ecx")
    expect(R, D, 0x0020E602, "add rax, qword ptr [rip + 0x1d74f27]")
    R.check("decoder base cell is 01F83530 (QWORD)", 0x0020E602 + 7 + 0x1d74f27 == CODEC_BASE and D[0x0020E602].mems[0]["size"] == 8)
    expect(R, D, 0x0020E609, "ret")
    expect(R, E, 0x0020E620, "sub ecx, dword ptr [rip + 0x1d74f0a]")
    R.check("encoder subtracts the low DWORD of the same cell", 0x0020E620 + 6 + 0x1d74f0a == CODEC_BASE and E[0x0020E620].mems[0]["size"] == 4)
    expect(R, E, 0x0020E626, "mov eax, ecx")
    expect(R, E, 0x0020E628, "ret")
    R.check("decoder/encoder write no memory and no rbx/rsi/rdi", not D.mem_writes() and not E.mem_writes() and not any(
        {"rbx", "rsi", "rdi"} & B[a].reg_writes for B in (D, E) for a in B.order))


def Dec(x, B):
    return ((x & M32) + B) & M64


def Enc(y, B):
    return ((y & M32) - (B & M32)) & M32


def c_fixup(img, R):
    B = Body(img, *FIX)
    expect(R, B, 0x003E1C50, "test rcx, rcx")
    expect(R, B, 0x003E1C53, "je 0x3e27ff")
    expect(R, B, 0x003E1C5E, "mov rdi, rcx")
    rdi_w = [a for a in B.order if "rdi" in B[a].reg_writes and B[a].mnemonic != "call"]
    R.check("rdi written only at 003E1C5E (rig) and the final pop", rdi_w == [0x003E1C5E, 0x003E27FE],
            str(["%08X" % a for a in rdi_w]))
    # +70 gate and owner lookup
    expect(R, B, 0x003E1C66, "mov ecx, dword ptr [rcx + 0x70]")
    expect(R, B, 0x003E1C6E, "call 0x20e600")
    expect(R, B, 0x003E1C75, "test rax, rax")
    expect(R, B, 0x003E1C78, "je 0x3e1cc6")
    expect(R, B, 0x003E1C73, "xor ebx, ebx")
    expect(R, B, 0x003E1C7A, "movzx eax, word ptr [rdi + 0x68]")
    expect(R, B, 0x003E1C7E, "cmp ax, -1")
    expect(R, B, 0x003E1C84, "mov ecx, ebx")
    expect(R, B, 0x003E1C88, "movsx rax, ax")
    expect(R, B, 0x003E1C8C, "imul rcx, rax, 0x740")
    expect(R, B, 0x003E1C93, "add rcx, qword ptr [rip + 0x1ee528e]")
    R.check("003E1C93 adds global 022C6F28", 0x003E1C93 + 7 + 0x1ee528e == POOL)
    expect(R, B, 0x003E1C9A, "cmp dword ptr [rcx + 0x284], ebx")
    expect(R, B, 0x003E1CA0, "cmove rcx, rbx")
    expect(R, B, 0x003E1CA4, "call 0x20e620")
    expect(R, B, 0x003E1CAB, "mov dword ptr [rdi + 0x70], eax")
    expect(R, B, 0x003E1CAE, "call 0x20e600")
    expect(R, B, 0x003E1CB3, "mov rcx, rax")
    expect(R, B, 0x003E1CB6, "call 0x421d20")
    expect(R, B, 0x003E1CBE, "call 0x20e620")
    expect(R, B, 0x003E1CC3, "mov dword ptr [rdi + 0x78], eax")
    R.check("no compare/test of the derived pointer between 003E1CA0 and the 421D20 call",
            not [a for a in B.order if 0x003E1CA0 < a < 0x003E1CB6 and B[a].mnemonic in ("cmp", "test")])
    w78 = [a for a, m in B.mem_writes(lambda m: m["base"] == "rdi" and m["disp"] == 0x78)]
    R.check("the only direct [rdi+78] writes are %s" % ["%08X" % a for a in w78], 0x003E1CC3 in w78)
    R.check("+70==0 path (003E1C78 taken) cannot reach the 003E1CC3 store", 0x003E1CC3 not in B.reach(0x003E1CC6))
    R.check("003E1CC3 store is reached only through the +70!=0 fall-through",
            B.dominates(0x003E1C7A, 0x003E1CC3))
    # cache compare
    expect(R, B, 0x003E1D49, "mov eax, dword ptr [rdi + 0x84]")
    expect(R, B, 0x003E1D4F, "cmp eax, edi")
    expect(R, B, 0x003E1D51, "je 0x3e27f0")
    R.check("+70/+78 refresh (003E1CC3) can precede the cache check: 003E1D49 reachable from 003E1CC3",
            0x003E1D49 in B.reach(0x003E1CC3))
    R.check("every path to the cache check passes the +70 gate at 003E1C78", B.dominates(0x003E1C78, 0x003E1D49))
    eq = B.reach(0x003E27F0)
    R.check("equal-cache path 003E27F0 reaches only the epilogue (no +84/+88 write)", max(eq) == 0x003E27FF and
            not [a for a in eq if any(m["write"] and m["base"] == "rdi" for m in B[a].mems)])
    expect(R, B, 0x003E1D57, "mov ecx, dword ptr [rdi + 0x88]")
    expect(R, B, 0x003E1D62, "test eax, eax")
    expect(R, B, 0x003E1D64, "jne 0x3e22b7")
    # fresh
    expect(R, B, 0x003E1D6E, "call 0x20e600")
    expect(R, B, 0x003E1D73, "lea ecx, [rdi + rax]")
    expect(R, B, 0x003E1D76, "call 0x20e620")
    expect(R, B, 0x003E1D7D, "mov dword ptr [rdi + 0x88], eax")
    R.check("ecx (old +88) not rewritten between 003E1D57 and 003E1D6E",
            not [a for a in B.order if 0x003E1D57 < a < 0x003E1D6E and "rcx" in B[a].reg_writes])
    # relocation
    expect(R, B, 0x003E22B7, "mov esi, edi")
    expect(R, B, 0x003E22B9, "sub esi, eax")
    expect(R, B, 0x003E22BB, "call 0x20e600")
    expect(R, B, 0x003E22C0, "lea ecx, [rsi + rax]")
    expect(R, B, 0x003E22C3, "call 0x20e620")
    expect(R, B, 0x003E22CA, "mov dword ptr [rdi + 0x88], eax")
    R.check("0x3E1D64->0x3E22B7 edge carries ecx = old +88 (no writer at 003E1D5D..003E1D64)",
            not [a for a in B.order if 0x003E1D57 < a <= 0x003E1D64 and "rcx" in B[a].reg_writes])
    # +84 store
    expect(R, B, 0x003E27EA, "mov dword ptr [rdi + 0x84], edi")
    w84 = [a for a, m in B.mem_writes(lambda m: m["base"] == "rdi" and m["index"] is None and m["disp"] < 0x88 and m["disp"] + m["size"] > 0x84)]
    R.check("003E27EA is the only direct write overlapping rig +84..+87", w84 == [0x003E27EA], str(["%08X" % a for a in w84]))
    R.check("003E27EA stores raw EDI (no encoder call between 003E27E5 and it)",
            not [a for a in B.order if 0x003E27E5 <= a < 0x003E27EA and B[a].mnemonic == "call"])
    R.check("fresh path: 003E27EA reached on every path 003E1D6A -> ret",
            0x003E27FF not in B.reach(0x003E1D6A, avoid=[0x003E27EA]))
    R.check("relocation path: 003E27EA reached on every path 003E22B7 -> ret",
            0x003E27FF not in B.reach(0x003E22B7, avoid=[0x003E27EA]))
    w88 = [a for a, m in B.mem_writes(lambda m: m["base"] == "rdi" and m["index"] is None and m["disp"] < 0x8C and m["disp"] + m["size"] > 0x88)]
    R.check("direct writes to rig +88 are exactly 003E1D7D and 003E22CA", w88 == [0x003E1D7D, 0x003E22CA], str(["%08X" % a for a in w88]))
    a8c = [a for a in B.order for m in B[a].mems if m["base"] == "rdi" and m["index"] is None and m["disp"] < 0x90 and m["disp"] + m["size"] > 0x8C]
    R.check("no direct rdi-relative access overlapping +8C in the fixup", not a8c, str(["%08X" % a for a in a8c]))


def c_reset(img, R):
    B = Body(img, *RESET)
    expect(R, B, 0x003E3C3F, "mov rsi, rcx")
    expect(R, B, 0x003E3C42, "mov ecx, dword ptr [rcx + 0x88]")
    expect(R, B, 0x003E3C48, "call 0x20e600")
    expect(R, B, 0x003E3C4F, "mov rbx, rax")
    expect(R, B, 0x003E3C52, "cmp dword ptr [rsi + 0x8c], edi")
    expect(R, B, 0x003E3C4D, "xor edi, edi")
    expect(R, B, 0x003E3C58, "jbe 0x3e3c8d")
    R.check("decode of +88 (003E3C48) precedes the count check (dominates 003E3C52)", B.dominates(0x003E3C48, 0x003E3C52))
    expect(R, B, 0x003E3C60, "mov ecx, dword ptr [rsi + 0x78]")
    expect(R, B, 0x003E3C63, "call 0x20e600")
    expect(R, B, 0x003E3C68, "mov ecx, dword ptr [rbx]")
    R.check("003E3C68 index read is a DWORD (zero-extended into rcx)", B[0x003E3C68].mems[0]["size"] == 4)
    expect(R, B, 0x003E3C6A, "add rax, 0x230")
    expect(R, B, 0x003E3C70, "imul rcx, rcx, 0x290")
    expect(R, B, 0x003E3C77, "add rcx, rax")
    expect(R, B, 0x003E3C7A, "call 0x203170")
    expect(R, B, 0x003E3C7F, "inc edi")
    expect(R, B, 0x003E3C81, "lea rbx, [rbx + 4]")
    expect(R, B, 0x003E3C85, "cmp edi, dword ptr [rsi + 0x8c]")
    expect(R, B, 0x003E3C8B, "jb 0x3e3c60")
    cmps = [a for a in B.order if B[a].mnemonic in ("cmp", "test")]
    R.check("the only compares are the two unsigned count compares (no per-index bound)",
            cmps == [0x003E3C52, 0x003E3C85] and B[0x003E3C58].mnemonic == "jbe" and B[0x003E3C8B].mnemonic == "jb")
    R.check("count 0: 003E3C58 taken skips every list read and 00203170 call",
            not ({0x003E3C68, 0x003E3C7A} & B.reach(0x003E3C8D)))
    # model of the passed address in 64-bit
    base = 0x00007FF600000000
    for idx in (0, 1, 0xFFFFFFFF):
        a = (base + 0x230 + idx * 0x290) & M64
        R.check("model: index %08X -> arg = Decode(+78)+230h+index*290h = %X (64-bit, no wrap at 32)" % (idx, a),
                a == base + 0x230 + idx * 0x290)


def c_lookup(img, R):
    B = Body(img, *LOOK)
    expect(R, B, 0x00421D20, "push rbx")
    expect(R, B, 0x00421D22, "sub rsp, 0x20")
    expect(R, B, 0x00421D26, "mov ebx, dword ptr [rcx + 0x18]")
    R.check("00421D26 is the first non-stack memory access and no test of rcx precedes it",
            all(all(m["base"] == "rsp" for m in B[a].mems) and B[a].mnemonic not in ("test", "cmp") for a in B.order if a < 0x00421D26))
    R.check("00421D26 reads a DWORD", B[0x00421D26].mems[0]["size"] == 4 and B[0x00421D26].mems[0]["read"])
    expect(R, B, 0x00421D29, "cmp ebx, -1")
    expect(R, B, 0x00421D2E, "mov ecx, dword ptr [rcx + 0x10]")
    expect(R, B, 0x00421D31, "call 0x20e600")
    expect(R, B, 0x00421D3B, "mov rcx, qword ptr [rax + 0xd98]")
    expect(R, B, 0x00421D42, "mov edx, ebx")
    expect(R, B, 0x00421D44, "call 0x2ed570")
    expect(R, B, 0x00421D49, "test rax, rax")
    expect(R, B, 0x00421D4E, "mov ecx, dword ptr [rax + 0x84]")
    expect(R, B, 0x00421D59, "jmp 0x20e600")
    expect(R, B, 0x00421D5E, "xor eax, eax")
    R.note("421D20 returns 0 (00421D5E) for index -1 or a NULL row, else tail-decodes row +84; both need a readable input")


def c_math(R):
    rnd = random.Random(1002)
    ok_f = ok_r = True
    for _ in range(20000):
        Bb = rnd.getrandbits(64)
        rig = rnd.getrandbits(64)
        cur = rnd.getrandbits(64)
        old88 = rnd.getrandbits(32)
        old84 = rnd.getrandbits(32)
        # fresh: ecx=old88; rax=Dec(ecx); ecx=low32(rdi+rax); eax=Enc(ecx)
        f = Enc((rig + Dec(old88, Bb)) & M32, Bb)
        ok_f &= f == (old88 + (rig & M32)) & M32
        # relocation: esi=low32(edi-eax); rax=Dec(old88); ecx=low32(rsi+rax); Enc
        esi = ((cur & M32) - old84) & M32
        r = Enc((esi + Dec(old88, Bb)) & M32, Bb)
        ok_r &= r == (old88 + ((cur - old84) & M32)) & M32
    R.check("math (20,000 random bases/pointers): fresh new88 = low32(old88 + low32(rig)) for a stable base", ok_f)
    R.check("math: relocated new88 = low32(old88 + low32(currentRig - oldRawSelf84)) for a stable base", ok_r)
    p1, p2 = 0x0000000123456780, 0x0000000223456780
    R.check("math: pointers 4 GiB apart share the low DWORD (cache collision)", (p1 & M32) == (p2 & M32))
    R.check("math: a nonzero pointer with low DWORD 0 equals the cold zero cache value", (0x0000000500000000 & M32) == 0)
    # nullable: Encode(0) then Decode
    for Bb in (0, 0x0000000100000000, 0x00007FF612340000):
        rcx = Dec(Enc(0, Bb), Bb)
        R.note("Decode(Encode(0)) at base %X = %X; first read at %X" % (Bb, rcx, (rcx + 0x18) & M64))
    R.check("math: at base 0 the derived pointer is 0 and the 421D20 read is at 18h", (Dec(Enc(0, 0), 0) + 0x18) == 0x18)
    R.check("math: at a nonzero base the address is not 18h (e.g. base 7FF612340000)",
            (Dec(Enc(0, 0x00007FF612340000), 0x00007FF612340000) + 0x18) & M64 != 0x18)


def run_all(img, R):
    c_bodies(img, R)
    c_codec(img, R)
    c_fixup(img, R)
    c_reset(img, R)
    c_lookup(img, R)


def main():
    img = Img.load()
    R = Report("riglist")
    print("== image sha256 verified, base %X" % img.base)
    check_manifest(R, "rig-index-list-producer", "49f2d7af98080cdde1a4ba3fa36fa7ec4f44439e7f8f40d3d3d95f6b3daf37f7")
    run_all(img, R)
    c_math(R)
    print("== controls (each mutation must be REJECTED)")
    ctl = [
        ("reset count compare signed (jbe -> jle at 003E3C58)", lambda: img.patched(0x003E3C58, bytes([0x7E])), c_reset),
        ("reset loop compare signed (jb -> jl at 003E3C8B)", lambda: img.patched(0x003E3C8B, bytes([0x7C])), c_reset),
        ("cache compare against eax,esi (3b c6) instead of edi", lambda: img.patched(0x003E1D4F, bytes([0x3B, 0xC6])), c_fixup),
        ("+84 store source edi -> esi (89 bf -> 89 b7 at 003E27EA)",
         lambda: img.patched(0x003E27EA, bytes([0x89, 0xB7])), c_fixup),
        ("421D20 first read at +1C instead of +18", lambda: img.patched(0x00421D28, bytes([0x1C])), c_lookup),
        ("encoder subtracts a different cell", lambda: img.patched(0x0020E622, bytes([0x0E])), c_codec),
    ]
    for label, fac, fn in ctl:
        R.check("CONTROL rejects: " + label, run_control(label, fac, fn))

    def wrong_formula(im, RR):
        Bb, rig, old88 = 0x7FF600000000, 0x7FF612345678, 0x100
        RR.check("x", Enc((rig + Dec(old88, Bb)) & M32, Bb) == (old88 + rig) & M64)  # 64-bit claim must fail
    R.check("CONTROL rejects: wrong 64-bit (no low32) fresh formula", run_control("wf", lambda: img, wrong_formula))
    print("== %d FAIL" % R.fails)
    sys.exit(1 if R.fails else 0)


if __name__ == "__main__":
    main()
