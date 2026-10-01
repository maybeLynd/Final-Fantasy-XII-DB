# Widget roots, attachment and completion at the restore boundary

ASTRA, 2026-09-13. [Spawn page section19](../../../05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md#19-native-widget-roots-and-completion--astra-2026-09-13).
Player version: the UI really does allocate parent objects; the database's
permanently-empty-parent claim missed a loop. The load and area controllers
can join the same parent, so one is not automatically destroyed with the other.
Sorting and separate completion gates still matter for saved enemy-state order.

Method A only:18 newly collected whole bodies plus3 reused bodies, exact
EXE73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8,
preferred base00120000, Capstone5.0.7. No B/live run and no PC controls.
Reused EXP069 establishes the generic factory caller only; its stub factory
never established the real hierarchy. Existing constructor campaigns not rerun.

247AE0 initializes RDI=208EA20 and RBP=3, calls2465F0 for C8-byte roots with
handler2445D0, storesRBX at[RDI], advancesRDI8 and repeats. The second write
is208EA28.250540 walks and dereferences those same three slots.248220 actually
dereferencesRCX and links the supplied child. This refutes the widget contract's
permanent-null and always-ignored-parent claim using its own cited loop,
without asserting observed live allocation, full initialization or reachability.

247950(self,0) clearsflag1 and attaches a parentless widget to*(208EA28), or
delegates existing-parent state to247870; it does not close it.280140 init
and27FB70 init use this path.583930 constructs582860, size5A0, normalizing
two boolean inputs. The load handler attaches through244960 only on message16,
at582A14, after resource calls; raw dispatch table recovered and verified.
The separately named583260 constructs57E4D0, size178: a write-operation object.

244980 performs optional child sorting via2479B0, then246C20. Completion in
the latter sends19 for a positive signed2-bit direction or20 for a negative
one, before244980 rechecks lowstate1 andflag6 to enter245020. Callback changes
remain consequential.248700 is a different two-message readiness widget,
not the general exit-animation driver.249CE0's sort implementation, native
easing, callbacks and other resource callees are not executed here.

check.py compares all21 selected bodies to shipping bytes, checks loop/index,
positive root-store/read, attachment and completion anchors, and revalidates
the load handler's original jump table. It also reads915120 as message25.
The first checker guessed17 and failed before producing a passing result;
control-correction.json preserves that error and actual bytes. Corrected
assertion passes; no invalid run or guessed constant counts as evidence.

Manifest maps original source serialization to canonical LF copies. Scripts
retain scratch paths for reproduction in a private directory with the same
reference and ledger. Peer-owned root/types/contracts/sort and UI prose need
independent review and propagation. Actual initialized hierarchy, load/area
message18 chronology, native banks/field/timer sequencing, L12/L13 and full
L1/L2 reviews remain open; no integrated parity or final audit is claimed.
