"""CONTRACT-widget-object.md section 16 restatement (OPUS, 2026-09-26, on FABLE-REQ-OPUS-WIDGET-S16-CONTINUATION-JMP-RAX): the +0x08
continuation of the release 002482E0 is skipped when null and otherwise entered by `jmp rax` after `mov rax, rbx` / `add rsp,0x20` /
`pop rbx`. STATIC, from the shipping image, every instruction decoded at its address - a rejecting regression:
 J1  002483CA reads the continuation (mov rbx, [rdi+8]) before 002483CE nulls the handler (mov [rdi], 0).
 J2  002483F8 test rbx, rbx / je 00248408, and 00248408..0024840D is add rsp,0x20 / pop rbx / ret: a null +0x08 is skipped.
 J3  002483FD..00248405 is mov rax, rbx / add rsp, 0x20 / pop rbx / jmp rax: the jump is through rax, on the caller's frame.
A reimplementation that jumps through the restored rbx, or that calls a null continuation, fails J2/J3. Writes result.json."""
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
seq = [("%08X" % i.address, ("%s %s" % (i.mnemonic, i.op_str)).strip()) for i in md.disasm(img[0x2483CA - IB:0x24840E - IB], 0x2483CA)]
d = dict(seq)
cases = {
    "J1_continuation_read_before_the_handler_is_nulled": d.get("002483CA") == "mov rbx, qword ptr [rdi + 8]" and d.get("002483CE") == "mov qword ptr [rdi], 0",
    "J2_null_continuation_is_skipped_with_a_plain_ret": d.get("002483F8") == "test rbx, rbx" and d.get("002483FB") == "je 0x248408"
        and d.get("00248408") == "add rsp, 0x20" and d.get("0024840C") == "pop rbx" and d.get("0024840D") == "ret",
    "J3_non_null_is_entered_by_jmp_rax_after_the_frame_is_restored": d.get("002483FD") == "mov rax, rbx" and d.get("00248400") == "add rsp, 0x20"
        and d.get("00248404") == "pop rbx" and d.get("00248405") == "jmp rax",
}
res = {"evidence_class": "STATIC", "live_game": False, "listing": seq, "cases": cases, "ok": all(cases.values())}
json.dump(res, open(os.path.join(HERE, "result.json"), "w"), indent=1, sort_keys=True)
for k, v in cases.items():
    print("%-66s %s" % (k, "PASS" if v else "FAIL"))
print("ALL PASS" if res["ok"] else "FAILED")
sys.exit(0 if res["ok"] else 1)
