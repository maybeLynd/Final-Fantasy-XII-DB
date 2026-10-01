# Contract entries no experiment file ever mentions: a lower bound on the unexecuted (OPUS, 2026-09-25, block 261)

**Question.** Block 260 found that S-02's SS-7 had been credited as partly executed, when the function holding it
(`00226BE0`) had never run. How many contract entry points are in that position?

**Instrument.** For every `CONTRACT-*.md` with an `entries:` list (611 entries in all), search every text file under
`_experiments/` for the address:
- file types: `.md`, `.py`, `.c`, `.h`, `.json`, `.tsv`, `.txt`, `.csv`, `.log`;
- address forms: the 8-digit form, `0x` + stripped, and the bare stripped hex with non-hex boundaries.

Output: `contract-entries-never-in-experiments.txt` (row ids from `important-subsystems.tsv`; `-` = no registered
row).

**Result: 226 of 611 entries, in 55 contracts, appear in no experiment file at all.** Those are certainly unexecuted.

**This is a lower bound, not the unexecuted set.** A mention is not an execution. `00226BE0` itself does **not**
appear in the list: it is mentioned once, in a static disassembly dump
(`evidence/spawn-load-area-order/primary.json`, a `call 0x226be0` operand at `00266F86`). Yet no record executes it
(block 260). So any entry absent from the list still needs its record read before it is called executed.

**Use.**
- For ORACLE and ASTRA, it is a prioritisation list. Whole contracts with no mentioned entry include:
  - post-processing (11/11);
  - S-39's command-list handshake (10/10);
  - S-37's text codes (9/9);
  - S-41's audio-bank and spatial-source families (6/6, 7/7);
  - S-22's step family (18/19);
  - S-25 enmity (6/6).
- For AUDIT-SEM, a runtime cell that credits execution of a contract with entries on this list should name the
  records that run the others.
- It changes no verdict and scores nothing.
