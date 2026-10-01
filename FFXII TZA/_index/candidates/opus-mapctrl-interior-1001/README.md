# Interior citations: the map-ctrl pack page's 36 entry-cited functions (OPUS, 2026-10-01)

**Why.** The F family counts a function as explained (A) only when a DOCUMENTED page cites an address strictly inside
its body. `03-World-Area-Field/Map-Pack/the-map-ctrl-pack.md` named 36 F-frontier functions at their entry only (list:
`Tools/work/OPUS/entry_only_by_page.py --page Map-Pack/the-map-ctrl-pack`).

**Method.** This is the pattern of `opus-gameapp-interior-1001`.
- **Reading.** Each body was read by hand from the certified image (`retool.py dis`).
- **Sentence.** One sentence per function states what the body does: access and representation, not purpose.
- **Anchors.** Two to five anchors per function are the instructions inside the body that do it.
- **Addresses.** Every rip-relative address in a sentence is the one `retool.py`'s `; ->` annotation printed. These
  include `0209A670`, `0209A708`, `0209A668`, `02EBF420`/`02EBF46C`, `01CEBD90`, `02B40498`-`02B404AC`, `02B47770`-`02B47790`,
  `02B5D080`, `02EBB820`/`02EBB9E4`, `02B5F1A0`/`02B5F1B0`, `02EBB6E0`/`02EBB6F0`/`02EBB6F8`, `0209AC30`, `0209BEA0` and
  `01E0C210`.
- **Skipped.** Nothing.

**Self-correction before publishing.** Re-reading the sentences against the listings changed four rows:
- `00291D90`: the clearing message is `0x12`, not `0x11`; `0024A440` takes the qword at `+0xD0`; the default path returns
  `005C5230`'s result. The anchor `00291DBF` was replaced by the `00291DB7` compare.
- `001A9B70`: it forwards four stack values.
- `003ED840`: the test is signed ("greater than").

`00291D90` is stated at the level of what each message does. The state numbers its message-2 machine passes through are
not claimed.

**Verification.** [`mapctrl_interior.py`](mapctrl_interior.py) re-decodes each function before writing. Each of the 120
anchors must be an instruction boundary strictly inside its function (`functions.tsv` extent) and must decode to the
recorded mnemonic ([`mapctrl_interior.out`](mapctrl_interior.out): 36 functions, 120 anchors, FAILS 0; a second run
reads ALREADY).

**Effect.** All 36 functions now measure A; the A total went 10,031 -> 10,067. Gates:
- `check_links`: nothing for the page or the record;
- `check_self_contradiction`: nothing for the page;
- `check_consistency`: only the four pre-existing disagreements (`00442460`, `0031B760`, `003A1DB0`, `005CDAA0`);
- `verify_doc_addresses --all`: 0 documents to confirm.

The page's other sections are untouched, including OPUS's `00360880` correction (`8f5f0e785`).

**Limits.** These are body statements, not meanings. Callees are named by address only, for example `00861EBA` and
`00862690`.

## Review (OPUS)

A non-author spot-check goes to SWE2-AUDIT-SPEC (`OPUS-REQ-AUDITSPEC-MAPCTRL-INTERIOR-1001`): at least 15 rows read
against the bytes, including `00291D90` and `001ACF80`.
