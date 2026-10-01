# Navigation-grid constructor — exact budget and quantization

Question: the current NavGridParams type prose refines to max(w/trunc(w/c),
h/trunc(h/c)), then "nudges it by an epsilon"; the unit-definition page states
cell budget2800h/(n+1), omitting the prefix. The corridor contract labels070 as
cell size. Does original construction instead subtract the36-byte working mask,
floor the refinement and add exactly1, and is070 actually an origin?

Also qualify the type constructor's "no-op if383740 returns zero": the original
bitsetBytes=36 store precedes the rectangle getter and its admission guard.
Competing explanations are no write on missing root versus that one partial reset.

Consumers: OPUS NavGridParams type/field explanations and corridor contract;
FABLE unit-definition grid builder paragraph. Already-correct vestigial stack-copy
fields and unexamined allocation release remain unchanged; no bulk navigation RE.

Method A: exact complete607B builder,252B rectangle getter,10B encoded-reference
decoder; shipping import thunk/IAT/name identity for sqrtf and floorf, and shipping
constant1.0 read at both addition/subtraction sites. Derive RIP field bindings
before normalisation. Original instructions establish control/data flow; qualified
import names establish intended library operations, not observed native DLL effects.
No new B/live run is required to distinguish the stated formulas or guard order.

Controls/illustrations: square100x100 isolates floor omission (refined6.25 becomes
7, not7.25); rectangle336x320 isolates275 versus276 initial budget at the ratio
boundary (grid240 versus256 cells under otherwise stated corrected quantization).
Both admit positive integer dimensions expressible by byte tile size/count fields.
Examples are A arithmetic illustrations, assuming intended standard math and f32
round-to-nearest; not original execution/captured allocation/shipped-map occurrence.

Accept: precise source formula and global bindings, full body/RET coverage, actual
library-name bindings and constant bytes, unambiguous early store before null-root
exit; explicit limits and owner/independent routing. Stop on identity/extent/import
or operand ambiguity. No exceptional-float/zero-dimension/budget exhaustive campaign.

Cleanup: read-only image/artifacts, PC OFF. No game/native/input/save/config/reference
changes. Existing live permission and persistent spent S19 setup budget unchanged.
Goal remains accepted whole L1+L2/required reviews and final audit, not a report.
