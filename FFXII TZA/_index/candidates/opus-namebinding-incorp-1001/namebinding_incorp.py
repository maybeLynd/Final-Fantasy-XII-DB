"""namebinding_incorp.py - incorporate ASTRA's namebinding-deletion (ACCEPTed by SWE2-AUDIT-SPEC) into the per-frame update
gate contract (OPUS, 2026-10-01; ASTRA-REQ-OPUS-NAMEBINDING-DELETION-CONTRACT-1001). Byte-preserving (CRLF-aware),
idempotent. Prints PATCHED / ALREADY and FAILS n."""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "..", "..", "..", "00-Engine-Core-Runtime", "CONTRACT-per-frame-update-gate.md")
EV = "../_experiments/evidence/namebinding-deletion/README.md"
RV = "../_index/candidates/auditspec-review-namebinding-deletion-1001/REVIEW.md"
ANCHOR = "\n## SWE2-EC7-30 update (2026-09-18)"
SECTION = (
    "## Name-binding removal, completion and the release drain (OPUS, 2026-10-01)\n\n"
    "*Consumed from ASTRA's [`namebinding-deletion`](" + EV + ") (SWE2-AUDIT-SPEC [review](" + RV + "), ACCEPT, no "
    "narrowing). OPUS re-read `002EAEB0`-`002EAECC`, `002E6D66`-`002E6DEA` and `002E93E1`-`002E93F7` at the bytes. Static and conditional: "
    "valid records and lists, normal ABI returns and no interfering writes are premises.*\n\n"
    "- **Removal can be mark-only.** `002EAEB0` sets `+0x18` bit `0x04` (`002EAEC4`) and returns, with no other write "
    "or call, when `+0x18` bit `0x02` and `+0x19` bit `0x04` are both clear. Otherwise it advances the stamp, unlinks "
    "the record and retires it. `+0x19` bit `0x04` bypasses the mark-only arm; its meaning is not inferred.\n"
    "- **Completion of a marked record.** The completion `002E4D20` unpins first. A record marked by removal "
    "(`+0x18` bit `0x04`) gets bit `0x08` and skips registration (`0041E580`). `002EA6E0` returns 0 early under that bit, "
    "and the callback then sets bit `0x02` and retires the record. Without the mark, the follow-up allocation may "
    "return 1, so the callback does not always set bit `0x02`. A successful follow-up sets it at the `002E60F0` tail.\n"
    "- **This gate's drain releases them.** `002E6D60` enters the cleanup only when `002E6900(0)` returns 0 "
    "(`002E6D66`/`002E6D6B`) and a selected retired record has a non-zero handle `+0x10` (`002E6DAC`). `+0x18` bit "
    "`0x08` (`002E6DB3`) or `+0x19` bit `0x04` (`002E6DB9`) skips the unregister `0041E490` (`002E6DDD`) but not the "
    "release `002E9360` (`002E6DEA`). `002E9360` requests the child and secondary releases, calls `00369800` on the "
    "handle (`002E93E1`, `002E93F2`), clears the handle after it returns (`002E93F7`) and recycles the record. A record "
    "with a zero handle bypasses that call.\n"
    "- **The stamp stays 16-bit.** `INC dword +0x24` then a clear of `word +0x26` is `(old + 1) & 0xFFFF`, as the "
    "name-binding page already records; this corroborates it.\n\n"
    "**Open.** The producer of `+0x19` bit `0x04`, any natural overlap with a pending read, `00369800`'s and the "
    "allocator's own effects, real delivery timing, list progress, and OV-21/OV-25 as wholes. The `movsxd` completion "
    "argument and the low-32-bit list comparisons do not establish 64-bit pointer placement.\n\n")
fails = 0
b = open(P, "rb").read()
crlf = b"\r\n" in b[:4000]
nl = b"\r\n" if crlf else b"\n"
s = SECTION.encode("utf-8")
if crlf:
    s = s.replace(b"\n", b"\r\n")
a = ANCHOR.encode("utf-8")
if crlf:
    a = a.replace(b"\n", b"\r\n")
if s.strip() in b:
    print("ALREADY section")
elif b.count(a) != 1:
    print("REFUSING: anchor x%d" % b.count(a)); fails += 1
else:
    b = b.replace(a, nl + s.rstrip() + nl + a, 1)
    open(P, "wb").write(b)
    print("PATCHED section")
print("FAILS", fails)
sys.exit(1 if fails else 0)
