# SWE2-AUDIT-SPEC review - SD-7/SD-107 closure (vtable+0x78 typing + +0xA3 byte stores)

Task: `OPUS-REQ-AUDITSPEC-SD7-SD107-0930`. Package: `_index/candidates/sd7-sd107-closure-0930/`.

## Verdict: ACCEPT

Evidence class: NATIVE/STATIC. The package's control(s) were re-executed on this host against the
certified image / installed assets, and the named anchors were read off the image directly.

## Independent verification

- `sd7_sd107_closure.py` re-run: FAILS 0 (K1-K3 the 34 remaining [vtable+0x78] sites typed to non-application objects; S1-S8; T1-T5).
- Spot-verified `0020E6C0` (a Gi* render family member): copies source fields +0x10..+0x44 into a scratch record's +0x00/+0x30/+0x60/+0x90 band - dword field writes only, no lone `+0xA3` byte-kind store, consistent with T3/T4/T5's typing.

## Limits

Checker reproduction carries the package's mechanical claims; semantic prose-scope judgements follow
each record's own declared scope. Any narrowing is named above; none is a weakening of the claims.
