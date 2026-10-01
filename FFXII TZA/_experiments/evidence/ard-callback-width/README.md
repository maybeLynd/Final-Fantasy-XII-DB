# ARD read destination is distinct from its callback root

Method A STATIC_ONLY,825 original bytes: complete loader normal fragments,
binder and pointer tag. Producer checked, independent review/incorporation
pending. EXE SHA256
73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8,
base120000. No native/emulated/live/CRT execution or new placement sample.

3EA820 obtains a pointer from36A100, tags it through36C660 and tests fullRAX.
The normally returning tag preserves its full incoming pointer viaRBX. At
3EA971 the loader supplies that fullRAX asR8 read destination to32E620, but at
3EA976 it saves onlyEAX into DWORD descriptor+8. Descriptor+10 names3EA710.
Submission is not queue acceptance or an executed callback.

3EA710 starts MOV EBP,ECX at3EA732. That zeroextends the lowDWORD into64-bitRBP,
including inputs with bit31 set. It also MOV ECX,ECX before the tag call. No other
local assignment changes the savedRBP until AFTER3EA809 publishes it as a qword
at02B5E0C0. Under normal ABI-preserving callees, every normal execution of this
writer publishes0..FFFFFFFF. This is a writer invariant, not an all-writer census
or global lifetime guarantee. Unload zero is not evidence of successful loading.

Therefore that published-root sample cannot recover a full high allocator result.
A future observer answering GR18 must record fullRAX at3EA93E, orR8 at3EA97F,
and prove object/request/callback identity and session health. A hypothetical
high read destination and its low callback root are different storage identities
unless separate mapping evidence says otherwise. No high bits are restored here.
Actual allocator placement and normal queued reachability still need sufficient
evidence; no claim a natural high allocation or resulting fault happened.

Nor does a low root guarantee low section pointers. The binder SIGN-extends the
resolver's lowDWORD and adds it to that root in64bits. Conditional rootFFFFFF00
plus offset1000 produces100000F00. This is arithmetic under supplied values, not
shipped data or a native/live run. Whole-buffer extents, section/row identity,
reward-store truncation and actual allocation placement have separate bounds.

Retained EXP077/078 already cover initializer high-pointer retention and controlled
original allocator-link effects. EXP079 records low placement in one actual
title/loaded session. They were read, not rerun, and none gives an alltime placement
guarantee. Their reported controls/external reviews are not new tests by this package.
Do not spend runtime sampling a root whose highbits this writer already discards.

Reproduce the source proof with existing analysis Python into a fresh output:

    python <packet>/prove-ard-callback-width.py <fresh.json>

Exact original .pdata parent triples qualify both loader continuations. The
actual capture and reducer use the reviewed shared access-role adapter and
byte redecoding. Full image/range/driver identity, actual exit/output and complete
normal binder/tag control flow are checked. Three actual CLI refusals reuse the
valid positive: failed capture exit, consistently changed root-input register,
missing loader tail. Missing evidence cannot become a valid empty success.
Immutable driver/input/case/result/receipts retained; producer controls are not
independent semantic acceptance. No historical mutation campaigns rerun.

OPUS consumes the GR18/full-pointer-versus-callback-root distinction; FABLE
consumes binder parameter width and signed64-bitsection arithmetic limits. Keep
natural placement/queue/lifetime gaps open. No whole GR18/OV/AQ row closure.

Player version: battle data can be read into one address while the later binding
code uses only that address's lower32bits. Looking at the later root alone cannot
tell us where Windows/the allocator put the original buffer. We are checking that
handoff before asking for gameplay evidence.

Cleanup: finite source reads/disposable refusal copies only. No game/PC/input/
instrument/native/save/config/reference or peer-process mutation. Full goal
ACTIVE/NOT_MET; menu spent/unapproved and EXP127 invalid remain unchanged.
