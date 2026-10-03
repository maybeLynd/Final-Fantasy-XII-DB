"""S-43: execute CONTRACT-save-image-pipeline.md's seven bodies - the clears 002EF5F0 / 002EF650, the getters 002EF640 / 002EF620
/ 002EF630, the backup copy 002EF570 and the submission copy 002EF690 - and test SV-1..SV-6 (OPUS, 2026-09-25, block 335).

Evidence class: NATIVE-REPLAY (unicorn), live_game false. The contract's section 13: "No experiment executes these seven bodies".
world.py (block 318/319's builder, Session; UCRT rand bridge from block 332) supplies the image, the IAT traps and the named
bridges (memset among them); shipped_pack.py binds battle_pack by shipped code, for the compound clear's reinitialisers.
No application stub. STOP BOUNDARIES (recorded, nothing substituted): 0020E540, the platform write 002EF690 tail-jumps into (it fetches the
platform storage object 001C18E0), its arguments recorded; and 001DBAC0, where the compound clear's 00253A80 applies
sound settings through the audio registry (S-41's object). Fixtures: the four buffers' contents (patterns),
the selector bit d[q[02EBF190]+4] bit 12 that 00236760 returns, and six idle objects (zeroed blocks, the world's
convention): [0209BE80], [01F7FFE0], [0215E6E0], [0209CC40], and [02092758] / [020927C0], which the compound clear's
00253A80 clears (0x58 and 0x4818 bytes).
Writes result.json next to this file.
"""
import hashlib
import json
import os
import struct

from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.x86_const import UC_X86_REG_RAX, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_RIP

import world as W
import shipped_pack as SP

HERE = os.path.dirname(os.path.abspath(__file__))
FX = json.load(open(os.path.join(HERE, "world.json")))
CLEAR, CLEAR2, GET_ACTIVE, GET_CAPTURE, GET_SUBMIT, BACKUP, SUBMIT = 0x2EF5F0, 0x2EF650, 0x2EF640, 0x2EF620, 0x2EF630, 0x2EF570, 0x2EF690
WRITER, SELECTOR = 0x20E540, 0x236760
ACTIVE, CAPTURE, SUBMISSION, BACKUPBUF = 0x2164280, 0x21BA940, 0x2211000, 0x22676C0
IMAGE, GAP = 0x56690, 0x566C0
AUDIO = 0x1DBAC0
W.ALLOWED |= {0x16D6A0, WRITER, AUDIO} | SP.allowed(W) | set().union(*(W.closure(f) for f in (CLEAR, CLEAR2, GET_ACTIVE, GET_CAPTURE,
                                                                                        GET_SUBMIT, BACKUP, SUBMIT)))
S = W.Session(FX["fixes"], FX["inits"])
uc = S.uc
made, skipped = SP.bind(W, S)
IDLE = 0x76200000
for i, cell in enumerate((0x209BE80, 0x1F7FFE0, 0x215E6E0, 0x209CC40, 0x2092758, 0x20927C0)):   # +2: 00253A80 clears these
    uc.mem_write(IDLE + i * 0x20000, bytes(0x20000))
    uc.mem_write(cell, struct.pack("<Q", IDLE + i * 0x20000))
STATS_BLOCK = struct.unpack("<Q", bytes(uc.mem_read(0x2EBF190, 8)))[0]

ev = {}


def on_writer(u, a, n, _):
    ev["writer"] = ["%X" % (u.reg_read(r) & 0xFFFFFFFFFFFFFFFF) for r in (UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8)]
    u.emu_stop()


uc.hook_add(UC_HOOK_CODE, on_writer, begin=WRITER, end=WRITER)


def on_audio(u, a, n, _):
    ev["stopped_at"] = "001DBAC0 audio"
    u.emu_stop()


uc.hook_add(UC_HOOK_CODE, on_audio, begin=AUDIO, end=AUDIO)
snap = {}
uc.hook_add(UC_HOOK_CODE, lambda u, a, n, _: snap.setdefault("at_253A80", bytes(u.mem_read(ACTIVE, IMAGE + 0x30))), begin=0x253A80,
            end=0x253A80)
uc.hook_add(UC_HOOK_CODE, lambda u, a, n, _: ev.setdefault("order", []).append("selector 00236760"), begin=SELECTOR, end=SELECTOR)
first_sub_write = {}


def on_sub_write(u, acc, a, n, v, _):
    if "first" not in first_sub_write:
        first_sub_write["first"] = "%08X" % u.reg_read(UC_X86_REG_RIP)
        ev.setdefault("order", []).append("first write to the submission buffer")


uc.hook_add(UC_HOOK_MEM_WRITE, on_sub_write, begin=SUBMISSION, end=SUBMISSION + IMAGE)
for a, nm in ((0x253A80, "00253A80 header/image reinit"), (0x2EF2D0, "002EF2D0"), (0x238A80, "00238A80"), (0x16D6A0, "0016D6A0")):
    uc.hook_add(UC_HOOK_CODE, lambda u, x, n, _, nm=nm: ev.setdefault("called", []).append(nm), begin=a, end=a)


def call(fn, *args):
    ev.clear()
    first_sub_write.clear()
    ok = S.call(fn, *args)
    return ok, uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFFFFFFFFFF


def pattern(seed, n=IMAGE + 0x30):
    return hashlib.shake_256(seed).digest(n)


def fill(addr, b):
    uc.mem_write(addr, b)


def region(addr, n):
    return bytes(uc.mem_read(addr, n))


results, allok = {}, True


def record(name, ok, **kw):
    global allok
    allok &= bool(ok)
    results[name] = dict(pass_=bool(ok), **kw)
    print("%-34s %s  %s" % (name, "PASS" if ok else "FAIL", kw.get("note", "")))


# ---- SV-1: the getters and the spacing ----
got = {nm: call(fn)[1] for nm, fn in (("active 002EF640", GET_ACTIVE), ("capture 002EF620", GET_CAPTURE), ("submission 002EF630", GET_SUBMIT))}
record("SV1_getters_and_spacing", got == {"active 002EF640": ACTIVE, "capture 002EF620": CAPTURE, "submission 002EF630": SUBMISSION}
       and CAPTURE - ACTIVE == GAP and SUBMISSION - CAPTURE == GAP and BACKUPBUF - SUBMISSION == GAP,
       getters={k: "%X" % v for k, v in got.items()}, gaps=["%X" % (b - a) for a, b in ((ACTIVE, CAPTURE), (CAPTURE, SUBMISSION),
                                                                                         (SUBMISSION, BACKUPBUF))],
       note="the three getters return 02164280 / 021BA940 / 02211000; with the backup 022676C0 the gaps are 0x566C0 each - 0x30 of "
            "padding past each 0x56690 image")

# ---- SV-2: both copies are complete, tail included, and stop at the image ----
src = pattern(b"active")
fill(ACTIVE, src[:IMAGE])
fill(BACKUPBUF, b"\xCC" * (IMAGE + 0x30))
okb, _ = call(BACKUP)
back = region(BACKUPBUF, IMAGE + 0x30)
cap = pattern(b"capture")
fill(CAPTURE, cap[:IMAGE])
fill(SUBMISSION, b"\xCC" * (IMAGE + 0x30))
w_sel = r = None
uc.mem_write(STATS_BLOCK + 4, struct.pack("<I", 1 << 12))
oks, _ = call(SUBMIT)
sub = region(SUBMISSION, IMAGE + 0x30)
sv2 = (okb and back[:IMAGE] == src[:IMAGE] and back[IMAGE:] == b"\xCC" * 0x30 and sub[:IMAGE] == cap[:IMAGE]
       and sub[IMAGE:] == b"\xCC" * 0x30 and back[IMAGE - 0x10:IMAGE] == src[IMAGE - 0x10:IMAGE])
record("SV2_copies_complete_with_tail", sv2, backup_last16_copied=back[IMAGE - 0x10:IMAGE] == src[IMAGE - 0x10:IMAGE],
       submission_last16_copied=sub[IMAGE - 0x10:IMAGE] == cap[IMAGE - 0x10:IMAGE],
       note="002EF570 copies all 0x56690 active bytes to the backup and 002EF690 all capture bytes to the submission buffer, the last "
            "16 (the tail after the 0xACD-block loop) included; the 0x30 of padding after each image is not written")

# ---- SV-6: the selector is read before the copy, and the writer receives it with the explicit size ----
order = ev.get("order", [])
record("SV6_selector_first_then_copy_then_writer", order[:2] == ["selector 00236760", "first write to the submission buffer"]
       and ev.get("writer") == ["1", "%X" % SUBMISSION, "%X" % IMAGE], order=order, writer_args=ev.get("writer"),
       note="00236760 (bit 12 of d[q[02EBF190]+4], planted 1) runs before the first byte of the copy; the tail jump reaches 0020E540 "
            "with ecx = that selector, rdx = the submission buffer, r8d = 0x56690 (the recorded boundary)")

# ---- SV-4: nothing reads the backup (execution side: none of these bodies touches it but the backup copy) ----
fill(BACKUPBUF, b"\x5A" * 0x100)
reads = []
from unicorn import UC_HOOK_MEM_READ
hr = uc.hook_add(UC_HOOK_MEM_READ, lambda u, acc, a, n, v, _: reads.append("%08X" % u.reg_read(UC_X86_REG_RIP)), begin=BACKUPBUF,
                 end=BACKUPBUF + IMAGE)
for fn in (GET_ACTIVE, GET_CAPTURE, GET_SUBMIT, CLEAR, SUBMIT):
    call(fn)
uc.hook_del(hr)
record("SV4_backup_unread_by_the_family", reads == [], reads=reads[:5],
       note="none of the other six bodies reads the backup buffer (its image-wide single reference is 002EF570's lea - static)")

# ---- SV-5: two clears - the bare one, and the compound clear-then-reinitialise ----
fill(ACTIVE, b"\xAB" * (IMAGE + 0x30))
ok1, _ = call(CLEAR)
bare = region(ACTIVE, IMAGE + 0x30)
called_bare = ev.get("called", [])
fill(ACTIVE, b"\xAB" * (IMAGE + 0x30))
snap.clear()
ok2, _ = call(CLEAR2)
at = snap.get("at_253A80", b"")
called_comp = ev.get("called", [])
record("SV5_two_clears", ok1 and bare[:IMAGE] == bytes(IMAGE) and bare[IMAGE:] == b"\xAB" * 0x30 and "0016D6A0" in called_bare
       and at[:IMAGE] == bytes(IMAGE) and at[IMAGE:] == b"\xAB" * 0x30 and called_comp[:2] == ["0016D6A0", "00253A80 header/image reinit"]
       and ev.get("stopped_at") == "001DBAC0 audio",
       bare_calls=called_bare, compound_calls=called_comp, compound_stopped_at=ev.get("stopped_at"),
       note="002EF5F0 zeroes exactly 0x56690 bytes (the padding keeps its 0xAB) and tail-jumps to 0016D6A0; 002EF650 zeroes the same "
            "extent, calls 0016D6A0, and only then enters the reinitialiser 00253A80 (the buffer is all zero at its entry); 00253A80 "
            "applies sound settings through the audio registry (the recorded boundary), so 002EF2D0 / 00238A80 are not reached here")

json.dump({"ok": allok, "bound": made, "allowed_functions": len(W.ALLOWED), "results": results},
          open(os.path.join(HERE, "result.json"), "w"), indent=1, default=str)
print("ok" if allok else "NOT ok")


# EXIT STATUS FOLLOWS THE RECORDED VERDICT (OPUS, 2026-10-03, the user's root-cause directive item 4): this package
# recorded "ok" in result.json but always exited 0, so no automated re-run could see it fail.
import json as _ej, os as _eo, sys as _es
_es.exit(0 if _ej.load(open(_eo.path.join(_eo.path.dirname(_eo.path.abspath(__file__)), "result.json"),
                            encoding="utf-8")).get("ok") is True else 1)
