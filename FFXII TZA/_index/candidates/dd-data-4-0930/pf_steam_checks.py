"""Checks for the Steam achievement catalogue page (SWE2-DATA 2026-09-30, DD owner read batch 4). Static: the shipping
image through ../rc22-34-resource-readers-0930/pe.py.

  S1 the 1101 receipt handler 0020C940 awards entry 0 itself: it compares the achieved count [rbx+0x14]
     (0020CA82), tests entry 0's +0x190 (0020CAB1) and the stats-received byte +0x18 (0020CABA), then calls
     vtable +0x38 (SetAchievement, 0020CADB) and +0x50 (StoreStats, 0020CAF2)
  S2 the 1103 receipt handler 0020C8C0 compares [rcx+0x14] (0020C8D9), tests entry 0's +0x190 (0020C908) and calls
     the award helper 0020CE10 (0020C918)
  S3 the updater 00316A50's kind-0 arm (descriptor byte +0 == 0, 00316A81) with mode 0 compares the PASSED amount
     (edi) against 003165C0's override or descriptor +4 (00316AF8..00316B0B) and fires on amount >= target
  S4 the counter reader 00316760 returns -1 for a kind-0 id other than 5 and 8 (00316774, 00316787, 0031678C ->
     0031678F jne, esi = -1 returned)
  S5 descriptor rows (00D10460, 8-byte stride): id 18 has kind 0 / mode 0; id 11 has kind 4 / mode 0 and threshold 0
  C  control: the kind-4 arm clamps a negative sum to zero (00316BA5 cmp al, 4; 00316B9F jns; 00316BA1 xor ebx, ebx),
     and the kind-2 arm saturates at 0x7FFF (00316B8B) - the arms S3 is distinguished from
"""
import os, struct, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "rc22-34-resource-readers-0930"))
from pe import dis, d, off  # noqa

FAILS = 0


def check(name, ok, detail=""):
    global FAILS
    print(("PASS " if ok else "FAIL ") + name + (" - " + detail if detail else ""))
    if not ok:
        FAILS += 1


def ops(fn):
    return {x.address: (x.mnemonic, x.op_str) for x in dis(fn)}


r = ops(0x0020C940)
check("S1 0020C940: count, entry-0 +0x190, +0x18, SetAchievement +0x38, StoreStats +0x50",
      r[0x0020CA82] == ("cmp", "dword ptr [rbx + 0x14], eax") and r[0x0020CAB1] == ("cmp", "byte ptr [rax + 0x190], 0")
      and r[0x0020CABA] == ("cmp", "byte ptr [rbx + 0x18], 0") and r[0x0020CADB] == ("call", "qword ptr [rax + 0x38]")
      and r[0x0020CAF2] == ("call", "qword ptr [rax + 0x50]"))
q = ops(0x0020C8C0)
check("S2 0020C8C0: count, entry-0 +0x190, award helper 0020CE10",
      q[0x0020C8D9] == ("cmp", "dword ptr [rcx + 0x14], eax") and q[0x0020C908] == ("cmp", "byte ptr [rdx + 0x190], 0")
      and q[0x0020C918] == ("call", "0x20ce10"))
u = ops(0x00316A50)
check("S3 updater kind-0 mode-0 arm compares the passed amount against the override / threshold",
      u[0x00316A81] == ("cmp", "byte ptr [r14 + rbp*8 + 0xbf0460], 0") and u[0x00316A68] == ("mov", "edi, edx")
      and u[0x00316AF8] == ("call", "0x3165c0") and u[0x00316B01] == ("mov", "eax, dword ptr [r14 + rbp*8 + 0xbf0464]")
      and u[0x00316B09] == ("cmp", "edi, eax") and u[0x00316B0B][0] == "jl" and u[0x00316B47] == ("call", "0x8632b0"))
v = ops(0x00316760)
check("S4 00316760 returns -1 for a kind-0 id other than 5 and 8",
      v[0x00316774] == ("cmp", "eax, -1") and v[0x00316787] == ("cmp", "bl, 5") and v[0x0031678C] == ("cmp", "bl, 8")
      and v[0x0031678F] == ("jne", "0x3167f2") and v[0x003167F7] == ("mov", "eax, esi"))


def desc(i):
    o = off(0x00D10460 + 8 * i)
    return d[o], d[o + 2], struct.unpack_from("<i", d, o + 4)[0]


k18, k11 = desc(18), desc(11)
print("   descriptor 18 (kind, mode, threshold) = %s; descriptor 11 = %s" % (k18, k11))
check("S5 id 18 kind 0 mode 0; id 11 kind 4 mode 0 threshold 0", k18[:2] == (0, 0) and k11 == (4, 0, 0))
check("C  control: kind-4 clamp and kind-2 saturation arms",
      u[0x00316BA5] == ("cmp", "al, 4") and u[0x00316B9F] == ("jns", "0x316bbd") and u[0x00316BA1] == ("xor", "ebx, ebx")
      and u[0x00316B8B] == ("mov", "eax, 0x7fff"))
print("RESULT entry 0 is awarded by the two receipt handlers; a kind-0 counter (id 18, the chain) is compared as the "
      "value passed to the updater, since the stored-counter reader returns -1 for it; kind-4 sums never go below 0")
print("FAILS %d" % FAILS)
