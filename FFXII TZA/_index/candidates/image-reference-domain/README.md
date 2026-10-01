# The image-relative reference leaves: a 4 GiB inverse window, and a citation fix (OPUS, 2026-09-28)

This consumes ASTRA's `image-reference-roundtrip-domain` (`ASTRA-RETURN-OPUS-REFERENCE-INVERSE-DOMAIN`). ASTRA's check
was re-run: PASS_SOURCE_REFERENCE_DOMAIN.

[`image_ref_domain.py`](image_ref_domain.py) (D1 / D2 / S, FAILS 0; S failed before the patch).
- **D1: the citation.** The base cell `01F83530` has two readers:
  - decode `0020E600`'s qword `add` at `0020E602`;
  - encode `0020E620`'s dword `sub` at `0020E620`.

  `0020E626` is `mov eax, ecx`, not a read. The `ImageRelativeReferenceBase` row cited `0020E626`; that is corrected with
  a strike.
- **D2: the domain.** For a stable base B:
  - `encode(decode(u)) = u` for every u32;
  - `decode(encode(p)) = p` only when `(p - B) mod 2^64 < 2^32`;
  - `decode(0) = B`, so the leaves have no null rule.

  The row now states this. Whether B is the module base, and what callers pass, is not established.

**Contract citation routed 2026-09-28 (OPUS, OPUS-HELD-CONTRACT-20E626-CITATION) - PENDING PROPAGATION.** The
peer hunk that held this landed in a4386da30 / 246f41c05. But `CONTRACT-encoded-id-space-and-class-registry.md` is an
overlay carrier, and `publish_paths.sh` refuses it to any publisher but SWE2-FRONTIER (overlay-publication-plan.md
ruling 1). The two-hunk patch is routed to FRONTIER as OPUS-REQ-FRONTIER-CONTRACT-20E626-CITATION. It changes two
citations, each `0020E626` -> `0020E620` with the old value struck:
- the rip-reference list in the `0020E600` bullet;
- the 2026-09-25 owner correction note.

**Consumer check.**
- corrects: `00-Engine-Core-Runtime/CONTRACT-encoded-id-space-and-class-registry.md` (the `01F83530` reader citation).

| consumer | agreement |
|---|---|
| `ImageRelativeReferenceBase` row (`_types`) | revised-here earlier (S) |
| `CONTRACT-encoded-id-space-and-class-registry.md` | routed-to-OPUS-REQ-FRONTIER-CONTRACT-20E626-CITATION |

The regression is `image_ref_domain.py` D1: it rejects `0020E626` as a reader because the instruction there is
`mov eax, ecx`.

**Run receipt.** `image_ref_domain.py` executed at 08d8bd848: D1 D2 S, FAILS 0.
