73 Exact consumer defect: FABLE7af8e8da4 clamp() returns Python dim-1 unbounded;
its default tests pass only sampled dim3/0/-2. At signed32 dimension INT_MIN,
original LEA EAX,[RSI-1] wraps to7FFFFFFF, then signed CMOVL does not select the
nonnegative lower index. Does the advertised negative-dimension rule preserve
the original width or extrapolate a real-number formula past the boundary?

Method A sufficient: exact retained591B/originalopcode/operand identity, original
unchanged producer clamp() AST/default invocation, boundary conditional reasoning.
Calculations/model execution are NOT original FF12 instruction execution. Controls
positive3/dim0/negative-2/MIN+1 versusMIN; corrected private low32 model must differ
only requiredboundary. Existing69scientific finding intact, affected consumer's
unqualified negative rule needs producer/check/default/contract/prose correction.

FABLE/OPUS/DATA owners, SPEC audit. No assetcensus, actualMINarray, fullresolver/
nativefault/storagevalidity/live/reachability/lifetime or productoverflow claim.
Do not editpeerconsumer. PC OFF/S19spent/unapprovedextension/fullL1+L2 NOT_MET.
