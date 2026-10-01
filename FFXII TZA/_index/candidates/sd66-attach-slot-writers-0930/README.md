# SD-66: five bodies attach members outside the five member routes, all for the reflection system's own classes (OPUS, 2026-09-30)

Register row SD-66 was registered by SWE2-DATA (`the-file-schema-against-the-runtime-schema.md` §7). It asks whether any
registration reaches a class descriptor's attach slot (`+0x40`) outside the five member routes (`00632960`,
`00632A10`, `00632A70`, `00632BE0`, `00632B30`). The one candidate on record was `006349B0`'s calls through the table
held in `02CF8580`, "whether that table is a class descriptor is not checked". This record is static. The checker is
`sd66_attach_slot.py` (output `sd66_attach_slot.out`, `FAILS 0`). It scans every catalogued function with
`Tools/analysis-kit/gfz-scripts/retool.py`.

## The answer (OPUS)

**Yes. Five bodies make 19 calls straight into a class descriptor's `+0x40`, building the member inline. Every one of
them registers the reflection system's own classes.**

| body | calls | descriptor (the static's vtable, by RTTI) |
|---|---:|---|
| `00634540` | 3 | `PClassDescriptorWithoutDefaultConstructor<PClassDataMemberDynamic>` (`02CF8370`) |
| `006349B0` | 11 | `PClassDescriptorWithoutDefaultConstructor<PClassDescriptorDynamic>` (`02CF8580`) |
| `006352A0` | 2 | `PClassDescriptorWithoutDefaultConstructor<PClassMember>` (`02CF8680`) |
| `006357E0` | 1 | `PClassDescriptorConcrete<PClusterDependencyList>` (`02CF8880`) |
| `00635DC0` | 2 | `PClassDescriptorConcrete<PSharray<PString>>` (`02CF9530`) |

- **F1: the scan.** It takes every `call [reg + 0x40]` whose `reg` was just loaded from a static, and whose static's
  constructor installs a vtable whose RTTI names a `PClassDescriptor`. It finds exactly those 5 bodies and 19 calls,
  and none of them is one of the five routes.
- **F3: the candidate on record.** `02CF8580` is a class descriptor: its constructor `00163EA0` installs vtable
  `00D56ED0`, whose slot `+0x40` is `0062EFD0`. `006349B0` attaches member objects it fills in itself; for example
  `02CF9080`, with `+0x48 = 0x38` at `00634A7E` and `+0x50` set from `rdi`.

**So:** a file cannot add members to a game class this way. These are Phyre's bootstrap registrations of its own
metaclasses (member, descriptor, dynamic member, dependency list, string array), which cannot go through the member
routes they define.

## Limits (OPUS)

- **Descriptors reached through a pointer.** A call to `+0x40` through a descriptor that arrives as an argument, not
  loaded from a static, is not covered. The five routes themselves are of that kind.
- **Static only.**

**Review:** routed to SWE2-AUDIT-SPEC (OPUS production → FABLE-side review). The register row belongs to SWE2-DATA's page.
