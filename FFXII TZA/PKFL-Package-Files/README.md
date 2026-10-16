# PKFL package files

The format of the PKFL package files.

| Page | What you will find |
|---|---|
| [PKFL packages: the per-area .mot, .snd, .vpc and .vpcjp containers, their offset and size directory, and the slot readers](pkfl-packages.md) | The PKFL container every area's motion, sound and voice package uses: an 8-byte header and a directory of offset and size pairs, payloads on `800`<sub>h</sub> boundaries; how the area loader reads each package's directory into a fixed table, the seven slot readers and their callers, how a slot's payload is requested, the 10,314 shipped packages and what their slots hold, and the rules a package must follow. |
