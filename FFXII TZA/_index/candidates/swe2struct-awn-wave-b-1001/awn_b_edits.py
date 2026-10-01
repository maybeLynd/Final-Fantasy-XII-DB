# -*- coding: utf-8 -*-
"""The exact edits SWE2-STRUCT (for OPUS) applied on 2026-10-01 for the second half of
SWE2AUDITSPEC-REQ-OPUS-0930-WAVE-NARROWINGS. Data only: awn_b_checks.py verifies them and
Database/Tools/work/SWE2-STRUCT/awnb/apply_awnb.py applies them (idempotent).

Each edit: id, review (the auditspec-review folder), file (relative to Database/FFXII TZA), old (the
exact text before), new (the exact text after), struck (spans that must appear wrapped in ~~ ~~).
"""

C = "_index/candidates/"
RV = "auditspec-review-%s-0930/REVIEW.md"


def S(x):
    return "~~" + x + "~~"


def note_c(review, extra=""):
    """dated note for a record under _index/candidates/<x>/"""
    return ("narrowed 2026-10-01, SWE2-STRUCT for OPUS, on SWE2-AUDIT-SPEC's [review](../" + RV % review + ")"
            + extra)


def note_p(review, depth, extra=""):
    up = "../" * depth
    return ("narrowed 2026-10-01, SWE2-STRUCT for OPUS, on SWE2-AUDIT-SPEC's [review](" + up + C + RV % review + ")"
            + extra)


EDITS = []


def E(id_, review, file, old, new, struck=()):
    EDITS.append(dict(id=id_, review=review, file=file, old=old, new=new, struck=list(struck)))


# ---------------------------------------------------------------- types-sections
F = C + "opus-types-section-tables-0930/README.md"
o = "- **P4.** `+0x0A0` and `+0x0A8` have no other writer. `+0x100` has one more, the teardown `0032ED80`, which stores 0.\n"
s1 = "`+0x0A0` and `+0x0A8` have no other writer. `+0x100` has one more, the teardown `0032ED80`, which stores 0."
E("TS-1", "types-sections", F, o,
  "- **P4.** " + S(s1) + " The only non-zero writers are the setters (one caller each); all three fields are also zeroed by\n"
  "  `ActorManager_BindLoadedDefinitionPayload` `0026C8C0` (`0026CC31` / `0026CC49` / `0026CC50`, on every definition\n"
  "  bind), by the boot clear `00266D10` (`memset` of each 0x288-byte slot, `00266EFC`) and, for `+0x100`, by the teardown\n"
  "  `0032ED80`. *(" + note_c("types-sections", "; the store census that is not limited to the setters' callers is the review's "
  "`slot_writers.py`. `types_sections.py` P4 is unchanged and still counts the setters' callers only.)*") + "\n",
  [s1])

TT = "the only non-zero writers are the setters (one caller each); all three fields are also zeroed by ActorManager_BindLoadedDefinitionPayload 0026C8C0 (0026CC31 / 0026CC49 / 0026CC50, on every definition bind), by the boot clear 00266D10 (memset of each 0x288-byte slot, 00266EFC) and, for +0x100, by the teardown 0032ED80"
TN = " (narrowed 2026-10-01, SWE2-STRUCT for OPUS, on SWE2-AUDIT-SPEC's review _index/candidates/auditspec-review-types-sections-0930/REVIEW.md)"
s2 = "the slot pointer is written only by the bind (0026C880 / 0026C8A0 have one caller each)"
E("TS-2", "types-sections", "_types/types.tsv", s2, S(s2) + " " + TT + TN, [s2])
o = "as it frees the per-tag blocks; the table itself ends with the payload's release."
E("TS-3", "types-sections", "_types/types.tsv", o, o + " Writers of the slot: " + TT + TN + ".")

# ---------------------------------------------------------------- sd164-167
F = C + "sd164-167-arena-allocator-0930/README.md"
h1 = ("`002E6D60` takes the **tail of the request list `0215FD88`**, the list the per-frame gate drains. It delivers\n"
      "    that entry (`0041E490`) and frees it (`002E9360`), unless the entry is flagged (`+0x18` bit 3, `+0x19` bit 2) or\n"
      "    empty.")
h2 = "It **always returns 0**."
h3 = ("So a failed allocation in arena 6 or 0xA first retires one pending request, freeing its memory. The allocator\n"
      "    never retries on the callback's answer (`test esi, esi` at `0036C0B7` sees 0); its reclaim step decides.")
E("SD164-1", "sd164-167", F,
  "- **H2: what the callback does.**\n  - " + h1 + "\n  - " + h2 + "\n  - " + h3 + "\n",
  "- **H2: what the callback does.** *(H2 " + note_c("sd164-167", ": the struck bullets are replaced by the review's wording "
  "that follows them; H1, A1 and K1 are unchanged.)*") + "\n"
  "  - " + S(h1) + "\n  - " + S(h2) + "\n  - " + S(h3) + "\n"
  "  - `002E6D60` first calls `002E6900(0)`. That call retires the tail node of a second list, `0215FD90`: each set\n"
  "    slot goes to `0041E490` and `00369800` and is cleared, the node is unlinked, and the rest of that list is walked.\n"
  "    It always returns 0 (one exit, `002E6A70 xor eax, eax`), so the skip at `002E6D6D` is never taken.\n"
  "  - The callback then takes the tail of `0215FD88`, the list the per-frame gate drains.\n"
  "    - An entry with `+0x10 = 0` is left in place.\n"
  "    - A flagged entry (`+0x18` bit 3, `+0x19` bit 2) is freed (`002E9360`) without being delivered.\n"
  "    - Any other entry is delivered (`0041E490`) and then freed.\n"
  "    - If `0215FD88` was empty, it calls `002E6900(0)` again.\n"
  "  - It always returns 0.\n"
  "  - `0036BFE0` calls it before **every** attempt in arena 6 or 0xA, including each retry after a reclaim. The three\n"
  "    allocation entries `0036A100`, `0036A1A0` and `0036B160` reach `0036BFE0` only after a direct `0036BC60` attempt\n"
  "    has returned null, so on those paths the retirement follows a failure. The realloc's null-pointer arm `0036D050`\n"
  "    (from `0036CAD0`) calls `0036BFE0` with no prior attempt, so there the callback runs before any failure.\n"
  "  - The allocator never retries on the callback's answer (`test esi, esi` at `0036C0B7` sees 0); its reclaim step\n"
  "    (`edi`) decides.\n",
  [h1, h2, h3])

# ---------------------------------------------------------------- sd166
F = C + "sd166-arena-7-0930/README.md"
a1 = "The only way to reach it is a script calling one of two debug verbs, and no shipped script does."
E("SD166-1", "sd166", F, a1 + "\n",
  S(a1) + " The only way to reach it is a script calling one of four class-2 debug verbs, and no shipped script calls any of\n"
  "them: `debug_tkmalloc` 0x2003 and `debug_tkmallochandle` 0x2008 (handlers `0050DA30` / `0050DBD0`, which jump into\n"
  "the push functions), and `debug_tkmalloc_4` 0x2004 and `debug_tkmallochandle_9` 0x2009, whose handlers are the push\n"
  "functions `0050D8F0` / `0050DAD0` themselves (class-2 table `01F26720`, slots `01F267C0` / `01F26860`). *("
  + note_c("sd166") + ")*\n", [a1])
E("SD166-2", "sd166", F,
  "| `0050D8F0` | `debug_tkmalloc` (`0x2003`, handler `0050DA30`): a script integer |",
  "| `0050D8F0` | `debug_tkmalloc` (`0x2003`, handler `0050DA30`) and itself the handler of `debug_tkmalloc_4` (`0x2004`): a script integer |")
E("SD166-3", "sd166", F,
  "| `0050DAD0` | `debug_tkmallochandle` (`0x2008`, handler `0050DBD0`): a script integer | the script's value |\n\n",
  "| `0050DAD0` | `debug_tkmallochandle` (`0x2008`, handler `0050DBD0`) and itself the handler of `debug_tkmallochandle_9` (`0x2009`): a script integer | the script's value |\n\n"
  "  *(The `0050D8F0` / `0050DAD0` rows " + note_c("sd166", ": the class-2 table `01F26720` holds the push functions "
  "themselves as the handlers of 0x2004 / 0x2009, slots `01F267C0` / `01F26860`, both DIR64-relocated. "
  "`sd166_check.py` A4 tests direct callers only and S1 censuses 0x2003 / 0x2008 only; the four-id census is the "
  "review's `census_debugverbs.out`.)*") + "\n\n")
s3 = "`debug_tkmalloc` and `debug_tkmallochandle` are **never called**."
E("SD166-4", "sd166", F, "  - " + s3 + "\n",
  "  - " + S(s3) + " `debug_tkmalloc`, `debug_tkmalloc_4`, `debug_tkmallochandle` and `debug_tkmallochandle_9` (0x2003,\n"
  "    0x2004, 0x2008, 0x2009) are never called. *(" + note_c("sd166") + ")*\n", [s3])
s4 = "`debug_tkmalloc(7, ...)`"
E("SD166-5", "sd166", F, "`debug_tkmalloc(7, ...)` would allocate over a live load buffer.",
  S(s4) + " any of the four debug verbs with 7 would allocate over a live load buffer. *(" + note_c("sd166") + ")*", [s4])
E("SD166-6", "sd166", "../Tools/analysis-kit/gfz-scripts/regval.py",
  "It does not see indirect callers, callers through tail jumps into the middle of a body, or stack-passed arguments.\n",
  "It does not see indirect callers, callers through tail jumps into the middle of a body, or stack-passed arguments,\n"
  "nor jump-table (indirect `jmp`) edges into a node that also has a direct predecessor (such a node gives no U), nor\n"
  "jumps into the body from code outside its extent. `movzx`/`movsx` from an 8- or 16-bit register is treated as a copy\n"
  "of the whole register, and a `cmp`/`test` on a sub-register pins the whole register.\n"
  "(Limits added 2026-10-01, SWE2-STRUCT for OPUS, on SWE2-AUDIT-SPEC's review\n"
  "Database/FFXII TZA/_index/candidates/auditspec-review-sd166-0930/REVIEW.md.)\n")

# ---------------------------------------------------------------- sd126
F = C + "sd126-hud-proc-arms-0930/README.md"
E("SD126-1", "sd126", F, "| procedure | id | message | arm | direct callees |",
  "| procedure | id | message | arm | ~~direct callees~~ calls before the arm's first jump (straight-line prefix) |",
  ["direct callees"])
E("SD126-2", "sd126", F, "| | 12 | enable/disable | `00278302` | none (inline) |",
  "| | 12 | enable/disable | `00278302` | ~~none (inline)~~ none before its first jump |", ["none (inline)"])
E("SD126-3", "sd126", F, "| | 2 | GENERATION RECONCILE | `004055BE` | none |",
  "| | 2 | GENERATION RECONCILE | `004055BE` | ~~none~~ none before its first jump |", ["none"])
s5 = "private to the command menu (no protocol name)"
E("SD126-4", "sd126", F, "| | 30, 31, 32, 35, 44, 45 | private to the command menu (no protocol name) |",
  "| | 30, 31, 32, 35, 44, 45 | " + S(s5) + " 31, 32, 35, 44, 45: no protocol row; 30: the protocol's narrowed id |", [s5])
s6 = "six private message ids (30–45)"
E("SD126-5", "sd126", F, "- The command dispatcher (`002778C0`) adds six private message ids (30–45) of its own.",
  "- The command dispatcher (`002778C0`) adds " + S(s6) + " five private ids (31–45) and the narrowed id 30 of its own.")
E("SD126-6", "sd126", F, "  not a message dispatch, and is not decoded here.\n- **Static only.**\n",
  "  not a message dispatch, and is not decoded here.\n"
  "- **The prefix column** *(" + note_c("sd126", "; the column rename, the two \"none before its first jump\" cells, the "
  "id 30 row and the modding line come from the same review)") + ")*:\n\n"
  "  > This column is the straight-line prefix of each arm, not its callee set. Measured over each arm's own code (the\n"
  "  > code no other arm reaches), 13 of 31 arms call more:\n"
  "  > - `002778C0` id 12 makes 18 direct calls, and id 2 makes 22;\n"
  "  > - `00405310` id 2 calls `00244F00` and `00404D40`.\n"
  "  >\n"
  "  > See `auditspec-review-sd126-0930/sd126_indep.out`.\n"
  "- **Static only.**\n")

# ---------------------------------------------------------------- sd127
F = C + "sd127-hud-key-base-reads-0930/README.md"
k = ["**K1: none of the 86 keys is read by any of three non-rip routes.** Image-wide:",
     "**R1:** no image-base-relative operand has a displacement of key − `0x120000`.",
     "**R2:** there are 37 `lea`s of a layout-block address outside the console installer, and no read through such a\n"
     "    register lands on a HUD key.",
     "**R3:** no stored qword holds a key's address."]
E("SD127-1", "sd127", F,
  "- " + k[0] + "\n  - " + k[1] + "\n  - " + k[2] + "\n  - " + k[3] + "\n",
  "- " + S(k[0]) + "\n  - " + S(k[1]) + "\n  - " + S(k[2]) + "\n  - " + S(k[3]) + "\n\n"
  "  *K1 " + note_c("sd127") + "; it becomes:*\n\n"
  "  > No battle-HUD key is read by an image-base-relative operand at its own displacement, by a stored pointer, or\n"
  "  > through a block lea followed in its function and two callees deep, apart from the indirect calls `00267A79`\n"
  "  > (`[r15 + 0x88]`, `rdx = 01E0C32E`) and `00244EF5` / `00246C09` (`call rax`), which are not resolved.\n"
  "  >\n"
  "  > Indexed table reads next to the keys are not excluded by code:\n"
  "  > - `00266530` (`00266588`) and the code at `00266B83` index the 8-entry `01E0C328` table with a 5-bit field, so\n"
  "  >   entries 8..31 would read HUD-key bytes up to `01E0C3A5`;\n"
  "  > - `002AEB20` (`002AECA3`, `002AEE26`) indexes the 32-byte tables `01E0CE30` / `01E0CE10` with a text byte − 0x40\n"
  "  >   that is not bounded below `TargetInfoMoveY` (`01E0CE94`).\n"
  "  >\n"
  "  > Whether authored data reaches those indices is not checked.\n\n", k)
E("SD127-2", "sd127", F,
  "    in code: a count above 8 would read HUD keys as table entries. That would be an overrun, not a key read.\n",
  "    in code: a count above 8 would read HUD keys as table entries. That would be an overrun, not a key read.\n"
  "  - **Two more readers of the `01E0C328` table:** `00266530` (`00266588`) and the code at `00266B83`, each indexing\n"
  "    it with a 5-bit field. *(" + note_c("sd127") + ")*\n")
m = ("editing a battle-HUD key's global, or the instruction that reads it, is enough. No HUD code reaches\n"
     "a key through a copied pointer, so there is no second read to patch.")
E("SD127-3", "sd127", F, "**For modding:** " + m + "\n",
  "**For modding:** " + S(m) + " No HUD code reaches a key through a copied pointer; the open cases are the indexed table\n"
  "reads above. *(" + note_c("sd127") + ")*\n", [m])
r2 = ("**R2** follows a `lea`'d address within the same function only. Handed-on addresses are covered for the two cases\n"
      "  in K3, which are the only `lea` targets within 0x40 bytes of a HUD key. The other `lea` targets have no HUD key\n"
      "  within 0x40.")
E("SD127-4", "sd127", F, "- " + r2 + "\n",
  "- " + S(r2) + " R2 swept `01E0C000`..`01E0D100`. Outside the console installer, the lea targets within 0x40 below a HUD\n"
  "  key are K3's two, `001B44A0`'s two (K2), and, outside the block, `0209E608` (+0x10, read to +6 by `00285F00`) and\n"
  "  `0209E610` (+0x8, index 0..4 at `002BDB3B`). Neither reaches a key. *(" + note_c("sd127") + ")*\n", [r2])

# ---------------------------------------------------------------- sd169
F = C + "sd169-draw-surface-cells-0930/README.md"
g = "It has one writer (the boot `0036D280`) and one reader, `0036D2F0`."
E("SD169-1", "sd169", F, g + " That reader\n",
  S(g) + " It has one writer (the boot `0036D280`). Its one use is `0036D2F0`'s word\n"
  "  read (`0036D342`), which passes it only to the bare `ret` `0016D6A0`. Three qword loads of `+0x9C` also load it as\n"
  "  their high half: `00244224` (in `00244200`), `002443E7` (in `002443D0`) and `004FDDC7` (in `004FDDA0`). None of\n"
  "  them uses that half. *(" + note_c("sd169") + ")* That reader\n", [g])

# ---------------------------------------------------------------- sd121
F = C + "sd121-effect-actor-slots-0930/README.md"
h = "**S3: the writers are four script verbs.**"
E("SD121-1", "sd121", F, "- " + h + "\n",
  "- " + S(h) + " **S3: the non-zero writers are two script verbs; four more paths store 0.** `effectactor` /\n"
  "  `bgeffectactor` are the only writers of a handle. Zeroes come from `clear_effectactor` / `clear_bgeffectactor`, from\n"
  "  `0036E080` (called by the area unload `002628B0` at `00262997`, it clears in all three arrays every slot whose handle\n"
  "  bits 16-19, the actor's `+0x15` nibble, equal the unloaded area index), and from the reset `0036E3B0` (called by\n"
  "  `ActorManager_BindLoadedDefinitionPayload` `0026C8C0` at `0026CA57`). *(" + note_c("sd121") + ")*\n", [h])
u = ("**Using the handle.** The element resolves it through `ActorHandle_ResolveRegistryEntryByPackedId` (`003588B0`)\n"
     "    and copies the actor's position into its own `+0x30` / `+0x34` / `+0x38` (`00265020`).")
E("SD121-2", "sd121", F, "  - " + u + "\n",
  "  - " + S(u) + "\n"
  "    **Using the handle.** `003A40F0` first maps the handle through `002E9B80` (the actor's `+0xC0` record index). For\n"
  "    an actor that has one, the element takes the 0x740-byte record `[022C6F28] + i*0x740` and copies no position.\n"
  "    Only for an actor without one does it resolve the handle through `003588B0` and copy `[actor+0xB8]`'s three dwords\n"
  "    (`Actor_GetWorldPosition`, `00265020`) into its `+0x30` / `+0x34` / `+0x38`. `003A4220` returns\n"
  "    `002E9B80(handle)` (an index, or -1) and copies nothing. An empty slot in the `99B0` / `98B0` table falls back to\n"
  "    `97B0`. *(" + note_c("sd121") + ")*\n", [u])
f = "follows whichever actor"
E("SD121-3", "sd121", F, "**For modding:** an effect bound to effect-actor slot *n* follows whichever actor last ran",
  "**For modding:** an effect bound to effect-actor slot *n* " + S(f) + " is anchored to (or, for an actor with a battle\n"
  "record, bound to the record of) whichever actor *(" + note_c("sd121") + ")* last ran", [f])
li = "**`0036E080`.** The slot clearer the world-tick page reads (the first two arrays) is not re-read."
E("SD121-4", "sd121", F, "- " + li + "\n",
  "- " + S(li) + " `0036E080` is read (see S3). It covers all three arrays, not the first two. The world-tick page's\n"
  "  \"dual-table\" line is the source of the old wording. *(" + note_c("sd121") + ")*\n", [li])

# ---------------------------------------------------------------- sd123
F = C + "sd123-kind52-image-record-0930/README.md"
t = "paletted image (texture) record"
E("SD123-1", "sd123", F,
  "# SD-123: effect record kind `0x52` is the effect container's paletted image (texture) record (OPUS, 2026-09-30)\n",
  "# SD-123: effect record kind `0x52` is the effect container's " + S(t) + " image (texture) record: 4- or 8-bit indexed with one palette, or 4-byte-per-pixel direct colour (OPUS, 2026-09-30)\n\n"
  "*(Title, answer, I2, I3 and the modding line " + note_c("sd123", "; the register row's summary is proposed for OPUS in "
  "[swe2struct-awn-wave-b-1001](../swe2struct-awn-wave-b-1001/README.md).)*") + "\n", [t])
an = ("**A kind-`0x52` record is a CLUT-paletted image: a format, N palettes and a size, from which the loader creates the\n"
      "palettes and the image surface.**")
E("SD123-2", "sd123", F, an + "\n",
  S(an) + "\n\n"
  "A kind-`0x52` record is an image: a format, a palette count and a size. The loader masks the format to 6 bits\n"
  "(`00500C39`; bit 7 is kept at `+0x1CA`, bit 6 at `+0x1C8`). Format 0 is 4-bit indexed (64-byte palettes, w·h/2\n"
  "pixel bytes), format 1 is 8-bit indexed (1,024-byte palettes, w·h), and formats 2 / 3 / 4 are 2 / 3 / 4 bytes per\n"
  "pixel with no palette. A palette count above 0 with any format other than 0 / 1 fails the load.\n", [an])
E("SD123-3", "sd123", F,
  "  - Format 1 (or `0x81`) takes 1,024-byte palettes (count << 10: 256 colours × 4 bytes). Format 0 (or `0x80`) takes\n"
  "    64-byte palettes (count << 6: 16 colours × 4). Any other format fails the load.\n",
  "  - Format 1 ~~(or `0x81`)~~ takes 1,024-byte palettes (count << 10: 256 colours × 4 bytes). Format 0 ~~(or `0x80`)~~ takes\n"
  "    64-byte palettes (count << 6: 16 colours × 4). Any other format fails the load. File bytes with bit 7 or 6 set\n"
  "    select the same palettes through the mask. *(" + note_c("sd123") + ")*\n", ["(or `0x81`)", "(or `0x80`)"])
p = ("Each palette goes through the CLUT submit `001837A0` and `00183760`, and the two handles are stored at\n"
     "    `+0xC8 + 8i` and `+0x148 + 8i`.")
E("SD123-4", "sd123", F, "  - " + p + "\n",
  "  - " + S(p) + " Each palette's data goes through `001837A0` (+0xC8 + 8i); `00183760` makes a same-size handle with\n"
  "    no data (+0x148 + 8i). *(" + note_c("sd123") + ")*\n", [p])
i3 = ("The surface is then\n"
      "  created through the render-layer calls (`00183EE0`, `00184140`, `00184130`, `00184370`, `00183A00`, `00183C60`,\n"
      "  `00183EB0`), sized by `+0xA8` × `+0xAA`.")
E("SD123-5", "sd123", F, i3 + "\n",
  S(i3) + " The live surface calls are `00183EE0` / `00184140` / `00183A00` / `00183C60` / `00183EB0`; `00184130` /\n"
  "  `00184370` are the unreachable 0x80 / 0x81 arms. The surface is sized by `+0xA4` × `+0xA6` (copies of `+0xA8` /\n"
  "  `+0xAA`). *(" + note_c("sd123", "; `sd123_kind52.py` still pins `00500CF1` and `00500FA4` / `00500FB4`, which sit in "
  "the dead arms)") + ")*\n", [i3])
mo = ("the 13,161 kind-`0x52` records are the effect containers' textures: indexed images with 16- or\n"
      "256-colour palettes.")
E("SD123-6", "sd123", F, "**For modding:** " + mo + " Replacing",
  "**For modding:** " + S(mo) + " the 16,862 kind-`0x52` records over every EFX stream (13,161 in the .efx / .efb-only\n"
  "walk) are the effect containers' textures: 11,076 indexed (1,131 with 16 colours, 9,945 with 256, one palette each)\n"
  "and 5,786 direct colour at 4 bytes per pixel. No shipped record uses formats 2 or 3. *(" + note_c("sd123") + ")* Replacing",
  [mo])

# ---------------------------------------------------------------- sd160
F = C + "sd160-free-target-type3-0930/README.md"
oc = ("`sd160-census.tsv` (every call of the two verbs) and\n"
      "  `sd160-type3-scripts.tsv` (the type-3 sites).")
E("SD160-1", "sd160", F, "Its output is " + oc + "\n",
  "Its output is " + S(oc) + " `sd160-census.tsv` (the 612 type-3 sites, all languages) and\n"
  "  `sd160-type3-scripts.tsv` (one row per zone, verb and script). *(" + note_c("sd160") + ")*\n", [oc])
ce = "`THIRD_*` (Gabranth, Larsa, Montblanc and seven more third-party allies)"
E("SD160-2", "sd160", F, "| `btlAtelSetUnitType(2)` | " + ce + " |",
  "| `btlAtelSetUnitType(2)` | " + S(ce) + " `THIRD_*` (Gabranth and Larsa, from `ガブラス` / `ラーサー`, and eight more third-party scripts, among them `モーニ` twice; `モーニ` is not Montblanc's Japanese name `モンブラン` and is not resolved to a character here) |",
  [ce])
rd = ("The Japanese script names are decoded as cp932; the English names in the table (Gabranth, Larsa, Montblanc) are\n"
      "  readings of `ガブラス`, `ラーサー`, `モーニ`, and the \"seven more\" are `カロリーヌ`, `アルマ`, `シーク`, `バンサト`,\n"
      "  `ヴィエラ`, `ガリフ` and a second `モーニ`.")
E("SD160-3", "sd160", F, "- " + rd,
  "- " + S(rd) + " The Japanese script names are decoded as cp932. `THIRD_*` (Gabranth and Larsa, from `ガブラス` /\n"
  "  `ラーサー`, and eight more third-party scripts, among them `モーニ` twice; `モーニ` is not Montblanc's Japanese name\n"
  "  `モンブラン` and is not resolved to a character here). The other six are `カロリーヌ`, `アルマ`, `シーク`, `バンサト`,\n"
  "  `ヴィエラ` and `ガリフ`. *(" + note_c("sd160") + ")*", [rd])

# ---------------------------------------------------------------- sd161
F = C + "sd161-counter11-writers-0930/README.md"
hl = ("**So every writer this census and AB-8 find stores 0 or a non-negative value.** On a new game the check passes the\n"
      "first time it runs.")
E("SD161-1", "sd161", F, hl + "\n",
  S(hl) + "\n\n"
  "**Every store this census places at a known offset on the field is a memset to 0, and AB-8's accessor writers store\n"
  "only non-negative values.** So a new game starts counter 11 at 0. The census's other 365 stores that can reach the\n"
  "field were bounded by SWE2-AUDIT-SPEC (review 2026-09-30). All cannot reach it except three groups: the backup\n"
  "restore `00583C00`, which copies the backup's bytes over image `[0, 0xE240)`; the bit helpers `00315AD0`, `00252D40`\n"
  "and `00254E00` and the `0046B290`–`0046B490` family, whose index is bounded only by their callers; and `003112F0`,\n"
  "which stores only values that are non-negative at their width. Until those callers are bounded, the first evaluation\n"
  "passes unless one of them sets the field's sign bit first. *(" + note_c("sd161") + ")*\n", [hl])
cr = ("this census\n"
      "  did not see them, because it follows the record pointer and they write through a destination pointer.")
E("SD161-2", "sd161", F, cr + "*\n",
  S(cr) + " the census listed `00583C00` (INDEXED-UNKNOWN, reached through the getter `002EF640`) but the record\n"
  "  did not classify it; the storage-read chain writes through a destination pointer the census does not follow. ("
  + note_c("sd161") + ")*\n", [cr])
lm = ("It reports its\n"
      "  `INDEXED-BELOW` stores (202, most with low base offsets such as `+0x30`, `+0x70`, `+0x90` and `+0x3404`) as\n"
      "  *able to reach* the field only if their index is large. Their indices were not bounded here.")
E("SD161-3", "sd161", F, lm,
  S(lm) + " It reports 202 `INDEXED-BELOW` and 163 `INDEXED-UNKNOWN` stores that can reach the field (bounded in the\n"
  "  SWE2-AUDIT-SPEC review, 2026-09-30). *(" + note_c("sd161", "; most `INDEXED-BELOW` stores have low base offsets such as "
  "`+0x30`, `+0x70`, `+0x90` and `+0x3404`)") + ")*", [lm])

# ---------------------------------------------------------------- sd163
F = C + "sd163-steamcontroller-poll-0930/README.md"
q = "(qwords `02EA9510`…`02EA9590`)"
E("SD163-1", "sd163", F, "For each of 16 digital action handles " + q + ", `+0x48` returns the\n",
  "For each of 16 digital action handles " + S(q) + " (qwords `02EA9510`…\n"
  "  `02EA9588`) *(" + note_c("sd163") + ")*, `+0x48` returns the\n", [q])
nm = "That naming is an identification matched to the call shapes, not a symbol."
E("SD163-2", "sd163", F, nm + "\n",
  S(nm) + " The slot names are confirmed against the shipped `steam_api64.dll` (`SteamController005`): its flat\n"
  "exports `SteamAPI_ISteamController_*` call through the same slots (SWE2-AUDIT-SPEC review 2026-09-30). *("
  + note_c("sd163") + ")*\n", [nm])
l1 = ("**Which game input each action means.** The 16 action handles are looked up by name elsewhere, and their mapping is\n"
      "  not read here.")
l2 = "**What `007A15A0` does per binding** beyond walking the list is not read."
E("SD163-3", "sd163", F, "- " + l1 + "\n- " + l2 + "\n",
  "- " + S(l1) + " **Which button each byte is** (the review's optional wording): the name table at `01F40210` names the\n"
  "  cells Up, Down, Left, Right, Circle, Cross, Square, Triangle, L1, L2, L3, R1, R2, R3, Start, Select in order, so\n"
  "  `+0x43C`..`+0x44B` are Square, Cross, Circle, Triangle, L1, R1, L2, R2, Select, Start, L3, R3, Up, Right, Down,\n"
  "  Left, the XInput poll's PlayStation order. *(" + note_c("sd163") + ")*\n"
  "- " + S(l2) + " **`007A15A0`'s edge rule** (the review's optional wording): it walks the ring at `this+0x18`; for a\n"
  "  node with a state pointer `+0x38` it sets `+0x31` = 1 on a 0->1 edge and `+0x32` = 1 on a 1->0 edge, then `+0x30` =\n"
  "  the new state; otherwise, with `+0x40` set, it calls `0079A5F0`. *(" + note_c("sd163") + ")*\n", [l1, l2])

# ---------------------------------------------------------------- sd192
F = C + "sd192-attached-bit-readers-0930/README.md"
ti = "every reader of the \"attached\" bit refuses movement on it"
E("SD192-1", "sd192", F, "# SD-192: " + ti + " (OPUS, 2026-09-30)\n",
  "# SD-192: " + S(ti) + " every movement-side reader of the attached bit (the eight checked; not the attach guard `002E274A` or the two presentation readers) refuses movement on it (OPUS, 2026-09-30)\n\n"
  "*(Title " + note_c("sd192", "; the register row's lead is proposed for OPUS in "
  "[swe2struct-awn-wave-b-1001](../swe2struct-awn-wave-b-1001/README.md).)*") + "\n", [ti])
fv = "Those five were not read here."
E("SD192-2", "sd192", F, "of the same byte) would not appear. " + fv,
  "of the same byte) would not appear. " + S(fv) + " SWE2-AUDIT-SPEC read them (2026-09-30): they use bits 1 and 3-7, not\n"
  "  bit 0. *(" + note_c("sd192") + ")*", [fv])

# ---------------------------------------------------------------- dd-mixed (record note only; the status line is proposed)
F = C + "opus-dd-restatus-mixed-0930/README.md"
o = "`what-each-script-verb-touches.md`. It is added to the report SWE2-EC7 reads (`OPUS-REQ-EC7-A-DRIFT-REFUSALS-2-0930`).\n"
E("DDMIX-1", "dd-mixed", F, o,
  o + "\n*(" + note_c("dd-mixed", ": the measuring-text status line still ends \"what the reveal stepper's modes are for is "
  "SD-100 (status line current 2026-09-30, SWE2-DATA)\", which reads as open residue beside \"SD-100 answered\". The "
  "replacement is a status-line edit, so it is proposed for OPUS in "
  "[swe2struct-awn-wave-b-1001](../swe2struct-awn-wave-b-1001/README.md) rather than applied.)*") + "\n")

# ---------------------------------------------------------------- dd-02-restatus
F = "02-Resource-And-Asset-Pipeline/a-typed-list-measured-once-and-built-in-one-allocation.md"
c1 = "108 call sites, 36 UI-owned"
E("DD02R-1", "dd-02-restatus", F, "| " + c1 + " | `edges.tsv`",
  "| " + S(c1) + " 108 calling functions (113 call sites), 36 UI-owned | `edges.tsv`", [c1])
oldA = ("| ~~what the types mean~~ | ~~**not established**~~ superseded: §5b, §5e and UQ-75..78 name every type (2026-09-17 / 2026-09-22); marked 2026-09-30, SWE2-CONTRACT | constructors and drawers read | 1 | PROVEN |\n"
        "| ~~any runtime observation~~ | ~~**none exists**~~ superseded: the 2026-09-08 live read of the slot registry (AUDIT-LOG, `7593db615`), §5c; marked 2026-09-30, SWE2-CONTRACT | live read, read-only | live | OBSERVED |\n")
newA = ("| ~~what the types mean~~ — superseded: §5b, §5e and UQ-75..78 name every type (2026-09-17 / 2026-09-22); marked 2026-09-30, SWE2-CONTRACT | ~~**not established**~~ constructors and drawers read | 1 | PROVEN |\n"
        "| ~~any runtime observation~~ — superseded: the 2026-09-08 live read of the slot registry, §5c; marked 2026-09-30, SWE2-CONTRACT | ~~**none exists**~~ live read, read-only (AUDIT-LOG, `7593db615`) | 10 | OBSERVED |\n")
E("DD02R-2", "dd-02-restatus", F, oldA, newA, ["what the types mean", "**not established**", "any runtime observation", "**none exists**"])
E("DD02R-3", "dd-02-restatus", F,
  "| resources 111 / 127 are `save_load.mrp` / `DataFace_c.tm2` | SWE2-DATA `kind7.py`, `b6_typed_list.py` K1–K3 | 1 | PROVEN |\n\n## 11. Related",
  "| resources 111 / 127 are `save_load.mrp` / `DataFace_c.tm2` | SWE2-DATA `kind7.py`, `b6_typed_list.py` K1–K3 | 1 | PROVEN |\n\n"
  "*(§10 " + note_p("dd-02-restatus", 1, " correction 1: the first row counts calling functions and sites as §2 does; the "
  "two rows SWE2-CONTRACT rewrote are re-cut to four cells, and the runtime row's tier is 10, not \"live\".)*") + "\n\n## 11. Related")
F = "02-Resource-And-Asset-Pipeline/resource-section-addressing.md"
E("DD02R-4", "dd-02-restatus", F,
  "`@ALL` absent from every entry | data (2026-09-12) |",
  "`@ALL` absent from every entry | ~~data (2026-09-12)~~ 9 |", ["data (2026-09-12)"])
E("DD02R-5", "dd-02-restatus", F,
  "and `0040969C`–`004096A8` | 1 |\n\n**On the inherited names.**",
  "and `0040969C`–`004096A8` | 1 |\n"
  "| §2a: nonempty PRF lookup and setup (SECTION-10) | retained original bodies, byte-exact (FRONTIER-REVIEW-AUDITSPEC-OV-ACCEPTANCE-0929); their isolated original-code fixture replays are Linux-gated and were not re-run by the acceptance | 1 (bodies); fixture execution UNMEASURED on Windows |\n\n"
  "*(§8 " + note_p("dd-02-restatus", 1, " correction 2: the authored-data row's tier is 9, and §2a gets its row.)*") + "\n\n"
  "**On the inherited names.**")
o6 = ("`RenderResourceEntry` (OPUS, with `RenderResourceEntryBank` at `0x60`, `aa3470a36` / `0cca6e0f0`), and the `0xC0`\n"
      "family is `RenderStrideC0Element` (FABLE 2026-09-26, J-4, the box above).")
E("DD02R-6", "dd-02-restatus", F, o6 + "\n",
  S(o6) + "\n`RenderResourceEntry` (declared by OPUS at `8c13cfe3f`, 2026-09-19; its bank `RenderResourceEntryBank`, `0x60`, at\n"
  "`aa3470a36`), and the `0xC0` family is `RenderStrideC0Element` (declared by OPUS at `4fee674b9`, 2026-09-19; read\n"
  "from the type store as J-4's answer by FABLE on 2026-09-26, the box above). *(" + note_p("dd-02-restatus", 1,
  " correction 3, which applies the [DDRES-B6 review](../_index/candidates/auditspec-review-ddres-b6-0930/REVIEW.md)'s "
  "correction 1.)*") + "\n", [o6])
F = C + "opus-dd-restatus-02-0930/README.md"
o = "by these pages.\n"
E("DD02R-7", "dd-02-restatus", F, "**A-drift checked.** `adrift_report.py` after the two re-statuses shows no new refused family row: still 10, none caused\n" + o,
  "**A-drift checked.** `adrift_report.py` after the two re-statuses shows no new refused family row: still 10, none caused\n" + o +
  "\n*(" + note_c("dd-02-restatus", ": corrections 1-3 are applied on the two pages (typed list §10; section addressing §8 and "
  "the type-store attribution); the status words stay DOCUMENTED. The optional front-matter `external_production.status` "
  "update is not applied, because it is front matter and optional.)*") + "\n")

# ---------------------------------------------------------------- dd-02-b2
P = "02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/"
B2 = lambda extra="": "*(" + note_p("dd-02-b2", 2, extra) + ")*"
F = P + "as7-menu-graphics-containers.md"
E("DD02B-1", "dd-02-b2", F,
  "| `+0x02` count | slot binder (dynamic) | — | — | reader not isolated to field |\n"
  "| `+0x04` tailOff | — | — | — | no reader found |\n"
  "| `offsets[]` | page/payload indexer | — | — | field-level walk not isolated |\n\n",
  "| `+0x02` count | slot binder (dynamic) | — | — | reader not isolated to field *(since read: the walker `0024AA00` reads it big-endian at `0024AA0A` / `0024AA26`, RC-22..24; pointer 2026-09-30)* |\n"
  "| `+0x04` tailOff | — | — | — | no reader found *(since read: the tail block every page decode `00248500` reads, RC-23)* |\n"
  "| `offsets[]` | page/payload indexer | — | — | field-level walk not isolated *(since read: the walker `0024AA00`, RC-24)* |\n\n"
  + B2(" correction 1: the three Inert cells above carry their answers.") + "\n\n")
F = P + "btm-exfont-bitmaps.md"
E("DD02B-2", "dd-02-b2", F,
  "the `fontpack`/`fontheader` half, ids 130–135) |\n",
  "the `fontpack`/`fontheader` half, ids 130–135) *(superseded: ids 130–135 are never requested; the glyph tables come from `fontpack_fs.bin`, RC-27)* |\n")
E("DD02B-3", "dd-02-b2", F,
  "read `pixelOffset` into the `.btm` buffer |\n",
  "read `pixelOffset` into the `.btm` buffer *(`00364380` is the `.btm` requests' completion callback, not a glyph measure, RC-27)* |\n")
E("DD02B-4", "dd-02-b2", F,
  "| leading zeros | — | — | — | pixel data, not a signature |\n\n",
  "| leading zeros | — | — | — | pixel data, not a signature |\n\n"
  + B2(" correction 2: the §3 glyph-table-slot and consumers rows above and the §4 `00364380` row carry their answers.") + "\n\n")
E("DD02B-5", "dd-02-b2", F,
  "| `00364380` / `003649A0` | glyph measure/quad push |\n",
  "| `00364380` / `003649A0` | glyph measure/quad push *(`00364380` is the `.btm` requests' completion callback, not a glyph measure, RC-27)* |\n")
F = P + "lst-menuquest-list.md"
E("DD02B-6", "dd-02-b2", F,
  "| `+0x08` dataOff | — | — | — | no field-level reader isolated |\n"
  "| `+0x0E` dirCount | — | — | — | no field-level reader isolated |\n"
  "| dir `questId`/`dataRel` | quest-list row lookup (screen family) | — | — | exact reader not isolated |\n\n",
  "| `+0x08` dataOff | — | — | — | no field-level reader isolated *(since read: `0037EFC0` reads it as a u16 at `0037F02A`, RC-31)* |\n"
  "| `+0x0E` dirCount | — | — | — | no field-level reader isolated *(since read: `0037EFC0` `0037EFD9` and `0037E5B0`, RC-31)* |\n"
  "| dir `questId`/`dataRel` | quest-list row lookup (screen family) | — | — | exact reader not isolated *(since read: `0037EFC0` compares `+0` and takes `+2` (`0037F01C`); `0037E5B0` takes the `+4` byte's low nibble, RC-31)* |\n\n"
  + B2(" correction 3: the three Inert cells above carry their answers.") + "\n\n")
F = P + "mg-worldmap-mesh.md"
E("DD02B-7", "dd-02-b2", F,
  "| `+0x04..+0x10` offsets | mesh binder (presumed) | — | — | field-level reader not isolated |\n"
  "| `+0x24` nameCount | — | — | — | no reader found |\n"
  "| name slots | texture-source binder | — | — | the `mainN.psd` → `w_mainN.tm2` mapping is inferred, not traced |\n\n",
  "| `+0x04..+0x10` offsets | mesh binder (presumed) | — | — | field-level reader not isolated *(superseded: the header is a two-entry `{offset, size}` sub-mesh directory read by `00274780`, RC-32)* |\n"
  "| `+0x24` nameCount | — | — | — | no reader found *(superseded: file `+0x24` is sub-mesh 0's slot count, read by `005556A0` at `00555808`, RC-32)* |\n"
  "| name slots | texture-source binder | — | — | the `mainN.psd` → `w_mainN.tm2` mapping is inferred, not traced *(since traced: `00563110` matches the slot names against `00D23270`; `mainN.psd` → `w_mainN`, RC-34)* |\n\n"
  + B2(" correction 4: the three rows above carry their answers.") + "\n\n")
F = P + "lmap-menumap-location-graph.md"
LM = ("*(Superseded 2026-09-30: the field meanings are read in §10 and in §3's rebuilt table; the page is DOCUMENTED.)* "
      + B2(" correction 5"))
l38 = "**Status is `PARTIAL` and deliberately so.**"
E("DD02B-8", "dd-02-b2", F, l38 + " The container", S(l38) + " " + LM + " The container", [l38])
l242 = "The status stays `PARTIAL` because most entry fields are still shapes."
E("DD02B-9", "dd-02-b2", F, "rows above.)* " + l242 + "\n", "rows above.)* " + S(l242) + " " + LM + "\n", [l242])
F = P + "cmap-menumap-common-sublocation-directory.md"
E("DD02B-10", "dd-02-b2", F,
  "- The `+2` auxId and sec2's value semantics stay unbound; both are reported measured.\n\n",
  "- The `+2` auxId and sec2's value semantics stay unbound; both are reported measured.\n\n"
  "## What this document does not claim (SWE2-STRUCT for OPUS)\n\n"
  + B2(" correction 6. These are declared limits, not open register rows; the status-line wording that names them is "
       "proposed for OPUS in [swe2struct-awn-wave-b-1001](../../_index/candidates/swe2struct-awn-wave-b-1001/README.md).") + "\n\n"
  "- **The entry `+2` auxId** (§2.1, §5): measured (-1 in 45 entries; 81 / 82 / 265 at entries 8 / 10 / 47), not bound\n"
  "  to a meaning.\n"
  "- **Section 2's value semantics** (§2.2, §5): the 369 values and their indexing source are read; what the threshold\n"
  "  means is not bound.\n"
  "- **The corpus figures** on this page come from the session-scratch decoder `Tools/work/DATA/menumap/decode_menumap.py`,\n"
  "  which is untracked. SWE2-AUDIT-SPEC's tracked\n"
  "  [cmap_corpus.py](../../_index/candidates/auditspec-review-dd-02-b2-0930/cmap_corpus.py) reproduces this page's\n"
  "  figures from all nine shipped copies without it; that is a review re-derivation, not the page's own tool.\n\n")
F = P + "wmap-menumap-world-map-graph.md"
E("DD02B-11", "dd-02-b2", F,
  "- The `+8` aux i16 (`-1`, twice otherwise) and the `B2` sub-table remain unbound; both are\n  stated as measured, not named.\n\n",
  "- The `+8` aux i16 (`-1`, twice otherwise) and the `B2` sub-table remain unbound; both are\n  stated as measured, not named.\n\n"
  "## What this document does not claim (SWE2-STRUCT for OPUS)\n\n"
  + B2(" correction 6. These are declared limits, not open register rows; the status-line wording that names them is "
       "proposed for OPUS in [swe2struct-awn-wave-b-1001](../../_index/candidates/swe2struct-awn-wave-b-1001/README.md).") + "\n\n"
  "- **The area record's `+8` aux i16** (§2.2, §7): -1 in 37 of 39 records, 10 at record 13 and 1450 at record 37; not\n"
  "  named.\n"
  "- **The `B2` sub-table** (§2.2, the 39 × 8-byte table after the area records, §7): measured, not bound.\n"
  "- **The corpus figures** on this page come from the session-scratch decoder `Tools/work/DATA/menumap/decode_menumap.py`\n"
  "  (full dump `decode_menumap.out.txt`), which is untracked. No tracked tool re-derives this page's figures.\n\n")
F = C + "opus-dd-restatus-02-0930/batch2.md"
E("DD02B-12", "dd-02-b2", F,
  "| `cmap-menumap-common-sublocation-directory.md` | re-status (layout and loader read; nothing carried as open) | READY |\n"
  "| `wmap-menumap-world-map-graph.md` | re-status (the same) | READY |\n",
  "| `cmap-menumap-common-sublocation-directory.md` | re-status (layout and loader read; ~~nothing carried as open~~ the entry `+2` auxId and section 2's value semantics are declared unbound limits) | READY |\n"
  "| `wmap-menumap-world-map-graph.md` | re-status (~~the same~~ layout and loader read; the area `+8` aux i16 and the `B2` sub-table are declared unbound limits) | READY |\n",
  ["nothing carried as open", "the same"])
E("DD02B-13", "dd-02-b2", F,
  "refreshed.\n",
  "refreshed.\n\n"
  "*(" + note_c("dd-02-b2", ": corrections 1-6 are applied on the pages (as7, btm, lst and mg stale rows annotated; lmap's "
  "two PARTIAL sentences marked; a \"What this document does not claim\" section on cmap and wmap). The cmap / wmap "
  "status-line wording is a status-line edit and is proposed for OPUS in "
  "[swe2struct-awn-wave-b-1001](../swe2struct-awn-wave-b-1001/README.md). The optional source-block-mover front-matter "
  "items are not applied.)*") + "\n")
