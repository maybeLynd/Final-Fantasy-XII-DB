"""measuring-text-by-drawing-it-with-the-output-off (DD batch 3, SWE2-DATA 2026-09-30), static.

A1 002AF340 has one ret; eax there is r12d, or -1 when arg 4 is set, a stop-set is armed and it was never met
   (002AF902..002AF927) - the function does return a value, which the decompiler dropped.
A2 r12d starts at 0 (002AF392), gains 1 at each character-arm exit (002AF51D / 002AF535, the arm bytes > 0x0F take at
   002AF490 through 002AC2F0) and the count the interpreter 002AC5F0 reports through its 4th argument (002AF775,
   002AF79C) - so it counts the characters laid out.
A3 [rsp+0x20] = stop-set armed: ctx+0x10C8 non-null and non-empty (002AF414..002AF46D); r13d = 1 once memcmp(stop,
   text, strlen(stop)) == 0 (002AF563 -> the VCRUNTIME140 memcmp import, 002AF56F); arg 4 is kept at [rsp+0x3C].
A4 the stop-set 002ABB20 installs, 00916548, is the string 0F 23: the '#' page-wait escape.
A5 the signed text-state byte (state +0xAA, copied to [rbp+0xA]) is subtracted from the line width at three break sites
   when negative (002AF591, 002AF6A5, 002AF832) and becomes the starting width when positive (002AF75D).
A6 the stepper 002ABF70 switches on the low byte of +0xB0 through the 8-entry table at 002AC1B4; modes 3 and 7
   decrement the wait count +0x88 (002ABF9F, 002AC18B), and mode 3's expiry sets +0x9B to 0x1E (002ABFBC).
C1 control: the page's own anchor - 002B2150 nulls 0209CC48 with a zeroed rax (002B226F / 002B2271).
C2 control: a different IAT slot (00861EC0's, the memset thunk) does not resolve to memcmp, so A3's name is read.
"""
import os, struct, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "rc22-34-resource-readers-0930"))
from pe import d, off, dis, EXE  # noqa

FAILS = 0


def check(name, ok, detail=""):
    global FAILS
    print(("PASS " if ok else "FAIL ") + name + (" - " + detail if detail else ""))
    if not ok:
        FAILS += 1


def ins(fn):
    return {x.address: x for x in dis(fn)}


def iat_name(thunk):
    x = dis(thunk)[0]
    disp = int(x.op_str.split("0x")[1].rstrip("]"), 16)
    slot = thunk + x.size + disp
    import pefile
    pe = pefile.PE(EXE, fast_load=True)
    pe.parse_data_directories(directories=[pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_IMPORT"]])
    for e in pe.DIRECTORY_ENTRY_IMPORT:
        for i in e.imports:
            if i.address == slot:
                return (i.name or b"").decode()
    return None


f = dis(0x002AF340)
m = {x.address: x for x in f}
rets = [x for x in f if x.mnemonic == "ret"]
check("A1 one ret; eax = r12d, or -1 when arg4 && armed && not met",
      len(rets) == 1 and m[0x002AF922].op_str == "eax, 0xffffffff" and m[0x002AF927].op_str == "eax, r12d"
      and m[0x002AF902].op_str == "dword ptr [rsp + 0x3c], 0" and m[0x002AF915].op_str == "eax, dword ptr [rsp + 0x20]"
      and m[0x002AF91D].op_str == "r13d, r13d")
check("A2 r12d = characters: init 0, +1 per character arm, + the interpreter's reported count",
      m[0x002AF37C].op_str == "ebx, ebx" and m[0x002AF392].op_str == "r12d, ebx"
      and m[0x002AF490].op_str == "byte ptr [rbx], 0xf" and m[0x002AF4AD].op_str == "0x2ac2f0"
      and m[0x002AF51D].mnemonic == "inc" and m[0x002AF535].mnemonic == "inc"
      and m[0x002AF775].op_str == "r9, [rsp + 0x30]" and m[0x002AF783].op_str == "0x2ac5f0"
      and m[0x002AF79C].op_str == "r12d, dword ptr [rsp + 0x30]")
name = iat_name(0x00861ED2)
check("A3 armed = ctx+0x10C8 non-empty; met = memcmp match; arg4 at [rsp+0x3C]",
      m[0x002AF414].op_str == "r15, qword ptr [rax + 0x10c8]" and m[0x002AF46D].op_str == "dword ptr [rsp + 0x20], eax"
      and m[0x002AF563].op_str == "0x861ed2" and m[0x002AF56F].op_str == "r13d, eax"
      and m[0x002AF382].op_str == "dword ptr [rsp + 0x3c], r9d" and name == "memcmp", str(name))
o = off(0x00916548)
check("A4 the stop-set 00916548 is the string 0F 23 (the '#' page-wait escape)", d[o:o + 3] == b"\x0f\x23\x00",
      d[o:o + 12].hex())
sites = [a for a in (0x002AF591, 0x002AF6A5, 0x002AF75D, 0x002AF832) if m[a].op_str == "sil, sil"]
check("A5 state +0xAA: subtracted when negative at three breaks, starting width when positive",
      len(sites) == 4 and m[0x002AF479].op_str == "esi, byte ptr [rbp + 0xa]" and m[0x002AF352].op_str == "rbp, [rsp - 0x70]"
      and m[0x002AF357].op_str == "rsp, 0x170" and m[0x002AF3E8].op_str == "xmm1, xmmword ptr [rcx + 0xa0]"
      and m[0x002AF3FA].op_str == "xmmword ptr [rax + 0x20], xmm1"
      and m[0x002AF594].mnemonic == "jns" and m[0x002AF6A8].mnemonic == "jns" and m[0x002AF835].mnemonic == "jns"
      and m[0x002AF760].mnemonic == "jle" and m[0x002AF76D].op_str == "dword ptr [r14 + 0x10], xmm0")
s = ins(0x002ABF70)
tab = [0x120000 + struct.unpack_from("<I", d, off(0x002AC1B4 + 4 * i))[0] for i in range(8)]
check("A6 stepper: modes 3 and 7 decrement +0x88; mode 3's expiry sets +0x9B = 0x1E",
      s[0x002ABF7F].op_str == "eax, cl" and tab[3] == 0x002ABF9F and tab[7] == 0x002AC18B
      and s[0x002ABF9F].op_str == "eax, word ptr [rbx + 0x88]" and s[0x002AC18B].op_str == "eax, word ptr [rbx + 0x88]"
      and s[0x002ABFBC].op_str == "byte ptr [rbx + 0x9b], 0x1e", " ".join("%X" % t for t in tab))
b = ins(0x002B2150)
check("C1 control: 002B2150 nulls 0209CC48 from a zeroed rax", b[0x002B226F].op_str == "eax, eax"
      and b[0x002B2271].mnemonic == "mov" and b[0x002B2271].op_str.endswith(", rax"))
other = iat_name(0x00861EC0)
check("C2 control: another thunk resolves to a different import", other not in (None, "memcmp"), str(other))
print("RESULT 002AF340 returns the characters laid out up to the stop string, or -1 when an armed stop-set is never "
      "met; 002ABB20's stop string is the '#' page-wait escape 0F 23")
print("FAILS %d" % FAILS)
