# Steam and achievements

The Steam integration and the achievements.

| Page | What you will find |
|---|---|
| [Achievements: the achievement list, the counters and conditions that award each one, and how an award reaches Steam](achievements.md) | The 41 achievement records with their developer tags and Steam titles, the 30 descriptors that give each tracked achievement a counter or a test, the saved counter block and award bits, the menuhandbook.bin targets and lists the tests read, the code that feeds every counter, the periodic sweep and its re-send, the script and scene awards, the path from an award to SetAchievement and StoreStats, and the Sky Pirate's Den statues that show the awards. |
| [Steam integration: how the game starts and pumps Steam, the interfaces and callbacks it uses, and what it does without Steam](steam-integration.md) | The start-up order (interface context, SteamAPI_Init, the achievement manager, the overlay listener, the relaunch check with app id 595520), the interface context and the five interface slots the game calls, the eight callbacks and their handlers, the per-window-pump SteamAPI_RunCallbacks, the stats receipt, the Steam language and user id the game reads, the teardown, and every path that changes when Steam is absent. |
