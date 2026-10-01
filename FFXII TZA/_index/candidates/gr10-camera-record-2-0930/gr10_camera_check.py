"""gr10_camera_check.py - GR-10: when is camera record 2 the view on screen? (OPUS, 2026-09-30)
Static, the certified image (kit retool.py, regval.py, structflow.py).

C1  the view selector 00259820 (called from 00314370) shows the record of the HIGHEST set bit of the active mask
    02098DEC among bits 7..0 (rol 7, then ror 1 down to bit 0); kind +0xF0 == 1 follows the camera context +0xF4
    (00259990), 2 and 3 take other paths, anything else is a fixed pose.
C2  the mask's writers: the area-init clear 00259E90 (esi = 0) and the bit setter 0025A520(bit, on); its callers pass
    bit 5 (002555D0, on / off), bits 6 / 4 off (00258B90), bit 2 off (PartyControl_UpdateControlledActorLocomotion
    00358C60, the world tick's mode-0 step), bit 2 on (PartyFocus_ProcessActorControlPresentationState 00358F90), a
    computed bit >= 4 on (003D9150: (ebx | 8) >> 1) and bit 1 on (0050E480).
C3  record kinds +0xF0 are written by the area-init loop (0) and the kind setter 0025A500(record, kind); record 2 is
    given kind 1 only by 00358F90 (tail jump at 0035908F). Every call of 00358F90 sets both mask bit 2 and kind 1 on
    record 2 (0035906B-0035908F, reached on every path). 003D9150's index is >= 4, never 2.
C4  00358EE0 (called at the world tick's fixed tail, 00314278) calls 00358F90 on three arms: no event focus
    ([022C7FEC] == 0) with manager 0 live and the leader handle [022C7FE0] > 0; the intervention handle [022C7FE8]
    non-zero; or an event focus with a manager 1..3 live.
C5  record 2's context +0xF4 is written only by 0025A280(record, context): 1 by PartyFocus_SetSecondaryPackedActorHandle
    00359410 (setinterventioncamera) at 00359424, 0 by the same on clear (00359499) and by the manager-0 unload 002628B0
    (00262B5D); the area init leaves it 0.
Prints PASS/FAIL per check and FAILS n last.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import retool as T  # noqa: E402
import regval as V  # noqa: E402

R, SZ, c = T.R, T.sizes(), T.scan()
fails = 0


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def txt(a):
    i = next(R.md.disasm(R.at(a, 16), a, 1))
    return ("%s %s" % (i.mnemonic, i.op_str)).strip()


def rip(a):
    i = next(R.md.disasm(R.at(a, 16), a, 1))
    m = re.search(r"\[rip ([+-]) (0x[0-9a-f]+)\]", i.op_str)
    return a + i.size + int(m.group(2), 16) * (1 if m.group(1) == "+" else -1)


MASK, STACK = 0x02098DEC, 0x02097300
# C1
ok = rip(0x0025983E) == MASK and txt(0x00259851) == "mov edx, 7" and txt(0x00259856) == "rol eax, 7" \
    and txt(0x00259865) == "ror eax, 1" and txt(0x0025986F) == "imul rbx, rax, 0x110" and rip(0x00259876) == STACK \
    and txt(0x002598AA) == "mov ecx, dword ptr [rbx + 0xf0]" and txt(0x00259916) == "mov edx, dword ptr [rbx + 0xf4]" \
    and txt(0x00259921) == "call 0x259990" and sorted(set(c["calls"].get(0x00259820, ()))) == [(0x00314370, 0x003143C0)]
check("C1", ok, "the view = the highest active record (bits 7..0 of 02098DEC); kind 1 follows context +0xF4 through 00259990")
# C2
calls = sorted(set(c["calls"].get(0x0025A520, ())))
args = {s: (V.value_at(f, s, "rcx", 1), V.value_at(f, s, "rdx", 1)) for f, s in calls}
exp = {0x002556E2: ({("C", 5)}, {("C", 0), ("C", 1), ("C", 4)}), 0x00258BBE: ({("C", 6)}, {("C", 0)}),
       0x00258BD3: ({("C", 4)}, {("C", 0)}), 0x00258C15: ({("C", 6)}, {("C", 0)}), 0x00258C2A: ({("C", 4)}, {("C", 0)}),
       0x00358C77: ({("C", 2)}, {("C", 0)}), 0x00359073: ({("C", 2)}, {("C", 1)}), 0x0050E497: ({("C", 1)}, {("C", 1)})}
ok = all(args.get(s) == v for s, v in exp.items()) and set(args) == set(exp) | {0x003D9285} \
    and txt(0x003D927E) == "or ebx, 8" and txt(0x003D9281) == "shr ebx, 1" \
    and txt(0x00259EB2).startswith("mov dword ptr [rip") and rip(0x00259EB2) == MASK and V.value_at(0x00259E90, 0x00259EB2, "rsi", 1) == {("C", 0)} \
    and sorted(set(c["calls"].get(0x00358C60, ()))) == [(0x00314020, 0x003140D4)]
check("C2", ok, "mask writers: init 0; 0025A520 callers %s" % ["%08X" % s for _, s in calls])
# C3
kc = sorted(set(c["calls"].get(0x0025A500, ())))
kargs = {s: (V.value_at(f, s, "rcx", 2), V.value_at(f, s, "rdx", 2)) for f, s in kc}
rec2 = [s for s, (a, b) in kargs.items() if ("C", 2) in a]
ok = txt(0x0025A503) == "imul rcx, rax, 0x110" and rip(0x0025A50A) == STACK + 0xF0 and txt(0x0025A511) == "mov dword ptr [rcx + rax], edx" \
    and rec2 == [0x0035908F] and kargs[0x0035908F][1] == {("C", 1)} \
    and txt(0x0035906B) == "mov edx, 1" and txt(0x00359070) == "lea ecx, [rdx + 1]" and txt(0x00359073) == "call 0x25a520" \
    and txt(0x0035908F) == "jmp 0x25a500" and txt(0x00358FAF) == "je 0x35906b" and txt(0x00358FBF) == "jne 0x35906b" \
    and kargs[0x003D9291][0] == {("U", "003D9281 shr ebx, 1")}
check("C3", ok, "kind setter callers %s; record 2 -> kind 1 only at 0035908F, on every path of 00358F90" % ["%08X" % s for _, s in kc])
# C4
ok = sorted(set(c["calls"].get(0x00358EE0, ()))) == [(0x00314020, 0x00314278)] and rip(0x00358EE6) == 0x022C7FEC \
    and rip(0x00358EFC) == 0x022C7FE0 and rip(0x00358F1C) == 0x022C7FE8 \
    and [s for f, s in sorted(set(c["calls"].get(0x00358F90, ())))] == [0x00358F17, 0x00358F42, 0x00358F84]
check("C4", ok, "00358EE0 (world tick tail) calls 00358F90 for the leader focus, the intervention handle 022C7FE8, or an event focus")
# C5
cc = sorted(set(c["calls"].get(0x0025A280, ())))
cargs = {s: (V.value_at(f, s, "rcx", 1), V.value_at(f, s, "rdx", 1)) for f, s in cc}
ok = txt(0x0025A29B) == "mov dword ptr [r8 + 0xf4], edx" and cargs == {0x00262B5D: ({("C", 2)}, {("C", 0)}),
                                                                     0x00359424: ({("C", 2)}, {("C", 1)}),
                                                                     0x00359499: ({("C", 2)}, {("C", 0)})}
check("C5", ok, "record 2 context: 1 by setinterventioncamera (00359424), 0 on its clear (00359499) and the manager-0 unload (00262B5D)")
print("FAILS %d" % fails)
