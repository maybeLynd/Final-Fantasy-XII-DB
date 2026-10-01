# Brief: reconstruction-readiness map (stream R)

You are a cloud session working for OPUS on the FF12 TZA knowledge database (this private repo, a text-only snapshot).
Read `docs/CLOUD_PROGRAM.md` first.

## Why

The database exists so that the game's engine and logic can later be re-implemented (the RE repo,
maybeLynd/Final-Fantasy-XII-RE). That work is not authorized yet. When it is, each system will be written from what
the database documents. This map says, per system:
- what a re-implementer would find;
- what they would still be missing.

The missing items are also database gaps, which is why the map is useful now.

## The task

For each system folder named in the launch message (for example `FFXII TZA/16-UI/`):
1. **Read the folder's pages:** status lines, the "What the player sees", "Native mechanism", "Key addresses", "Data
   structures", "Call chain" and "What is not known" sections, and the CONTRACT-*.md pages.
2. **Write the system's interface as the database states it:**
   - **Entry points:** functions with their callers.
   - **Inputs and outputs:** data read and written, with record layouts.
   - **State:** globals and objects, with lifetime.
   - **Order:** what runs when in a frame, and what triggers it.
   - **Dependencies:** on other systems.
   Cite page and section for each item.
3. **List what a re-implementer would still need and cannot find.** Examples: an undocumented field that a documented
   function writes; a callee named but not described; a state whose initial value is not given; a formula given only
   for some inputs. Give the page and line that shows the gap.
4. **Rate the system.** READY (could be written from the database alone), MOSTLY (named gaps), or NOT YET (structural
   gaps).

## Output

Write `cloud-reports/re-readiness/<system-slug>.md` per system, with sections:
1. Interface
2. Gaps
3. Rating

Quote and cite; do not invent behaviour. Where the database is silent, say "not stated". Do not write any code.

## Git

1. Work on the branch `cloud/re-readiness-<first slug>`.
2. Commit and push after each system.
3. Use the git author `maybeLynd` with an empty email, and no Co-Authored-By trailer.
4. Never push to `main`.
5. When done, open a pull request to `main` titled `cloud: reconstruction readiness for <systems>`.
