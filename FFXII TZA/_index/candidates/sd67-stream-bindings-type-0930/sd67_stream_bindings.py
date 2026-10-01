"""sd67_stream_bindings.py - the native type and width of PMeshInstanceSegmentContext::m_streamBindings (OPUS, 2026-09-30;
register SD-67). Asserts over the certified image via Database/Tools/analysis-kit/gfz-scripts/retool.py.
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


def txt(a):
    i = next(R.md.disasm(R.at(a, 16), a, 1))
    return "%s %s" % (i.mnemonic, i.op_str)


def raw_rtti(vt):
    col = struct.unpack("<Q", R.at(vt - 8, 8))[0]
    d = R.at(col, 0x18)
    base = col - struct.unpack_from("<I", d, 0x14)[0]
    td = base + struct.unpack_from("<I", d, 0x0C)[0]
    return R.at(td + 0x10, 200).split(b"\0")[0].decode("latin1")


# F1 - the one reference to the name "m_streamBindings" (00D4A1C0) is the registration in 005E67C0, a call to the array
#      member constructor 00632A10 with offset 0x38, a6 0, a7 (kind) 4, a8 (element size) 8, element type from 005EFE60
refs = sorted((f, a) for f, a, k in c["refs"].get(0x00D4A1C0, ()))
check("F1", refs == [(0x005E67C0, 0x005E6848)] and T.cstr(0x00D4A1C0) == "m_streamBindings"
      and txt(0x005E6823) == "call 0x5efe60" and txt(0x005E6828) == "mov dword ptr [rsp + 0x38], 8"
      and txt(0x005E6830) == "mov dword ptr [rsp + 0x30], 4" and txt(0x005E6838) == "mov dword ptr [rsp + 0x28], 0"
      and txt(0x005E6840) == "mov dword ptr [rsp + 0x20], 0x38" and txt(0x005E6860) == "call 0x632a10",
      "00632A10(member, class, elementType = 005EFE60(), \"m_streamBindings\", offset 0x38, 0, kind 4, element size 8)")
# F2 - 00632A10 (PClassDataMemberArray by RTTI of the vtable it installs, 00D58100) stores the kind at +0x5C and the
#      element size at +0x58
check("F2", txt(0x00632A21) == "mov ebx, dword ptr [rsp + 0x80]" and txt(0x00632A4D) == "mov dword ptr [rdi + 0x5c], ebx"
      and txt(0x00632A58) == "mov eax, dword ptr [rsp + 0x88]" and txt(0x00632A5F) == "mov dword ptr [rdi + 0x58], eax"
      and T.rtti_class(0x00D58100) == "Phyre::PClassDataMemberArray",
      "kind -> +0x5C, element size -> +0x58; kind 4 = PSharray (UQ-281)")
# F3 - the element type: 005EFE60 builds the static descriptor 02CEC990 (size 0x10, alignment 8 via 00632D80) and gives
#      it the vtable 00D4DD98, whose RTTI names PClassDescriptorAbstract<PSharray<const PMeshInstanceSegmentStreamBinding *>>
name = raw_rtti(0x00D4DD98)
check("F3", name == ".?AV?$PClassDescriptorAbstract@V?$PSharray@PEBVPMeshInstanceSegmentStreamBinding@PRendering@Phyre@@@Phyre@@@Phyre@@"
      and txt(0x005EFEF1) == "mov dword ptr [rsp + 0x20], 8" and txt(0x005EFEF9) == "lea r9d, [r15 + 0x10]"
      and txt(0x005EFF03) == "call 0x632d80" and txt(0x005EFF09).startswith("lea rax, [rip") and txt(0x005EFF10).endswith("rax"),
      "raw RTTI %s; descriptor size 0x10, alignment 8" % name)
print("FAILS %d" % fails)
