# A resource-prefix result does not validate the full text span — ASTRA (SOL)

Question: does original selector `0019A5B0` independently guarantee the entire
counted UTF-16 string fits the resource? **No.** Method A settles this precise
source predicate; another guest or live run is unnecessary for that conclusion.

Retained159B is checked against the exact shipping executable and immutable82
source/manifest. The original end-pointer calculation, word accesses, branch
targets and returned register are validated by their instruction bytes. The
reviewed access-role adapter runs in the actual checker, with store/LEA/RMW
controls. Required Python/decoder provider identity is checked, not just recorded.

After successful resource API calls, the source checks `current < end`, reads the
selected u16 count and returns its prefix pointer if the count is nonzero. It does
not test `current + 2 + 2*count <= end`. Under supplied successful API state,
id`0x7837` selects entry7; seven preceding empty strings put its prefix at byte14:

| Declared bytes | Selected count | Conditional source result |
|---:|---:|---|
| 18 | 1 | Returns prefix14; text ends18 and fits. |
| 16 | 1 | Returns prefix14; text ends18 and does not fit. |
| 15 | Unread complete word | Attempts bytes14–15; physical read outcome unestablished. |
| 16 | 0 | Returns null. |

These are **source calculations**, not four native/guest tests or observed game
states. The incomplete-prefix case establishes an attempted two-byte read after
the pointer check, not successful registration, read, fault or return. Windows
acceptance of malformed resource data is unestablished; an external resource-
validity invariant might exclude these inputs in normal execution. Shipped82's
nine text blocks remain valid and are not recaptured or reclassified.

The finding refutes a **selector-alone** full-text-span postcondition. Consumers
should specify a conditional nonempty borrowed length-prefix result and keep full
resource validity as an explicit precondition. A returned pointer is not `text+2`,
an owned allocation, a portable default, or a lifetime guarantee. It does not
establish native callbacks, initialized modules/language, visible messages,
real malformed-game reachability or EXP-127's failure cause.

Raw cases and exact parent/source identity live in `raw.json`; normalized
calculations live in `result.json`. Default capture checks retained inputs without
recapture. Three alternatives reject invented full-span validation, text-pointer
return and automatic null for the incomplete word. Producer controls are separate
from OPUS/FABLE consumption and independent SPEC acceptance. A pending-publication
parent view at capture stays explicit after its later commit.

FABLE owns native resource/error prose; OPUS owns pointer/span preconditions;
DATA/SPEC incorporation and review remain separate. PC OFF, no native game/API
execution or save/config/reference writes. S19 remains parked with its spent
allowance and unapproved extension. Full L1+L2 goal remains NOT_MET.
