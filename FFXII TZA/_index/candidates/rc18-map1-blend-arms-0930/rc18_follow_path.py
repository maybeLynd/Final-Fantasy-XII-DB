"""rc18_follow_path.py - RC-18: which party map the follow machinery, the appearance verbs, the unit re-bind and the
model read-in each consult. ORACLE, 2026-09-30. Static; every check reads the shipped bytes.

 F1 0031B810 (BattleUnit_FindMappedDefinitionSelectorByIndex): class-0x17 check, then byte [[02EBF190] + i*2 + 0x5A5A]
    (map 1), tail-jump 002367A0 (BattleUnit_FindByDefinitionSelector).
 F2 PartyFollow_SolveFormation 00338490: per slot i < 4, 0031B810(i); skips (+0x64 | +0x3C) & 0x80000003 and the
    unit equal to BattleUnit_GetPartyLeader 003272A0.
 F3 PartyFollow_ApplyGoal 003246C0 walks 0030A880(buf, 1) -> 0030A8A0(buf, 4, 1): slots i < 4 through 0031B810; with
    flag 1 a unit with KO / Stone / X-Zone is dropped unless 00377C20 (field record bit 15) holds; no bit-4, no kind test.
 F4 the appearance verbs' collector 0031B5A0 reads map 1 (+0x5A5A) inline.
 F5 BattleGroup_RefreshFourActorDefinitions 003266C0 ends with a loop over roster slots 0..3 (PartyRoster_GetActorBySlot
    00263750) that compares each slot's unit definition with word [r15] (r15 = block + 0x5A48 + 0x12 = map 1) and
    re-binds the unit through BattleUnit_ApplyUnitDefinition 0023A570.
 F6 0031C250, called by the read-in machine 0037B4D0 (0037B59F), answers a roster actor's definition from map 4
    (+0x5A90), not map 1.
Positive control: F1's read site is 0031B841, the address the roster page cites for the same read.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import img  # noqa: E402


def text(root):
    return " | ".join(("%08X %s %s" % (x.address, x.mnemonic, x.op_str)).strip() for x in img.fn_ins(root))


def check(name, ok, why):
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, why))
    return ok


def main():
    r = []
    f1 = text(0x0031B810)
    r.append(check("control", "0031B841 movzx eax, byte ptr [rax + rbx*2 + 0x5a5a]" in f1, "0031B841 reads map 1"))
    r.append(check("F1", "lea ecx, [r8 + 0x17]" in f1 and "call 0x322c50" in f1 and f1.count("jmp 0x2367a0") == 2,
                   "0031B810: class 0x17, map-1 byte, tail 002367A0"))
    f2 = text(0x00338490)
    r.append(check("F2", "003385C2 call 0x31b810" in f2 and "test edx, 0x80000003" in f2 and "003385EC call 0x3272a0" in f2
                   and "00338686 cmp esi, 4" in f2, "00338490: map-1 slot walk, status and leader gates"))
    f3a, f3b = text(0x003246C0), " | ".join(("%08X %s %s" % (x.address, x.mnemonic, x.op_str)).strip() for x in img.dis(0x0030A880, 0x1F))
    f3c = text(0x0030A8A0)
    r.append(check("F3", "call 0x30a880" in f3a and "003246D9 mov edx, 1" in f3a and "call 0x339a60" in f3a
                   and "mov edx, 4" in f3b and "jmp 0x30a8a0" in f3b and "call 0x31b810" in f3c and "cmp esi, 4" in f3c
                   and "test eax, 0x80000003" in f3c and "call 0x377c20" in f3c,
                   "003246C0 -> 0030A880(buf,1) -> 0030A8A0: map-1 walk, status gate waived by field bit 15"))
    f4 = " | ".join(("%s %s" % (x.mnemonic, x.op_str)).strip() for x in img.dis(0x0031B5A0, 0xD0))
    r.append(check("F4", "0x5a5a" in f4, "0031B5A0 reads map 1"))
    f5 = text(0x003266C0)
    r.append(check("F5", "003266FC lea r15, [rdi + 0x12]" in f5 and "00326A42 call 0x263750" in f5
                   and "00326A7B movzx esi, word ptr [r15]" in f5 and "00326B0A call 0x23a570" in f5,
                   "003266C0 tail: roster slot i's unit re-bound to map 1 word i"))
    f6 = text(0x0031C250)
    r.append(check("F6", "0x5a90" in f6 and "call 0x263750" in f6 and "0037B59F call 0x31c250" in text(0x0037B4D0),
                   "0031C250 (from the read-in machine) answers a roster actor's definition from map 4"))
    print("FAILS %d" % r.count(False))
    return 0 if all(r) else 1


if __name__ == "__main__":
    sys.exit(main())
