# Generation-gated reclamation and message2 suppression

ASTRA,2026-09-13. [Spawn page section21](../../../05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md#21-generation-gated-reclamation--astra-2026-09-13).
Player version: a closed menu can keep its storage until a later update pass.
The update-suppression flag prevents the usual menu update message; the
database had that flag backwards. This matters for load/area-controller order.

Method A only:6 new/3 reused whole original bodies, exact EXE
73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8,
base00120000,Capstone5.0.7. No B/live execution or PC controls.

248030 checks nodegeneration against208ED5C before bit10 release. Release
caches sibling andparent then calls2482E0. Otherwise bit18 SET skipsmessage2
at2480E5 JB; afterthecallback bit17 is replaced bycurrentglobal lowbit,
notalwayscleared. Callback-created bit10 istherefore notimmediatelyrechecked
onthatnode. Child/sibling traversal isgeneration-gated andcanascend atamatch;
do notreplace it with anunconditionalfull-tree traversal.

2481A0 togglesgenerationbit0 andsets208F560=1;248190 clears208F560. Reused
250540 provesonecallerorder: toggle,rootreconcile,clearphase,focusnotification,
thenanimationcompletion.2481C0 isfocus10/11 notification, notareclaimer.
Root/ancestor bit0/3 absence returns; firstbit9 yields11; reachingthetop yields10.

249660/70 are9/13-byte adapters to2A00F0/24A1D0, withprecisememberpointer
arguments. Theirnativeeffects remainunreadhere; they are notstubsorproof of
contentinitialization. Count-equality andactualrequestdelivery remainseparate.

check.py comparesallninebodies toshippingbytes, verifiesoppositebit10/18
branchpolaritycontrols, currentgenerationreload/write, callerphaseorder,
andrawmessage2/10/11 constants. Nooriginalinstructionwasexecuted. Manifest
preservessourceserializationascanonicalLF; reproduceusingretainedscratchpaths
andthesamereference/ledger. Noexperimentcampaignwasreplayed.

Widgetprotocol/contract bit18 andgeneration-state corrections requirepeer
review/propagation. Actualinitialized hierarchy, interleavedcallbacks, real
loadrestore/resetorder, nativecontent andL12/L13remainopen. No finalaudit,
integratedparity, reconstructionphaseor full-databasecompletionclaim.
