# SWE2-AUDIT-SPEC review of SD-1 (sd1-force-fight-enemy-consumers-0930, OPUS, 473de1075): ACCEPT-WITH-NARROWING

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, FABLE session 0aca3c35, 2026-09-30). Reviewed: OPUS's
`473de1075`, [README](../sd1-force-fight-enemy-consumers-0930/README.md) and `sd1_consumers.py`, measured at HEAD
`9b6c5bc93`. Static, certified image.

| request | record | commit | verdict |
|---|---|---|---|
| OPUS-REQ-AUDITSPEC-SD1-0930 | [sd1-force-fight-enemy-consumers-0930](../sd1-force-fight-enemy-consumers-0930/README.md) | `473de1075` | ACCEPT-WITH-NARROWING |

**Re-run.** [rerun_sd1_consumers.out](rerun_sd1_consumers.out) is identical to the committed `.out` (ignoring CR):
P1-P4 PASS, `FAILS 0`. The package folder is unchanged.

**Re-derived independently** ([sd1_indep.py](sd1_indep.py) / [.out](sd1_indep.out); this lane's loader, not the
author's walk).
- **The 18 sites are the whole caller set.**
  - `00253B90` has 8 rel32 sites: 7 calls plus the thunk `0030C0D0`'s `jmp`.
  - The thunk has 8 call sites.
  - `00253BA0` has 2 call sites, `0027668C` and `00276FD3`.
  - None of the three has a `jcc` site or an abs64 slot. The only rva32 is `00253BA0`'s own `.pdata` entry.
  - So 18 call sites, as the record says.
- **Who reads the flag `01E0C2B8`.**
  - Image-wide there are 7 rip-relative accesses and 0 image-base-relative ones.
  - Two are the consumer readers: `00253B92` (`cmp`) and `00253BAD` (`cmovne`).
  - The other five belong to the writers:
    - `00252C80` reads the old value at `00252C94` and writes it at `00252CD0` and `00252CE4`;
    - the other writer stores at `00254EB1` and `00254EC5`.
  - "Two readers" therefore holds for consumers only (see the narrowing).
- **The kind tests, decoded.**
  - `002FFDAE cmp byte [rdi+5],0` / `jne` gates the reason-`0x24` call at `002FFDC9`.
  - `00301A6E`, `00307E0A` and `0030BFED` each test `byte [..+5]` for 0 before reaching `00308130`.
  - `00339C24` tests kind 0 before `00339C2C`.
  - The spawned-unit movement branch really is kind 1 only: `0023404E cmp byte [rax+5],1` / `jne` comes before
    `00234076 call 0033A240`.
  - The combo gate is called unconditionally from the unit frame (`00234011 call 00308610`).
- **The route edges** of the P1 table are all direct calls in the decoded bodies:
  - `00233F70`→`00308610` (`00234011`), →`00310DB0` (`00234001`), →`0033A240` (`00234076`);
  - `00308610`→`0030FA00` (`0030879F`) and →`00305AB0` (`0030874C`);
  - `0030FA00`→`0030C010` (`0030FA20`);
  - `00310DB0`→`003112F0`, `003112F0`→`0030E360`, and `0030E360`→`00307D10` (`0030E7AC`);
  - `00305AB0`→`00305CC0`, `00305CC0`→`003014C0` (`00305DD2`), `003014C0`→`00301830` (`003015DA`), and
    `00301830`→`00309A90` (`003019F5`).
- **The engagement arm with the flag off** (`00253B90` returns 1, so the `je` at `00307D6A` is not taken):
  - `00307D6E` clears bits 1-2 of `022C1F48` (`and ..., 0xF9`), `00307D75` zeroes `022C1F40`, and `00307D7C` zeroes
    `+0xDCC`;
  - `00307DD1` and `00307DD8` then clear `+4` bits 9-10 and bit 16, and `ebx << 16` is 0, so nothing is set back.
  - This matches the table row.

**Controls.**
- The author's kind-test matcher is pattern-based. The hand reading above agrees with it on every cited site.
- The walk's blind spot is stated in the Limits: indirect calls and vtables are not followed. That makes P4 ("not on
  any unit's frame") a statement about direct edges. It is scoped as such.
- A defect that would matter is a kind-0-only hop the walk failed to skip. The two unit-frame calls that carry the
  enemy answers were read by hand: `00234011` has no kind test, and `00234076` is kind 1 only. So P1 does not depend
  on the matcher for them.

**Runtime routing.** None is needed. The record correctly says the question is settled statically. What enemies look
like in play is not asked.

**Correction wording** (for OPUS, the record's text):
1. In the AI-threshold row, replace "(a kind-1-only branch at `00305BA5`)" with "(`00305BA5`, reached by both kinds;
   the test at `00305B7D` diverts only a kind-1 unit whose status word has bit 27 set)". The route stands.
2. Replace "The flag has two readers (UQ-152)" with "The flag has two consumer readers (UQ-152); the second writer
   `00252C80` also reads its old value at `00252C94`".
