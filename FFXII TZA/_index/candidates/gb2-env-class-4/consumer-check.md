# Affected-consumer check: GB-2 answered - environment class 4 is tested by nothing (FABLE, Claude Opus 5.5, 2026-09-27)

affected: GB-2; 09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md

**Regression:** `gb2_env_class.py`, in this directory. It has four checks:
- the RIP-relative census of the global;
- the getter's six call sites;
- the stage's five compares;
- the shipped opcode-48 census, with the page's opcode 7 and opcode 6 totals as controls.

run: gb2_env_class.py at 1ff3df7cd (PASS, FAILS 0), 2026-09-27.

| consumer | what it said | state |
|---|---|---|
| `gambit-evaluation-and-enmity.md` selector table, opcode 48/49 | "two global getters, unread" | revised-here (struck; `00263E10` is the environment class, and all 17 shipped uses test Rain; `00377BA0` stays unread) |
| `_index/OPEN-QUESTIONS.md` GB-2 | OPEN | revised-here (ANSWERED; the designer label is NO ADMISSIBLE SOURCE) |
| `03-World-Area-Field/CONTRACT-weather.md` §14 item 2 | "whether the designers had a name for it is not in the image" | agrees |
| `08-Combat-Formula/Weather-Terrain-Element-Scaling/weather-terrain-element-scaling.md`, OPUS's domain section | "4 … applies no environmental element scaling" | agrees; the AI condition now joins it as the only other consumer |
