"""sdk_vtable.py - SWE2-AUDIT-SPEC (SD-163 review, 2026-09-30). Independent check of the ISteamController method names
by vtable slot, from the Steamworks binaries shipped next to the certified game exe (no SDK header is needed):

  - steam_api64.dll (x64) and CSteamworks.dll export flat wrappers named ISteamController_<Method> /
    SteamAPI_ISteamController_<Method>; each loads the interface's vtable and calls / jumps through [vtable + disp].
    The disp of the first indirect call/jmp through a register loaded from [this] gives the slot (x64: disp/8,
    x86: disp/4), which is compared with the offsets 007A1CD0 uses (0x18, 0x48, 0x60, 0x88).
  - Every file's interface version string is printed (the game exe asks for SteamController005).
Read-only; prints to stdout.
"""
import re, sys
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64, CS_MODE_32, CS_OP_MEM

DIR = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64"
WANT = ("GetConnectedControllers", "GetDigitalActionData", "GetAnalogActionData", "TriggerVibration")


def slots(fn):
    raw = open(DIR + "\\" + fn, "rb").read()
    print("== %s  versions=%s" % (fn, sorted(set(m.group().decode() for m in re.finditer(rb"SteamController0[0-9]{2}", raw)))))
    pe = pefile.PE(data=raw)
    x64 = pe.FILE_HEADER.Machine == 0x8664
    md = Cs(CS_ARCH_X86, CS_MODE_64 if x64 else CS_MODE_32)
    md.detail = True
    w = 8 if x64 else 4
    rows = []
    for e in pe.DIRECTORY_ENTRY_EXPORT.symbols:
        if not e.name or b"ISteamController_" not in e.name:
            continue
        name = e.name.decode()
        off = pe.get_offset_from_rva(e.address)
        disp = None
        seq = []
        for i in md.disasm(raw[off:off + 0x80], pe.OPTIONAL_HEADER.ImageBase + e.address):
            seq.append("%s %s" % (i.mnemonic, i.op_str))
            if i.mnemonic in ("call", "jmp") and i.operands and i.operands[0].type == CS_OP_MEM \
                    and i.operands[0].mem.base != 0 and i.operands[0].mem.index == 0 and "rip" not in i.op_str:
                disp = i.operands[0].mem.disp
                break
            if i.mnemonic in ("ret",) or (i.mnemonic == "jmp" and not seq[-1].startswith("jmp qword") and not seq[-1].startswith("jmp dword")):
                break
            if len(seq) > 24:
                break
        rows.append((disp if disp is not None else -1, name, disp, " ; ".join(seq[-3:])))
    rows.sort()
    for d, name, disp, tail in rows:
        mark = "  <==" if any(name.endswith("_" + x) for x in WANT) else ""
        if disp is None:
            print("  %-60s  (no vtable call found)  %s" % (name, tail))
        else:
            print("  slot %2d  disp %s -> x64 0x%02X  %s%s" % (disp // w, hex(disp), (disp // w) * 8, name, mark))


for fn in ("steam_api64.dll", "CSteamworks.dll"):
    try:
        slots(fn)
    except Exception as ex:  # noqa: BLE001
        print("== %s: %s" % (fn, ex))
