[Home](../../README.md) / Game files and data tables

# Game files and data tables

How game files are found, loaded and read: archives, file tables, the battle and game data tables and the image formats.

Jump to: [Archives and file loading](#archives-and-file-loading) · [Loaded resources](#loaded-resources) · [Data tables and configs](#data-tables-and-configs) · [Image files](#image-files) · [Menu and map files](#menu-and-map-files)

## Start here

Start with these pages, in this order:

1. [Bigfile archive](bigfile-archive.md): starts with the big archive
2. [File path resolution](file-path-resolution.md): shows how a name finds its bytes
3. [File requests and the read queue](file-requests-and-the-read-queue.md): follows one request
4. [Resource lifecycle](resource-lifecycle.md): follows the block once it arrives

## Archives and file loading

How the game finds a file by name or id and reads it from the archive or the cache.

| Page | Kind | What it helps you understand |
|---|---|---|
| [Bigfile archive](bigfile-archive.md) | Explanation | The VBF container, how its index loads and how a read reaches a file. |
| [File path resolution](file-path-resolution.md) | Explanation | How a file name becomes bytes through the cache or the archive. |
| [File requests and the read queue](file-requests-and-the-read-queue.md) | Explanation | How a load is queued, sized, read in parts and completed. |
| [Asynchronous load manager](async-load-manager.md) | Explanation | The loading thread, its request records and its load kinds. |
| [File size tables](file-size-tables-fst.md) | Format | The per-language table that sizes every file by kind and id. |
| [PKFL packages](pkfl-packages.md) | Format | How an area's motion, sound and voice packages are laid out and read. |
| [Prefetch and asset-header manifests](prefetch-manifests.md) | Format | The lists that preload files into the cache and name a model's parts. |
| [Asset paths](asset-paths.md) | Reference table | Every file the game asks for by resource kind and id. |

## Loaded resources

What happens to a block once loaded: where it lives, who owns it and how its sections are found.

| Page | Kind | What it helps you understand |
|---|---|---|
| [Resource lifecycle](resource-lifecycle.md) | Lifecycle | A loaded block from its request to the free. |
| [Resource arenas and relocation](resource-arena-and-relocation.md) | Explanation | The memory arenas, block headers, handles and how blocks move. |
| [Resource ownership and disposal](resource-ownership-and-disposal.md) | Explanation | Who owns a loaded source, copy or borrow and how each is released. |
| [Resource sections](resource-sections.md) | Explanation | How a section inside a loaded resource is found by tag and name. |

## Data tables and configs

The file formats that hold the game's authored numbers, text and settings.

| Page | Kind | What it helps you understand |
|---|---|---|
| [Authored data tables](authored-data-tables.md) | Explanation | The registry holding the battle tables, area tables and license boards. |
| [Authored expressions](authored-expressions.md) | Explanation | The value records in effect data, their operands, curves and operators. |
| [Area battle data (.ard and .nmb)](ard-area-battle-data.md) | Format | The per-area file of enemy definitions, stat rows and order sets. |
| [Battle and menu text tables](battle-text-tables.md) | Format | The word banks and string tables, and how a text id becomes a string. |
| [Character sound tables (chse)](character-se-tables-chse.md) | Format | The per-model table naming the sounds a model's animations play from. |
| [Small .bin tables](small-bin-tables.md) | Format | Small tables for footsteps, vibration, window sizes, button legends and more. |
| [Standard file formats](standard-file-formats.md) | Format | The common file types the game ships and which of them it reads. |
| [JSON configs](json-configs.md) | Reference table | Every key of the JSON documents, the code reading it and what it sets. |
| [PS2-era .bin families](ps2data-bin-families.md) | Reference table | Every .bin file family from the PS2 data and what it holds. |

## Image files

The picture and palette formats the game loads.

| Page | Kind | What it helps you understand |
|---|---|---|
| [Bin_menu images](binmenu-images.md) | Format | The headerless guest portraits and area icons pasted into menu pictures. |
| [ExFont sheets (.btm)](btm-exfont-bitmaps.md) | Format | The glyph sheets of the staff-roll faces and how a glyph finds its cell. |
| [Location-map colour tables (.cl2)](cl2-menu-colour-tables.md) | Format | The palettes some location maps draw with. |
| [Menu graphics containers (.as7)](as7-menu-graphics.md) | Format | The compressed archives behind item pictures and character silhouettes. |
| [Texture animation lists](texture-animation-lists-ta.md) | Format | The lists of a map texture's animation frames and what drives them. |
| [TIM2 images](tim2-images.md) | Format | The PS2-era picture format and how the game reads one. |

## Menu and map files

The files behind menus, the location map and the World Map.

| Page | Kind | What it helps you understand |
|---|---|---|
| [Handbook files](handbook-files.md) | Format | The files behind Clan Primer entries and what each field shows. |
| [Map menu files](menu-map-files.md) | Format | The picture files and tables behind the location map and World Map. |
| [Menu resource packages (.mrp)](mrp-menu-resource-packages.md) | Format | The menu layout files, who loads each and how a request is served. |
| [Quest menu files](quest-menu-files.md) | Format | The quest list, petitioner strings and detail tables, and what each field shows. |
| [UI typed lists](ui-typed-lists.md) | Format | The authored item lists menus are composed from and where their sprites come from. |
| [World map mesh (.mg)](world-map-mesh-mg.md) | Format | The World Map geometry file and how the map screen draws it. |
