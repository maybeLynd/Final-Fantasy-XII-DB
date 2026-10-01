"""seb-se-block-index.md section 3.4 correction (OPUS, 2026-09-26, on FABLE-CONTRA-OPUS-SEB-ID-BLOCK-FIELD-IS-THE-REGISTRY-INDEX):
the 'block' in a sound id's `id >> 9` is the SE-block REGISTRY INDEX (bank +0x3C), not the .seb file's block number n (bank +0x38).

STATIC, from the shipping image (sha256 73461d08...), every instruction decoded at its address - a rejecting regression:
 C1  id side: 003A1180 rebuilds (word +0xA << 16) | word +8 of registry entry k = handle low word, compares it with the handle
     (bit 31 cleared), and shifts that same word +8 left by 9 before adding the slot argument.
 C2  loader side: 003A1650 passes the registry entry's word +8 to 002DEF00, which masks it & 0x3F and forwards it as the index,
     with the file's own word +8 (n) as the second value, through 001DBD20 -> 00210B60 -> 0021B430 -> 00223AD0.
 C3  00223AD0 stores the index (its edx) at bank +0x3C and n (its r8d) at bank +0x38; its entry check compares n with the file's
     word +8.
 C4  lookup side: the group player 0021B5B0 computes id >> 9 (cdq / and 0x1FF / add / sar 9) and compares it with bank +0x3C -
     never +0x38; 0021B430 finds an installed bank by +0x3C the same way.
A reading of id >> 9 as n (bank +0x38) fails C4; a registry that did not key banks by the masked index fails C2/C3.
Writes result.json."""
import json
import os
import sys

import capstone
import pefile

HERE = os.path.dirname(os.path.abspath(__file__))
EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
IB = 0x120000
pe = pefile.PE(EXE, fast_load=True)
img = pe.get_memory_mapped_image()
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)


def ins(a, n=1):
    return [("%s %s" % (i.mnemonic, i.op_str)).strip() for i in md.disasm(img[a - IB:a - IB + 16 * n], a, count=n)]


def at(a):
    return ins(a)[0]


R = {
    "C1": {"003A11BF": at(0x3A11BF), "003A11C4": at(0x3A11C4), "003A11C9": at(0x3A11C9), "003A11CE": at(0x3A11CE),
           "003A11D7": at(0x3A11D7), "003A11DA": at(0x3A11DA), "table": at(0x3A11B8)},
    "C2": {"003A16BA": at(0x3A16BA), "003A16C3": at(0x3A16C3), "003A16CC": at(0x3A16CC), "003A16CE": at(0x3A16CE),
           "003A16D4": at(0x3A16D4), "002DEF00": at(0x2DEF00), "002DEF0B": at(0x2DEF0B), "002DEF0F": at(0x2DEF0F),
           "001DBD55": at(0x1DBD55), "00210B64": at(0x210B64), "0021B4F8": at(0x21B4F8), "0021B4F0": at(0x21B4F0),
           "0021B4FD": at(0x21B4FD), "0021B448": at(0x21B448), "0021B45A": at(0x21B45A),
           "001DBD32": at(0x1DBD32), "001DBD34": at(0x1DBD34), "001DBD41": at(0x1DBD41), "001DBD44": at(0x1DBD44)},
    "C3": {"00223B07": at(0x223B07), "00223B18": at(0x223B18), "00223C7A": at(0x223C7A), "00223C83": at(0x223C83),
           "00223C9C": at(0x223C9C), "00223B53": at(0x223B53), "00223B59": at(0x223B59)},
    "C4": {"0021B5C8": at(0x21B5C8), "0021B5CC": at(0x21B5CC), "0021B5D0": at(0x21B5D0), "0021B5DC": at(0x21B5DC),
           "0021B5DF": at(0x21B5DF), "0021B5FA": at(0x21B5FA), "0021B476": at(0x21B476)},
}
# the table base 02AEEDC0 from 003A11B8's rip-relative lea
lea = next(md.disasm(img[0x3A11B8 - IB:0x3A11B8 - IB + 16], 0x3A11B8, count=1))
R["C1"]["table_base"] = "%08X" % (lea.address + lea.size + int(lea.op_str.split("rip + ")[1].rstrip("]"), 16))
cases = {
    "C1_id_is_registry_word8_shifted_by_9_after_self_index_validation":
        R["C1"]["003A11BF"] == "movzx edx, word ptr [rcx + rax*8 + 8]" and R["C1"]["003A11C4"] == "movzx ecx, word ptr [rcx + rax*8 + 0xa]"
        and R["C1"]["003A11C9"] == "shl ecx, 0x10" and R["C1"]["003A11CE"] == "cmp ecx, r8d"
        and R["C1"]["003A11D7"] == "shl edx, 9" and R["C1"]["003A11DA"] == "add edx, ebx" and R["C1"]["table_base"] == "02AEEDC0",
    "C2_loader_masks_the_registry_word_to_the_index_and_forwards_n_separately":
        R["C2"]["003A16BA"] == "movzx ecx, word ptr [rbx + rax*8 + 8]" and R["C2"]["003A16CE"] == "cmovne ecx, edx"
        and R["C2"]["003A16D4"] == "call 0x2def00" and R["C2"]["002DEF00"] == "and ecx, 0x3f"
        and R["C2"]["002DEF0B"] == "movsx edx, word ptr [rdx + 8]" and R["C2"]["002DEF0F"] == "jmp 0x1dbd20"
        and R["C2"]["001DBD32"] == "mov edi, edx" and R["C2"]["001DBD34"] == "mov esi, ecx"
        and R["C2"]["001DBD41"] == "mov r8d, edi" and R["C2"]["001DBD44"] == "mov edx, esi" and R["C2"]["001DBD55"] == "jmp 0x210b60"
        and R["C2"]["00210B64"] == "jmp 0x21b430" and R["C2"]["0021B448"] == "mov edi, edx" and R["C2"]["0021B45A"] == "mov ebp, r8d"
        and R["C2"]["0021B4F0"] == "mov r8d, ebp" and R["C2"]["0021B4F8"] == "mov edx, edi" and R["C2"]["0021B4FD"] == "call 0x223ad0",
    "C3_bank_plus3C_is_the_index_plus38_is_n":
        R["C3"]["00223B07"] == "mov r13d, r8d" and R["C3"]["00223B18"] == "mov dword ptr [rsp + 0x34], edx"
        and R["C3"]["00223C7A"] == "mov eax, dword ptr [rsp + 0x34]" and R["C3"]["00223C83"] == "mov dword ptr [r15 + 0x3c], eax"
        and R["C3"]["00223C9C"] == "mov dword ptr [r15 + 0x38], r13d"
        and R["C3"]["00223B53"] == "movsx eax, word ptr [rbp + 8]" and R["C3"]["00223B59"] == "cmp eax, r13d",
    "C4_lookup_matches_id_shr_9_against_plus3C_not_plus38":
        R["C4"]["0021B5C8"] == "mov eax, edx" and R["C4"]["0021B5CC"] == "cdq" and R["C4"]["0021B5D0"] == "and edx, 0x1ff"
        and R["C4"]["0021B5DC"] == "lea edi, [rdx + rax]" and R["C4"]["0021B5DF"] == "sar edi, 9"
        and R["C4"]["0021B5FA"] == "cmp dword ptr [r10 + 0x3c], edi" and R["C4"]["0021B476"] == "cmp dword ptr [rdx + 0x3c], edi",
}
res = {"evidence_class": "STATIC", "live_game": False, "results": R, "cases": cases, "ok": all(cases.values())}
json.dump(res, open(os.path.join(HERE, "result.json"), "w"), indent=1, sort_keys=True)
for k, v in cases.items():
    print("%-72s %s" % (k, "PASS" if v else "FAIL"))
print("ALL PASS" if res["ok"] else "FAILED")
sys.exit(0 if res["ok"] else 1)
