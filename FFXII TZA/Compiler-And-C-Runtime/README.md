[Home](../../README.md) / Compiler and C runtime

# Compiler and C runtime

Code the compiler and the C runtime library add to the executable.

Jump to: [Program start-up and memory](#program-start-up-and-memory) · [Library and generated code](#library-and-generated-code)

## Program start-up and memory

How the executable is set up, starts and ends, manages memory and objects, and handles failures.

| Page | Kind | What it helps you understand |
|---|---|---|
| [Exception handling](exception-handling.md) | Explanation | How the executable's C++ exception tables and funclets work. |
| [Image hardening](image-hardening.md) | Explanation | The executable's load address, DEP, Control Flow Guard and stack cookies. |
| [Lazy statics and one-time initialisation](lazy-statics-and-one-time-init.md) | Explanation | How thread-safe local statics are guarded and released. |
| [Memory and allocation](memory-and-allocation.md) | Explanation | The heap, the game's allocation wrappers and the subsystem allocators. |
| [Object construction and destruction](object-construction-and-destruction.md) | Explanation | How vtables are installed and objects destroyed and freed. |
| [Runtime services](runtime-services.md) | Explanation | What the game asks Windows and the C runtime for, including crash dumps. |
| [Static initialisation and teardown](static-initialisation-and-teardown.md) | Explanation | The start-up order, initialiser tables, atexit registration and the quit path. |

## Library and generated code

Code the compiler and its libraries put in the executable, and how to recognise it.

| Page | Kind | What it helps you understand |
|---|---|---|
| [Maths library](maths-library.md) | Explanation | The maths imports, inline SSE maths and floating-point setup. |
| [MSVC containers](msvc-containers.md) | Explanation | The std::map, std::string and std::regex code in the executable. |
| [Thunks and import stubs](thunks-and-import-stubs.md) | Explanation | Jump forwarders, tail calls and import stubs, and the import table. |
| [Generated function families](generated-function-families.md) | Reference table | The small compiler-generated function bodies and how to recognise each form. |
