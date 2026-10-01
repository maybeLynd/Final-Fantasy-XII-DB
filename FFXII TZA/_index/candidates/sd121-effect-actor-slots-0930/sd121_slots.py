"""sd121_slots.py - SD-121: what the three dword arrays 022D97B0 / 022D98B0 / 022D99B0 hold (OPUS, 2026-09-30). Static,
the certified image, via Database/Tools/analysis-kit/gfz-scripts/retool.py, and the script-VM verb table
01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-table.tsv.
"""
import csv, os, sys

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


def callers(f):
    return sorted(set(g for g, _ in c["calls"].get(f, ())))


A97, A98, A99 = 0x022D97B0, 0x022D98B0, 0x022D99B0
# S1 - every rip reference into the three arrays is in the ten accessor bodies below; the reset 0036E3B0 (image-base-relative)
#      zeroes all 3 x 64 dwords (and the 32 24-byte records at 022D94B0)
refs = sorted(set(f for g in range(A97, A99 + 0x100) for f, _, _ in c["refs"].get(g, ())))
ACC = {0x0036E040, 0x0036E080, 0x0036E160, 0x0036E1A0, 0x0036E4B0, 0x0036E4E0, 0x0036E620, 0x0036E7B0, 0x0036E7E0, 0x0036E880}
reset = txt(0x0036E414).endswith("0x21b97b0], r8d") and txt(0x0036E42F).endswith("0x21b98b0], r8d") and txt(0x0036E44C).endswith("0x21b99b0], r8d")
check("S1", set(refs) == ACC and reset and txt(0x0036E3FC) == "mov edx, 0x3f" and txt(0x0036E454) == "cmp eax, 0x40",
      "rip references only from the 10 accessors (%d); 0036E3B0 zeroes 64 slots of each (base-relative stores)" % len(refs))
# S2 - one accessor trio per array: get (slot <= 63, else 0), set (slot clamped to 0..63), clear
trio = {A98: (0x0036E4B0, 0x0036E7B0, 0x0036E040), A97: (0x0036E4E0, 0x0036E7E0, 0x0036E160), A99: (0x0036E620, 0x0036E880, 0x0036E1A0)}
ok = True
for arr, fs in trio.items():
    for f in fs:
        ok &= any(g == arr for g in range(arr, arr + 1) for fn, _, _ in c["refs"].get(arr, ()) if fn == f)
check("S2", ok and txt(0x0036E4B0) == "cmp ecx, 0x3f" and txt(0x0036E4BF) == "mov eax, dword ptr [rcx + rax*4]"
      and txt(0x0036E7C0) == "mov dword ptr [rcx + rax*4], edx" and txt(0x0036E05A) == "mov dword ptr [rcx + rax*4], 0",
      "get / set / clear per array: 022D98B0 (0036E4B0/7B0/040), 022D97B0 (4E0/7E0/160), 022D99B0 (620/880/1A0)")
# S3 - the writers are four script verbs (scriptvm-verb-table.tsv): effectactor 0x126 = 00352270 (sets 022D97B0 or
#      022D99B0), bgeffectactor 0x570 = 00352940 (sets 022D98B0), clear_effectactor 0x56F = 00342010 (clears 022D97B0 and
#      022D99B0), clear_bgeffectactor 0x571 = 003423C0 (clears 022D98B0)
vt = os.path.join(HERE, "..", "..", "..", "01-Script-VM-Native-Bridge", "Verb-Dispatch", "scriptvm-verb-table.tsv")
verbs = {r["verb"]: (r["call_id"], r["arg_handler"]) for r in csv.DictReader(open(vt, encoding="utf-8"), delimiter="\t")}
check("S3", verbs.get("effectactor") == ("0126", "00352270") and verbs.get("bgeffectactor") == ("0570", "00352940")
      and verbs.get("clear_effectactor") == ("056F", "00342010") and verbs.get("clear_bgeffectactor") == ("0571", "003423C0")
      and callers(0x0036E880) == [0x00352270] and callers(0x0036E7E0) == [0x00352270] and callers(0x0036E7B0) == [0x00352940]
      and callers(0x0036E1A0) == [0x00342010] and callers(0x0036E160) == [0x00342010] and callers(0x0036E040) == [0x003423C0],
      "setters and clearers are the verbs effectactor / bgeffectactor / clear_effectactor / clear_bgeffectactor")
# S4 - effectactor stores, at the slot its argument names (00267E10), the packed handle of the running script's actor
#      (00263F10 -> 003589B0); a script context with byte +0x15 == 3 writes 022D99B0, any other 022D97B0
check("S4", txt(0x00352280) == "call 0x267e10" and txt(0x0035228A) == "call 0x263f10" and txt(0x00352292) == "call 0x3589b0"
      and txt(0x00352297) == "cmp byte ptr [rbx + 0x15], 3" and txt(0x003522AB) == "jmp 0x36e880" and txt(0x003522BA) == "jmp 0x36e7e0"
      and txt(0x00352962) == "call 0x3589b0",
      "value = the script actor's packed handle; slot = the verb argument; table by the context's +0x15")
# S5 - the readers are the effect-element bodies 003A40F0 / 003A4220: the table is chosen by the mode word at
#      [02F97348]+0x36A (bits 12-14 == 3 -> 022D99B0) and byte [02F97348] (== 2 -> 022D98B0), else 022D97B0; the handle
#      is resolved (ActorHandle_ResolveRegistryEntryByPackedId 003588B0) and the actor's position copied to the
#      element's +0x30 / +0x34 / +0x38 (00265020)
check("S5", txt(0x003A4118) == "movzx eax, word ptr [rcx + 0x36a]" and txt(0x003A4122) == "mov edx, 0x3000"
      and txt(0x003A412E) == "call 0x36e620" and txt(0x003A4179) == "cmp byte ptr [rcx], 2" and txt(0x003A4180) == "call 0x36e4b0"
      and txt(0x003A4189) == "call 0x36e4e0" and txt(0x003A4147) == "call 0x3588b0" and txt(0x003A4160) == "call 0x265020"
      and txt(0x003A415C) == "lea rdx, [rbx + 0x30]"
      and callers(0x0036E4B0) == callers(0x0036E4E0) == callers(0x0036E620) == [0x003A40F0, 0x003A4220],
      "effects read the slot's actor handle, resolve it and anchor at the actor's position")
print("FAILS %d" % fails)
