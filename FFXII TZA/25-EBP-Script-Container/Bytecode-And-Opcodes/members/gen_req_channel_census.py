#!/usr/bin/env python3
"""Census of REQ-family channel operands across every shipped EBP script.

Closes FABLE-REQ-SWE2-DATA-REQ-CHANNEL-RANGE (UQ-54): the channel byte
stored into the request descriptor at native 002689B1 becomes the
signed-char channel index later consumed by
ActorResource_SelectPendingEntryForExecution. This script measures the
authored low-byte distribution of that operand.

Model (NATIVE/STATIC, verified against 002688A0-002689B1 + handler pop counts):
  * Opcodes 0x21-0x29 (REQ FREQ TREQ REQSW FREQSW TREQSW REQEW FREQEW TREQEW)
    pop 3 stack values; the descriptor channel = the 3rd popped value
    = the FIRST of the three pushed arguments.
    Source order is `PUSH channel; PUSH target; PUSH funcid; REQ*`.
  * PREQ* (0x2A-0x2C) consume an already-built pending entry
    (movsx byte[r15+0x11] + stride-40 table) and carry no new channel
    operand; REQWAIT/PREQWAIT/REQCHG/REQCANCEL/REQALL/REQIALL/REQWAITALL
    operate on descriptors or whole actor state. Their leading pushes
    are still recorded in args_push_order for completeness.

Arg resolution: backward symbolic-stack walk from the request opcode.
Channel = arg0 (first pushed). Producer classes:
  const-int    PUSHII imm16 or PUSHI0-3 -> low byte = imm & 0xFF
  const-pool   PUSHI operand -> index into the script's int constant pool
               (section-000-bytecode.md: [pool + operand*4 + 4], header +0x20);
               the immediate is NOT the pushed value - it selects a pool slot
  const-float  PUSHF/PUSHF0-3 -> runtime cvttss2si; imm reported raw
  dynamic      PUSHV/PUSHA/PUSHX/PUSHY/PUSHTAG/PUSHACT/PUSHP/PUSHDBG/DVAR
  expr         result of a binary/unary op
  unresolved:* walk aborted (boundary, control-flow, call, spans-request,
               stack-underrun)

Outputs members/req-channel-census.tsv (one row per REQ-family site).
"""

import io, os, sys, struct, collections

sys.path.insert(0, r"agent_flow/tools")
import vbfextract as V

VBF = r"D:\FFXII MP Mod\FFXII_TestClient1\FFXII_TZA.vbf"
OUT = os.path.join(os.path.dirname(__file__), "req-channel-census.tsv")

U32 = lambda b, o: struct.unpack_from("<I", b, o)[0]

OPN = {
    0x00: "NOP", 0x01: "LABEL", 0x02: "TAG",
    0x05: "OPLOR", 0x06: "OPLAND", 0x07: "OPOR", 0x08: "OPEOR", 0x09: "OPAND",
    0x0A: "OPEQ", 0x0B: "OPNE", 0x0C: "OPGT", 0x0D: "OPLS", 0x0E: "OPGTE",
    0x0F: "OPLSE", 0x10: "OPSLL", 0x11: "OPSRL", 0x12: "OPADD", 0x13: "OPSUB",
    0x14: "OPMUL", 0x15: "OPDIV", 0x16: "OPMOD", 0x17: "OPNOT", 0x18: "OPBNOT",
    0x19: "OPUMINUS", 0x1A: "OPFIXADRS", 0x1B: "PUSHA", 0x1C: "POPA",
    0x1D: "PUSHX", 0x1E: "PUSHY", 0x1F: "POPX", 0x20: "POPY",
    0x21: "REQ", 0x22: "FREQ", 0x23: "TREQ", 0x24: "REQSW", 0x25: "FREQSW",
    0x26: "TREQSW", 0x27: "REQEW", 0x28: "FREQEW", 0x29: "TREQEW",
    0x2A: "PREQ", 0x2B: "PREQSW", 0x2C: "PREQEW",
    0x2D: "RET", 0x2E: "RETN", 0x2F: "RETT", 0x30: "RETTN", 0x31: "DRET",
    0x32: "REQWAIT", 0x33: "PREQWAIT", 0x34: "REQCHG", 0x35: "REQCANCEL",
    0x03: "UNK03", 0x04: "UNK04",          # real 1-byte ops, unnamed in table
    0x46: "DVAR", 0x47: "LONGCODESTART",
    0x48: "PUSHV", 0x49: "POPV", 0x4A: "PUSHDBG", 0x4B: "PUSHP",
    0x4C: "PUSHTAG", 0x4D: "PUSHACT", 0x4E: "PUSHI", 0x4F: "PUSHII",
    0x50: "PUSHF", 0x51: "JMP", 0x52: "JMPPOPX", 0x53: "JMPPOPY",
    0x54: "JMPX", 0x55: "JMPY", 0x56: "JMPXC", 0x57: "JMPYC",
    0x58: "CALL", 0x59: "CALLACT", 0x5A: "UNK5A", 0x5B: "UNK5B", 0x5C: "UNK5C",
    0x5D: "CALLPOPA", 0x5E: "CALLACTPOPA", 0x5F: "REQALL",
    0x60: "JMPINTERNAL", 0x61: "REQWAITALL", 0x62: "INCINITTAG", 0x63: "REQIALL",
}
for i in range(0x36, 0x3A): OPN[i] = "POPI%d" % (i - 0x36)
for i in range(0x3A, 0x3E): OPN[i] = "POPF%d" % (i - 0x3A)
for i in range(0x3E, 0x42): OPN[i] = "PUSHI%d" % (i - 0x3E)
for i in range(0x42, 0x46): OPN[i] = "PUSHF%d" % (i - 0x42)

# pushes exactly one stack value, producer = the instruction itself
PUSH_OPS = set(range(0x3E, 0x42)) | set(range(0x42, 0x46)) | {
    0x1B, 0x1D, 0x1E, 0x46, 0x48, 0x4A, 0x4B, 0x4C, 0x4D, 0x4E, 0x4F, 0x50}
POP_OPS = {0x1C, 0x1F, 0x20, 0x49} | set(range(0x36, 0x3E))
BIN_OPS = set(range(0x05, 0x17))       # pop 2 push 1
UN_OPS = set(range(0x17, 0x1B))        # pop 1 push 1
ZERO_OPS = {0x00, 0x01, 0x02, 0x47, 0x62}   # markers / INCINITTAG
RET_OPS = {0x2D, 0x2E, 0x2F, 0x30, 0x31}
JMP_OPS = set(range(0x51, 0x58)) | {0x60}
CALL_OPS = {0x58, 0x59, 0x5A, 0x5B, 0x5C, 0x5D, 0x5E}
REQ_OPS = set(range(0x21, 0x36)) | {0x5F, 0x61, 0x63}

CHANNEL_OPS = set(range(0x21, 0x2A))   # 3-pop descriptor builders
DESCRIPTOR_CONSUMERS = {0x2A, 0x2B, 0x2C, 0x32, 0x33, 0x34, 0x35, 0x5F, 0x61, 0x63}
NARGS = {**{o: 3 for o in CHANNEL_OPS},
         0x2A: 2, 0x2B: 2, 0x2C: 2,
         0x32: 2, 0x33: 2, 0x34: 7, 0x35: 3,
         0x5F: 1, 0x61: 0, 0x63: 1}

VERB_TSV = os.path.join(
    os.path.dirname(__file__), "..", "..", "..",
    "01-Script-VM-Native-Bridge", "Verb-Dispatch", "scriptvm-verb-table.tsv")


def load_verbs():
    """call_id -> (arity, pushes) from the measured verb table."""
    import csv
    verbs = {}
    with open(VERB_TSV, encoding="utf-8") as t:
        for row in csv.DictReader(t, delimiter="\t"):
            cid = int(row["call_id"], 16)
            try:
                arity = int(row["arity"]) if row["arity"] else None
            except ValueError:
                arity = None
            if arity is None:
                try:
                    arity = int(row["pops_int"] or 0) + int(row["pops_float"] or 0)
                except ValueError:
                    arity = None
            try:
                pushes = int(row["pushes"] or 0) + int(row["result_writes"] or 0)
            except ValueError:
                pushes = 0
            verbs[cid] = (arity, pushes, row["verb"])
    return verbs


def decode(code):
    """Linear decode; returns (ins, anomaly_pc|None)."""
    ins = []
    i = 0
    anomaly = None
    while i < len(code):
        op = code[i]
        if op > 0x63:
            anomaly = i
            break
        if op >= 0x48:
            if i + 2 >= len(code):
                anomaly = i
                break
            ins.append((i, op, code[i + 1] | (code[i + 2] << 8)))
            i += 3
        else:
            ins.append((i, op, None))
            i += 1
    return ins, anomaly


def resolve_args(ins, j, need, verbs):
    """Backward stack-slot attribution. Returns (args_push_order, status).

    `slots` holds the unattributed stack entries above the arg region,
    topmost first; arg slots are their arg index, popped-later entries
    are SKIP. Each instruction's produced entries claim the leading
    slots; its consumed entries prepend SKIPs (they were above the
    surviving entries and must be attributed by earlier producers).
    """
    SKIP = -1
    slots = list(range(need - 1, -1, -1))   # [argN-1 .. arg0], top-down
    found = {}
    k = j - 1
    while any(s != SKIP for s in slots):
        if k < 0:
            return None, "unresolved:boundary"
        pc, op, imm = ins[k]
        k -= 1
        if op in ZERO_OPS:
            continue
        if op in PUSH_OPS:
            P, Q, prod = 0, 1, (OPN.get(op, hex(op)), imm, "push")
        elif op in POP_OPS:
            P, Q, prod = 1, 0, None
        elif op in BIN_OPS:
            P, Q, prod = 2, 1, (OPN.get(op, hex(op)), None, "expr")
        elif op in UN_OPS:
            P, Q, prod = 1, 1, (OPN.get(op, hex(op)), None, "expr")
        elif op in (0x58, 0x59, 0x5D, 0x5E):
            v = verbs.get(imm)
            if v is None or v[0] is None:
                return None, "unresolved:call-arity"
            arity, pushes, vname = v
            P = arity + (1 if op in (0x59, 0x5E) else 0)   # actor id pop
            if op in (0x58, 0x59):
                Q = pushes
            elif pushes > 0:
                Q = pushes - 1                            # *POPA pops result
            else:
                P, Q = P + 1, 0
            prod = ("call:" + vname, imm, "call")
        elif op in CALL_OPS:
            return None, "unresolved:call-op"
        elif op in RET_OPS:
            return None, "unresolved:ret-boundary"
        elif op in JMP_OPS:
            return None, "unresolved:control-flow"
        elif op in REQ_OPS:
            return None, "unresolved:spans-request"
        else:
            return None, "unresolved:op-%02x" % op
        for _ in range(Q):
            if not slots:
                return None, "unresolved:underrun"
            s = slots.pop(0)
            if s != SKIP:
                found[s] = prod
        slots = [SKIP] * P + slots
    return [found[i] for i in range(need)], "ok"


def classify_arg(opname, imm, kind):
    if kind == "expr":
        return "expr", None
    if opname == "PUSHI":
        return "const-pool", imm
    if opname == "PUSHII":
        return "const-int", imm & 0xFF
    if opname.startswith("PUSHI") and opname[-1].isdigit():
        return "const-int", int(opname[-1])
    if opname == "PUSHF" or opname.startswith("PUSHF"):
        return "const-float", imm
    return "dynamic", imm


def main():
    f = io.open(VBF, "rb")
    names, blocks = V.load_index(f)
    verbs = load_verbs()
    ebps = sorted(p for p in names if p.lower().endswith(".ebp"))
    rows = []
    seen = set()
    files = scripts = anomalies = 0
    for path in ebps:
        try:
            b = V.read_entry(f, names, blocks, path)
        except Exception:
            continue
        if len(b) < 0x80 or U32(b, 0x80) != 0x8000000B:
            continue
        files += 1
        sec = b[0x80:0x80 + U32(b, 0x84)]
        diroff = U32(sec, 0x18)
        cnt = U32(sec, diroff)
        if cnt > 0x400 or diroff + 4 + cnt * 0x30 > len(sec):
            continue
        starts = sorted(U32(sec, diroff + 4 + s * 0x30 + 8) for s in range(cnt))
        bounds = sorted(set(starts) | {diroff, len(sec)})
        for si, start in enumerate(starts):
            end = min((x for x in bounds if x > start), default=len(sec))
            if start >= len(sec) or end <= start:
                continue
            scripts += 1
            ins, anomaly = decode(sec[start:end])
            if anomaly is not None:
                anomalies += 1
            for j, (pc, op, imm) in enumerate(ins):
                if op not in CHANNEL_OPS and op not in DESCRIPTOR_CONSUMERS:
                    continue
                need = NARGS.get(op, 3)
                site_key = (path, start + pc)
                if site_key in seen:
                    continue
                seen.add(site_key)
                args, status = resolve_args(ins, j, need, verbs) if need else ([], "ok")
                argstr = ";".join(
                    "%s%s" % (a[0], ":%x" % a[1] if a[1] is not None else "")
                    for a in args) if args else ""
                if op in CHANNEL_OPS and status == "ok":
                    ccls, cval = classify_arg(*args[0])
                    ch_byte = cval if ccls == "const-int" else ""
                    ge80 = (ccls == "const-int" and cval >= 0x80)
                elif op in CHANNEL_OPS:
                    ccls, ch_byte, ge80 = status, "", False
                else:
                    ccls, ch_byte, ge80 = "n/a", "", False
                rows.append((
                    path, str(si), "%x" % (start + pc), "0x%02X" % op,
                    OPN.get(op, "?"), argstr,
                    ccls, str(ch_byte), "1" if ge80 else "0"))
    with open(OUT, "w", newline="") as w:
        w.write("\t".join(("file", "script", "pc", "opcode", "opname",
                          "args_push_order", "channel_class", "channel_byte",
                          "ge80")) + "\n")
        for r in rows:
            w.write("\t".join(r) + "\n")
    print("files=%d scripts=%d sites=%d anomalies=%d -> %s"
          % (files, scripts, len(rows), anomalies, OUT))
    agg = collections.Counter((r[4], r[6]) for r in rows)
    for k in sorted(agg):
        print(k, agg[k])
    hits = [r for r in rows if r[8] == "1"]
    print("ge80 hits:", len(hits))
    for h in hits[:60]:
        print("  ", h)


if __name__ == "__main__":
    main()
