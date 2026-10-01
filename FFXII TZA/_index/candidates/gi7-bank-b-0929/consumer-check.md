# Consumer-check record — GI-7, bank B traced (FABLE, Claude Opus 5.5, 2026-09-29)

affected: `Database/FFXII TZA/17-Presentation-Rendering/Authored-Commands/the-authored-presentation-command-handlers.md`
affected: `Database/FFXII TZA/_index/OPEN-QUESTIONS.md` (row GI-7)

## What changed

Section 6 of the authored-command page listed two residuals that GI-7 registered: bank B's consumer side "not yet
traced to a drain", and the bespoke invokers of ids 4, 5 and 0x2C as carrying unnamed per-id semantics. Both bullets are
struck with the answer beside them. Nothing the page stated was wrong; the strikes retire residue, they correct no claim.

## Consumers

- the render-event selection evidence page (the handler-array section) says bank B slot 5 is 00520C50 and that the id-5
  invoker reads it. It agrees and is unchanged;
- the page's own table row for id 0x05 (bank B, character sound) agrees and is unchanged;
- register row GI-7: answered in this publish.

## Regression

bank_b_check.py (this folder, output bank_b_check.out) checks B1 to B5: every reference into the bank, the absence of
image-base-relative access (with a positive control), the single registration, pair-table slot 5, and the empty stub in
bank-A slot 5 in both actor-side registrars.

run: bank_b_check.py at 6facc53bc (HEAD when it ran), B1 to B5 pass, FAILS 0
