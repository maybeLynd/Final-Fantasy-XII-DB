[Home](../../README.md) / EBP script files

# EBP script files

The format of the .ebp files that hold area and event scripts.

Jump to: [Script files](#script-files) · [Script sections](#script-sections) · [Debug files](#debug-files)

## Script files

The directory of a zone or event script and the image its code runs from.

| Page | Kind | What it helps you understand |
|---|---|---|
| [EBP script container](ebp-script-container.md) | Format | The section directory of every script and how each section reaches its loader. |
| [EBP script image](ebp-script-image.md) | Format | The header, actor directory and function tables a script runs from. |

## Script sections

The data sections a script can carry beside its code.

| Page | Kind | What it helps you understand |
|---|---|---|
| [Actor manifest](ebp-actor-manifest.md) | Format | The section listing the models a script's bind verbs name. |
| [EBP camera shake](ebp-camera-shake.md) | Format | The shake lists and curves that make a scripted camera tremble. |
| [EBP camera tables](ebp-camera-tables.md) | Format | The shot lists a script's camera verbs play. |
| [EBP navigation icons](ebp-navigation-icons.md) | Format | The block a map script carries for its minimap markers. |
| [EBP text sections](ebp-text-sections.md) | Format | The message and field-sign banks a script's text ids refer to. |
| [LGT2 light sets](ebp-lighting-lgt2.md) | Format | The light records of an event script and how the renderer picks them. |
| [Position entries (FF12POS3)](ebp-position-entries.md) | Format | A zone's authored points, boxes and ellipses and what reads them. |

## Debug files

Files shipped beside the control scripts.

| Page | Kind | What it helps you understand |
|---|---|---|
| [ATEL debug companions](atel-debug-companions.md) | Explanation | The debug files shipped beside the control scripts, and why they go unopened. |
