# Counted resource prefix versus text-span postcondition — ASTRA SOL

Exact remaining question from82: does a successful original selector0019A5B0
guarantee the whole counted UTF16 string fits SizeofResource, or only that its
current prefix pointer is before the end? This changes OPUS resource-pointer
postconditions and FABLE native resource/error-path prose. Separate from82's
embedded valid text and from unproved live module/language/lifetime behavior.

Choose A retained original159B and exact source accesses/branches. A controlled
counterexample can distinguish the postconditions without running the game or
mock APIs. The source is decisive for whether a full text-span check exists.
B is not automatically needed to repeat that settled branch. Actual physical
fault behavior, Windows callbacks and runtime allocation would require a different
prepared discriminator, not inferred from these logical spans.

Conditional controls under LoadResource/LockResource/SizeofResource success:
id7837 selects7; seven prior zero-length records put its prefix at byte14.
size18/count1 fullfit; size16/count1 prefixfits but two textbytes do not;
size15 permits p14<end15 but wordprefix requires byte15 outside logical span;
size16/count0 emptyresult. Keep incomplete-prefix read outcome unknown, do not
invent a successful word or native crash. Input/API states are hypotheses, not
shipping malformed resources or real initialized modules.

Pin exact82 immutable manifest/input/code/reader/adapter/tool/source parents.
Validate code/control identity, distinguish conditional source calculations from
execution, reject stronger fullspan/nulltermination assumptions with targeted
controls, preserve raw/reducer/status/consumer scope and independently reviewed
acceptance. No new generalharness/broadexport/nativecall/live/setup, no nine-string
recapture. Read82 trap/tool lessons before any later original-code test.
PC OFF/S19 spent+extensionunapproved/fullL1+L2 NOT_MET.
