"""sd190_tween.py - SD-190: what 003E6A70's result bit 0 reports, the bit that sends the facing integrator 002E5750
down its direct-delta path (OPUS, 2026-09-30). Static, the certified image, via Database/Tools/analysis-kit/gfz-scripts/retool.py.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import retool as T  # noqa: E402

R, SZ, c = T.R, T.sizes(), T.scan()
fails = 0


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def txt(a):
    i = next(R.md.disasm(R.at(a, 16), a, 1))
    return ("%s %s" % (i.mnemonic, i.op_str)).strip()


# T1 - 003E6A70(render record): when the record's handle resolves (003E6E60), tail-call 003AEF50 on the record's
#      embedded tween object at +0x550 (fields.tsv embeddedTweenObj)
check("T1", txt(0x003E6A79) == "call 0x3e6e60" and txt(0x003E6A89) == "lea rcx, [rbx + 0x550]" and txt(0x003E6A95) == "jmp 0x3aef50",
      "003E6A70 = resolve, then 003AEF50(record + 0x550)")
# T2 - 003AEF50 walks the tween object's node list ([+0x18], next at node +0x48) when its count [+0] is non-zero, and
#      ORs: bit 0 if any node's byte +1 is set, bit 1 if any node's byte +2 is set
check("T2", txt(0x003AEF52) == "cmp dword ptr [rcx], eax" and txt(0x003AEF56) == "mov r8, qword ptr [rcx + 0x18]"
      and txt(0x003AEF60) == "movzx ecx, byte ptr [r8 + 1]" and txt(0x003AEF6A) == "cmp byte ptr [r8 + 2], 0"
      and txt(0x003AEF6F) == "mov r8, qword ptr [r8 + 0x48]" and txt(0x003AEF78) == "or eax, 1" and txt(0x003AEF67) == "or edx, 2",
      "bit 0 = some node has byte +1, bit 1 = some node has byte +2")
# T3 - a node is started by 003AED70 (callers 003E6340 = authored command 0x1A 'move and turn toward the target along a
#      profile', and 003E65E0) from a 128-slot, 0x60-stride pool, with bytes +0..+2 = 1, 1, 1; starting one clears byte +1
#      on every node already on the object
check("T3", sorted(f for f, s in c["calls"].get(0x003AED70, ())) == [0x003E6340, 0x003E65E0]
      and txt(0x003AED9D) == "cmp edx, 0x80" and txt(0x003AED97) == "add rcx, 0x60" and txt(0x003AEDD7) == "mov word ptr [rcx], 0x101"
      and txt(0x003AEDE3) == "mov byte ptr [rcx + 2], r10b" and txt(0x003AEEA0) == "mov byte ptr [rax + 1], r11b",
      "003AED70 starts a node with +1 = +2 = 1 and clears +1 on the older nodes")
# T4 - the per-frame stepper 003AEF90 (from 003AF220): while byte +2 holds it adds a scaled vec3 (node +0x30..+0x38) to
#      the translation output and clears +2 when the move is done; while byte +1 holds it steps an angle into the
#      rotation output (+4) and clears +1 when the turn is done
check("T4", txt(0x003AF0D4) == "movss dword ptr [r14], xmm0" and txt(0x003AF0CA) == "mulss xmm0, dword ptr [rbx + 0x30]"
      and txt(0x003AF104) == "mov byte ptr [rbx + 2], 0" and txt(0x003AF1E4) == "movss dword ptr [r15 + 4], xmm4"
      and txt(0x003AF1EC) == "mov byte ptr [rbx + 1], 0" and [f for f, s in c["calls"].get(0x003AEF90, ())] == [0x003AF220],
      "byte +2 = the move phase (translation), byte +1 = the turn phase (angle)")
# T5 - the one caller 0025DF00 turns bit 0 into 002E5750's second argument (esi takes bit 1 separately)
check("T5", txt(0x0025E35A) == "call 0x3e6a70" and txt(0x0025E365) == "shr esi, 1" and txt(0x0025E36A) == "test al, 1"
      and [f for f, s in c["calls"].get(0x003E6A70, ())] == [0x0025DF00],
      "0025DF00: bit 0 -> the integrator's direct-delta argument")
# T6 - a second gate before T5 (AUDIT-SEM dd-owner-read-5 C2): 0025E31D calls 003E68B0(record) = the same resolve, then
#      003AEF20(record + 0x550) = 1 when the tween object's count [+0] is non-zero and its list [+0x18] is non-empty; the
#      result counts only when the actor's byte +0x0D has bit 1 (cmovne at 0025E32E; ebp is 0 from 0025DF1F), and 0
#      skips the 003E6A70 read, so ebp (the integrator's direct-delta argument) stays 0
check("T6", txt(0x0025E31D) == "call 0x3e68b0" and txt(0x0025E328) == "test byte ptr [rdi + 0xd], 2" and txt(0x0025E32E) == "cmovne eax, ecx"
      and txt(0x0025E333) == "je 0x25e373" and txt(0x0025DF1F) == "xor ebp, ebp" and txt(0x0025E36E) == "mov ebp, 1"
      and txt(0x003E68C9) == "lea rcx, [rbx + 0x550]" and txt(0x003E68D5) == "jmp 0x3aef20"
      and txt(0x003AEF22) == "cmp dword ptr [rcx], eax" and txt(0x003AEF26) == "cmp qword ptr [rcx + 0x18], rax",
      "the read runs only when 003E68B0 (tween armed, list non-empty) and actor +0x0D bit 1 both hold")
print("FAILS %d" % fails)
