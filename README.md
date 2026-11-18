# Final Fantasy XII: The Zodiac Age - how the game works

A guide to the inside of the PC release of *Final Fantasy XII: The Zodiac Age*: how its battles, gambits, enemies,
items, story and other systems work, what its data files hold, and which part of the game's program does each thing.
Everything here comes from reading the game's own program and files.

You do not need to be a programmer to use it. Explanation pages start with what you see as a player and then show
how the game makes it happen.

## Where to start

- **Pick a topic** from the list below. Each topic has a contents page that sorts its pages into groups.
- **Start from something you noticed in the game.** The [phenomenon index](FFXII%20TZA/phenomenon-index.tsv) is a
  searchable table: find what you saw or heard, and it gives the cause and the page that explains it.
- **Look up game data** such as item stats, enemy lists or shop prices on the *Reference table* pages. Each comes
  with the same data as a `.tsv` file you can open in a spreadsheet.
- **Look up a name or an address from the game's program** in the [symbol index](FFXII%20TZA/symbol-index.tsv), which
  gives the page that explains it.

Each page has a Home / topic / page trail at the top to find your way back.

## Topics

### The game

- [World, areas and travel](FFXII%20TZA/World-Areas-And-Travel/README.md) - Areas and zone changes, the per-area map information table, weather, save crystals, teleports, chocobos and airships.
- [Characters and objects](FFXII%20TZA/Characters-And-Objects/README.md) - The records behind every character, enemy and object in an area, and how they are created, identified and removed.
- [Enemy spawning](FFXII%20TZA/Enemy-Spawning/README.md) - When and where enemies appear, respawn and are removed.
- [Movement and pathfinding](FFXII%20TZA/Movement-And-Pathfinding/README.md) - How characters and enemies move, turn, follow, avoid obstacles and find paths.
- [Battle actions](FFXII%20TZA/Battle-Actions/README.md) - How an attack, spell, technick or item use is chosen, charged, targeted and carried out.
- [Damage and battle formulas](FFXII%20TZA/Damage-And-Battle-Formulas/README.md) - Damage, healing, hit, evade and other battle calculations.
- [Enemy AI and gambits](FFXII%20TZA/Enemy-AI-And-Gambits/README.md) - How enemies choose what to do, and how the party's gambits are evaluated.
- [Status effects and KO](FFXII%20TZA/Status-Effects-And-KO/README.md) - Status ailments and buffs, their timers and periodic effects, what ends them, and KO.
- [Party](FFXII%20TZA/Party/README.md) - Party members, the leader, guests, swapping members in and out, and party formation.
- [Items, equipment, shops and licenses](FFXII%20TZA/Items-Equipment-Shops-And-Licenses/README.md) - The inventory, equipment and its stats, shops and prices, and the license board.
- [Rewards: EXP, LP, gil and loot](FFXII%20TZA/Rewards-EXP-Gil-And-Loot/README.md) - What a defeated enemy gives: EXP, LP and gil, loot drops and pickups, the kill chain, levelling up and the gil cap.
- [Story, events and hunts](FFXII%20TZA/Story-Events-And-Hunts/README.md) - Story progress, event scenes, side quests and hunts.
- [Controls and input](FFXII%20TZA/Controls-And-Input/README.md) - Controller, keyboard and mouse input and how it reaches the game.
- [Menus and HUD](FFXII%20TZA/Menus-And-HUD/README.md) - The menus, the battle HUD, text and number display.
- [Graphics](FFXII%20TZA/Graphics/README.md) - Rendering, cameras, models, effects, lighting and the screen.
- [Sound and music](FFXII%20TZA/Sound-And-Music/README.md) - Sound effects, music and voice playback.
- [Saving, loading and settings](FFXII%20TZA/Saving-Loading-And-Settings/README.md) - Save files, loading, the game options and language selection.
- [Steam and achievements](FFXII%20TZA/Steam-And-Achievements/README.md) - The Steam integration and the achievements.
- [Random numbers](FFXII%20TZA/Random-Numbers/README.md) - Every random number generator in the game, how each is seeded and which rolls use it.

### The program and its files

For modders and programmers: how the program is put together and the formats of its files.

- [Engine core](FFXII%20TZA/Engine-Core/README.md) - The main loop and per-frame update, startup and the values set at boot, the developer tuning console, logging, the object model and the engine's shared state.
- [Scripts and script commands](FFXII%20TZA/Scripts-And-Script-Commands/README.md) - How area and event scripts run: the script virtual machine, its instructions, and every native command a script can call.
- [Game files and data tables](FFXII%20TZA/Game-Files-And-Data-Tables/README.md) - How game files are found, loaded and read: archives, file tables, the battle and game data tables and the image formats.
- [PhyreEngine](FFXII%20TZA/PhyreEngine/README.md) - The PhyreEngine middleware the PC release is built on.
- [Third-party libraries](FFXII%20TZA/Third-Party-Libraries/README.md) - Libraries compiled into the executable.
- [Compiler and C runtime](FFXII%20TZA/Compiler-And-C-Runtime/README.md) - Code the compiler and the C runtime library add to the executable.
- [EBP script files](FFXII%20TZA/EBP-Script-Files/README.md) - The format of the .ebp files that hold area and event scripts.
- [PKFL package files](FFXII%20TZA/PKFL-Package-Files/README.md) - The format of the PKFL package files.

## Kinds of page

- **Explanation**: how a part of the game works.
- **Walkthrough**: one thing the game does, step by step, in the order it happens.
- **Format**: what one kind of game file holds.
- **Reference table**: a list of game values, with the same data as a `.tsv` file.

## For modders and programmers

Pages name parts of the program by their address, such as `0x0022A580`. [Reading the database](reading-guide.md)
explains the addresses and names, the tables of reads and writes, and the columns of both indexes.
