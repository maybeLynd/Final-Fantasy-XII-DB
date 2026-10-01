# Interior citations: the-selection-the-menu-publishes.md's entry-cited functions (OPUS, 2026-10-01)

The page named 27 F-frontier functions only at their entry. OPUS read all 27 from the certified image and anchored all 27.

**Method.** The pattern is that of `opus-pfgate-interior-1001`. Each row has one sentence on what the body does (access
and representation, not purpose) and 1-5 interior anchors that do it. Every rip-relative address in a sentence was
resolved by `retool.py`:
- `01E0C1D8`/`01E0C1DC`;
- `0209BE80`;
- `0208F570`;
- `02089340`;
- `022D9240`-`022D9260`.

The float constants were read from the image:

| address | value |
|---|---|
| `01CEBBA8` | 1.0 |
| `01CEBC50` | 3.14159 |
| `008F8D80` | 30.0 |
| `009159F8` | 32.0 |
| `00915BA0` | 96.0 |
| `01CEBC08` | 2.0 |
| `00901B3C` | 1.5 |
| `01CEBB70` | 0.5 |
| `01CEBB68` | 0.25 |
| `00900320` | (1, 1, 1, 1) |

`00861F0E` is a `jmp [008C2BB0]` thunk. The import table names that slot `sinf` (`api-ms-win-crt-math-l1-1-0.dll`).

**Verification.** [`menusel_interior.py`](menusel_interior.py) re-decodes every function first. All 109 anchors are
instruction boundaries inside their extents with the recorded mnemonic ([`.out`](menusel_interior.out): FAILS 0;
idempotent; without `--apply` it only verifies).

**Effect and gates.** All 27 now measure A; none remains in the frontier (3,646 after this record). Gates on the page:
- `check_links`: nothing for the page or the record;
- `check_self_contradiction --db`: nothing for the page;
- `check_consistency`: only the four pre-existing disagreements;
- `verify_doc_addresses --all`: 0 documents to confirm.

**Limits.** These are body statements, not meanings. Some rows describe the bytes literally where the code looks odd:
- `0028F9E0` and `00290B70` address word `+0x850` through `mov eax, ecx`, which is the zero-extended low dword of
  `rcx`.
- `003F3660` shifts `2*r8d` left by 37 (`shl r8, 0x25`).
- `003F6370`'s copy path stores stack floats at `rsp+0x20`-`0x28`, which only the other path writes. The row says
  "three stack floats" and makes no claim about their value.

## Review (OPUS)

A non-author spot-check goes to SWE2-AUDIT-SPEC: at least 15 rows read against the bytes.
