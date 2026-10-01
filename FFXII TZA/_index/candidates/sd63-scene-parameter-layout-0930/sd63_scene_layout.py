"""sd63_scene_layout.py - what the 703-byte body 005FD2A0 (PClassLayoutInterface fetched at 00608DA2's callee) lays out
(OPUS, 2026-09-30; register SD-63). Asserts over the certified image via Database/Tools/analysis-kit/gfz-scripts/retool.py
and prints the table it reads.
"""
import os, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import retool as T  # noqa: E402

R = T.R
fails = 0


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def txt(a):
    i = next(R.md.disasm(R.at(a, 16), a, 1))
    return "%s %s" % (i.mnemonic, i.op_str)


# F1 - the loop: 0x17 source entries of 16 bytes at 00D3EB38 ({name at -8, dword, dword}) -> 24-byte records at
#      02CB7DA8: the name copied into the pool at 02CBC390, the two dwords as bytes at -6 / -5, word +8 zeroed, word +0xA
#      cut to its top 3 bits; the count 0x80000017 at 02CB8448
check("F1", txt(0x005FD2F8) == "mov dword ptr [rip + 0x26bb146], 0x80000017" and txt(0x005FD317) == "mov r15d, 0x17"
      and txt(0x005FD32A) == "mov rdx, qword ptr [r14 - 8]" and txt(0x005FD373) == "mov eax, dword ptr [r14]"
      and txt(0x005FD376) == "mov byte ptr [rdi - 6], al" and txt(0x005FD37D) == "mov byte ptr [rdi - 5], al"
      and txt(0x005FD380) == "mov word ptr [rdi + 8], r12w" and txt(0x005FD389) == "shr ax, 0xd"
      and txt(0x005FD39B) == "add r14, 0x10" and txt(0x005FD39F) == "add rdi, 0x18",
      "23 records built from the 16-byte source table 00D3EB38")
rows = []
for k in range(23):
    e = 0x00D3EB38 + 0x10 * k
    nm = T.cstr(struct.unpack("<Q", R.at(e - 8, 8))[0])
    d0, d1 = struct.unpack("<II", R.at(e, 8))
    rows.append((nm, d0, d1))
    print("      %2d %-34s index %2d  type code %d" % (k, nm, d0, d1))
names = [r[0] for r in rows]
check("F2", names[:7] == ["EyeDirWS", "EyePosWS", "Proj", "View", "ViewInv", "ViewInvTranspose", "ViewProj"]
      and names[-1] == "SceneWideParameterConstantBuffer" and "Time" in names and "GlobalAmbientColor" in names
      and all(d1 == 49 for n, _, d1 in rows if n in ("Proj", "View", "ViewInv", "ViewInvTranspose", "ViewProj"))
      and all(d1 == 52 for n, _, d1 in rows if n.endswith(("Texture", "Buffer"))),
      "the scene-wide shader parameters: matrices type 49, textures / buffers type 52")
# F3 - the layout: 005FD700(8, [02CB8450], count, &size, layout interface 006372B0()); the size rounded up to 16 is stored
#      at 02CB8458, and a zeroed buffer of size x (even instance count) is allocated at 02CB8460
check("F3", txt(0x005FD3AD) == "call 0x6372b0" and txt(0x005FD3BE) == "mov qword ptr [rsp + 0x20], rax" and txt(0x005FD3D6) == "call 0x5fd700"
      and txt(0x005FD3E2) == "add eax, 0xf" and txt(0x005FD3E5) == "and eax, 0xfffffff0" and txt(0x005FD401) == "call 0x17d260"
      and txt(0x005FD422) == "call 0x861ec0",
      "005FD700 lays the records out with the PClassLayoutInterface; size rounded to 16 (02CB8458), buffer 02CB8460 zeroed")
print("FAILS %d" % fails)
