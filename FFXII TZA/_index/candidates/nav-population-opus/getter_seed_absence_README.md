# Getter-seeded census over OPUS's other absence rows (OPUS, 2026-09-28)

**Why.** `nav_population.py` C showed that a cell-seeded census missed reads made through the root getter 00383840. The same blind spot could sit under other "no access" rows on pointer-routed types.

**Scope.**
- Every type whose route is `PTR <cell>`, whose cell has a getter (`mov rax, [cell]; ret`, a byte scan of `.text`), and which has absence-style rows. There are 7 such types and 27 rows:
  - ImageBackedStateBlock and AchievementState (getter 002536A0);
  - BootSingleton01F7F598 (00189120);
  - PApplication (00796E20);
  - PendingCompletionQueue01F81248 (001BDAB0);
  - CPostEffect (006DF410, 006DF510);
  - InputManager (00198790).
- Each was run with `census_receiver_fixpoint.py SEED=call <getter>` and the absence rows as `DEBT`.

**Result** ([`getter_seed_absence_receipt.txt`](getter_seed_absence_receipt.txt)). The getter seeds reach 0 to 68 functions per type, and **no absence row's span has an access**. The receipt prints only non-empty spans, and there are none. The 27 claims hold under both seeds. No row is changed.

**Limit.** A getter seed follows the returned pointer. It cannot see a reader that obtains the object some other way, such as a second cell, an interior pointer or a vtable. The rows stay absence claims bounded by the seeds used.
