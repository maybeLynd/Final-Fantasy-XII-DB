# PH-4 consumer check (FABLE, Claude Opus 5.5, 2026-09-26)

**What changed.** No fact is corrected. `PH-4` asked whether "84 in every shipped file" rested only on the
169-file sample. `CU-4` (FABLE, 2026-09-12, on the cluster-header page) had already checked every `.phyre` entry in
`FFXII_TZA.vbf` from its first compressed block and found `m_size` = 84 in 35,984 of 35,984. Two sentences written
before that check still presented the uniformity as unproven.

| Consumer | What it says | Disposition |
|---|---|---|
| `CONTRACT-phyre-cluster-header.md` §14 item 5 (`PH-4`) | "the claim is about the sample" | Answer appended in this publish; nothing struck |
| the cluster-header page, after the CU-4 box | "a property of the sample, not a proven property of the shipping data" | Supersession note added directly after it; the text kept, since it stays true of the sample's proportions |
| the same page, header table `+0x04` | "84 in every shipped file" | Now true as written. Unchanged |
| `CONTRACT-phyre-cluster-header.md` header table and §6 | "84 in all 169 sampled files"; "dead against shipped data — all 169 sampled files report 84" | True of the sample, and CU-4 extends it. Unchanged |
| `the-file-schema-against-the-runtime-schema.md` | the corpus is small and unrepresentative | About the schema join, not the header size. Unchanged |
| `OPEN-QUESTIONS.md` PH-4 | OPEN | Restated ANSWERED in this publish |
