"""rv_rebind.py - FABLE independent re-derivation for ASTRA packet rig-owner-rebind-preconditions (b1490763c).

Own reader (rvlib.py: struct + capstone 5). Does not import ASTRA's prove.py or the shared role adapter.
Each claim group is a function of the image; the controls rerun it on privately patched copies.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rvlib import check_manifest, Img, Body, Report, expect, run_control  # noqa: E402

POOL = 0x022C6F28
PROD = (0x00372350, 0x003723A4)
LINK = (0x003E3CA0, 0x003E3D64)
FULL = (0x003E3D70, 0x003E4131)
SEC = (0x004215A0, 0x00421892)
FACT = (0x0041F340, 0x0041F72E)
M32 = 0xFFFFFFFF


def sx16(w):
    w &= 0xFFFF
    return w - 0x10000 if w & 0x8000 else w


def c_bodies(img, R):
    tot = 0
    for s, e in (PROD, LINK, FULL, SEC):
        B = Body(img, s, e)
        ents, ok = img.pdata_cover(s, e)
        rets, tails, outs = B.exits()
        R.check("body %08X..%08X decodes exactly (%d B)" % (s, e, e - s), B.exact)
        R.check("body %08X .pdata tiles it (%d record(s))" % (s, len(ents)), ok,
                " ".join("%08X..%08X%s" % (b, en, "~chain" if fl & 4 else "") for b, en, fl, r in ents))
        R.check("body %08X: no jcc leaves; rets=%s tails=%s" % (s, ["%08X" % r for r in rets],
                ["%08X->%s" % (a, "%08X" % t if t else "ind") for a, t in tails]), not outs)
        tot += e - s
    R.check("new source total 1,995 bytes (84+196+961+754)", tot == 1995, str(tot))


def c_producer(img, R):
    B = Body(img, *PROD)
    expect(R, B, 0x0037235A, "cmp dword ptr [rcx + 0x90], 0")
    expect(R, B, 0x00372366, "jle 0x372399")
    expect(R, B, 0x00372361, "mov edi, edx")
    expect(R, B, 0x00372368, "mov ecx, dword ptr [rcx + 0x94]")
    expect(R, B, 0x0037236E, "call 0x20e600")
    expect(R, B, 0x00372373, "test rax, rax")
    expect(R, B, 0x00372376, "je 0x372399")
    expect(R, B, 0x00372383, "mov dword ptr [rax + 0x68], edi")
    R.check("00372383 is a DWORD write", B[0x00372383].mems[0]["size"] == 4 and B[0x00372383].mems[0]["write"])
    expect(R, B, 0x00372391, "mov rcx, rax")
    expect(R, B, 0x00372394, "call 0x3e3d70")
    cmps = [a for a in B.order if B[a].mnemonic in ("cmp", "test")]
    R.check("producer's only guards are +90 signed>0 and Decode(+94)!=0 (no index/owner check)",
            cmps == [0x0037235A, 0x00372373], str(["%08X" % a for a in cmps]))
    R.check("edi (index) not rewritten between 00372361 and 00372383",
            not [a for a in B.order if 0x00372361 < a < 0x00372383 and "rdi" in B[a].reg_writes and B[a].mnemonic != "call"])
    F = Body(img, *FACT)
    expect(R, F, 0x0041F608, "movsx edx, word ptr [r14]")
    expect(R, F, 0x0041F60C, "mov rcx, rsi")
    expect(R, F, 0x0041F60F, "call 0x372350")
    r14w = [a for a in F.order if "r14" in F[a].reg_writes and F[a].mnemonic != "call"]
    R.check("factory r14 = its arg0 (0041F361 mov r14, rcx; only other writer is the epilogue pop)",
            r14w == [0x0041F361, 0x0041F726] and F.dominates(0x0041F361, 0x0041F608), str(["%08X" % a for a in r14w]))
    R.check("factory 0041F608 reads a WORD and sign-extends into edx", F[0x0041F608].mems[0]["size"] == 2)
    expect(R, F, 0x0041F4BC, "or dword ptr [r14 + 0x284], 0x10000")


def rebinder_common(img, R, B, s, ret, after6c_skip, cmp6c, sec_cmp):
    expect(R, B, s, "test rcx, rcx")
    R.check("%08X outer NULL rig -> %08X (ret)" % (s, ret), B[s + 3].direct_target() == ret and B[ret].mnemonic == "ret")
    o = s + 0x0E
    expect(R, B, o, "movzx eax, word ptr [rcx + 0x68]")
    expect(R, B, o + 0x0E, "cmp ax, -1")
    expect(R, B, o + 0x18, "movsx rax, ax")
    expect(R, B, o + 0x1C, "imul rcx, rax, 0x740")
    R.check("%08X adds global 022C6F28" % (o + 0x23), B[o + 0x23].mems[0]["disp"] + o + 0x23 + 7 == POOL)
    expect(R, B, o + 0x2A, "cmp dword ptr [rcx + 0x284], edi")
    expect(R, B, o + 0x30, "cmove rcx, rdi")
    expect(R, B, o + 0x34, "call 0x20e620")
    expect(R, B, o + 0x3B, "mov dword ptr [rbx + 0x70], eax")
    expect(R, B, o + 0x3E, "call 0x20e600")
    expect(R, B, o + 0x43, "mov rcx, rax")
    expect(R, B, o + 0x46, "call 0x421d20")
    call421 = o + 0x46
    R.check("%08X: xor edi,edi before the select (FFFF/inactive -> 0)" % s, B[s + 0x1A].text == "xor edi, edi")
    R.check("%08X: primary 421D20 call dominates the +6C compare and every ret after the non-NULL entry" % s,
            B.dominates(call421, cmp6c, entry=s + 9) and B.dominates(call421, ret, entry=s + 9))
    R.check("%08X: no compare/test of the derived pointer before the 421D20 call" % s,
            not [a for a in B.order if o + 0x30 < a < call421 and B[a].mnemonic in ("cmp", "test")])
    expect(R, B, cmp6c, "cmp dword ptr [rbx + 0x6c], -1")
    R.check("%08X +6C sentinel test is a full DWORD compare" % cmp6c, B[cmp6c].mems[0]["size"] == 4)
    R.check("%08X je -> %08X (secondary skip)" % (cmp6c + 7, after6c_skip), B[cmp6c + 7].mnemonic == "je" and
            B[cmp6c + 7].direct_target() == after6c_skip)
    expect(R, B, cmp6c + 9, "movzx eax, word ptr [rbx + 0x6c]")
    expect(R, B, cmp6c + 0x0D, "cmp ax, -1")
    # secondary path always calls 421D20 again
    sec_calls = [a for a, t in B.calls() if t == 0x00421D20 and a > cmp6c]
    R.check("%08X: secondary path 421D20 call %s is reached from both WORD outcomes" % (s, ["%08X" % a for a in sec_calls]),
            len(sec_calls) == 1 and sec_calls[0] in B.reach(cmp6c + 9) and
            B.dominates(cmp6c + 9, sec_calls[0], entry=s + 9))
    sx = [a for a in B.order if cmp6c < a < sec_calls[0] and B[a].text == "movsx rax, ax"]
    R.check("%08X: secondary index is the WORD sign-extended (%s)" % (s, ["%08X" % a for a in sx]), len(sx) == 1)
    # no direct +74/+7C write reachable from the skip target; rbx is not rewritten in body
    skip = B.reach(after6c_skip)
    w = [a for a in skip for m in B[a].mems if m["write"] and m["base"] == "rbx" and m["index"] is None and
         m["disp"] < 0x80 and m["disp"] + m["size"] > 0x74]
    R.check("%08X: no direct [rbx+74..7F] write reachable from the skip target %08X" % (s, after6c_skip), not w,
            str(["%08X" % a for a in w]))
    rdiw = [a for a in B.order if "rdi" in B[a].reg_writes and B[a].mnemonic != "call"]
    R.note("%08X writers of rdi (the zero source for Encode(0)): %s" % (s, ["%08X %s" % (a, B[a].text) for a in rdiw]))
    R.check("%08X: rdi stays 0 from %08X to both Encode(0) selects (only writer in between is the secondary cmove/mov)" % (s, s + 0x1A),
            [a for a in rdiw if s + 0x1A < a < cmp6c] == [])
    rbxw = [a for a in B.order if "rbx" in B[a].reg_writes and B[a].mnemonic not in ("call", "push")]
    R.check("%08X: rbx (rig) written only by the entry mov and the final pop" % s, len(rbxw) == 2, str(["%08X" % a for a in rbxw]))
    return skip


def c_link(img, R):
    B = Body(img, *LINK)
    skip = rebinder_common(img, R, B, 0x003E3CA0, 0x003E3D63, 0x003E3D59, 0x003E3D01, 0x003E3D0E)
    R.check("link-only 003E3CA0 calls only codec/421D20 (no 3E3C30 reset)",
            set(t for a, t in B.calls()) == {0x0020E600, 0x0020E620, 0x00421D20})
    R.check("link-only skip path 003E3D59 goes straight to ret", max(skip) == 0x003E3D63 and len(skip) == 4)


def c_full(img, R):
    B = Body(img, *FULL)
    skip = rebinder_common(img, R, B, 0x003E3D70, 0x003E4130, 0x003E3E28, 0x003E3DD1, 0x003E3DDE)
    expect(R, B, 0x003E3E2B, "call 0x3e3c30")
    R.check("full-reset skip target 003E3E28 still calls the 3E3C30 reset", 0x003E3E2B in skip)
    R.check("full-reset reset call is reached on both secondary outcomes (dominates ret from non-NULL entry)",
            B.dominates(0x003E3E2B, 0x003E4130, entry=0x003E3D79))


def c_secwriter(img, R):
    B = Body(img, *SEC)
    expect(R, B, 0x004215B8, "mov rsi, rcx")
    rsiw = [a for a in B.order if "rsi" in B[a].reg_writes and B[a].mnemonic != "call"]
    R.check("rsi = first argument from 004215B8 until the epilogue restore", rsiw == [0x004215B8, 0x00421883],
            str(["%08X" % a for a in rsiw]))
    expect(R, B, 0x004216D3, "movsx ebx, word ptr [rsi]")
    R.check("004216D3 reads WORD [arg0+0]", B[0x004216D3].mems[0]["size"] == 2 and B[0x004216D3].mems[0]["disp"] == 0)
    expect(R, B, 0x004216D6, "call 0x20e600")
    expect(R, B, 0x004216DB, "mov dword ptr [rax + 0x6c], ebx")
    R.check("004216DB is a full DWORD store", B[0x004216DB].mems[0]["size"] == 4)
    expect(R, B, 0x004216CC, "mov ecx, dword ptr [r14 + 0x94]")
    expect(R, B, 0x004216DE, "mov ecx, dword ptr [r14 + 0x94]")
    expect(R, B, 0x004216EA, "mov rcx, rax")
    expect(R, B, 0x004216ED, "call 0x3e3ca0")
    R.check("r14 not rewritten in 004216C6..004216ED",
            not [a for a in B.order if 0x004216C6 < a < 0x004216ED and "r14" in B[a].reg_writes and B[a].mnemonic != "call"])
    w6c = [a for a, m in B.mem_writes(lambda m: m["index"] is None and m["disp"] < 0x70 and m["disp"] + m["size"] > 0x6C
                                      and m["base"] != "rsp")]
    R.note("4215A0 direct writes overlapping +6C..+6F (any base): %s" % ["%08X %s" % (a, B[a].text) for a in w6c])


def c_repr(R):
    # reader predicates from 003E3D01/003E3D0E (and 003E3DD1/003E3DDE)
    def reader(v):
        full_skip = (v & M32) == 0xFFFFFFFF
        word_missing = (v & 0xFFFF) == 0xFFFF
        return "SKIP" if full_skip else ("WORD_MISSING_LOOKUP" if word_missing else "INDEXED")
    agree = True
    for w in range(0x10000):
        v = sx16(w) & M32  # 004216D3 movsx ebx, word / 004216DB DWORD store
        r = reader(v)
        agree &= (r == "SKIP") == (w == 0xFFFF) and r != "WORD_MISSING_LOOKUP"
    R.check("math (65,536 values): signed16 writer -> SKIP exactly for FFFF, never the WORD-missing branch", agree)
    R.check("math: 0000FFFF takes the WORD-missing lookup path, FFFFFFFF the skip",
            reader(0x0000FFFF) == "WORD_MISSING_LOOKUP" and reader(0xFFFFFFFF) == "SKIP")
    R.check("math: no signed16 value stores 0000FFFF", all((sx16(w) & M32) != 0x0000FFFF for w in range(0x10000)))
    # primary: factory movsx edx, word -> DWORD +68; reader movzx word +68 then movsx -> index
    ok = all(sx16((sx16(w) & M32) & 0xFFFF) == sx16(w) for w in range(0x10000))
    R.check("math: factory signed16 -> DWORD +68 -> reader WORD/movsx gives back the same signed16 index", ok)


def run_all(img, R):
    c_bodies(img, R)
    c_producer(img, R)
    c_link(img, R)
    c_full(img, R)
    c_secwriter(img, R)
    L = Body(img, 0x00421D20, 0x00421D66)
    R.check("421D20 writes no rdi; 20E600/20E620 write no rdi (Encode(0) source survives the primary calls)",
            not [a for a in L.order if "rdi" in L[a].reg_writes])


def main():
    img = Img.load()
    R = Report("rebind")
    print("== image sha256 verified, base %X" % img.base)
    check_manifest(R, "rig-owner-rebind-preconditions", "ffe2b7cc1ce242076b3106930ddfa1c2988d9abd20d591876b55ae103008288e")
    run_all(img, R)
    c_repr(R)
    print("== controls (each mutation must be REJECTED)")
    ctl = [
        ("secondary skip edge inverted (je -> jne at 003E3D08)",
         lambda: img.patched(0x003E3D08, bytes([0x75])), c_link),
        ("insert a derived-pointer test before 421D20 (mov rcx,rax -> test rax,rax at 003E3DC1)",
         lambda: img.patched(0x003E3DC1, bytes([0x48, 0x85, 0xC0])), c_full),
        ("secondary writer zero-extends (movsx 0f bf -> movzx 0f b7 at 004216D3)",
         lambda: img.patched(0x004216D4, bytes([0xB7])), c_secwriter),
        ("producer index guard: +90 compare jle -> jl at 00372366", lambda: img.patched(0x00372366, bytes([0x7C])), c_producer),
        ("a direct +74 clear on the link-only skip path (mov rdi,[rsp+30] -> mov [rbx+74],edi ; nop)",
         lambda: img.patched(0x003E3D59, bytes([0x89, 0x7B, 0x74, 0x90, 0x90])), c_link),
    ]
    for label, fac, fn in ctl:
        R.check("CONTROL rejects: " + label, run_control(label, fac, fn))

    def wrong_writer(im, RR):  # claim a zero-extending writer: must fail on the real bytes
        RR.check("x", any(((w & 0xFFFF) & M32) == 0x0000FFFF for w in [0xFFFF]) and
                 im.read(0x004216D3, 3) == bytes([0x0F, 0xB7, 0x1E]))
    R.check("CONTROL rejects: wrong expectation that 004216D3 is movzx", run_control("ww", lambda: img, wrong_writer))
    print("== %d FAIL" % R.fails)
    sys.exit(1 if R.fails else 0)


if __name__ == "__main__":
    main()
