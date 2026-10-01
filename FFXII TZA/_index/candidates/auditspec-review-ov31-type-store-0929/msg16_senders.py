"""msg16_senders.py - SWE2-AUDIT-SPEC (OV-31 review, 2026-09-29).

The page says bit 0 of the asset's +0xC0 "is set only by the batch's message 16". The only writer is the msg-16 arm of
the own handler (003940E3), so the sentence is really a claim about SENDERS of message 16 that can reach this object.
This lists every `mov dword ptr [rsp+disp8], 0x10` (C7 44 24 xx 10 00 00 00) in executable sections whose next
<=12 instructions include an indirect call through a handler slot (call qword ptr [reg] / call reg after mov reg,[reg]),
grouped by .pdata chain root - the widget message-send shape the batch uses at 00249456/0024953B/0024960B.
It is a candidate census of the send shape, not a reachability proof: it bounds what the sentence would have to exclude.
"""
import struct, sys
import ov31_indep as T

PDATA = []
dd = T.pe.OPTIONAL_HEADER.DATA_DIRECTORY[3]
o = T.off(T.IB + dd.VirtualAddress)
for k in range(dd.Size // 12):
    PDATA.append(struct.unpack_from("<III", T.raw, o + 12 * k))
PDATA.sort()
import bisect
STARTS = [e[0] for e in PDATA]


def root(va):
    rva = va - T.IB
    j = bisect.bisect_right(STARTS, rva) - 1
    if j < 0 or not (PDATA[j][0] <= rva < PDATA[j][1]):
        return None
    e = PDATA[j]
    while True:
        uo = T.off(T.IB + e[2])
        flags = T.raw[uo] >> 3
        cnt = T.raw[uo + 2]
        if not (flags & 4):
            return T.IB + e[0]
        e = struct.unpack_from("<III", T.raw, uo + 4 + ((cnt + 1) & ~1) * 2)


pat = b"\xC7\x44\x24"
hits = {}
for n, v, vs, p, rs in T.TEXT:
    blob = T.raw[p:p + min(vs, rs)]
    k = blob.find(pat)
    while k >= 0:
        if blob[k + 4:k + 8] == b"\x10\x00\x00\x00":
            va = v + k
            ins = list(T.md.disasm(blob[k:k + 80], va, 13))
            if ins and ins[0].size == 8:
                calls = [i for i in ins[1:] if i.mnemonic == "call" and ("qword ptr [r" in i.op_str and "rip" not in i.op_str
                                                                        or i.op_str in ("rax", "rcx", "rdx", "r8", "r9"))]
                if calls:
                    hits.setdefault(root(va), []).append((va, calls[0].address, calls[0].op_str))
        k = blob.find(pat, k + 1)
print("msg-16 send-shape sites: %d in %d functions" % (sum(len(x) for x in hits.values()), len(hits)))
for r in sorted(hits, key=lambda x: x or 0):
    print("  %s  %s" % ("%08X" % r if r else "--------",
                        ", ".join("%08X->%08X call %s" % h for h in hits[r])))
