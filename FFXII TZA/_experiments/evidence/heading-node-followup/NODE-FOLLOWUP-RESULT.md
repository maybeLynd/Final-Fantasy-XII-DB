# Two specific consumers behind the type-0x67/0x72 field writes

Method A / original-source only. This follows the immutable first consumer
package (`9241ba12c7ad6e1030ace56fcde0a09502200a68`) one level where it
left exact questions. No original-code execution, live FF12, or repeated
capture of the four constant-store entries. The earlier valid statement that
`0045FD10` has no direct `+0x3D8` operand remains true; its reader is delegated.

For node byte `0x67`, `0045FD10` calls `002F2530`, returns if EAX is zero,
and otherwise passes its saved entry node as RCX to `004607C0` (`0045FD33/
0045FD36`). The 894-byte catalogued `004607C0` body copies entry RCX to RBX.
At `00460ACA` it reads `[rbx+0x3D8]`, comparing to R12D; R12D is zeroed at
`00460A5B`. If unequal, `00460AD3` writes R12D back and the `00460ADA..
00460AF3` source loop initializes ESI to `0x20`, calls `00533B20` on
`rbx+0x280`, decrements ESI and repeats while nonzero. The normal-path
zero/32 interpretation depends on intervening native callees preserving
nonvolatile R12/RBX/RSI and returning. This package does not establish
`00533B20`'s full effects or when the step is scheduled. `002F2530`'s
predicate is not claimed always true. The immediate callee `002F2530` has
no direct `+0x3D8` operand in its bounded 2094-byte catalogued body; it is
not an image-wide negative.

For node byte `0x72`, published step source checks `[rbx+0x3F8]` at
`0052BB35` and calls `0052BBD0` at `0052BB45` on the nonzero arm, with
RCX restored from RBX. The original `0052BBD0` full 925-byte body matches
one rooted exception/unwind range. At `0052BBF5/BBF7` it clears
`[rcx+0x3F8]` before any callee call. Its later `0052BF21..0052BF4C`
source loop sets EBX to `0x20`, calls `0054B1F0` with RCX=`rdi+0x280`,
RDX=`rsp+0x30`, R8D=1 and R9D=0, decrements RBX, then repeats while
nonzero. All seven direct branches inside the captured body are internal,
with one RET after that loop; under normal nested returns and ABI-preserved
RBX, the path reaches 32 parameter-install calls. The canonical per-model
oscillator page already describes `0054B1F0`'s parameter-install role; this
package consumes that description, not a new proof of its nested math.
Prior calls in `0052BBD0` include an import thunk and several other native
targets whose state/effects are not closed here. The source path does not
establish actual live execution, initialized object identity, scheduler
order, frame duration, visual motion, or class preservation.

The combination narrows the four flags to candidate one-shot update requests:
the `0x67`/`0x72` paths read a nonzero value and clear it before repeated
work. It does **not** prove identical meaning for 0x6B/0x71, general
thread-safety, or that any flag was set and consumed in one real instance.
Consumer should replace only the “0x67 reader unknown” and “0x72 gated
callee unknown” local dependencies after independent review, preserving
all live/ownership and broader class unknowns.

Player version: one switch sends a model through repeated update calls when
that model's update runs; another clears its switch and repeatedly installs
oscillator parameters. This is what the source is set up to do under normal
calls, not a report of motion seen in the game.
