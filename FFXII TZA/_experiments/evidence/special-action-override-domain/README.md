# Conditional native special-action override domain

Question: what initialized values and state invariant does the original override
supply, and can those values produce candidate action511..534? Method A: original
constructor/control/initializer source, width effect and finite-state induction.
No new FF12/native execution, process, controls, saves/config or archive census.

Original1CCB20 stores QWORD2710 at object+ADC (1CCC06), so its high DWORD+AE0
is zero at that instruction. Original console arm1D2DD3..1D2DFA, under state0..8,
saturates left/right inside0..8 and calls setter2F7A00 with new value minus1.
That gives global01EEBAF0 index-1..7. Initializer2F79E0 copies eight original
u16 words241,231,234,237,229,228,227,226 fromD0F9E0 to022BE930. Under unchanged
array and the stated object/state premises none can be511..534. Original
file-backed indexFFFFFFFF is only a file value, not live state.

Limits matter: pairing the constructor/control with a valid same object and
no intervening/alias writes is a premise. This is not complete writer closure
or initialized process lifetime proof. Initial corruption9 stays9 and produces
index8: this arm is not an arbitrary-state sanitizer. Direct first-section
caller discovery (1D03DC init,1D2DFA setter) is bounded, not an indirect census.
Calls, resource binding and other action-id producers remain separate. External
EXP190 replay corroborates an initializer under its disclosed stubs; its runs
are not ASTRA executions and do not establish omitted effects.

Reproduce prove-special-override-domain.py FRESH_JSON from repo root with the
project Python and certified image73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8.
Actual capture invocation hashes, original spans/instructions and reviewed
store/LEA/read-modify-write controls are required. The qword width must cover
AE0; narrower constructor or wider control bound source witnesses are refused.
Finite transitions and eight constants are static deductions, not execution
samples. Independent SPEC derivation and FABLE/OPUS canonical adoption required.
Next cheapest discriminator: actual field/array/global-index alias/write/lifetime
closure and other action selectors, not another identical sample or game setup.
Whole OV42 remains OPEN.
