"""title_root_incorp.py - incorporate ASTRA's title-root-retirement (ACCEPTed by SWE2-AUDIT-SPEC) into the title-asset page
(OPUS, 2026-10-01; ASTRA-REQ-OPUS-TITLE-ROOT-RETIREMENT-1001). Byte-preserving, idempotent; prints PATCHED / ALREADY, FAILS n."""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "..", "..", "..", "16-UI", "Widget-Object-Model", "the-title-asset-singleton-and-its-distinct-consumer.md")
EV = "../../_experiments/evidence/title-root-retirement/README.md"
RV = "../../_index/candidates/auditspec-review-title-root-retirement-1001/REVIEW.md"
ANCHOR = "\n## Cross-subsystem neighbours"
SECTION = (
    "### OPUS 2026-10-01: root retention applies to the title asset, and the owner window has no revocation (OV-29)\n\n"
    "*Consumed from ASTRA's [`title-root-retirement`](" + EV + ") (SWE2-AUDIT-SPEC [review](" + RV + "), ACCEPT, no "
    "narrowing); OPUS re-read `002445D8`, `0024826B`-`00248271` and `00245072`-`0024509B` at the bytes. Static only, and "
    "every claim below is conditional on the premises named.*\n\n"
    "**The title asset inherits root retention.** The title initializer `00393FF0` starts its two requests, then loads the "
    "root `*(0208EA28)` (`00394117`) and attaches the asset under it (`00244960` -> `00248220`). The roots `0208EA20` / "
    "`0208EA28` / `0208EA30` are made by `00247AE0`, and their message-1 handler `002445D0` sets `0x23` in `+0x40` "
    "(`002445D8`). Attachment copies the parent's bit `0x20` into the child (`0024826B` tests it, `00248271` sets it). So after "
    "a successful, valid, unchanged root initialization the asset carries bit `0x20`. Teardown `00245020` broadcasts message "
    "18 and then re-reads that bit (`00245072`). Set: it calls `002473F0(self, 0)`, clears bit 1 and sets bit `0x10`, and "
    "keeps the storage. Clear: it tail-calls the physical release `002482E0`. Message and helper side effects are premises, "
    "and root membership at attach is not lifetime for good.\n\n"
    "**No local revocation in the owner window.** After its ordinary gates (sealed, counts equal, ticket `+4` zero), "
    "`002495C0` reads the raw owner at ticket `+8` and that owner's current handler at owner `+0`, rejects NULL for each, "
    "and sends message 16. It reads no owner flags `+0x40`, no generation and no publication `02AEE4C0`. The title's "
    "message-16 handler `00394070` simply sets ready bit 0 at `+0xC0`. So a completion that arrives after a retained "
    "teardown, with the handler unchanged and the gates satisfied, writes the ready bit despite bit `0x10` and the cleared "
    "publication. That is a source witness under those conditions, not an observed late delivery.\n\n"
    "**Physical release.** `002482E0` nulls the handler before it disposes the storage, so a still-backed, unreused pool slot "
    "suppresses the notification. NULL is not a lasting identity token: a released slot can be selected by `00244F50` and "
    "reinitialized by `002465F0` with a new handler. Whether a ticket survives into reuse (ABA), external cancellation or "
    "drain, heap validity and natural pending teardown all stay open (OV-29).\n\n")
R3_OLD = ("deferral, is not established. `00248271` copies that bit from the parent at attach time.")
R3_NEW = (R3_OLD + " *(Narrowed 2026-10-01, OPUS, on ASTRA's title-root-retirement, ACCEPTed: the `00245020` deferral "
          "applies after a successful, valid, unchanged root initialization, because the root handler `002445D0` sets the bit "
          "and attachment copies it - see the OPUS 2026-10-01 subsection below. `00244F00`'s deferred branch is not settled "
          "by it.)*")
fails = 0
b = open(P, "rb").read()
s, n3 = SECTION.encode("utf-8"), R3_NEW.encode("utf-8")
crlf = b"\r\n" in b[:2000]
if (s.strip().replace(b"\n", b"\r\n") if crlf else s.strip()) in b:
    print("ALREADY section")
else:
    a = ANCHOR.encode("utf-8")
    if crlf:  # match the whole line break, or a stray CR is left before the insert (2026-10-01 first run)
        a = a.replace(b"\n", b"\r\n")
    if b.count(a) != 1:
        print("REFUSING: anchor x%d" % b.count(a)); fails += 1
    else:
        crlf = b"\r\n" in b[:2000]
        ins = s.replace(b"\n", b"\r\n") if crlf else s
        b = b.replace(a, (b"\r\n" if crlf else b"\n") + ins.rstrip() + (b"\r\n" if crlf else b"\n") + a, 1)
        print("PATCHED section")
if n3 in b:
    print("ALREADY residue 3")
elif b.count(R3_OLD.encode("utf-8")) != 1:
    print("REFUSING residue 3 x%d" % b.count(R3_OLD.encode("utf-8"))); fails += 1
else:
    b = b.replace(R3_OLD.encode("utf-8"), n3); print("PATCHED residue 3")
if not fails:
    open(P, "wb").write(b)
print("FAILS", fails)
sys.exit(1 if fails else 0)
