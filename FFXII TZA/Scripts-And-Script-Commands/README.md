# Scripts and script commands

How area and event scripts run: the script virtual machine, its instructions, and every native command a script can call.

| Page | What you will find |
|---|---|
| [Script interpreter: the hundred opcodes, the value stack, the registers and how a script waits and resumes](script-interpreter.md) | The bytecode interpreter 0025E4C0 that runs every zone script: who calls it each frame, the 100-entry opcode dispatch and the two coupled tables that drive it, the shared value stack at 02099AC0, the per-actor registers, the wait slot that lets a native call suspend and resume at the same instruction, the instruction budget and the stop rule, and what each of the hundred opcodes does, with the full table in script-interpreter-opcodes.tsv. |
| [Script variables: the six storage classes behind PUSHV and POPV, where each lives and how long it lasts](script-variables.md) | How a zone script's variables are resolved: the descriptor word with its class, width, float bit and offset, the resolver 00262440 that turns it into an address in one of six homes (the save payload, the script image, the actor's local area, the image's msp area and the two 512-byte scratch banks), array indexing with its clamp, the width-saturating store, the reference form PUSHP hands to native verbs, and which bank survives a save, an area change or a script unload; with the corpus census in the companion tables. |
