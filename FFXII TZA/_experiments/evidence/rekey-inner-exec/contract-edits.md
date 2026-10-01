# EXP-151 landing checklist — apply only AFTER files are in repo

## Board
1. `add` task SWE2-ORACLE-REKEY-INNER-EXEC (or claim directly if self-added)
   resources: dir:database/ffxii tza/_experiments/evidence/rekey-inner-exec
              file:database/ffxii tza/_experiments/EXP-151-rekey-inner-exec.md
              file:.../CONTRACT-battle-unit-construction.md (check conflicts first)
2. Copy files:
   - Temp\exp151_check.py  -> _experiments/evidence/rekey-inner-exec/check.py
   - (result.json regenerates)  -> run harness in place, keep result.json
   - Temp\EXP-151-rekey-inner-exec.md -> _experiments/EXP-151-rekey-inner-exec.md

## Contract edits (04-Actor-Entity/Unit-Definition/CONTRACT-battle-unit-construction.md)

### §13 — EXP-150 paragraph boundary list (line ~180)
OLD: "Remaining scripted boundaries (`003220E0`, `00313F60→77C20`,
`00308010`, `003271D0`, `003105D0`, `0023AC80`) are disclosed in
the record."
NEW: "Remaining scripted boundaries (`00313F60→77C20`, `00308010`,
`003271D0`, `003105D0`, `0023AC80`) are disclosed in the record;
`003220E0` is now executed by `EXP-151`."

### §13 — append EXP-151 paragraph after the EXP-150 block
"**`EXP-151` (NATIVE-REPLAY, `live_game: false`) executed the rekey
inner `003220E0` through `00322050` end-to-end** — id compose
`003589B0`, generation bump `002659D0` (`w[+0x16]=(w+1)&0x7FF`,
wrap→1, **no null guard**), slot-occupant search `00327150` (idx
`b[q[02EBF190]+0x5AA4] ≤ 0x27`; scans `q[0208E688]+i*0xF50` for
`q[+0x698]` == slot row), id→object resolve `003588B0` (cls-table
`02098E10`, bounds+flag+generation checks), leaves `263FF0`/
`236850`/`236820`/`263E30` — **24/24 cases, stable ×3**
**[EXP-151]**. Executed: match on the occupant's `d[+8]` == old id
always stores `d[glob+0x5AA4]` (DWORD — clobbers +0x5AA5..7) and
notifies `00326500` (scripted); `b[02089340]&0x10` gates only the
resolve — flag clear stores `0xFF` directly."

### §14 — split the unresolved bullet
OLD: "* **`003220E0` (rekey inner) and `0023AC80` (spawn-record init)
internals** remain scripted boundaries **[EXP-150]**."
NEW:
"* ~~`003220E0` (rekey inner) internals~~ — **closed by `EXP-151`**:
  executed real through `00322050`; gen bump, slot-occupant match,
  resolve flag gating, dword store + notify all proven
  **[EXP-151]**. Only `00326500` (notify dispatcher) stays scripted.
* **`0023AC80` (spawn-record init) internals** remain scripted
  **[EXP-150]** — mapped (memset 0x1C8, mode-byte dispatch to
  `02EBF120`/`02EBF130` descs, `30C470` stats header reusing
  EXP-148's `30C650`/`30FED0`, member vs foe slot fills,
  `323910`/`327CB0`/`326030`/`327DE0`) but not yet executed."

### §15 — evidence line
Append: "EXP-151's rekey-inner execution (id compose, generation
bump, occupant search, resolve chain, flag-gated store + notify) is
that record's **[EXP-151]**."

## Gates after landing
- run harness in place (writes result.json)
- check_contract_runtime --db . | EXP-151 should link
- check_questions --db . ; check_contract_runtime_links
- verify_doc_addresses if the record's address prose is checked
- board: finish REKEY-INNER-EXEC (result_refs=commit hash) →
  EXP151-PUB task → @publication → publish_paths.sh named paths →
  release → findings request to OPUS

---

# EXP-152 landing checklist — apply only AFTER files are in repo

## Board
1. add/claim SWE2-ORACLE-SPAWN-INIT-EXEC
   resources: dir:database/ffxii tza/_experiments/evidence/spawn-record-init-exec
              file:database/ffxii tza/_experiments/EXP-152-spawn-record-init-exec.md
              file:.../CONTRACT-battle-unit-construction.md
2. Copy: Temp\exp152_check.py -> evidence/spawn-record-init-exec/check.py;
   Temp\EXP-152-spawn-record-init-exec.md -> _experiments/;
   run harness in place (regenerates result.json)

## Contract edits (CONTRACT-battle-unit-construction.md)

### §13 boundary list — remove 0023AC80
OLD: "Remaining scripted boundaries (`00313F60→77C20`, `00308010`,
`003271D0`, `003105D0`, `0023AC80`) are disclosed in the record;
`003220E0` is now executed by `EXP-151`."
NEW: "Remaining scripted boundaries (`00313F60→77C20`, `00308010`,
`003271D0`, `003105D0`) are disclosed in the record; `003220E0` and
`0023AC80` are now executed by `EXP-151`/`EXP-152`."

### §13 — append EXP-152 paragraph
"**`EXP-152` (NATIVE-REPLAY, `live_game: false`) executed
`0023AC80` with the real callee layer** — stats header `0030C470`,
slot writer `0031A630` (+change-notify `30FED0(rec,0x97)`), gil clamp
`00323790`, ability-scan loop into scripted `00323910`, pair copy
`00327CB0` through real `00322C50` (0xA arm), snapshot `00326030`,
order materializer `00327DE0` — **22/22 cases, stable ×3**
**[EXP-152]**. Executed: the `0x5B10`-chain snapshot lands at
`idx*3` exactly where `327DE0` scans; fault boundaries at
`0x23ADA8`/`0x23AD7B`/`0x326057`/`0x327E27`."

### §14 — close the 23AC80 bullet
OLD: "* **`0023AC80` (spawn-record init) internals** remain scripted
  **[EXP-150]** — mapped (...) but not yet executed."
NEW: "* ~~`0023AC80` (spawn-record init) internals~~ — **closed by
  `EXP-152`**: executed real end-to-end; snapshot/order pipeline,
  slot writes, gil clamp, scan gating, fault boundaries all proven
  **[EXP-152]**. Scripted inside: `323910` grant, the
  `30F690`/`30F340`/`30F5A0` cluster, `30C650`/`30FED0` as callees."

### §15 — append
"EXP-152's spawn-init execution (memset+sentinels, mode dispatch,
stats header, slot/pair/order fills, snapshot chain) is that
record's **[EXP-152]**."

## Gates: same as EXP-151 (harness, runtime link, questions,
runtime_links AGREE).


# ============================================================
# EXP-153 — stat-cluster-exec (prepared, validated 37/37 x3)
# ============================================================
# Land AFTER EXP-152 (contract already updated by it).
# Files:
#   Temp\exp153_check.py -> evidence/stat-cluster-exec/check.py
#   Temp\EXP-153-stat-cluster-exec.md -> _experiments/
# Run check.py in evidence dir -> result.json (37/37, x3).
# Board: claim SWE2-ORACLE-STAT-CLUSTER-EXEC (new task).
#
# Contract edits (CONTRACT-battle-unit-construction.md):
# 1. In EXP-152's paragraph/scripted list: change
#    "the mutually-recursive stat cluster 0030F690/0030F340/0030F5A0
#     (pulls 00377C20/003105D0/0030E360 — separate package surface)"
#    to note they are now executed by EXP-153 (keep the EXP-152-era
#    wording but append "— executed by EXP-153").
# 2. New paragraph after EXP-152's: EXP-153 promoted
#    30F690/30F340/30F5A0/31B860/377C20-chain real; new scripted
#    30E360/300530/3243F0/300BC0/300CE0; 37/37 x3; key semantics
#    (bit0 fixup clears owner bit26 unless can-die; FED0 tail
#    unconditional; F340 flags bt0x10/0x1C -> 300530 delta; F5A0
#    two-section reconcile via 300CE0/300BC0).
# 3. Correct any "377C20 ~400 insns" wording -> 4-leaf chain
#    (2EF640->2164280, +0x200, max(d[21654C4],0), 3-byte-stride bit15).
# 4. Correct "30F340 self-recursion" wording if present -> 30F340 is
#    ~60i ending 0x30F3EB; 30F3F0/30F4B0 are the broadcast wrappers.
# 5. §15 evidence: append EXP-153 stat-cluster-exec (37/37 x3).
# Gates: check_contract_runtime, check_questions,
#   check_contract_runtime_links, verify_doc_addresses.


## EXP-154 landing plan (after EXP-153 lands)

1. Claim `PERBIT-CORE-EXEC` package (or create if absent) on TEAM.
2. Copy `Temp\exp154_check.py` -> `_experiments/exp154_check.py`;
   copy `Temp\EXP-154-per-bit-core-exec.md` ->
   `_experiments/EXP-154-per-bit-core-exec.md`.
3. Contract edits:
   - boundary list: remove 0030E360 (now executed; keep its scripted
     arm bodies 301140/312280/3299B0/300140/307D10/3284D0/30B9B0/
     30B8E0/300FC0/3112F0/2FA390/46AB10 disclosed).
   - add EXP-154 paragraph under the stat-cluster section: six-arm
     flag mutation {clear,set}x{+0x38,+0x3C,+0x64}, jt2 per-bit arm
     dispatch (bit0/1/0x1F unlink, bit2/8 b[+0xE9A], bit4 3299B0,
     bit5/1B 300140+307D10), CASCD cascade via 0x02EBF118, arg6
     notify decode, 3876D0 = b[row+9]*d[0x1DFE0B4]*0x1E.
   - evidence line: NATIVE-REPLAY 53/53 x3.
4. Re-run `_experiments/exp154_check.py` from repo before publish.
5. Gates + publish per standard flow.


## EXP-155 landing plan (after EXP-154 lands)

1. Claim `STAT-APPLY-EXEC` package (or create) on TEAM.
2. Copy `Temp\exp155_check.py` -> `_experiments/exp155_check.py`;
   `Temp\EXP-155-stat-apply-exec.md` ->
   `_experiments/EXP-155-stat-apply-exec.md`.
3. Contract edits:
   - boundary list: remove 300BC0/300CE0 (+30E060/3283D0 real);
     keep 30B770/30B7F0/28F1F0/2FA540/2FA3B0 disclosed.
   - stat section: HP apply = clamp(movsx w6 + delta, 0, cap),
     cap = deadgate(b6C/b7C) ? 0 : (b37 ? w28*b37 : w28);
     w4C apply + notify decodes (r13->3283D0, r15->28F1F0, &1
     veto skip, delta<0 hi-word re-veto), +delta cascades HP;
     30E060 fraction cache b[+0x4E], 16D6A0 = stub sink.
   - CORRECTION: 30F5A0 sec2 computed = b37 ? b37*w28 : w28.
   - evidence line: NATIVE-REPLAY 68/68 x3.
4. Re-run `_experiments/exp155_check.py` from repo before publish.
5. Gates + publish per standard flow.


## EXP-156 landing plan (after EXP-155 lands)

1. Claim `BROADCAST-WRAPPERS-EXEC` package (or create) on TEAM.
2. Copy `Temp\exp156_check.py` -> `_experiments/exp156_check.py`;
   `Temp\EXP-156-broadcast-wrappers-exec.md` ->
   `_experiments/EXP-156-broadcast-wrappers-exec.md`.
3. Contract edits:
   - broadcast section: 30F3F0 = 9 member slots via
     320AB0->31B9F0(cls3 map b[glob+slot*2+0x5A7E], 322C50/0x17
     bound 9) -> glob+8+idx*0x1C8; 30F4B0 = f3f0 + f4d0 tail;
     30F4D0 = 13 foe slots ids 0xC012..0xC01E -> 30B0E0 class-desc
     table 0x1EEBCC0 (0x58 stride, count d[row+0x3C], validator cb
     q[row+0x50]=2FD970 bitmap test on runtime q[row+8]) ->
     320A40(idx+0x1B).
   - mask = (flags&4 ? d[208D320]:0)|(flags&8 ? d[208D324]:0)|
     (flags&0x10 ? 0x544 : 0) -- 0x544 gated ON by bit4 (byte-verified;
     corrects earlier inverted read).
   - f690 null-rec guard -> unmapped slots silent.
   - boundary: cls-0xC bitmap pointer is runtime-populated; planted.
   - evidence line: NATIVE-REPLAY 77/77 x3.
4. Re-run `_experiments/exp156_check.py` from repo before publish.
5. Gates + publish per standard flow.


## EXP-157 landing plan (after EXP-156 lands)

1. Claim `STAT-APPLY-300530-EXEC` package (or create) on TEAM.
2. Copy `Temp\exp157_check.py` -> `_experiments/exp157_check.py`;
   `Temp\EXP-157-stat-apply-300530-exec.md` ->
   `_experiments/EXP-157-stat-apply-300530-exec.md`.
3. Contract edits:
   - 300530 paragraph: arg2 = DELTA onto d[rec+0x48]; floor =
     d[ownerrow+0x48]|0; cap = flag0x10000 ? max(d48,1) : d[+0x24]
     (x2 on flag0x1C); notify&1 skips 30B8E0 veto (consulted only
     when r12<=0); engaged-bit: delta>0&&old<=0 -> e360 arm0 clear,
     delta<=0&&new<=floor -> e360 arm3 set (r9=-1 resolver); else
     3299B0(owner, ~(notify>>4)&1 + 0x2005) msg.
   - note 3008A0 sibling resolver is NOT part of 300530.
   - boundary: 30B9B0/30B8E0 scripted returns.
   - evidence line: NATIVE-REPLAY 86/86 x3.
4. Re-run `_experiments/exp157_check.py` from repo before publish.
5. Gates + publish per standard flow.

## EXP-158 (id resolver 3008A0 — spawn-bitmap update + registration)

1. Copy `Temp\exp158_check.py` -> `_experiments/exp158_check.py`;
   `Temp\EXP-158-spawn-id-resolver-exec.md` ->
   `_experiments/EXP-158-spawn-id-resolver-exec.md`.
2. Contract edits:
   - 3008A0(id, delta, mode, dispatch, flag): validates
     0xFFFF/0x1000/>0xE000/oob -> -1; calls 309F30(id, dispatch)
     validator then q[row+0x48] mutator; dispatch==1 && validator<=0
     && mutator>0 -> q[0x2EBF190]+4 |= {cls3:1|tbl, cls4:0x40,
     foe<=0xC011:0x80, foe 0xC012..0xC01E:0x100}.
   - 309F30 = shared validator dispatch (mode==4 -> 2FD970 direct,
     else jmp q[row+0x50]).
   - 2FD420 = cls-C spawn-bitmap mutator: mode==0 -> old+delta else
     delta; <0 btr / >1 bts / else 0->btr nz->bts; 325F40(id,old,new)
     notify; mode==0&&flag&1 -> 46A630 -> 46AB10.
   - 325F40 = notify router gated 322C50(1,id); cls-C foes early-ret.
   - boundary: 46AB10/252E60 scripted; runtime bitmap + state cell
     planted+disclosed.
   - evidence line: NATIVE-REPLAY 102/102 x3.
3. Re-run `_experiments/exp158_check.py` from repo before publish.
4. Gates + publish per standard flow.

## EXP-159 (stat-change dispatcher 30FED0)

1. Copy `Temp\exp159_check.py` -> `_experiments/exp159_check.py`;
   `Temp\EXP-159-stat-change-dispatch-exec.md` ->
   `_experiments/EXP-159-stat-change-dispatch-exec.md`.
2. Contract edits:
   - 30FED0(rec, notify): r15 = edx|0x202. Three seed sources for a
     128-bit stack bitmap: (A) FOED desc-walk -> d[row+0x50] watch
     mask; (B) b[rec+5]==1 -> owner row b[+0xE80] array; (C) field
     snapshot XOR -> changed map rsp+0x50 / cleared map rsp+0x60.
     Then 128-iter dispatch: set bit -> 30E130(rec,i,0,notify,3);
     cleared -> 30E130(rec,i,0,notify,1). Tail 2FEF30(rec,0,0);
     member epilogue: owner d[+0xE90] bits -> 30E360 clears.
   - NO null guard on 30FED0: rcx=0 faults at 0x310080 (w[0x50]);
     f690 owns the caller-side guard.
   - boundary: 30E130/3112F0/3279B0/2F8E50/2F9180/252E60 scripted;
     member-rec 2FEF30 arm faults on unplanted state (disclosed).
   - evidence line: NATIVE-REPLAY 109/109 x3.
3. Re-run `_experiments/exp159_check.py` from repo before publish.
4. Gates + publish per standard flow.

## EXP-160 (per-bit handler 30E130)

1. Copy `Temp\exp160_check.py` -> `_experiments/exp160_check.py`;
   `Temp\EXP-160-per-bit-handler-exec.md` ->
   `_experiments/EXP-160-per-bit-handler-exec.md`.
2. Contract edits:
   - 30E130(rec,bit,arg3,notify,arm): arm {0,1,2,3} = {clr,set} x
     byte arrays {+0x68,+0x78}, edge-gated. Bound = 322C50(0x1D,bit)
     vs d[q[0x2EBF040]+4] (runtime cell). Transition work: memset
     0x148 blk, 386A50/386AE0 pair, optional 3112F0, 46A720/46A790
     pair on ~(notify>>1)&1, 3279B0 for bits 0x68..0x71, fed0
     recursion suppressed by notify bit9 (fed0 sets |0x202).
   - fed0's dispatch arms: set-map -> e130 arm3, cleared-map ->
     e130 arm1 (corrects earlier guess: 0x78 = pending-change array).
   - boundary: 384B10/3112F0/3279B0/fed0-inbound scripted.
   - evidence line: NATIVE-REPLAY 117/117 x3.
3. Re-run `_experiments/exp160_check.py` from repo before publish.
4. Gates + publish per standard flow.

## EXP-161 (teardown chain 301140/3105D0)

1. Copy `Temp\exp161_check.py` -> `_experiments/exp161_check.py`;
   `Temp\EXP-161-teardown-unlink-exec.md` ->
   `_experiments/EXP-161-teardown-unlink-exec.md`.
2. Contract edits:
   - 301140(rec): despawn/death teardown. Entry gate
     `(d[q[rec+0x698]+0x64] | d[+0x3C]) & 0x80000003` -> bail;
     null back-pointer faults 0x301150. 311F70 only when
     2E9600(q[rec+0x10])==0 AND d[rec] bit 0x1A clear. Chain:
     238BF0 -> 3105D0 -> field clears -> 2EACD0 (thunk ->
     0x3B02A0 wait) -> 2E8060 -> mode-byte name ptr select
     (q[+0x6E8]) -> 2ECF10 -> 3299B0(0x200D) -> flag pass ->
     319E30/32A150 -> d[+0xDD0] timer recompute -> 3125E0 ->
     26DC60 -> d[+0x30]=0.
   - 3105D0(rec): unlink/reset — 310780, 30C970 x3, 300280,
     16D6A0, 236850/236820, 316CF0, 3291B0, 33C9B0.
   - 300280 -> 3008A0: unlink deregisters through the EXP-158
     spawn id-resolver (loop closed).
   - boundary: 311F70/238BF0/0x3B02A0/3299B0/290DF0 scripted;
     planted: q[0x209BE80] obj registry, q[0x2EBF190] state
     cell, q[rec+0x10] object, +0x698 bidirectional link.
   - evidence line: NATIVE-REPLAY 122/122 x3.
3. Re-run `_experiments/exp161_check.py` from repo before publish.
4. Gates + publish per standard flow.

## EXP-162 (object detach chain 238BF0)

1. Copy `Temp\exp162_check.py` -> `_experiments/exp162_check.py`;
   `Temp\EXP-162-object-detach-exec.md` ->
   `_experiments/EXP-162-object-detach-exec.md`.
2. Contract edits:
   - 238BF0(rec): object detach/param-normalize inside 301140.
     Guards on rec/q[rec+0x10]/q[rec+0x698]. b[objrow+5]==0 ->
     e60+0x7A float normalize + class byte (b4-0x1B)<=0xC picks
     269F30(obj,3,8) else (obj,2,1); ==1 -> member path e68+0x10
     float, rec+0x6A0 bit0x20 -> 267CC0+26B4A0 else b[rec+0x58]
     dispatch. Shared detach chain ~18 real callees on
     q[rec+0x10]; 236210 member arm (e68+0x18 bits -> 3204D0);
     tail 312700 scripted (246i).
   - boundary: 312700 scripted; planted e60/e68/6a0, objrow b4/b5.
   - evidence line: NATIVE-REPLAY 126/126 x3.
3. Re-run `_experiments/exp162_check.py` from repo before publish.
4. Gates + publish per standard flow.

## EXP-163 (reposition 311F70 + 312700 wrapper)

1. Copy `Temp\exp163_check.py` -> `_experiments/exp163_check.py`;
   `Temp\EXP-163-reposition-312700-exec.md` ->
   `_experiments/EXP-163-reposition-312700-exec.md`.
2. Contract edits:
   - CORRECTION: 312700 is a 12i wrapper (3125E0 -> 26DC60 ->
     2EBB80), NOT the 246i dispatcher — that body is sibling
     312730 (0x4000..0x4035 opcode jump table, still unexecuted).
   - 311F70(mode,rec,arg3): 30D9A0 -> 336E40 transform-struct
     fill -> 265020 pos read -> ucomiss compare (diff OR
     unordered -> 263F40->26B0C0 write) -> movups rec+0xD0/+0xE0
     -> 392170 -> member arm (arg3 && b[objrow+5]==1) mirrors
     quad to q[rec+0x6A0]+0x50 -> q[rec]|=0x4000000 ->
     d[+0x15C]/+0x160 scalar -> 263F40->26A0D0, 26B620, 808C40.
   - boundary: 336E40 scripted (struct semantics unproven);
     inbound 311F70 scripted on 301140 callsites.
   - evidence line: NATIVE-REPLAY 131/131 x3.
3. Re-run `_experiments/exp163_check.py` from repo before publish.
4. Gates + publish per standard flow.

## EXP-164 (transform-struct fill 336E40)

1. Copy `Temp\exp164_check.py` -> `_experiments/exp164_check.py`;
   `Temp\EXP-164-transform-fill-336E40-exec.md` ->
   `_experiments/EXP-164-transform-fill-336E40-exec.md`.
2. Contract edits:
   - 336E40(ctx): d[ctx+0]=BOOL mode (sete(30D9A0()==1)),
     q[ctx+8]=aux obj, q[ctx+0x10]=obj. Null-aux arm ->
     kind accessors 2646C0/265200/265090 (b[obj+3]>>5 ->
     q[obj+0xB8] node, floats +0/+0x50/+0xA8). Aux arm ->
     202F00 4x4 copy -> CRT IAT stubs -> 383F10 zone lookup
     (q[0x2AEDFB0] runtime global). Mode-1 arm ->
     265090/309AE0/259B10 (0x110-stride table +0x90/94/98)/
     203080/4687F0.
   - 30D9A0 full decode: cl=d[q[0x2EBF190]+0x5B04] ->
     cl&8->5, cl&4->4, 377C20()!=0->3, cl&2->2, else cl&1.
   - 377C20: 3148F0() idx -> q[0x2ADD100] 3-byte-stride table;
     null/OOB -> 0 else word bit15.
   - boundary: 861F08/861F0E CRT jmp q[IAT] stubs scripted;
     32A790->26E350->231900 scripted; expect_fault disclosures
     0x383F23 (null zone global) and 0x1CCEF20 (call q[IAT]
     wild exec — IAT holds name RVAs in file image).
   - evidence line: NATIVE-REPLAY 132/132 x3.
3. Re-run `_experiments/exp164_check.py` from repo before publish.
4. Gates + publish per standard flow.

## EXP-165 (opcode dispatcher 312730 + scatter 312DF0)

1. Copy `Temp\exp165_check.py` -> `_experiments/exp165_check.py`;
   `Temp\EXP-165-opcode-dispatch-312730-exec.md` ->
   `_experiments/EXP-165-opcode-dispatch-312730-exec.md`.
2. Contract edits:
   - CORRECTION: the EXP-162 "312700 scripted (246i)" body is
     sibling 312730 — a transform/position opcode dispatcher.
   - 312730(rec,cmd,out1,out2,a5): w[cmd]=opcode, w[cmd+2]=arg;
     xmm6=maxss(265090). 0x4000..0x4025 -> 2-level jump table
     (0x312AF8/0x312B10); 0x4026..0x4035 -> 2367A0 entity scan
     (global q[0x41E6688], 0xF50 stride, w[q[row+0x698]+4]==sel);
     singles 0x4124/25/4A/4E/65. Success: out2=[out1] quad,
     d[a5]=xmm6, ret 1.
   - 312DF0 = spawn-scatter: seed via 3DFD00 group-0 row (0x30
     stride) or [rcx] quad; 9 iters 328370 RNG jitter
     (rand%(2*arg+1))-arg on x/z -> 317DE0 -> 337700/3377C0;
     ret 0/-2/-1.
   - 0x4020 member arm: b[objrow+5]==1 gate; seed =
     q[rec+0x6A0]+0x50 (311F70's mirror quad — cross-package).
   - boundary: 383F10 zone lookup faults on null q[0x2AEDFB0]
     (zone-context global — shared blocker for all position
     validation); 4026 arm faults at 265090 on resolved shipped
     row's null +0x10 (authentic — static rows unlinked).
   - evidence line: NATIVE-REPLAY 140/140 x3.
3. Re-run `_experiments/exp165_check.py` from repo before publish.
4. Gates + publish per standard flow.

## EXP-166 (zone-context fixture — 383F10/391410/231400 real)

1. Copy `Temp\exp166_check.py` -> `_experiments/exp166_check.py`;
   `Temp\EXP-166-zone-nav-fixture-exec.md` ->
   `_experiments/EXP-166-zone-nav-fixture-exec.md`.
2. Contract edits:
   - 383F10 = navmesh cell->link lookup on zctx q[0x2AEDFB0]:
     {+0xC verts, +0x10 linkdescs, +0x18 celltab, +0x20 grpdesc}
     resolved via 20E600(elemb+off); grid bounds -> cellid ->
     link bytes -> 382D10 tri winding (ring 0xD112B0) ->
     ret linkid or 0xFF.
   - 391410/3912E0 = layer occupancy scan on globals
     0x2AEE060..0xB9 (occupancy q[+0x48], scratch q[+0x50],
     cell-size f[+0x2F], dims d[+0]/d[+4]).
   - 337700 = candidate validator: 265090 y (KIND-3 ONLY —
     b[obj+3]&0xE0==0x60, else outs unwritten), 391410, 384130
     ->383F10, 336390 5-point footprint (32A6A0->26E100->
     231400 x5: center + 4 corners at +/-maxss(y0,y1)).
   - 231400 = entity-grid query on q[0x209A670] gate +
     q[0x209A678] ctx: 233050 pos->cell (odd-col stagger),
     233110 row select (230A40 mask filter -> 2324F0 eval),
     height solve, 22F830 span query w/ 22F8B0 callback;
     ret = ebx accept flag.
   - CRT import band 0x861EC0..0x862090 resolved by name:
     memset/_fdclass/cosf/sinf/sqrtf/tanf/atan2f/asinf.
     Harness host-computes them via MATH hooks (disclosed:
     not bit-exact); rand cell 0x8C3098 deterministic stub.
   - ACCEPTED SPAWN PROVEN: t2730-accept eax=1 end-to-end.
     t1f70-aux/mode1 bonus: full 24-node transform chain real
     (24x cosf/sinf/sqrtf + 48x z383f10), q[rec]|0x4000000,
     d[rec+0x15C]=0x3FC912DC ~pi/2.
   - evidence line: NATIVE-REPLAY 143/143 x3.
3. Re-run `_experiments/exp166_check.py` from repo before publish.
4. Gates + publish per standard flow.

## EXP-167 (surface snap — 32A790/26E350/231900/231820 real)

1. Copy `Temp\exp166_check.py` -> `_experiments/exp166_check.py`;
   `Temp\EXP-167-surface-snap-exec.md` -> `_experiments/`.
2. Contract edits:
   - 32A790 = jmp 26E350 trampoline (was scripted boundary).
   - 26E350 = walkable-surface snap: gate q[0x209A670],
     ctx q[0x209A678]; 231900 best-row find -> 231820 writes
     f[pos+4] = surface height.
   - 231900: 233050 cell -> ridx span -> f[row+4]>0.001f gate
     -> bt mask,(d[row+0xC]&7) -> 2324F0 eval (negative=usable)
     -> 231890 plane solve -> max-select row idx.
   - 231890/231820 = plane solvers on rowtab(+0x10 sector idx)
     x sectab(16b records): (dz*f8+dx*f0)/f4+secf4.
   - t26e350: pos.y 99 -> 0 snap write proven.
   - evidence line: NATIVE-REPLAY 144/144 x3.
3. Re-run `_experiments/exp166_check.py` from repo before publish.
4. Gates + publish per standard flow.

## EXP-168 (312730 opcode arms 0x4022/0x4024/0x4125/0x414A/0x414E)

1. Copy `Temp\exp166_check.py` -> `_experiments/exp166_check.py`;
   `Temp\EXP-168-opcode-arms-exec.md` -> `_experiments/`.
2. Contract edits:
   - CORRECTION: the shared owner/member resolver gate is
     `test b[0x2089340],0x10` — 7-byte insn, earlier notes said
     `0x208B340`/`0x2089341` (off-by-one; confirmed via
     UC_HOOK_MEM_READ). 31B7E0/31ABE0/3272A0/3272F0 all read it.
   - `3588B0(id)`: cls `id>>0x10&0xF` (<5), idx `id&0xFFFF`,
     gen `id>>0x14&0x7FF`; `263FF0(cls)` = cls desc
     `0x2098E10+cls*0x288` `{q+0 base, q+8 rowptrs{count,ptr..},
     b+0x10&1 active, d+0x20 count}`; bounds+active+
     `w[row+0x16]==gen`; `263E30(row)` = `q[row+0x30]` rec.
   - `3590D0` = leader id `d[0x22C7FE0]` (off-by-one corrected
     from 0x252D7E0).
   - `0x4022` foe arm: `q[rec+0x698]` + `b[objrow+5]==0` ->
     `31B7E0(d[rec+0x24])` owner -> out1=rec+0x120 quad,
     out2=owner+0xD0, outf=309B10+309A90.
   - `0x4024`: `3272A0` (leader-id resolve + `b[rec]&8` gate)
     -> shared `0x312918`; `0x414A`: `31B7E0` -> same body;
     both copy owner+0xD0 to out1/out2, outf=30A130+arg+xmm6.
   - `0x414E`: `31ABE0(d[rec+0x710])` -> ROW (no 263E30) ->
     `265390(row, out1, out1+4, out1+8)` kind-dispatch
     `b[row+3]>>5`; kind3 reads `q[row+0xB8]` node triple;
     arm writes `d[outf]=0`.
   - `0x4125`: `312DF0(rec+0xD0, edx=-1, r8d=0x14)` — uses
     `3377C0` validator (which calls `337700`); `31abe0` fires
     per iteration; exhaust -> reject (eax=0 proven).
   - evidence line: NATIVE-REPLAY 149/149 x3.
3. Re-run `_experiments/exp166_check.py` from repo before publish.
4. Gates + publish per standard flow.

## EXP-169 (265390 kind arms + 0x4125 accept)

1. Copy `Temp\exp166_check.py` -> `_experiments/exp166_check.py`;
   `Temp\EXP-169-decompose-arms-exec.md` -> `_experiments/`.
2. Contract edits:
   - `265390(row,&x,&y,&z)` dispatch `b[row+3]>>5`: kind1
     (`&0xE0==0x20`) node `{d+0x10,d+0x14,d+0x18}`; kind3
     (`==0x60`) node `{d+0, f+4, d+8}` + optional
     `q[row+0xC0]` `{f+0x140+f+0x144}` y-add +
     `b[node+0x107]&1` `{f+0x40,+0x44,+0x48}` adds;
     default zeroes outs.
   - `0x4125` accept path proven: `312DF0` seeded rec+0xD0,
     arg 0x14, edx=-1 -> `3377C0`->`337700` per iter;
     `31abe0` fires per iteration; `outf`=xmm6 scale.
   - `erowall` fixture: ridx span {0,1} all 64 cells.
   - evidence line: NATIVE-REPLAY 153/153 x3.
3. Re-run `_experiments/exp166_check.py` from repo before publish.
4. Gates + publish per standard flow.

## EXP-170 (0x4165/319850 closest-entity scan)

1. Copy `Temp\exp166_check.py` -> `_experiments/exp166_check.py`;
   `Temp\EXP-170-closest-entity-4165-exec.md` -> `_experiments/`.
2. Contract edits:
   - `0x4165` arm: `319850(rec, out1)` >= 0 -> copy quad to
     out2, `outf = xmm6 + f[0x1CEBBA7] - f[0x8C5F6C](=0.1f)`.
   - `319850`: list `q[0x2EC1360]` `{d+0 id, q+0x18 next}`;
     seed `f[0x2F973B8]` best-dist (runtime-init, 0 in
     image); per node `2FB310(id)` -> table
     `0x22BE7F0+id*0x20` {b+0 flag, quad +0x10};
     `3A1960(rec+0xE0,quad)` = squared XZ dist; strictly-
     closer wins; ret id or -1.
   - Output quad w lane = uninitialized stack (repacks
     x/y/z only) — authentic.
   - CORRECTIONS: list head 0x2EC1360 (not 0x3C92E60),
     table 0x22BE7F0 (not 0x4BE47F0) — RIP off-by-ones.
   - evidence line: NATIVE-REPLAY 155/155 x3.
3. Re-run `_experiments/exp166_check.py` from repo before publish.
4. Gates + publish per standard flow.

## EXP-171 (2FEF30 member arm — four-desc stat resolve)

1. Copy `Temp\exp166_check.py` -> `_experiments/exp166_check.py`;
   `Temp\EXP-171-member-arm-2FEF30-exec.md` -> `_experiments/`.
2. Contract edits:
   - `2FEF30` member arm (b[rec+5]!=0 -> 0x2FF0E1): four-level
     e600 chain — descs 0x2EBF120 (b[rec+4] idx -> member
     row r13), 0x2EBF148 (w[r13+0x22] -> rbp), 0x2EBF140
     (w[r13+0x24] -> rbx), 0x2EBF150 (w[r13] -> r11); each
     e600(d[g+0xC]) + w[g+8]*idx.
   - Stat accumulation: ecx = b[+0x1C2]-b[+0x88] level delta
     x rbx.b[+0x27..+0x2C] + rbp.b[same] + rec.w pairs ->
     8 stat slots; d[+0x20]/w[+0x24] HP pair; b[r11+0x29..
     0x2D] -> out+0x1C..0x20; b[r13+0x15] bit-gates two
     further arms; 322C50 loop over w[rec+0x50] slots.
   - 30FED0 member tail: 31B860 owner scan ->
     q[owner+0x6A0] bit7 -> b[obj+0x78] -> b[rec+0x40].
   - New keys: membarm (3 descs), obj6a0.
   - evidence line: NATIVE-REPLAY 155/155 x3.
3. Re-run `_experiments/exp166_check.py` from repo before publish.
4. Gates + publish per standard flow.

## EXP-172 (230A40 mask query + 2324F0 triangle eval)

1. Copy `Temp\exp166_check.py` -> `_experiments/exp166_check.py`;
   `Temp\EXP-172-usable-surface-exec.md` -> `_experiments/`.
2. Contract edits:
   - `230A40(ctx,rowidx,kind)` = row-usability bit query:
     row = q[ctx+0x10]+rowidx*0x20 (neg idx -> 0); mask =
     d[row+0xC]; two-level substitution over BSS table
     0x209A2D0 (idx1=mask>>0xD&0x1F, idx2=mask>>3&0xF+0x40;
     ecx=((B1&A1)|(~A1&mask))&~A2|(B2&A2); A=+0x110,B=+0x114);
     test cl,7 reject; kind0/1/2/3/5 -> !bit23/25/26/27/24,
     kind4/6+ -> 1. 233110 kind = w[in+0x50].
   - `2324F0(ctx,rowidx,scratch)` = point-in-triangle edge
     eval: q[scr+8]=P {f+0 x,f+8 z}; 3-edge loop
     (d[0x908DE8]={1,2,0} -> v0v1,v1v2,v2v0 over q[ctx+8]
     16b sector recs); n=cross(e2,e1) via 0x202E10;
     edge qualifies iff n.y<-1e-4 AND len>1e-4; ret argmin
     |dot(e1,e2n)/len-0.5| edge idx, init -1. 231900 uses
     ret<0 = inside = usable. CW-wound rows.
   - HARNESS FIXES: main() elif now matches `t2*` (dead
     t2730-*/t26e350 asserts since EXP-165 now live and
     passing); `epos` hoisted out of `ownerres` (t26e350
     gets real pos ptr); t312730 entry-tag asserts dropped
     (entry-block quirk; downstream tags prove path).
   - CORRECTIONS: mask table 0x209A2D0 (was 0x20942D0),
     midpoint const 0x1CEBB70=0.5f, edge table 0x908DE8.
   - evidence line: NATIVE-REPLAY 165/165 x3.
3. Re-run `_experiments/exp166_check.py` from repo before publish.
4. Gates + publish per standard flow.

## EXP-173 (22F830/22F8B0/381EB0 occupancy query)

1. Copy `Temp\exp166_check.py` -> `_experiments/exp166_check.py`;
   `Temp\EXP-173-occupancy-22F830-exec.md` -> `_experiments/`.
2. Contract edits:
   - `22F830(ctx)` = 4-lane occupancy driver: lanemask
     b[ctx+0x16]; span-idx = lane*(w[lane+0x40]+1)+w[ctx+0x10];
     CSR bounds w[ctx+0x12]/w[ctx+0x14]; call q[ctx].
     231400 seeds callback 22F8B0, lanes 6, filter 1.
   - `22F8B0` = span walker: ids 0x4000..0x4FFF -> ents
     q[lane+0x18]+(id-0x4000)*0x90; d[ctx+0x24] filter merges
     d[ent+4] via 0x209A3E0 (idx=(f>>0xD&0x1F)+0x20) skip on
     merged bit31; 381EB0(ent, q[ctx+0x18]) hit -> d[ctx+0x20]=1.
   - `381EB0` = local-space volume test: 217060 transforms
     probe by entity+0x50 4x4; kind1 box (runtime bounds
     0x1CEBBA7/0x1CEBC9B), kind2 cylinder |y|<1,sqrt(x2+z2)<1
     (consts 0x1CEBBA8/0x1CEBC9C); else ret 0.
   - `217060` = 4x4 matrix x point (out = M[p.x p.y p.z p.w]).
   - New f830 fixture: ctx/lane/bounds/ids/ents/probe keys.
   - evidence line: NATIVE-REPLAY 170/170 x3.
3. Re-run `_experiments/exp166_check.py` from repo before publish.
4. Gates + publish per standard flow.

## EXP-174 (336390 5-point footprint gate)

1. Copy `Temp\exp166_check.py` -> `_experiments/exp166_check.py`;
   `Temp\EXP-174-footprint-336390-exec.md` -> `_experiments/`.
2. Contract edits:
   - `336390(pos, ?, kind, xmm1=halfwidth)`: center + 4
     corner probes at +-halfwidth on x/z, each via
     `32A6A0`=`jmp 26E100` -> `231400` egrid commit; any
     probe ret 0 -> eax 0 (fail-fast); all pass -> eax 1.
     y/w lanes copied unchanged (2D footprint).
   - `26E100`: gate q[0x209A670], ctx q[0x209A678],
     kind = movzx dx -> 231400 r8d.
   - Corner probes DO consult 2324F0 triangle geometry:
     CW tri (0,0)-(0,4)-(4,0), pos (2,1,2) hw=1 -> corner
     (3,3) violates edge v1->v2 (n.y=-1.414) -> reject
     after 2 probes.
   - evidence line: NATIVE-REPLAY 172/172 x3.
3. Re-run `_experiments/exp166_check.py` from repo before publish.
4. Gates + publish per standard flow.

## EXP-175 (233050 pos->cell staggered-grid converter)

1. Copy `Temp\exp166_check.py` -> `_experiments/exp166_check.py`;
   `Temp\EXP-175-pos2cell-233050-exec.md` -> `_experiments/`.
2. Contract edits:
   - `233050(ctx, pos)`: wx=cvtdq2ps(d[ctx+0x38])+x,
     wz=cvtdq2ps(d[ctx+0x3c])+z; either <0 -> ret 0xFFFF
     (movzx r10w sentinel; callers test ax/js). col=trunc(wx)/
     cellw; odd col -> zint -= cellh/2 (constant, not
     remainder); row=zint/cellh via idiv (trunc to 0 ->
     stagger underflow clamps to row 0). col>=gcols or
     row>=grows -> 0xFFFF. ret row*gcols+col.
   - evidence line: NATIVE-REPLAY 180/180 x3.
3. Re-run `_experiments/exp166_check.py` from repo before publish.
4. Gates + publish per standard flow.

## EXP-176 (26E130/26E150 slot invalidate + 3278D0 sweep)

1. Copy `Temp\exp166_check.py` -> `_experiments/exp166_check.py`;
   `Temp\EXP-176-slot-invalidate-exec.md` -> `_experiments/`.
2. Contract edits:
   - `26E130(idx)`: d[0x209A3E0+idx*8]=0 (lo dword only),
     jmp 3278D0. `26E150(base,count)`: count<=0 ret; else
     clears base..base+count-1, sweep once per slot.
   - `3278D0`: i<d[0x208E6A0] -> obj=q[0x208E688]+i*0xF50;
     b[obj]&0x10 -> 3839C0 w[obj+0x20C/+0x20E]=0xFFFF +
     3839F0 b[obj+0x210..0x28F]=0xFF. Cells corrected via
     read-trace (not 0x209CAA0/0x209CA88).
   - evidence line: NATIVE-REPLAY 184/184 x3.
3. Re-run `_experiments/exp166_check.py` from repo before publish.
4. Gates + publish per standard flow.

## EXP-177 (0x209A3E0 bit-override mux family + 26E960 installer)

1. Copy `Temp\exp166_check.py` -> `_experiments/exp166_check.py`;
   `Temp\EXP-177-override-table-exec.md` -> `_experiments/`.
2. Contract edits:
   - **CORRECTION (supersedes EXP-173)**: 22F8B0's merge table
     base is 0x209A3E0, entries {A=override-enable, B=bits};
     merged=(B&A)|(d[ent+4]&~A), skip iff bit31. Index
     (e4>>0xD&0x1F)+0x20. (0x209A2D0 is 230A40's table.)
   - `26E850(slot,shift,width)`: A &= ~(mask<<shift) + sweep.
     `26E880(slot,val,shift,width)`: A |= mask; B = (B&~mask)
     | (val<<shift) + sweep. `26E8C0`: q[0x209A660]=rcx.
   - `26E960(ctx)` installer: q[0x209A670]=ctx (stored before
     null-check), q[0x209A678]=ctx+0x40, q[0x209A680]=ctx+0xA8,
     q[0x209A690]=q[q[ctx+0x40]+0x30], q[0x209A6A8]=..+0x38;
     d[0x209A6FC]=d[0x209A708]=1; f[0x209A6F4]=f[0x8B5778];
     d[0x209A6D0]=3ED0B0(); clears table lo dwords
     0x209A3E0..0x209A658 with 0x50 3278D0 sweeps; 3ED020 x3
     on 0x209A6F0, 3ECFD0(0x209A370), 3ED140, 3B6BA0, tail
     jmp 3ED7B0. (3ED0xx scripted in replay — disclosed.)
   - 22F8B0 mux proven both directions (inject bit31 -> skip;
     clear bit31 -> test).
   - Table builder: 0x3791FE..0x379607 calls 26E880/26E850
     en masse; 26E150+26E130 pairs at 0x3791DB/0x37922C/
     0x37927B.
   - evidence line: NATIVE-REPLAY 190/190 x3.
3. Re-run `_experiments/exp166_check.py` from repo before publish.
4. Gates + publish per standard flow.

## EXP-178 (slot-API wrappers + 379630 builder)

1. Copy `Temp\exp166_check.py` -> `_experiments/exp166_check.py`;
   `Temp\EXP-178-slot-api-builder-exec.md` -> `_experiments/`.
2. Contract edits:
   - `3791D0(idx)`: idx<0 -> 26E150(0,0x20); else 26E130(idx).
     `379270`: range 0x20..0x3F (22F8B0 group). `379220`:
     range 0x40..0x4F. `3791F0`/`379240`(idx+0x40): val<0 ->
     26E850 release; else 26E880 5-bit field bits 18-22
     (mask 0x7C0000).
   - `26E8D0(n)`: d[0x209A6E8]=n, d[0x209A708]=1,
     d[0x209A2D0]=3ED0B0() (triple-duty: 230A40 base +
     379630 count), same 3ED0xx tail as 26E960.
   - `379290`: q[0x2ADD090] -> b[0x2ADD0E9]=1 + 26E8D0
     (265920()); else b=0 + jmp 379630.
   - `379630`: free handles d[0x2ADD120..0x128]+0x2ADD11C via
     3ABCA0, 26E8D0(265920()), alloc clamp(d[0x209A2D0],0,3)
     records via 3AB960 from template 0x2A5A2E0 (stride 0x30,
     b[rec+7]|=0x20, d[rec]=0x1002001, b[rec+4]=1) ->
     handles stored back to array; tail 379760.
   - SCR tags land in w.rets["calls"], not w.trace.
   - evidence line: NATIVE-REPLAY 203/203 x3.
3. Re-run `_experiments/exp166_check.py` from repo before publish.
4. Gates + publish per standard flow.

## EXP-179 (generational-handle pool + 265920)

1. `Temp\exp166_check.py` -> `_experiments/exp166_check.py`;
   `Temp\EXP-179-handle-pool-exec.md` -> `_experiments/`.
2. Contract edits:
   - `3AB960(tpl)`: first-free slot in 0x80x0x70 pool at
     q[0x2B3F528]; handle=(++d[0x2B3F504])<<8|slot (wrap
     >0xFFFFFF->1) -> d[rec]; count b[0x2B3F500]++; copies
     0x50B tpl -> rec+0x20; kind b[+0x20] 2/3/4/5 derive
     floats (K=1.0f at 0x1CEBBA8); append dll (+8/+0x10,
     head 0x2B3F508 tail 0x2B3F510); ret handle; full->0.
   - `3ABCA0(h)`: list walk, d[node]=0, unlink, count--.
   - `3ABD00(h)`: slot=h&0xFF, ret rec+0x20 iff d[rec]==h
     (generational stale-handle reject).
   - `3ABD20()`: first live node with b[+0x23]==5 -> +0x20.
   - `3ABB60()`: clears pool + allocates builtin kind-7
     record via 3AC920(rec+0x20).
   - `265920()`: 17D490()>0 -> it; else b[0x21654E0]+1
     (2EF640 static 0x2164280 +0x200+0x1060).
   - evidence: NATIVE-REPLAY 220/220 x3.
3. Re-run before publish; gates per standard flow.

## EXP-180 (379760 extra-record alloc, 37AD10, 3AC920, 17D490)

1. `Temp\exp166_check.py` -> `_experiments/exp166_check.py`;
   `Temp\EXP-180-builder-tail-exec.md` -> `_experiments/`.
2. Contract edits:
   - `379760()`: 37AD10(0) cfg row -> quad scaled by
     f[0x209A370] (=3ECFD0 init block; BSS); kind-6 tpl
     (d+0=0x1042006, b4=1, b5|=0x80, b7=(b&3)|0x20, quad
     +0x10); 3AB960 -> free old d[0x2ADD11C] -> store.
   - `37AD10(i,&o)`: i<5 -> 0x2EBF460+i*0x50; i>=5 -> 0;
     negative i reads pre-table (signed jge quirk).
   - `3AC920(payload)`: in-place kind math, outputs
     shifted -0x20 vs rec view; kinds 0/1/6/7 no-op.
   - `1D50D0` lazy singleton q[0x1F81428] (210ec0(0x10E8)+
     1CCB20 when null); `17D490` = d[singleton+0xAAC].
   - evidence: NATIVE-REPLAY 229/229 x3.
3. Re-run before publish; gates per standard flow.

## EXP-181 (nav-row accessors un-stubbed; 26E8D0 fully real)

1. `Temp\exp166_check.py` -> `_experiments/exp166_check.py`;
   `Temp\EXP-181-navrow-accessors-exec.md` -> `_experiments/`.
2. Contract edits:
   - Nav row table: q[0x2EBB7F0], stride 0x180, row =
     d[0x209A6E8]-1; all accessors null-table early-out.
   - 3ED0B0=d[row+4] (->d[0x209A2D0] count); 3ECFD0(out)=
     row+0xF0 quad (26E8D0 writes 0x209A370 = 379760's
     scale); 3ED140=f[row+8] xmm0 (null->f[0x1CEBBA8]=1.0);
     3B6BA0: f[0x1EFE314]=xmm0; 3ED020(i,a,b): row+0x90+
     i*0x20 ->a, row+(i+5)*0x20 ->b (26E8D0 fills 3 recs at
     0x209A2F0 stride 0x30); 3ED7B0(i): row+0x10/+0x14/+0x1C
     -> d[0x2EBB7F8]/+4/+0xC.
   - 26E8D0 now fully real in harness; 379630 count driven
     via real 3ED0B0 (navtbl fixture).
   - evidence: NATIVE-REPLAY 237/237 x3.
3. Re-run before publish; gates per standard flow.

## EXP-182 (1CCB20 render-singleton ctor; 1D50D0 full chain)

1. `Temp\exp166_check.py` -> `_experiments/exp166_check.py`;
   `Temp\EXP-182-ctor-1CCB20-exec.md` -> `_experiments/`.
2. Contract edits:
   - `1D50D0` lazy singleton q[0x1F81428]: null -> 210ec0
     (0x10E8) -> 1CCB20 -> store+ret; now fully real in
     harness via `allocx` dynamic-alloc stub.
   - `1CCB20` = 0x10E8-byte render/lighting settings ctor:
     +0xA78=0x500/+0xA7C=0x2D0 dims, f[+0xC10]=pi/4 fov,
     f[+0xC14]=16/9, d[+0xC40]=0x63000C, +0xC68/+0xC6C=9999,
     f[+0xCF4]=45, f/q[+0xDB0]=30, d[+0xE18]=1000, q[+0xDDC]
     =0x11, d[+0x10D4]=0x280, +0xD0C/+0xD2C/+0xD4C =
     "None"/"Irradiance"/"Specular" (19C5D0 string copies,
     scripted). memset +0x130 len 0x938; 6x0xC zero loop
     +0xE68..+0x10A7.
   - `d[+0xAAC]` (17D490's nav-gen) zeroed by q[+0xAA8]
     store -> nav-gen starts 0, 265920 fallback arm first.
   - Sub-ctors real: 1E9F40(obj+8) leaf init, 1FE8B0
     (obj+0xA98) d=6/q+8=0. Scripted: 1D0390, 202880,
     5CC930, 19C5D0, 210EC0.
   - evidence: NATIVE-REPLAY 239/239 x3.
3. Re-run before publish; gates per standard flow.

## EXP-183 (2FEF30 member arm — nonzero tables)

1. `Temp\exp166_check.py` -> `_experiments/exp166_check.py`;
   `Temp\EXP-183-member-stats-nonzero-exec.md` -> `_experiments/`.
2. Contract edits:
   - 2FEF30 member stat math value-verified: stat =
     b[growth+k]*delta + b[base+k] + w[rec+f]; delta =
     b[rec+0x1C2]-b[rec+0x88]. HP d[out]=d[growth+0x20]*d+
     d[base+0x20] cap [1,9999] member (d[rsp+0x3C]=b[rec+5])
     / 0x3B9ACA00 nonmember. MP w[out+4] cap 999. Stats
     cap 99 (+6..9), 255 (+0xA/+0xB/+0xC), 100 (+0xD..+0x12),
     out+0x13 cap 3 (nonmember only).
   - member row b[+0x15] bit0 -> rbx+0x2D/rbp+0x2D arm;
     bit1 -> rbx+2/3, rbp+2/3 arm.
   - r11 row -> out+0x1C..0x20 in order +0x2C,+0x29,+0x2A,
     +0x2B,+0x2D.
   - 322C50(slot,6): slot-1 > 0x1F unsigned -> ret 0;
     equip loop skipped on zero slot list. License loops
     keyed on rec+0x68/+0x78 bitmaps, tables 0x1DF0290/
     0x1DF02A0/0x1DF02B0 — zero bitmap -> skip (disclosed).
   - Nonmember arm uses 2F8E50/2F9180 + rec floats — future.
   - evidence: NATIVE-REPLAY 240/240 x3.
3. Re-run before publish; gates per standard flow.
