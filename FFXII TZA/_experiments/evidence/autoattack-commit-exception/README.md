# Automatic engagement's cancellation-mode exception

Method A, exact shipping EXE73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8.
No game/native/forcedcall/emulator execution. Independent acceptance pending.

For a player: this checks the ordinary Attack inserted by automatic engagement.
It distinguishes that Attack from a different special action replacing a Summon.
No gameplay fault or naturally reached stale slot was observed.

Original312FA0 calls30EFF0 at31307B; if it returnsnonzero the originalstraightline
leg setsR8D=96hex (150) andstackfiftharg=0, then calls30F760 at3130DC. There
are no intervening calls/branches or laterR8/fiftharg writes. UnderWindowsx64ABI,
callerRSP+20 becomes calleeentryRSP+28; callee's fivepushes plusSUB32bytes move
it to postprologueRSP+70. Thus thiscaller deliberately disablescancellation.

30F760 zeroextendsR8W to EDI beforecheckingfiftharg, skips3105D0 onzero, and its
ordinaryallowedID leg storesDI atunit714 andphase0. Normalcallee/nonvolatileRDI,
validframe/initializedsameunit andnoninterference premises are explicit. This
is local originalcode/dataflow; the30EFF0 tag is not proof of nativeeffects.

The retainedUS actiontable's row150 hasbit30clear. Reused original304850
currentrow/carrier and304F3D/F45 bit30 guard therefore send thisstill150 action
to ordinary30FE10, skipping306760, if the registeredrowmatchesretainedbytes.
Thisknownmode0caller cannot itself choosearbitraryrow275/Dismiss. Lateraction
replacement, restore paths, actual tablebinding and scheduling remainopen.

Correction: earlierworking8b deliverynotes/maincheckpoint could implyallknown
commits usemode1. That wording is false;30FA00 recommit uses1 butthiscaller0.
correction.json names affectednotices/checkpoint andrequiredconsumerchange.
Publishedc40/8b proofs didnot dependonallmode1; retainoriginals, no rewrite or
unnecessaryrerun. OPUS/FABLE mustconsumethisadditive qualification afterreview.

Actual controls: positivecapture/proof andthreeCLI refusals failedcapture,
missingsource, coherent same-size mode0->1 mutation refusedoriginalEXEbytes.
A bit/constantcountermodel is not a nativeexecution test. Immutablefrozen case
inputs inheritidenticalbasehashes, retainchangedoverlays andactualrawreceipts.
Reproduceprove.py fromrepo rootwithfreshoutput. Forcontrols useadisposablecopy
ofbaseinputs/positive evidence, omittinggenerated controls/result/status outputs.
Nevereditpublishedinputs. Allownchildren terminal/noPC/game/state/save/config/
reference orpeer processchanges; no restoration operation needed.

Notproved: full30EFF0/suspendedslot lifetime/nativecallbackeffects/fullrestore,
allotherdirect/indirectcallers orarbitraryforcedmode0, naturalcurrentrowidentity,
actualresultingstatstype, integratedparity orwholeOV21/42 closure.
