[Home](../../README.md) / Graphics

# Graphics

Rendering, cameras, models, effects, lighting and the screen.

Jump to: [Character models](#character-models) · [Visual effects](#visual-effects) · [Screen effects and movies](#screen-effects-and-movies) · [Cameras](#cameras) · [Render pipeline](#render-pipeline)

## Start here

Start with these pages, in this order:

1. [Model files (.cm, .ca)](model-files-cm-ca.md): starts with what is on disk
2. [Model lifecycle](model-lifecycle.md): follows one model once bound
3. [Animation playback](animation-playback.md): shows how it is animated
4. [Character render records](character-render-records.md): shows the record the draw reads
5. [CharacterRenderObject](character-render-object.md): draws that record

## Character models

How a character's model files load, animate, light and draw.

### Animation And Motion

| Page | Kind | What it helps you understand |
|---|---|---|
| [Animation playback](animation-playback.md) | Explanation | The animation player, track pairing by bone and the sampler. |
| [Authored presentation commands](authored-presentation-commands.md) | Explanation | The presentation command handlers and their ramp channels. |
| [Model oscillators and the pose sequencer](model-oscillators-and-pose-sequencer.md) | Explanation | Procedural per-model motion and the pose sequencer. |
| [Presentation entries](presentation-entries.md) | Explanation | How a presentation entry picks its track and the choice selectors. |
| [Skeleton entries and bones](skeleton-entries-and-bones.md) | Explanation | The skeleton entries of render records and their listed bones. |

### Character Rendering

| Page | Kind | What it helps you understand |
|---|---|---|
| [Character render records](character-render-records.md) | Explanation | The render record array, its pool, parents and attachment. |
| [CharacterRenderObject](character-render-object.md) | Explanation | The per-character draw object, its model instances and shader bindings. |
| [Character fades](character-fades.md) | Explanation | The character fade channels, their owners and the coast-down latch. |
| [Character rig and look](character-rig-and-look.md) | Explanation | The procedural controllers, the staged look command and the focus point. |
| [Character status visuals](character-status-visuals.md) | Explanation | How a status changes a character's colour, light, opacity and shadow. |
| [How a character is lit](character-lighting-and-shadows.md) | Explanation | The light inputs, shadow casters and shadow pool of a character. |

### Model Files

| Page | Kind | What it helps you understand |
|---|---|---|
| [Model files (.cm, .ca)](model-files-cm-ca.md) | Format | The model file container and each entry type it holds. |
| [Model lifecycle](model-lifecycle.md) | Lifecycle | A character model from its binding to the render record's clear. |
| [Add-motion tables](add-motion-tables.md) | Format | The add-motion, skeleton mapping and high-model replacement tables. |
| [Model effects and motion commands](model-effects-and-motion-commands.md) | Format | The effect and motion entries stored inside a model. |
| [Model asset list](model-asset-list.md) | Reference table | Every model the game can bind, with its files and motion lanes. |
| [Weapon bones](weapon-bones.md) | Reference table | Each weapon model's keyed points, blade, grip and special bones. |

## Visual effects

The effect files, how they run and draw, and how characters and menus use them.

### Effect Elements And Drawing

| Page | Kind | What it helps you understand |
|---|---|---|
| [Bone trails](bone-trails.md) | Explanation | The ribbon trails drawn behind weapon bones. |
| [Effect anchors and targets](effect-anchors-and-targets.md) | Explanation | The target and anchor queries that place an effect. |
| [Effect drawing](effect-drawing.md) | Explanation | The display layers, drawing a group and an element, and soft particles. |
| [Effect element runtime](effect-element-runtime.md) | Explanation | Effect instances, emitters and elements, and their per-step update. |
| [Effect element types](effect-element-types.md) | Explanation | The handlers of each element type and what the types draw or change. |
| [Position to scalar](position-to-scalar.md) | Explanation | The distance fade colour of effect elements. |

### Effect Files

| Page | Kind | What it helps you understand |
|---|---|---|
| [Effect file loading](effect-file-loading.md) | Explanation | The battle effect slots and how files are filed, shared and released. |
| [Effect files (.efx, .efb)](effect-files-efx-efb.md) | Format | The effect containers, their chunk streams and the map effect bank. |
| [Effect file list](effect-file-list.md) | Reference table | Every effect file the game requests, and what asks for it. |
| [Effect lifecycle](effect-lifecycle.md) | Lifecycle | From the request naming an effect to its release, and what an area change ends. |

### Effects On Characters And Menus

| Page | Kind | What it helps you understand |
|---|---|---|
| [Character effects](character-effects.md) | Explanation | The ticket and handle tables behind effects on characters. |
| [Effects on actors and scripts](effects-on-actors-and-scripts.md) | Explanation | Numbered effects on actors and the script effect slots. |
| [Menu effects](menu-effects.md) | Explanation | The registry menu screens use to spawn, place and remove effects. |

## Screen effects and movies

What is applied to the whole picture: post-processing, fades, flares, reflections and movies.

| Page | Kind | What it helps you understand |
|---|---|---|
| [Lens flares](lens-flares.md) | Explanation | The flare slots, their occlusion queries and the dimming they drive. |
| [Map cubemaps](map-cubemaps.md) | Explanation | The reflection probes and how map models pick theirs. |
| [Post-processing](post-processing.md) | Explanation | The game's post-process passes, their constants and the PPFX features. |
| [Render parameters and shader assets](render-parameters-and-shader-assets.md) | Explanation | The post-process shader files and scene-parameter documents. |
| [Screen fades](screen-fades.md) | Explanation | The fade layers, the fade verbs and the per-movie fade schedule. |
| [Screen mode and aspect](screen-mode-and-aspect.md) | Explanation | The aspect fit, the Super Wide bound and the display object. |
| [Script screen effects](script-screen-effects.md) | Explanation | Cut-in, motion blur, soft focus and the screen blur sprites. |
| [Movies](movies.md) | Format | The movie seek index and the player's states. |

## Cameras

The follow camera and the scripted camera.

| Page | Kind | What it helps you understand |
|---|---|---|
| [Field camera](field-camera.md) | Explanation | The follow camera, its stick and mouse control, and wall avoidance. |
| [Scripted camera](scripted-camera.md) | Explanation | The shot channels, the camera stack and how a camera reaches the renderer. |

## Render pipeline

The command lists, threads and low-level layers that turn a frame into draw calls.

| Page | Kind | What it helps you understand |
|---|---|---|
| [Gi render commands](gi-render-commands.md) | Explanation | The Gi command family, its arena and the D3D11 primitive renderer. |
| [Graphics thread handshake](graphics-thread-handshake.md) | Explanation | The shared command-state word and the waits around the GS batch. |
| [Legacy PS2 GS layer](legacy-ps2-gs-layer.md) | Explanation | The GS memory model, map texture slot rebuild and VU leftovers. |
| [Render command list](render-command-list.md) | Explanation | The per-frame command objects and the lists that hold them. |
| [Sprite batcher](sprite-batcher.md) | Explanation | The 2D vertex batcher and the menu quad emitters. |
