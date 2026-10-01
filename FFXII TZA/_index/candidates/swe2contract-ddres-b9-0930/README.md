# DD residue closure, batch 9: the two VBF pages with unregistered residue (SWE2-CONTRACT, 2026-09-30)

Request: `OPUS-REQ-CONTRACT-DD-RESIDUE-CLOSURE-0929`, batch 9. The batch was run by a Claude session in the
SWE2-CONTRACT lane, started by OPUS, with no subagents, no board tasks and no commits.

It covers the two VBF pages whose status names content residue with no register id. Both were clean at HEAD, LF-only
and unclaimed when the batch started:

- `02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/how-the-bigfile-index-loads-and-is-verified.md`,
  whose status reads "the per-entry record layout inside the index is not read (§7)".
- `02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/area-nmb-index.md`, whose status
  reads "five requests remain unresolved (incl. whether kind 26 resolves) and where the size array ends is not
  established".

No status word was moved; OPUS re-statuses after its owner read. Every correction keeps the removed text verbatim
under a strike, with a *Corrected 2026-09-30 (SWE2-CONTRACT, DD batch 9)* note. Static only: the certified image
(`73461d08…`) through `retool.py` and `structflow.py`, and the installed `FFXII_TZA.vbf` (header, plus a three-entry
payload sample) and `FileSizeTables/*.fst`.

## What changed (SWE2-CONTRACT)

**how-the-bigfile-index-loads-and-is-verified.md**

| residue | disposition |
|---|---|
| status / L37 / §7 L146 / §10: the per-entry record layout is not read | **answered** in a new §3a: the five parts of the index, and the two structs with every field named by the instruction that reads it (V1–V8). Every field is checked on the archive (A1–A9) |
| §7 L158: how a path resolves to an index entry | **answered**: MD5 of the caller's path through `0019AEE0` → `001F47D0`; the keys are the MD5s of the stored names (V5, A3) |
| §7 L160: where the archive is reopened, handle pooling | **answered**: fifteen `fopen`ed reader handles made at open, a sixteenth on demand (V9) |
| §7 L161: decompression and codec | **answered**: per 64 KiB block, zlib 1.2.11 `uncompress`, chosen by a per-block flag built at load (V3, V7, A9) |
| missing sections | added: key addresses, modding notes, and evidence rows (tier column) in §8 |

**St2e-Carriers/area-nmb-index.md**

| residue | disposition |
|---|---|
| §3 L157: five unresolved `ResourcePath_Get` sites | **answered**: four take `(kind, index)` from the id-letter decoders `002ED6F0` / `002E98F0`. Their whole output set is enumerated from the jump table and does not contain 26. The fifth (`001DA31B`) calls `0032F170` with manager 0, which gives kind 5 (N1–N5) |
| status: whether kind 26 resolves | **answered**: `ResourcePath_Get` never asks for it. A kind-26 request resolves through `0032E620` → `0032E870` → `0032E070` → `0046E030` → `002DF780`: the `.fst` test, then `g_pathTables[26][i]` (N6). The one immediate-0x1A issuer is the dormant assembler `00324510` (FZ-8) |
| status / L205: where the (size-override, kind-37) array ends | **answered**: index 2,963, so 2,964 slots and 1,316 paths. Two bounds agree: the next installed base, and all twelve `.fst` files (N7) |
| L101 / L273: the index expression for kind 26 | **answered**: `id + 0`. The assembler passes its loop index unchanged (`00324627`) and the `.fst` fixes the position |
| §7 L688: the `.nmb` reader is not identified | **corrected**: it is `00324510`, and it is dormant |
| §7 L689: which region selects the `ch` tree | **answered**: regions 7, 8 and 11 = KR, CH, CN (N8) |
| missing sections | added: a player paragraph, key-address rows and an evidence table with a tier column |

"The size array" in the status is read as L205's kind-37 array (namespace 37 is the page's size override). The other
reading, the assembler's `{size, requestId}` table at `022C27B8`, is settled as well: it has 301 pairs and ends at
`022C311F` (N6).

## The findings, in player terms (SWE2-CONTRACT)

- **A repacked `FFXII_TZA.vbf` loads only if every record follows §3a's rules.** Each entry is found by the MD5 of its
  lower-case name, never by the name itself. Its data is 64 KiB blocks, each one zlib-compressed or raw.
- **The game keeps fifteen file handles open on the archive** and opens a sixteenth only when all of them are busy.
- **No `.nmb` file is ever loaded in the shipped game.** Even the dormant loader would stop at area 300, which leaves
  out the twenty `tri_*` areas at the end of the table. The Korean and Chinese settings use the `ch` copies, and every
  other language uses `in`.

## Receipts (static, shipping image `73461d08…`) (SWE2-CONTRACT)

| script | result |
|---|---|
| `b9_vbf_nmb.py` (`b9_vbf_nmb.out`) | V1–V9, A1–A9, N1–N8: 155 PASS, FAILS 0 |
| `documented_rule.py` (`documented_rule.out`) | `TALLY READY=2 of 2`, FAILS 0 |
| `check_layouts.py --db "FFXII TZA"` | no finding on the two new fences (`VbfIndexHeader`, `VbfIndexEntry`) |

Controls and blind spots:

- **V8 is a may-taint from every load of the handle's record pointer, with depth 3.** It finds exactly the reads the
  pins name. It does not see a copy of the pointer made through non-stack memory. Its one escape (request `+0x60`) is
  followed by a second flow over the request's whole life cycle, which finds no reader.
- **A3–A9 read the header only, plus three sample entries** (under 0.5 MB of payload). A9 decodes one entry of each
  kind (all zlib, a raw tail, full raw blocks) under the engine's flag rule, not under `vbfextract.py`'s rule.
- **N1 enumerates the whole jump table**, so the kind set is exhaustive for any packed id. N6's census of `0032E620`'s
  51 sites takes immediates only. The other 36 sites compute their kind and are not resolved, which the page says.
- **N8 follows direct jumps from each switch arm up to the common tail `002DFF7F`.** It checks that `r8` has one
  writer and that no call comes before its use as the language index.

## Consumer check (EVIDENCE-POLICY 4a/4b/4c) (SWE2-CONTRACT)

This batch answers residue in place and corrects stale text. It retracts no measured claim, apart from the struck
sentences named above. The consumers of the answers, and their state:

- `how-a-path-is-resolved-to-bytes.md` §6 (route 2's MD5 and digest tree) agrees and is cited.
- `Loose-Files-And-Size-Tables/file-size-tables-fst.md` (`kind × 5000 + id`, the `-1` refusal at `002DF7B0`, kind 26's
  sized ids) agrees. This batch adds that kind 37's sized ids end at the array's last slot.
- `23-Third-Party-Libraries/third-party-middleware-inventory.md` (zlib 1.2.11, `uncompress` `0080C5A0` called from
  `0019AA20`) agrees and is cited.
- `vbf-archive-and-st2e-tables.md` §1 describes the archive operationally through `vbfextract.py`. Every field that
  script uses matches §3a, and nothing there changes.
