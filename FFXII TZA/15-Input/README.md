# Input

**Engine category.** Pad arbitration, the configurable DecideButton, modal state, and the shared gameplay capability/inhibition policy.

| | |
|---|---|
| Classification source | PrimaryOwner: Input |
| Functions | 1,047 |
| Status | see [`../_index/COVERAGE.md`](../_index/COVERAGE.md) |

## Systems in this category

- [`how-a-gamepad-becomes-a-controller-object.md`](how-a-gamepad-becomes-a-controller-object.md) - **DOCUMENTED, tier 1.** DirectInput enumeration, the three controller kinds the engine's log lines name (Steam, XInput, DirectInput) and their precedence, hot-plug, and the Steam Input action names
- [`Gameplay-Capability-Policy/capability-inhibition-policy.md`](Gameplay-Capability-Policy/capability-inhibition-policy.md) - the 16x32-bit policy that decides which player operations are currently allowed
- [`Input-Stack/input-stack-device-channel-and-bindings.md`](Input-Stack/input-stack-device-channel-and-bindings.md) - the device, the sixteen-frame channel history and the per-frame control frame
- [`Binding-Profiles/binding-profiles-remapping-and-control-state.md`](Binding-Profiles/binding-profiles-remapping-and-control-state.md) - authoring, publication and translation of a binding; [`CONTRACT`](Binding-Profiles/CONTRACT-binding-profiles.md), [`keymap.ini`](Binding-Profiles/keymap-ini-file-format-and-default-controls.md)
- [`Input-Name-Registry/the-input-name-registry-and-channel-aliases.md`](Input-Name-Registry/the-input-name-registry-and-channel-aliases.md) - channel aliases and the name registration; [`CONTRACT`](Input-Name-Registry/CONTRACT-input-name-registry.md)
- [`Modal-Toggles/r2-force-fight-toggle.md`](Modal-Toggles/r2-force-fight-toggle.md) - one modal toggle read end to end
- [`CONTRACT-input-subsystem.md`](CONTRACT-input-subsystem.md) - **subsystem scope (FABLE, 2026-09-21)**: the published frame snapshot the three operations share, the frame ordering that touches it, and the six cross-operation invariants the narrower contracts leave unstated

## How to add a system here

1. Copy [`../_templates/SYSTEM.md`](../_templates/SYSTEM.md) into a descriptively-named
   subfolder (or as a `.md` file if it is a single mechanism).
2. Fill all eight sections. A missing section means `STUB` or `PARTIAL`, never `DOCUMENTED`.
3. Mirror every "What is not known" entry into
   [`../_index/OPEN-QUESTIONS.md`](../_index/OPEN-QUESTIONS.md).
4. Register any cross-subsystem chain in
   [`../_index/CALL-CHAINS.md`](../_index/CALL-CHAINS.md).
5. Obey [`../_index/EVIDENCE-STANDARD.md`](../_index/EVIDENCE-STANDARD.md).
   No banned evidence class, ever.
