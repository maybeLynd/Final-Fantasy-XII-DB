"""MapScreenPage type rows on FABLE-REQ-OPUS-MAPSCREENPAGE-TYPES-FROM-UQ156 (OPUS, 2026-09-26): a rejecting regression for the
corrections made to the type store. STATIC, from the shipping image, every instruction decoded at its address.
 E1  the +0xB140 region is an array of 0x70-byte marker entries: 00402D20 steps rbx by 0x70 (00402D88) and links each entry at
     +0x60 / +0x68 (00402D7C / 00402D80); 00402C30 copies a 0x30 record into +0x00..+0x2F (three movups) and clears +0x60 / +0x68.
 E2  the count is at most 24: the selector-2 scratch 002B7460 zeroes is 0x480 = 24 x 0x30 (002B7490), 002B74AF passes selector 2,
     and the builder 003C1A20's per-selector cap is 0x18 for its third case (003C1A71). 24 x 0x70 = 0xA80 = +0xBBC0 - +0xB140.
 N1  the +0x140 nodes are links built from selector 0 (00402A93 xor r9d, r9d before 00402A9E call 003BE3A0).
 N2  node +0x00 holds the sampled points: 004029FE / 00402A02 store float pairs, 00402A07 steps 8; +0x90 is their count, clamped to
     at most 16 (00402892 / 00402897) and at least 3 (004028A8).
 N3  node +0xA8 bit 0 is tested by the drawer (00404420) before sinf (0040444C); the drawer reads +0x90 (00404472) and follows +0x98.
A store that kept '+0xB140 96 B' / the three rows inside it, or read the +0x140 nodes as markers, contradicts E1/E2/N1.
Writes result.json."""
import json
import os
import sys

import capstone
import pefile

HERE = os.path.dirname(os.path.abspath(__file__))
EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
IB = 0x120000
img = pefile.PE(EXE, fast_load=True).get_memory_mapped_image()
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)


def at(a):
    i = next(md.disasm(img[a - IB:a - IB + 16], a, count=1))
    return ("%s %s" % (i.mnemonic, i.op_str)).strip()


SITES = {"E1": [0x402D88, 0x402D7C, 0x402D80, 0x402C3A, 0x402C43, 0x402C4A, 0x402C52, 0x402C93, 0x402C97],
         "E2": [0x2B7490, 0x2B74AF, 0x3C1A71, 0x2B74ED, 0x2B74FC, 0x2B7501],
         "N1": [0x402A93, 0x402A9E],
         "N2": [0x4029FE, 0x402A02, 0x402A07, 0x402890, 0x402892, 0x402897, 0x40289D, 0x4028A8],
         "N3": [0x404420, 0x40444C, 0x404472, 0x404481, 0x404486]}
R = {k: {"%08X" % a: at(a) for a in v} for k, v in SITES.items()}
g = lambda k, a: R[k]["%08X" % a]
cases = {
    "E1_marker_entries_are_0x70_with_links_at_60_68": g("E1", 0x402D88) == "add rbx, 0x70" and g("E1", 0x402D7C) == "mov qword ptr [rax + 0x60], rbx"
        and g("E1", 0x402D80) == "mov qword ptr [rbx + 0x68], rax" and g("E1", 0x402C43) == "movups xmmword ptr [rcx], xmm0"
        and g("E1", 0x402C4A) == "movups xmmword ptr [rcx + 0x10], xmm1" and g("E1", 0x402C52) == "movups xmmword ptr [rcx + 0x20], xmm0"
        and g("E1", 0x402C93) == "mov qword ptr [rbx + 0x60], rax" and g("E1", 0x402C97) == "mov qword ptr [rbx + 0x68], rax",
    "E2_at_most_24_entries_fill_B140_to_BBC0": g("E2", 0x2B7490) == "mov r8d, 0x480" and g("E2", 0x2B74AF) == "mov r9d, 2"
        and g("E2", 0x3C1A71) == "mov dword ptr [rsp + 0x40], 0x18" and g("E2", 0x2B74ED) == "lea rcx, [rbx + 0xb140]"
        and g("E2", 0x2B74FC) == "call 0x402d20" and g("E2", 0x2B7501) == "mov qword ptr [rbx + 0xbbc0], rax"
        and 0x480 // 0x30 == 24 and 24 * 0x70 == 0xBBC0 - 0xB140,
    "N1_link_nodes_come_from_selector_0": g("N1", 0x402A93) == "xor r9d, r9d" and g("N1", 0x402A9E) == "call 0x3be3a0",
    "N2_points_and_count_3_to_16": g("N2", 0x4029FE) == "movss dword ptr [rbx], xmm0" and g("N2", 0x402A02) == "movss dword ptr [rbx + 4], xmm1"
        and g("N2", 0x402A07) == "add rbx, 8" and g("N2", 0x402890) == "mov dword ptr [rsi], eax" and g("N2", 0x402892) == "cmp eax, 0x10"
        and g("N2", 0x402897) == "mov dword ptr [rsi], 0x10" and g("N2", 0x40289D) == "cmp dword ptr [rsi], 2"
        and g("N2", 0x4028A8) == "mov dword ptr [rsi], r14d",
    "N3_pulse_bit_and_draw_reads": g("N3", 0x404420) == "test byte ptr [rbx + 0xa8], 1" and g("N3", 0x40444C) == "call 0x861f0e"
        and g("N3", 0x404472) == "mov r8d, dword ptr [rbx + 0x90]" and g("N3", 0x404481) == "call 0x274ca0"
        and g("N3", 0x404486) == "mov rbx, qword ptr [rbx + 0x98]",
}
res = {"evidence_class": "STATIC", "live_game": False, "results": R, "cases": cases, "ok": all(cases.values())}
json.dump(res, open(os.path.join(HERE, "result.json"), "w"), indent=1, sort_keys=True)
for k, v in cases.items():
    print("%-56s %s" % (k, "PASS" if v else "FAIL"))
print("ALL PASS" if res["ok"] else "FAILED")
sys.exit(0 if res["ok"] else 1)
