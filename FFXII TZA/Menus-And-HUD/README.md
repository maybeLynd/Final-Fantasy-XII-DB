[Home](../../README.md) / Menus and HUD

# Menus and HUD

The menus, the battle HUD, text and number display.

Jump to: [How menus work](#how-menus-work) · [Menu screens](#menu-screens) · [Battle HUD](#battle-hud) · [Fonts and text drawing](#fonts-and-text-drawing) · [Game text tables](#game-text-tables) · [Dialogue](#dialogue)

## Start here

Start with these pages, in this order:

1. [Opening the main menu](opening-the-main-menu.md): the whole path from a request to the main menu on screen.
2. [Menus](menus.md): how every menu is requested and routed, and what refuses a request.
3. [Widgets](widgets.md): the object every menu is built from.
4. [Widget messages](widget-messages.md): the messages that drive those objects.
5. [Menu lists](menu-lists.md): the shared scroll list behind most menus.
6. [Confirm windows](dialogs.md): the shared confirm window and the boxes beside it.
7. [Message windows](message-windows.md): how a script's message window opens, steps and closes.

## How menus work

How a menu is requested and opened, the objects it is built from and the messages that drive them. Every menu screen uses these parts.

| Page | Kind | What it helps you understand |
|---|---|---|
| [Opening the main menu](opening-the-main-menu.md) | Walkthrough | Every step from pressing Triangle to the main menu on screen, and back. |
| [Menus](menus.md) | Explanation | How a menu is requested and routed, and what can refuse it. |
| [Widgets](widgets.md) | Explanation | The object every menu element is built from. |
| [Widget messages](widget-messages.md) | Reference table | Every message a menu element answers, and who sends it. |
| [Menu lists](menu-lists.md) | Explanation | The scroll list behind most menus: rows, cursor and scrolling. |
| [Confirm windows](dialogs.md) | Explanation | The yes-or-no window, notices, the item sort and three single-screen boxes. |
| [Message windows](message-windows.md) | Explanation | How a script opens, steps and closes a message window. |
| [Menu sprites](menu-sprites.md) | Explanation | The shared picture atlases, the hand cursor, arrows and marks. |
| [Screen layouts](screen-layouts.md) | Format | The layout files that place the parts of each screen. |
| [Menu screen reference](menu-screens.md) | Reference table | Every menu screen's code and resources, including the Status and Equip panels. |

## Menu screens

The screens a player opens, from the main menu's entries to the shops and the staff roll. Some pages cover several screens, and some describe what those screens share.

| Page | Kind | What it helps you understand |
|---|---|---|
| [Equipping an item](../Items-Equipment-Shops-And-Licenses/equipping-an-item.md) | Walkthrough | What happens when a piece is put on. |
| [Clan Primer](clan-primer.md) | Explanation | The Hunts, Bestiary, Sky Pirate's Den and Traveler's Tips pages. |
| [Config screen](config-screen.md) | Explanation | Every Config, Graphics and Controls option and what changing it does. |
| [Equip screen](../Items-Equipment-Shops-And-Licenses/equipment.md#the-equip-screen) | Explanation | The five slots, the list of pieces and the stat rows. |
| [Equipment](../Items-Equipment-Shops-And-Licenses/equipment.md) | Explanation | The equipment system behind the Equip screen. |
| [Gambits screen](gambit-screen.md) | Explanation | Editing the three gambit sets on screen. |
| [Inventory screen](inventory-screen.md) | Explanation | The item tabs and rows, the help line and moving an item. |
| [License Board screen](license-board-screen.md) | Explanation | The board grid, the square states, preview and obtaining a license. |
| [Map screens](map-screens.md) | Explanation | The World Map, the location map, the overlay and the minimap. |
| [Party marks](party-marks.md) | Explanation | The marks for who cannot wear an item or has learned an ability. |
| [Pause when the window loses focus](pause-screen.md) | Explanation | The overlay and hold while the game window is in the background. |
| [Pausing with Start](../Controls-And-Input/action-availability.md#the-start-button) | Explanation | What changes in menu availability while the Start screen is open. |
| [Shop screens](shop-screens.md) | Explanation | Buy, Sell and Bazaar, the price paid and how a trade completes. |
| [Staff roll](staff-roll.md) | Explanation | The ending credits and how the roll is laid out. |
| [Status and Equip screen](status-and-equip-screen.md) | Explanation | The Status and Equip screens: their panes, their buttons and where the numbers come from. |
| [Clan Primer entries](clan-primer-entries.md) | Reference table | Every Traveler's Tips and Bestiary entry, and how it unlocks. |
| [Equip stat panel](menu-screens.md#the-equip-screens-stat-panel) | Reference table | The panel comparing a piece with what is worn. |
| [Status screen](menu-screens.md#the-member-record-panel) | Reference table | The member panel shown under Status and Equip. |

## Battle HUD

What is drawn over a battle: the command menu, the party list, the numbers and the names.

| Page | Kind | What it helps you understand |
|---|---|---|
| [Enemy names on screen](enemy-names-on-screen.md) | Walkthrough | How an enemy's name reaches the screen. |
| [Battle menu](battle-menu.md) | Explanation | The command lists, the party HP and MP list, the help line and the gauges. |
| [Battle numbers](battle-numbers.md) | Explanation | The damage, healing and status words that rise over units. |
| [HUD](hud.md) | Explanation | The target lines, the target ring, the selection marker and the HUD manager. |
| [Party list](party-list.md) | Explanation | Member rows, the rolling HP and MP numbers, the action (ATB) bar and the status mark. |
| [Script gauges](script-gauges.md) | Explanation | The counter and timer gauge an event opens. |

## Fonts and text drawing

How a string becomes glyphs on the screen, then the font data.

| Page | Kind | What it helps you understand |
|---|---|---|
| [Text drawing](text-drawing.md) | Explanation | How a line of menu text becomes glyphs on screen. |
| [Fonts](fonts.md) | Format | Which font files each language uses and how glyphs are laid out. |
| [Font expansion lists](fonts-expansion-lists.md) | Reference table | Every expansion list of every font. |
| [Font files](fonts-files.md) | Reference table | Every shipped font file. |
| [Font glyphs](fonts-glyphs.md) | Reference table | Every glyph of every font. |
| [Font kerning pairs](fonts-kerning.md) | Reference table | Every kerning pair of every font. |
| [Text codes](text-codes.md) | Reference table | The codes inside strings: formatting, names, icons and choices. |

## Game text tables

The game's shipped strings in all languages, and the codes those strings contain.

| Page | Kind | What it helps you understand |
|---|---|---|
| [Area table text](text-area-tables.md) | Reference table | The text blocks of the enemy definition tables in the area files. |
| [Clan Primer text](text-handbook.md) | Reference table | Bestiary and Traveler's Tips text in all nine languages. |
| [Control script messages](text-control-messages.md) | Reference table | The debug menu text beside the four control scripts. |
| [NPC name strings](text-npc-names.md) | Reference table | Field characters' names in all nine languages. |
| [String tables](text-string-tables.md) | Reference table | Menu, help and battle message strings in all nine languages. |
| [Text codes](text-codes.md) | Reference table | The codes inside strings: formatting, names, icons and choices. |
| [Unrequested handbook text](text-handbook-unrequested.md) | Reference table | The story, world, person and knowledge books no Clan Primer page opens. |
| [Word bank](text-word-bank.md) | Reference table | Ability, item and other name strings, with plurals and articles. |

## Dialogue

Every line and caption of the game's scripts in all nine languages: by region, with recurring scenes and script groups on their own.

### Archades

| Page | Kind | What it helps you understand |
|---|---|---|
| [Archades dialogue](archades-dialogue.md) | Reference table | Spoken lines and field captions of the Archades scripts, in all nine languages. |
| [Cerobi Steppe dialogue](cerobi-steppe-dialogue.md) | Reference table | Spoken lines and field captions of the Cerobi Steppe scripts, in all nine languages. |
| [Draklor Laboratory dialogue](draklor-laboratory-dialogue.md) | Reference table | Spoken lines and field captions of the Draklor Laboratory scripts, in all nine languages. |
| [Old Archades dialogue](old-archades-dialogue.md) | Reference table | Spoken lines and field captions of the Old Archades scripts, in all nine languages. |

### Balfonheim, Ridorana and the Bahamut

| Page | Kind | What it helps you understand |
|---|---|---|
| [Balfonheim Port dialogue](balfonheim-port-dialogue.md) | Reference table | Spoken lines and field captions of the Balfonheim Port scripts, in all nine languages. |
| [Pharos - First Ascent dialogue](pharos-first-ascent-dialogue.md) | Reference table | Spoken lines and field captions of the Pharos - First Ascent scripts, in all nine languages. |
| [Pharos - Third Ascent dialogue](pharos-third-ascent-dialogue.md) | Reference table | Spoken lines and field captions of the Pharos - Third Ascent scripts, in all nine languages. |
| [Ridorana Cataract dialogue](ridorana-cataract-dialogue.md) | Reference table | Spoken lines and field captions of the Ridorana Cataract scripts, in all nine languages. |
| [Sky Fortress Bahamut dialogue](sky-fortress-bahamut-dialogue.md) | Reference table | Spoken lines and field captions of the Sky Fortress Bahamut scripts, in all nine languages. |

### Bhujerba and the Leviathan

| Page | Kind | What it helps you understand |
|---|---|---|
| [Bhujerba dialogue](bhujerba-dialogue.md) | Reference table | Spoken lines and field captions of the Bhujerba scripts, in all nine languages. |
| [Dreadnought Leviathan dialogue](dreadnought-leviathan-dialogue.md) | Reference table | Spoken lines and field captions of the Dreadnought Leviathan scripts, in all nine languages. |
| [Lhusu Mines dialogue](lhusu-mines-dialogue.md) | Reference table | Spoken lines and field captions of the Lhusu Mines scripts, in all nine languages. |

### Dalmasca desert

| Page | Kind | What it helps you understand |
|---|---|---|
| [Dalmasca Estersand dialogue](dalmasca-estersand-dialogue.md) | Reference table | Spoken lines and field captions of the Dalmasca Estersand scripts, in all nine languages. |
| [Dalmasca Westersand dialogue](dalmasca-westersand-dialogue.md) | Reference table | Spoken lines and field captions of the Dalmasca Westersand scripts, in all nine languages. |
| [Nam-Yensa Sandsea dialogue](nam-yensa-sandsea-dialogue.md) | Reference table | Spoken lines and field captions of the Nam-Yensa Sandsea scripts, in all nine languages. |
| [Ogir-Yensa Sandsea dialogue](ogir-yensa-sandsea-dialogue.md) | Reference table | Spoken lines and field captions of the Ogir-Yensa Sandsea scripts, in all nine languages. |
| [Tomb of Raithwall dialogue](tomb-of-raithwall-dialogue.md) | Reference table | Spoken lines and field captions of the Tomb of Raithwall scripts, in all nine languages. |
| [Zertinan Caverns dialogue](zertinan-caverns-dialogue.md) | Reference table | Spoken lines and field captions of the Zertinan Caverns scripts, in all nine languages. |

### Developer and test maps

| Page | Kind | What it helps you understand |
|---|---|---|
| [Developer dialogue](developer-dialogue.md) | Reference table | Spoken lines and field captions of the Developer scripts, in all nine languages. |

### Feywood and Giruvegan

| Page | Kind | What it helps you understand |
|---|---|---|
| [Feywood dialogue](feywood-dialogue.md) | Reference table | Spoken lines and field captions of the Feywood scripts, in all nine languages. |
| [Giruvegan dialogue](giruvegan-dialogue.md) | Reference table | Spoken lines and field captions of the Giruvegan scripts, in all nine languages. |

### Nabreus Deadlands and the Necrohol

| Page | Kind | What it helps you understand |
|---|---|---|
| [Nabreus Deadlands dialogue](nabreus-deadlands-dialogue.md) | Reference table | Spoken lines and field captions of the Nabreus Deadlands scripts, in all nine languages. |
| [Necrohol of Nabudis dialogue](necrohol-of-nabudis-dialogue.md) | Reference table | Spoken lines and field captions of the Necrohol of Nabudis scripts, in all nine languages. |

### Nalbina and the Mosphoran Highwaste

| Page | Kind | What it helps you understand |
|---|---|---|
| [Barheim Passage dialogue](barheim-passage-dialogue.md) | Reference table | Spoken lines and field captions of the Barheim Passage scripts, in all nine languages. |
| [Mosphoran Highwaste dialogue](mosphoran-highwaste-dialogue.md) | Reference table | Spoken lines and field captions of the Mosphoran Highwaste scripts, in all nine languages. |
| [Nalbina Dungeons dialogue](nalbina-dungeons-dialogue.md) | Reference table | Spoken lines and field captions of the Nalbina Dungeons scripts, in all nine languages. |
| [Nalbina Fortress dialogue](nalbina-fortress-dialogue.md) | Reference table | Spoken lines and field captions of the Nalbina Fortress scripts, in all nine languages. |
| [Nalbina Town dialogue](nalbina-town-dialogue.md) | Reference table | Spoken lines and field captions of the Nalbina Town scripts, in all nine languages. |

### Opening, ending and Trial Mode

| Page | Kind | What it helps you understand |
|---|---|---|
| [Ending message dialogue](ending-message-dialogue.md) | Reference table | Spoken lines and field captions of the Ending message scripts, in all nine languages. |
| [Trial Mode dialogue](trial-mode-dialogue.md) | Reference table | Spoken lines and field captions of the Trial Mode scripts, in all nine languages. |
| [Tutorial and staff roll dialogue](tutorials-dialogue.md) | Reference table | Spoken lines and field captions of the Tutorial and staff roll scripts, in all nine languages. |

### Ozmone Plain and Golmore Jungle

| Page | Kind | What it helps you understand |
|---|---|---|
| [Eruyt Village dialogue](eruyt-village-dialogue.md) | Reference table | Spoken lines and field captions of the Eruyt Village scripts, in all nine languages. |
| [Golmore Jungle dialogue](golmore-jungle-dialogue.md) | Reference table | Spoken lines and field captions of the Golmore Jungle scripts, in all nine languages. |
| [Henne Mines dialogue](henne-mines-dialogue.md) | Reference table | Spoken lines and field captions of the Henne Mines scripts, in all nine languages. |
| [Jahara dialogue](jahara-dialogue.md) | Reference table | Spoken lines and field captions of the Jahara scripts, in all nine languages. |
| [Ozmone Plain dialogue](ozmone-plain-dialogue.md) | Reference table | Spoken lines and field captions of the Ozmone Plain scripts, in all nine languages. |

### Paramina Rift and Mt Bur-Omisace

| Page | Kind | What it helps you understand |
|---|---|---|
| [Mt Bur-Omisace dialogue](mt-bur-omisace-dialogue.md) | Reference table | Spoken lines and field captions of the Mt Bur-Omisace scripts, in all nine languages. |
| [Paramina Rift dialogue](paramina-rift-dialogue.md) | Reference table | Spoken lines and field captions of the Paramina Rift scripts, in all nine languages. |
| [Stilshrine of Miriam dialogue](stilshrine-of-miriam-dialogue.md) | Reference table | Spoken lines and field captions of the Stilshrine of Miriam scripts, in all nine languages. |

### Rabanastre and Giza Plains

| Page | Kind | What it helps you understand |
|---|---|---|
| [Garamsythe Waterway dialogue](garamsythe-waterway-dialogue.md) | Reference table | Spoken lines and field captions of the Garamsythe Waterway scripts, in all nine languages. |
| [Giza Plains dialogue](giza-plains-dialogue.md) | Reference table | Spoken lines and field captions of the Giza Plains scripts, in all nine languages. |
| [Lowtown dialogue](lowtown-dialogue.md) | Reference table | Spoken lines and field captions of the Lowtown scripts, in all nine languages. |
| [Rabanastre dialogue](rabanastre-dialogue.md) | Reference table | Spoken lines and field captions of the Rabanastre scripts, in all nine languages. |
| [Royal Palace dialogue](royal-palace-dialogue.md) | Reference table | Spoken lines and field captions of the Royal Palace scripts, in all nine languages. |

### Salikawood, Phon Coast and Tchita Uplands

| Page | Kind | What it helps you understand |
|---|---|---|
| [Phon Coast dialogue](phon-coast-dialogue.md) | Reference table | Spoken lines and field captions of the Phon Coast scripts, in all nine languages. |
| [Salikawood dialogue](salikawood-dialogue.md) | Reference table | Spoken lines and field captions of the Salikawood scripts, in all nine languages. |
| [Sochen Cave Palace dialogue](sochen-cave-palace-dialogue.md) | Reference table | Spoken lines and field captions of the Sochen Cave Palace scripts, in all nine languages. |
| [Tchita Uplands dialogue](tchita-uplands-dialogue.md) | Reference table | Spoken lines and field captions of the Tchita Uplands scripts, in all nine languages. |

### Scenes that recur through the story

| Page | Kind | What it helps you understand |
|---|---|---|
| [Aerodrome airship dialogue](aerodrome-airship-dialogue.md) | Reference table | Spoken lines and field captions of the Aerodrome airship scripts, in all nine languages. |
| [Skyferry dialogue](skyferry-dialogue.md) | Reference table | Spoken lines and field captions of the Skyferry scripts, in all nine languages. |
| [Strahl dialogue](strahl-dialogue.md) | Reference table | Spoken lines and field captions of the Strahl scripts, in all nine languages. |
| [Summon dialogue](summons-dialogue.md) | Reference table | Spoken lines and field captions of the Summon scripts, in all nine languages. |
| [Title screen and location title dialogue](titles-dialogue.md) | Reference table | Spoken lines and field captions of the Title screen and location title scripts, in all nine languages. |
