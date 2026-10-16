# Characters and objects

The records behind every character, enemy and object in an area, and how they are created, identified and removed.

| Page | What you will find |
|---|---|
| [NPC names: the npcdic.bin name pairs, the actor's name id, and the story flag that swaps a name](npc-names.md) | How a field character's name tag is chosen: the name id every actor carries, the pair of strings that id selects in npcdic.bin, the persistent flag with the same number that switches to the second string once the player has talked to that character, the two script verbs that assign a name id, and the shipped dictionaries for the nine languages. |
| [Party member status record: the snapshot the menus and HUD read a party member through, field by field](party-member-status-record.md) | The 192-byte record that the status screen, the party menu, the licence board, the save screen and the HUD read a party member from: who builds it, from which fields of the party stats record, its battle unit and its party row, every field it carries with its source, the flag word that says whether the member is KO'd, engaged, idle, selected or out of range, the experience curve behind the points to the next level, and which screen reads which field. |
