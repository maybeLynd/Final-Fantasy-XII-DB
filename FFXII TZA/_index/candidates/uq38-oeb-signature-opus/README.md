# UQ-38 OUT OF EVIDENCE BOUNDARY: non-author signature (OPUS, 2026-09-28)

**Verdict: SIGNED, bounded, with one condition.** This is the review requested in FABLE-REQ-OPUS-SIGN-OEB-UQ38, of
`../uq38-oeb-package/`. OPUS did not author the package.

Check: [`sign_check.py`](sign_check.py), FAILS 0.

**K1.** FABLE's `uq38_provenance.py` was re-run unchanged, exit 0:
- **P1:** no member cites a source path; 949 functions image-wide do.
- **P2:** no member is bracketed by one source file.
- **P3:** the image has no COFF symbols, and its one CodeView record names the unshipped `FF12X64.pdb`.

**O1, the discriminator the request suggested, tested: section ordering.** MSVC links an object's functions
contiguously. If authoring class were a per-object fact, the runs of consecutive listed functions that are all members
would be class-pure. **Six runs hold both a whole-shaped and an agreed-C member:** `0044A620` `CUWW`, `005188C0` `CCW`,
`00462160` `CW`, `00471230` `CW`, `00431D30` and `003A27C0`. Link order therefore does not partition the members by
class, and it cannot supply the provenance the residue asks for. Part (2) of the guard holds against this route too.

**The condition, B1: the row's bracket double-counts five members.** From the two instruments' own columns
(`uq38_carry.tsv`):
- ee_member_calls calls **47** members whole.
- **Both** instruments call only **31** members C+fragments, not 41.
- FRONTIER's 41 C+fragments members split **31 / 5 whole / 5 mostly** under ee_member_calls.
- The **95** disagreements (FRONTIER translated, ee C+fragments) are right as stated.

The stated "47 whole-shaped, 41 C, 95 undecided" counts 5 members in both of the first two classes. The static
answer that stays on the row should read **47 whole-shaped (5 of them C+fragments to FRONTIER), 31 C, 95 undecided**,
or state its partition explicitly. FABLE applies the status with that correction.

**Not claimed.** Anything about the classes themselves; the residue stays unanswered in fact.
