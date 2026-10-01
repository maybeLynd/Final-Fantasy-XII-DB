# OV21 bank capacity and failure discriminator

Bounded target ASTRA-OV21-BANK-CAPACITY-DOMAIN-1001; existing OV21 owner ASTRA.
Canonical consumers: FABLE external-source owner and OPUS resource ownership.

Question: what capacity does the original render-root bank initializer actually
publish, can its reset produce capacity zero through an overlapping qword store,
and does registration failure alone distinguish full capacity from no backing
page? Competing explanations: zero-capacity fixture models ordinary completed
boot; boot sets a positive fixed capacity and zero instead belongs to pre-init,
reset or other history. Also distinguish 51FBB0's immediate used>=capacity
failure from its 51F7A0-null failure. A probe at40A1CC alone cannot name the path.

Method A first. Validated identities: 41E580 reads root+D90 and tail-calls
409FE0; 41E3A0 sets D90=root and passes saved arg2 into409F10. Located boot
caller33263C supplies10. Wrapper409F10 fixes element stride50 and shift5;
51F9F0 publishes low32(10<<5)=320 at+54. Reset51FB70 qword+50 covers+54,
so a starts-only +54 writer census is insufficient. Do not assert natural
initialized lifetime from a constructor call tag or negate all exhaustion.

Reuse existing reviewed capture/annotation/CFG helpers. Capture only bounded
boot/wrapper/constructor/reset/allocator/thunk bodies, verify exact original
bytes and Windows ABI carriers. Acceptance: guarded source-dataflow result,
failure-path distinction and valid boundary controls. Required inherited
unknowns: actual completed startup, backing allocation, other roots/writers,
owner/key cardinality, metadata consistency, callback timing and teardown.
No arbitrary zero-bank fixture promoted to gameplay proof.

No live/PC/process/save/config/reference changes. All helpers finite; focused
prerequisite and coherent-byte mutation controls only. Route qualified proof
and improved observation discriminator, preserve existing captures/results.
