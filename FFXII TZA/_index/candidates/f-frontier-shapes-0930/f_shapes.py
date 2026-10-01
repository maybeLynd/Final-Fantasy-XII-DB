"""f_shapes.py - the F family's undispositioned frontier by body shape (OPUS, 2026-09-30). Static; reads the dashboard's
captured requirement facts (the goal gate's F population) and the certified image. A planning census for SWE2-EC7, the
disposition owner - it declares nothing and explains nothing.

Buckets (first match wins), over the functions whose F state is "frontier (no disposition)":
  jmp-thunk        the body starts with an unconditional jmp
  getter-leaf      <= 2 instructions: a load from [rcx+..] into eax/rax/ax/al, then ret
  setter-leaf      <= 2 instructions: a store to [rcx+..], then ret
  tiny-leaf        ends in ret, body <= 16 bytes
  forwarder        ends in jmp, no call, body <= 24 bytes
  small            body <= 64 bytes
  larger           the rest
Writes f_shapes.tsv (entry, bucket, bytes, first instructions).
"""
import collections, io, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "rc9-log-channels-0930"))
import rc9_channels as R  # noqa: E402

FACTS = os.path.join(HERE, "..", "..", "..", "..", "Tools", "work", "dashboard", "_capture", "requirement_facts.json")


def bucket(a, n):
    ins = list(R.md.disasm(R.at(a, min(n, 64)), a))
    ms = [i.mnemonic for i in ins]
    if not ms:
        return "undecodable", ins
    if ms[0] == "jmp":
        return "jmp-thunk", ins
    if len(ms) <= 2 and ms[-1] == "ret" and ms[0] in ("mov", "movzx", "movsx", "movsxd", "lea") and "[rcx" in ins[0].op_str \
            and ins[0].op_str.split(",")[0] in ("eax", "rax", "al", "ax"):
        return "getter-leaf", ins
    if len(ms) <= 2 and ms[-1] == "ret" and ms[0] == "mov" and "ptr [rcx" in ins[0].op_str.split(",")[0]:
        return "setter-leaf", ins
    if ms[-1] == "ret" and n <= 16:
        return "tiny-leaf", ins
    if ms[-1] == "jmp" and "call" not in ms and n <= 24:
        return "forwarder", ins
    return ("small" if n <= 64 else "larger"), ins


def main():
    d = json.load(open(FACTS, encoding="utf-8"))
    un = sorted(int(f["k"][2:], 16) for f in d["facts"] if f.get("f") == "F" and not f.get("ok") and f.get("st") == "frontier (no disposition)")
    cnt = collections.Counter()
    with io.open(os.path.join(HERE, "f_shapes.tsv"), "w", encoding="utf-8", newline="\n") as o:
        o.write("entry\tbucket\tbytes\tfirst_instructions\n")
        for a in un:
            n = R.ext.get(a)
            if not n:
                cnt["no-extent"] += 1
                o.write("%08X\tno-extent\t\t\n" % a)
                continue
            b, ins = bucket(a, n)
            cnt[b] += 1
            o.write("%08X\t%s\t%d\t%s\n" % (a, b, n, " ; ".join("%s %s" % (i.mnemonic, i.op_str) for i in ins[:4])))
    print("frontier (no disposition): %d" % len(un))
    for k, v in cnt.most_common():
        print("  %-12s %5d" % (k, v))


if __name__ == "__main__":
    main()
