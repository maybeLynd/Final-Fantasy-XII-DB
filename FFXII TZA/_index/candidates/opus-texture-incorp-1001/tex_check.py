"""tex_check.py - the instruction facts OPUS's texture incorporation cites, re-read from the certified image (OPUS, 2026-10-01).

ASTRA's nine texture packages (ACCEPTed by SWE2-AUDIT-SPEC) are the evidence; this is OPUS's own cheap re-read of the
facts the incorporated notes state, and the regression for the one correction:

  T1  0061C250 (the 0x58-record tail fill) stores through rax = rcx + 0x10: qwords at record +0..+0x30, a dword at +0x38
      and the 00D54348 vtable at +0x40. REJECTS the page's old reading (dword at +0x28, vtable at +0x30).
  T2  00613770 (the head copy) copies qwords +0..+0x30, the dword +0x38, stores the vtable at +0x40, copies +0x48 / +0x50.
  T3  00627DA0 clears bit 31 of the old count and sets r9d = min(new, old) by cmp/cmovb right before calling 0061D100.
  T4  00628100: the 0062BCB0 gate exits before both; the 0062B100 wait precedes the 0062B100->00627DA0 resize on rbx+0x30.
  T5  0062EC70 selects context + 0x38*bank and compares node key +0x20.
  T6  00185A50 submits with the pre-call bank (01F7F590) and then stores (bank + 1) & 3.
  T7  00186610 reads dword +0x10 and the context 01F7F5B8, then tails 0062EBC0.
  T8  0062C360 returns 3 when the index is not below the element count.
Prints PASS/FAIL per check and FAILS n.
"""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(DB, "FFXII TZA", "_index", "candidates", "rc9-log-channels-0930"))
import rc9_channels as R  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64  # noqa: E402

md = Cs(CS_ARCH_X86, CS_MODE_64)
fails = 0


def check(tag, ok, text=""):
    global fails
    print("%s %s %s" % ("PASS" if ok else "FAIL", tag, text))
    fails += 0 if ok else 1


def dis(a, n):
    return list(md.disasm(R.at(a, n), a))


def rip(i):
    m = re.search(r"\[rip ([+-]) (0x[0-9a-f]+)\]", i.op_str)
    return (i.address + i.size + (1 if m.group(1) == "+" else -1) * int(m.group(2), 16)) if m else None


def at(ins, a):
    return next((i for i in ins if i.address == a), None)


def stores(ins, base_off):
    """record offset -> width for stores through [rcx] and [rax +/- d], with rax = rcx + base_off."""
    out = {}
    for i in ins:
        if i.mnemonic != "mov" or not i.op_str.startswith(("qword ptr [", "dword ptr [")):
            continue
        w = 8 if i.op_str.startswith("qword") else 4
        m = re.match(r"\w+ ptr \[(rcx|rax)(?: ([+-]) (0x[0-9a-f]+|\d+))?\], (\w+)", i.op_str)
        if not m:
            continue
        d = int(m.group(3), 0) if m.group(3) else 0
        d = -d if m.group(2) == "-" else d
        out[(base_off if m.group(1) == "rax" else 0) + d] = (w, m.group(4))
    return out


# T1
ins = dis(0x61C250, 0x5D)
lea = at(ins, 0x61C25F)
vt = at(ins, 0x61C263)
st = stores([i for i in ins if 0x61C279 <= i.address <= 0x61C297], 0x10)
want = {o: 8 for o in range(0, 0x31, 8)}
want.update({0x38: 4, 0x40: 8})
got = {o: w for o, (w, _r) in st.items()}
check("T1", lea and lea.op_str == "rax, [rcx + 0x10]" and vt and rip(vt) == 0xD54348 and got == want and st[0x40][1] == "r10"
      and not (got.get(0x28) == 4 or st.get(0x30, (0, ""))[1] == "r10"),
      "record stores %s (old reading dword+0x28 / vtable+0x30 rejected)" % sorted((hex(o), w) for o, w in got.items()))
# T2
ins = dis(0x613770, 0x85)
dst = {}
for i in ins:
    m = re.match(r"(qword|dword) ptr \[rax(?: \+ (0x[0-9a-f]+|\d+))?\], (\w+)", i.op_str)
    if i.mnemonic == "mov" and m:
        dst[int(m.group(2), 0) if m.group(2) else 0] = (8 if m.group(1) == "qword" else 4, m.group(3))
check("T2", {o: w for o, (w, _r) in dst.items()} == {**{o: 8 for o in range(0, 0x31, 8)}, 0x38: 4, 0x40: 8, 0x48: 8, 0x50: 4}
      and dst[0x40][1] == "r10" and rip(at(ins, 0x61377F)) == 0xD54348, sorted((hex(o), w) for o, (w, _r) in dst.items()))
# T3
ins = dis(0x627DA0, 0xAF)
seq = [(i.address, i.mnemonic, i.op_str) for i in ins]
check("T3", (0x627DB9, "btr", "r9d, 0x1f") in seq and (0x627DDE, "cmp", "esi, r9d") in seq and (0x627DE4, "cmovb", "r9d, esi") in seq
      and (0x627DE8, "call", "0x61d100") in seq and (0x627DF9, "lea", "eax, [rbp + 0xd]") in seq, "clamp + 0xD failure")
# T4
ins = dis(0x628100, 0x99)
seq = [(i.address, i.mnemonic, i.op_str) for i in ins]
check("T4", (0x628118, "call", "0x62bcb0") in seq and (0x62811F, "jne", "0x62818e") in seq and (0x628129, "call", "0x62b100") in seq
      and (0x628130, "lea", "rcx, [rbx + 0x30]") in seq and (0x628134, "call", "0x627da0") in seq and (0x628157, "cmove", "rax, rdx") in seq
      and (0x62815B, "cmp", "qword ptr [rax], rdx") in seq, "gate -> wait -> resize -> masked-0 selects null and reads it")
# T5
ins = dis(0x62EC70, 0x40)
seq = [(i.address, i.mnemonic, i.op_str) for i in ins]
check("T5", (0x62EC79, "imul", "rsi, rax, 0x38") in seq and (0x62EC90, "cmp", "qword ptr [rax + 0x20], rdx") in seq, "bank stride 0x38, key +0x20")
# T6
ins = dis(0x185A50, 0x2D)
a = {i.address: i for i in ins}
check("T6", rip(a[0x185A54]) == 0x1F7F590 and a[0x185A54].op_str.startswith("r8d,") and a[0x185A62].op_str == "0x5fea50"
      and rip(a[0x185A67]) == 0x1F7F590 and a[0x185A6D].mnemonic == "inc" and a[0x185A6F].op_str == "eax, 3" and rip(a[0x185A72]) == 0x1F7F590,
      "pre-call bank, then (bank+1)&3 regardless of the call's result")
# T7
ins = dis(0x186610, 0x0F)
a = {i.address: i for i in ins}
check("T7", a[0x186610].op_str == "edx, dword ptr [rcx + 0x10]" and rip(a[0x186613]) == 0x1F7F5B8 and a[0x18661A].op_str == "0x62ebc0",
      "bank +0x10, current context, tail 0062EBC0")
# T8
ins = dis(0x62C360, 0x48)
seq = [(i.address, i.mnemonic, i.op_str) for i in ins]
check("T8", (0x62C399, "cmp", "edx, eax") in seq and (0x62C39B, "jb", "0x62c3a7") in seq and (0x62C39D, "mov", "eax, 3") in seq, "index guard")
print("FAILS", fails)
sys.exit(1 if fails else 0)
