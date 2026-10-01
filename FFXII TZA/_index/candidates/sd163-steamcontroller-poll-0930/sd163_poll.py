"""sd163_poll.py - SD-163: what SteamController_PollState (007A1CD0) does with the controller state beyond the connect /
disconnect messages (OPUS, 2026-09-30). Static, the certified image, via Database/Tools/analysis-kit/gfz-scripts/retool.py.
The ISteamController method names are the Steamworks interface's vtable order (0x18 GetConnectedControllers, 0x48
GetDigitalActionData, 0x60 GetAnalogActionData, 0x88 TriggerVibration) - an identification, checked against the call
shapes, not against a symbol.
"""
import os, re, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import retool as T  # noqa: E402

R, SZ = T.R, T.sizes()
fails = 0


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def txt(a):
    i = next(R.md.disasm(R.at(a, 16), a, 1))
    return "%s %s" % (i.mnemonic, i.op_str)


ins = list(R.md.disasm(R.at(0x007A1CD0, SZ[0x007A1CD0]), 0x007A1CD0))
# P1 - the gate: the interface at [02EA9508] lists the connected controllers (+0x18); the poll runs only when the first
#      one is the stored handle [02EA95A0], logging "SteamController Connected" once (flag +0xA9), and otherwise logs the
#      disconnect once and clears the flag
check("P1", txt(0x007A1D06) == "call qword ptr [rax + 0x18]" and txt(0x007A1D18).startswith("cmp qword ptr [rsp + 0x50], r8")
      and T.cstr(0x01CB3908) == "SteamController Connected" and txt(0x007A1D44) == "mov byte ptr [rbx + 0xa9], 1"
      and T.cstr(0x01CB3928) == "SteamController Disconnected" and txt(0x007A210C) == "mov byte ptr [rbx + 0xa9], 0",
      "connected-controller gate on [02EA95A0], one-shot connect / disconnect logs")
# P2 - sixteen digital actions: for each action handle (qwords 02EA9510..02EA9590), +0x48 returns the action data and its
#      first byte (bState) is stored at this +0x43C .. +0x44B, one byte per action
dig = [i.address for i in ins if i.op_str == "qword ptr [rax + 0x48]"]
fields = sorted(set(int(m.group(1), 16) for i in ins for m in [re.match(r"byte ptr \[rbx \+ (0x4[0-9a-f]{2})\], cl", i.op_str)] if m))
check("P2", len(dig) == 16 and fields == list(range(0x43C, 0x44C)) and txt(0x007A1D77) == "movzx ecx, byte ptr [rax]",
      "16 GetDigitalActionData calls -> bytes +0x43C..+0x44B")
# P3 - two analog actions (handles 02EA9590, 02EA9598), each read twice through +0x60: x * 256 -> +0x414 / +0x418 and
#      y * -256 (inverted) -> +0x420 / +0x424
sc = struct.unpack("<f", R.at(0x00915A00, 4))[0], struct.unpack("<f", R.at(0x01CB3CF8, 4))[0]
ana = [i.address for i in ins if i.op_str == "qword ptr [rax + 0x60]"]
check("P3", len(ana) == 4 and sc == (256.0, -256.0) and txt(0x007A201F) == "mov dword ptr [rbx + 0x414], eax"
      and txt(0x007A2056) == "mov dword ptr [rbx + 0x420], eax" and txt(0x007A208D) == "mov dword ptr [rbx + 0x418], eax"
      and txt(0x007A20C3) == "mov dword ptr [rbx + 0x424], eax",
      "2 analog actions: x * 256 -> +0x414/+0x418, y * -256 -> +0x420/+0x424")
# P4 - rumble out: +0x88 (TriggerVibration) with the controller and the two motor bytes +0x98 / +0x99 scaled by 0x100
check("P4", txt(0x007A20E9) == "call qword ptr [r10 + 0x88]" and txt(0x007A2099) == "movzx r9d, byte ptr [rbx + 0x99]"
      and txt(0x007A20D4) == "movzx eax, byte ptr [rbx + 0x98]" and txt(0x007A20A1) == "mov r8d, 0x100",
      "vibration: motor bytes +0x98 / +0x99 x 256")
# P5 - then 007A15A0(this) walks the device's binding list (this +0x18) and updates each binding from its state byte
check("P5", txt(0x007A2116) == "call 0x7a15a0" and txt(0x007A15AF) == "mov rbx, qword ptr [rcx + 0x18]"
      and txt(0x007A15C5) == "mov rax, qword ptr [rbx + 0x38]",
      "then the device's binding list is updated (007A15A0)")
print("FAILS %d" % fails)
