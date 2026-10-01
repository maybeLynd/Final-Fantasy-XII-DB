"""rc19_blend_arms.py - RC-19: what the character render record's two blend arms do when 002EB0D0 starts a standard
motion. ORACLE, 2026-09-30. Static; every check reads the shipped bytes (capstone), none is transcribed.

Checks (each prints PASS/FAIL):
 R  routing in 002EB0D0: with the 4th argument zero, the blend (5th argument, [rsp+0x60]) is compared with 0.0;
    at or above -> call 004270A0 (002EB29F), below -> call 004272E0 (002EB2C9); the start itself is 00427320 (002EB154).
 N  004272E0 (negative blend) is one read-modify-write of dirtyFlags +0x294: and 0xFFFDFA7F, or 0x20
    (clear bits 7, 8, 10, 17; set bit 5) and nothing else.
 Z  004270A0 with blend == 0.0: calls 00426FA0, then the same mask/or as N.
 P  004270A0 with blend != 0.0: stores the blend at +0x308, and 0xFFFDFB5F, bts 8 (clear 5, 7, 10, 17; set 8).
 D  RenderRecords_ProcessDirtyState 00427DE0 takes bits 5, 7, 8 as one exclusive chain in that order:
    test 0x20 -> 0042A890; else sign of the low byte (bit 7) -> 0042B030; else bt 8 -> 00429F70.
 C  the cut leaf 00424C40 (reached from bit 5 through 0042A890 / 0042E130 -> 00423A10) writes no +0x354 and sets no
    entry bit 11; the blend leaves 00424A40 and 00424870 (reached from bit 8 through 00429F70 -> 0042DF10 ->
    00422E50 / 00422E40) store 1.0 / blend at entry +0x354 and bts 0xB on entry +0xC.
 T  00429F70 reads +0x308 (the blend the P arm stored) into the context its leaf 0042DF10 reads at +0x28.
Positive control: the database's dirty-bit table (../../../17-Presentation-Rendering/Character-Render-Records/members/
dirty-bits.tsv) must list 004272E0 and 004270A0 among bit 5's setters and 004270A0 as bit 8's setter.
"""
import io, os, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import img  # noqa: E402


def body(va, n):
    return [("%s %s" % (x.mnemonic, x.op_str)).strip() for x in img.dis(va, n)]


def text(va, n):
    return " | ".join(body(va, n))


def check(name, ok, why):
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, why))
    return ok


def main():
    res = []
    t = text(0x002EB271, 0x2EB2CE - 0x2EB271)
    res.append(check("R", "movss xmm1, dword ptr [rsp + 0x60]" in t and "comiss xmm1, xmm6" in t and "jb 0x2eb2a6" in t
                     and "call 0x4270a0" in t and "call 0x4272e0" in t and "call 0x427320" in text(0x002EB152, 8),
                     "002EB0D0: blend >= 0.0 -> 004270A0, blend < 0.0 -> 004272E0; start 00427320"))
    n = body(0x004272E0, 0x15)
    res.append(check("N", n == ["mov eax, dword ptr [rcx + 0x294]", "and eax, 0xfffdfa7f", "or eax, 0x20",
                               "mov dword ptr [rcx + 0x294], eax", "ret"], "004272E0 = %s" % " | ".join(n)))
    z = text(0x004270A0, 0x32)
    res.append(check("Z", "call 0x426fa0" in z and "and eax, 0xfffdfa7f" in z and "or eax, 0x20" in z,
                     "004270A0 zero arm: 00426FA0 then clear {7,8,10,17} set 5"))
    p = text(0x004270D2, 0x23)
    res.append(check("P", "movss dword ptr [rcx + 0x308], xmm1" in p and "and eax, 0xfffdfb5f" in p and "bts eax, 8" in p,
                     "004270A0 positive arm: +0x308 = blend, clear {5,7,10,17} set 8"))
    d = text(0x0042836D, 0x0042836D - 0x0042836D + 0x52)
    res.append(check("D", d.index("test al, 0x20") < d.index("call 0x42a890") < d.index("test al, al") <
                     d.index("call 0x42b030") < d.index("bt eax, 8") < d.index("call 0x429f70"),
                     "00427DE0: bit 5 -> 0042A890, else bit 7 -> 0042B030, else bit 8 -> 00429F70"))
    cut = text(0x00424C40, 0x135)
    bl1, bl2 = text(0x00424A40, 0x1FE), text(0x00424870, 0x1D0)
    res.append(check("C", "0x354" not in cut and "bts eax, 0xb" not in cut and all(
        "movss dword ptr [rdi + 0x354], xmm0" in b and "bts eax, 0xb" in b and "divss xmm0, xmm6" in b for b in (bl1, bl2))
        and struct.unpack("<f", img.rd(0x01CEBBA8, 4))[0] == 1.0,
        "cut 00424C40 writes no rate; 00424A40 / 00424870 store 1.0 / blend at +0x354 and set entry bit 11"))
    tt = text(0x00429F70, 0x60)
    res.append(check("T", "movss xmm0, dword ptr [rcx + 0x308]" in tt and "movss dword ptr [rsp + 0x48], xmm0" in tt
                     and "movss xmm1, dword ptr [rdi + 0x28]" in text(0x0042DF82, 8),
                     "00429F70 carries +0x308 in its context (+0x28 of rsp+0x20) to 0042DF10"))
    tsv = io.open(os.path.join(HERE, "..", "..", "..", "17-Presentation-Rendering", "Character-Render-Records", "members",
                               "dirty-bits.tsv"), encoding="utf-8").read().splitlines()
    b5 = [l for l in tsv if l.split("\t")[2:4] == ["+0x294", "5"]]
    b8 = [l for l in tsv if l.split("\t")[2:4] == ["+0x294", "8"]]
    res.append(check("control", bool(b5) and "004272E0" in b5[0] and "004270A0" in b5[0] and bool(b8) and "004270A0" in b8[0],
                     "dirty-bits.tsv: bit 5 set by 004270A0/004272E0, bit 8 set by 004270A0"))
    print("FAILS %d" % res.count(False))
    return 0 if all(res) else 1


if __name__ == "__main__":
    sys.exit(main())
