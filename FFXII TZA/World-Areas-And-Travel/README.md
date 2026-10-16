# World, areas and travel

Areas and zone changes, the per-area map information table, weather, save crystals, teleports, chocobos and airships.

| Page | What you will find |
|---|---|
| [Area flags: the navimapdata.bin record for every area, the town flag, the KO, Stone and X-Zone override and the other bits](area-flags-navimapdata.md) | The 3-byte per-area record shipped in navimapdata.bin: which areas count as towns, the bit that lets a KO'd, Stoned or X-Zoned character stay in play, the MP regime, the Map entry, the area-name flag, the party hold flag and the default leader, the seven accessor functions that read them, the two save-data overrides and the shipped census. |
| [Zone changes: mapjump and the other jump verbs, the loading flags, the moment the new zone is ready and what names a map](zone-changes-and-mapjump.md) | From the script line mapjump(map, entrance, mode) to the frame the new zone runs: the verb's wait and request, the transition record in the save data, the fade, the tick that tears the old zone down and starts the load, the pending-load and busy masks, the ready point, the scene loader, the jump-index verbs, the jump lock and the field id's file table. |
