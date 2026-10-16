# Engine core

The main loop and per-frame update, startup and the values fixed at boot, the developer tuning console, logging, the object model and the engine's shared state.

| Page | What you will find |
|---|---|
| [Game application object: the root object, its vtable and the boot order](game-application.md) | The root object of the running game: the static GameApplication at 01F7E350, its PhyreEngine base class and the thirty-one slot vtable it overrides, the archive mount and the window set-up the framework calls at start, the init job that builds the managers and closes the startup latch, the frame tick that drives the per-frame pump of thirteen singletons and the game step, and the pause flag and time scale the framework reads through it. |
