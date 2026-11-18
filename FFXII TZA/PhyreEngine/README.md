[Home](../../README.md) / PhyreEngine

# PhyreEngine

The PhyreEngine middleware the PC release is built on.

Jump to: [Engine framework](#engine-framework) · [Drawing and shaders](#drawing-and-shaders) · [Asset files and animation](#asset-files-and-animation)

## Start here

Start with these pages, in this order:

1. [PhyreEngine application framework](phyre-application.md): starts with the process
2. [Phyre frame](the-frame.md): follows one frame to the screen
3. [Phyre mesh-instance draws](phyre-mesh-instance-draws.md): shows how one mesh is drawn
4. [Shader variant selection](shader-variant-selection.md): picks the shader for that draw

## Engine framework

The engine's application frame, modules, containers, reflection, threads and script bindings.

| Page | Kind | What it helps you understand |
|---|---|---|
| [PhyreEngine application framework](phyre-application.md) | Explanation | How the game process starts, runs its frames and shuts down. |
| [Phyre arrays](phyre-arrays.md) | Explanation | The PArray and PSharray containers and their ownership bit. |
| [Phyre entities and components](phyre-entities-and-components.md) | Explanation | PEntity, its component list and the hooks on loaded components. |
| [Phyre reflection](phyre-reflection.md) | Explanation | How the engine describes classes at run time and creates instances. |
| [Phyre thread pool](phyre-thread-pool.md) | Explanation | The engine's worker-thread pool and its job batches. |
| [PhyreEngine Lua bindings](phyre-lua-bindings.md) | Explanation | How engine objects cross to and from Lua. |
| [PhyreEngine modules](phyre-modules.md) | Explanation | The engine libraries linked in and how they start and stop. |

## Drawing and shaders

How the engine draws a frame: its device, shaders, meshes, post effects, text and camera maths.

| Page | Kind | What it helps you understand |
|---|---|---|
| [Phyre frame](the-frame.md) | Explanation | From the frame tick to the drawn picture. |
| [Phyre mesh-instance draws](phyre-mesh-instance-draws.md) | Explanation | The segment loop, bone palette and per-draw parameter blocks. |
| [Shader variant selection](shader-variant-selection.md) | Explanation | How a draw picks its shader variant. |
| [Phyre bitmap-font text](phyre-bitmap-font-text.md) | Explanation | How a bitmap-font string is laid out, built into quads and drawn. |
| [Phyre D3D11 device and resources](phyre-d3d11-device-and-resources.md) | Explanation | Direct3D 11 device and swap-chain creation, formats, textures and buffers. |
| [Phyre D3D11 draws, state and buffers](phyre-d3d11-draws-and-state.md) | Explanation | Draw and dispatch calls and the state translation tables. |
| [Phyre math and camera](phyre-math-and-camera.md) | Explanation | The matrix helpers, camera matrices and node and bounds transforms. |
| [Phyre modifier codes](phyre-modifier-codes.md) | Explanation | The named skinning and morph kernels and their registry. |
| [Phyre post-effect classes](phyre-post-effect-classes.md) | Explanation | The post-effect classes the game links, and the one it runs. |

## Asset files and animation

The .phyre file format and how animation curves reach bones.

| Page | Kind | What it helps you understand |
|---|---|---|
| [Animation channel binding](phyre-animation-binding.md) | Explanation | How an animation curve finds its target and becomes a bone matrix. |
| [Phyre field schema](phyre-field-schema.md) | Format | The class and member tables in every .phyre file. |
| [PhyreEngine asset files](phyre-asset-files.md) | Format | The .phyre file layout and how the loader reads and fixes it up. |
