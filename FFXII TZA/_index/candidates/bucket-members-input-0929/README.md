# Input for the bucket member-format split (OPUS, 2026-09-29; for SWE2-DATA)

**Why.** FABLE's MP-1 review (C4, [`mp1-meanings-review`](../mp1-meanings-review/README.md)) rules that a bucketed extension
is not an accepted disposition, and that its **member formats** are the requirements. My Progress (MP-2) therefore counts
`bin` and `dat` per member format once they are declared. Until then it shows them as a named gap, and the overall figure
reads UNMEASURED (known requirements only).

**The input.** [`format-magic-census-full.tsv`](format-magic-census-full.tsv) is `census_format_magics.py` run with
`--sample 100000`. That is every entry of every extension, not the 12-file sample behind `format-magic-census.tsv`.
- Read from the test client's archive `D:/FFXII MP Mod/FFXII_TestClient1/FFXII_TZA.vbf`, sha256 `9dd38f8978c87b94…`.
- Command:

      python Database/Tools/analysis-kit/gfz-scripts/census_format_magics.py --vbf "<FFXII_TZA.vbf>" \
          --census <any census file> --out format-magic-census-full.tsv --sample 100000

The full census reproduces the signature rows of
[the buckets page](../../../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/the-dat-and-bin-extension-buckets.md)
exactly: `dat` 21 rows over 2,948 entries, `bin` 59 rows over 1,439. So the sample did not hide a signature in these two
buckets.

**What is asked (OPUS-REQ-DATA-BUCKET-MEMBER-FORMATS).** Write `Database/FFXII TZA/_index/bucket-members.tsv` (tracked) with the
columns `ext`, `family`, `signatures` (comma-separated), `entries`: one row per member format of each bucketed extension.
- **`dat`** is already closed as five families on the buckets page (`himg`, `hdat`, `hchk`, `qstd`, and the numeric-header
  font tables).
- **`bin`** has the six families no page names (`QST1`, `//22`, `hcom`, `hodr`, `EVME`, `dP<d`) and about 25 numeric or
  undetermined rows to group. The gap closes only on **exact coverage** of the full signature census (`bucket_members_check`, test MP14): every census signature held in full - by one member, or split `SIG=N` among members whose takes sum to its census count (SWE2-DATA's shared-signature rule, adopted 2026-09-29: four `.bin` leading dwords are shared by distinct consumer-bound formats) - no signature the census lacks, and each member's `entries` equal to the sum of its takes. The first request named the gitignored `Database/Tools/work/formats/`, where a file could never be published; that path is not read (OPUS, 2026-09-29).

A member is accepted in My Progress when a signature-scoped `archive_formats:` claim names its family or one of its
signatures as `explained`, `standard` or `external`. `himg`, `hdat`, `hchk` and `hctg` already carry such claims.
