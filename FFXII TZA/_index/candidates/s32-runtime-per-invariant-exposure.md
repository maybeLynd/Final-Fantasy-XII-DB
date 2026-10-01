# S-32 runtime: the award contract's stub exposure is empty; four sibling contracts not covered (OPUS, 2026-09-25)

**Row:** S-32 enemy death and rewards. The runtime cell is MIXED, *"no per-invariant stub-exposure analysis yet"*.
The binding gap (*"types PARTIAL and nothing executed"*) is stale on its runtime half. The row has five contracts.
This note covers the one OPUS owns, `13-Rewards-Progression-Economy/CONTRACT-experience-and-licence-award.md`, and
says what it does not cover. It scores nothing.

## The award contract (EXP / LP gates)

The contract's claims are:
- the §4 gate table: licence byte, recipient kind, owning-unit lookup, id bands, the status mask, subject checks,
  and the NULL-recipient bypass;
- the §2 interface: the NULL-tolerant recipient, signed EAX, and **no writes to the supplied records**.

The entries are `002F8BB0` (EXP), `002F90C0` (LP), and the gates `003135C0`, `00313800`, `0031B810`, `0031B860`,
`00320AB0` and `00264150`.

| evidence | substitutions |
|---|---|
| **EXP-090** (104 cases, 10 mutations) | **none**: *"the entire reachable closure is shipped code"*; fixture content only |
| **SECTION-03** native controls (71 controls, identical repeat, 6 private-image variants rejected) | **none**: *"Zero application callees are scripted or stubbed"*; synthetic state only |
| EXP-081 | live, read-only binding capture (the words, not reward contents) |

| claim | can a substitution reach it? |
|---|---|
| each §4 gate row (EXP and LP) | **no**: no application stub in either execution |
| NULL recipient bypasses only the recipient rows | **no** |
| no writes to the supplied records (§2) | **no**; SECTION-03 compares all synthetic data bytes |
| EXP rejects an ownerless kind-0 record that LP admits (an API distinction) | **no**; the contract already bounds it as synthetic, not a claim about the normal defeat caller |

**The exposure set is empty.** The distinction the contract itself keeps is evidence class, not stubs: reward
*contents* are not observed live (§11), and the executions use synthetic records.

## EXP-075 / EXP-076 name this contract but test the installer

Their subject is the reward-index guards inside the battle-unit installer `0023A570`. Their nine recording RET stubs
are the installer's callees: `00236A60`, `00303EC0`, `00322050`, `0020E600`, `00236100`, `002B58B0`, `00328FF0`,
`00237040`, `002FEAB0`. That is S-14's I5, and `s14-runtime-per-invariant-exposure.md` finds I5 unreachable by
EXP-150's stubs. EXP-150 runs those nine callees real, which retires EXP-075's stubbed-predecessor caveat for the
guard arithmetic.

## Not covered

S-32's other four contracts are not mapped here, and their owners are not OPUS:
- `CONTRACT-loot-rolls-and-the-chain`;
- `CONTRACT-gil-storage-and-movement`;
- `CONTRACT-defeat-rewards-sequence`;
- `CONTRACT-level-advance-and-growth`.

The row cannot be judged whole on this note.
