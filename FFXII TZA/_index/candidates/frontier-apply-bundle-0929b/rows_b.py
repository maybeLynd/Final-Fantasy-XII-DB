# rows_b.py IN OUT - mark register rows OV-11, OV-25, OV-39, OV-40, OV-41, OV-42, OV-43, OV-45, OV-46 ANSWERED (FABLE, Claude Opus 5.5, 2026-09-29).
# Replaces the status cell that starts " | **OPEN**" on each row, keeping the old status as struck history.
# Refuses unless each row is found exactly once and still OPEN.
import sys
NEW = {
 "OV-11": "**ANSWERED 2026-09-29 (FABLE, Claude Opus 5.5): the native wait services are a closed set (0025DF00's bounded eight-entry kind table, one predicate per service arm); actor reuse is the actor-request page's 2026-09-26 answer; in-frame order is the field-pass page sections 4-5; reentrancy stays superseded under OV-2.** Evidence `_index/candidates/ov11-wait-services-fable/waits.py` J A K.",
 "OV-25": "**ANSWERED 2026-09-29 (FABLE, Claude Opus 5.5): exactly four external-owner families register a loaded source (00409FE0 <- only 0041E580 <- four completions): the indexed owner, the motion cache 02B57F70, the script name-binding record and the per-lane sub-record 02161DA0, each with its release-in-flight rule; error recovery is the OV-42 record, nonempty registration OV-39/40/41.** Evidence `_index/candidates/ov25-queue-clients-fable/` (clients.py C K, families.py R R2 M1-M5 S L1-L3 U K).",
 "OV-39": "**ANSWERED 2026-09-29 (FABLE, Claude Opus 5.5): names and offset tables are guaranteed by census (every @FRP name NUL-terminated; OV-26's 320,736 entries in bounds); the @FEF-specific inputs have no shipped producer - the configuration table 02B64380 is never populated and @FEF appears only in 144 PS2-era obj_finish .cm files whose end-of-extent dword never locates their EFX data.** Evidence `_index/candidates/ov39-fef-producers-fable/producers.py` F M N K.",
 "OV-40": "**ANSWERED 2026-09-29 (FABLE, Claude Opus 5.5) for the page's path: after a successful read only fresh bytes are rebased - 00409FE0 is reached only from the four owner-family completions and each submit reads into the block its completion registers; the byte-count -1 failure callback and the five other 003EDAD0 drivers stay in the box.** Evidence `_index/candidates/ov40-reregistration-fable/reregister.py` E C B F K K2.",
 "OV-41": "**ANSWERED 2026-09-29 (FABLE, Claude Opus 5.5): EFX child construction is three registrars of one shape (0x700/0x800/0xA00, each called once from the walker 003EDAD0) with bounded subtype setup switches; the subtypes are a closed set (4 + 9 + 65 element types) whose setups rebase or link encoded dwords at fixed offsets (48 of 68 routines mapped; the 20 array-bearing ones stay in the box); the rendering consumers are the per-type methods and UQ-204's emits table.** Evidence `_index/candidates/ov41-efx-children-fable/subtypes.py` W G S S2 X C K.",
 "OV-42": "**ANSWERED 2026-09-29 (FABLE, Claude Opus 5.5): held state1 is never submitted (OV-34); the owner protocol has no recovery for a rejected submission (state 3 written, no queue entry, no callback, a delete parks it at 5); a failed read calls back only when its byte count is -1; no game leak is claimed, a higher-level arena release not being excluded.** Evidence `_index/candidates/ov42-submit-recovery-fable/recovery.py` Q S N I, db66f57fb; `ov45-owner-reload-fable/reload.py` E.",
 "OV-43": "**ANSWERED 2026-09-29 (FABLE, Claude Opus 5.5) for the copy half: the deployed CRT's memcpy (System32 vcruntime140.dll 14.51.36247.0; the game ships none) is overlap-safe in all 31,784 overlapping cases measured; the scheduling universality half stays superseded under OV-2.** Evidence `_index/candidates/ov46-overlap-copy-fable/overlap.py` D O K.",
 "OV-45": "**ANSWERED 2026-09-29 (FABLE, Claude Opus 5.5) for replacement/reload: a manager reload runs the group deleter at unload and the group initialiser at bind; only the BGM stream head-inserts, so every older owner read completes and frees its state-5 owner before the new payload binds; the all-callers part stays superseded under OV-2.** Evidence `_index/candidates/ov45-owner-reload-fable/reload.py` U I Q R H E.",
 "OV-46": "**ANSWERED 2026-09-29 (FABLE, Claude Opus 5.5): measured on the exact deployed dependency (System32 vcruntime140.dll 14.51.36247.0, sha256 d1f4225d..., loaded because the install ships none): its memcpy is overlap-safe in all 31,784 overlapping cases, so the mover's overlapping move yields the memmove result; another machine's redistributable is a different dependency.** Evidence `_index/candidates/ov46-overlap-copy-fable/overlap.py` D O K.",
}
def apply(t):
    lines = t.split("\n"); hits = {q: 0 for q in NEW}
    for i, l in enumerate(lines):
        for q, new in NEW.items():
            if not l.startswith("| %s |" % q): continue
            cr = "\r" if l.endswith("\r") else ""
            body = l.rstrip("\r")
            k = body.rfind(" | **OPEN**")
            if k < 0 or not body.endswith(" |"): continue
            old = body[k + 3:-2].strip()
            lines[i] = body[:k] + " | " + new + " *Previous status, kept as history:* ~~" + old.replace("~~", "") + "~~ |" + cr
            hits[q] += 1
    bad = {q: n for q, n in hits.items() if n != 1}
    if bad: sys.exit("REFUSE: %s" % bad)
    return "\n".join(lines)
if __name__ == "__main__":
    t = open(sys.argv[1], encoding="utf-8", newline="").read()
    open(sys.argv[2], "w", encoding="utf-8", newline="").write(apply(t)); print("ok")
