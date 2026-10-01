"""Check the source-record prerequisite used by this bounded title research.

Re-decode retained original bytes; use the reviewed access-role adapter.
This establishes annotation consistency, not native effects or original identity
beyond the separately pinned bytes/image/tool receipts.
"""
import hashlib, importlib.util, pathlib
import capstone
from capstone.x86_const import X86_OP_MEM

W = pathlib.Path(__file__).resolve().parent
ADAPTER_RELATIVE = "Database/Tools/analysis-kit/gfz-scripts/reg_tracking.py"
# Both owned preparation and its nested immutable copy need the same reviewed
# repository dependency. Resolve its actual ancestor rather than assuming depth.
ROOT = next((p for p in W.parents if (p / ADAPTER_RELATIVE).is_file()), None)
if ROOT is None:
    raise ValueError("reviewed repository adapter unavailable")
ADAPTER = ROOT / ADAPTER_RELATIVE
ADAPTER_SHA = "5fcc64842c96d99c3ef9df4f7e3adc528dfad0dfd44b2f6bb5bf43beda092a38"


def validate(v):
    if hashlib.sha256(ADAPTER.read_bytes()).hexdigest() != ADAPTER_SHA:
        raise ValueError("reviewed access-role adapter changed")
    if v.get("adapter_sha256") != ADAPTER_SHA or v.get("capstone") != capstone.__version__:
        raise ValueError("annotation tool/adapter provenance mismatch")
    if not isinstance(v.get("ranges"), list) or not v["ranges"]:
        raise ValueError("missing/zero original ranges")
    spec = importlib.util.spec_from_file_location("reviewed_annotation_roles", ADAPTER)
    roles = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(roles)
    cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    cs.detail = True
    checked = 0
    for q in v["ranges"]:
        records = q["instructions"]
        blob = bytes.fromhex("".join(i["bytes"] for i in records))
        start, end = int(q["start"], 16), int(q["end_exclusive"], 16)
        if not blob or len(blob) != end-start or hashlib.sha256(blob).hexdigest() != q["sha256"]:
            raise ValueError("empty/mixed original bytes")
        decoded = list(cs.disasm(blob, start))
        if len(decoded) != len(records) or sum(i.size for i in decoded) != len(blob):
            raise ValueError("incomplete/different instruction boundaries")
        for ins, record in zip(decoded, records):
            if (record["pc"], record["bytes"], record["mnemonic"], record["args"]) != (
                hex(ins.address), ins.bytes.hex(), ins.mnemonic, ins.op_str,
            ):
                raise ValueError("decoded annotation disagrees with bytes at " + record["pc"])
            memory = []
            for idx, operand in enumerate(ins.operands):
                if operand.type != X86_OP_MEM:
                    continue
                m = operand.mem
                base, index = ins.reg_name(m.base), ins.reg_name(m.index)
                memory.append(dict(
                    base=base, index=index, scale=m.scale, displacement=m.disp,
                    size=operand.size, role=roles.op_kind(ins, operand, idx),
                    rip_target=hex(ins.address+ins.size+m.disp) if base == "rip" else None,
                ))
            if record["memory"] != memory:
                raise ValueError("memory/address/access annotation disagrees at " + record["pc"])
            checked += 1
    if not checked:
        raise ValueError("zero annotation cases")
    return dict(
        status="VERIFIED_BYTE_ANNOTATION_AGREEMENT",
        instruction_records=checked, capstone=capstone.__version__,
        adapter_sha256=ADAPTER_SHA,
        validator_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
        limits="Retained bytes/annotation consistency only; not native effects, initialization, natural reachability or semantic acceptance",
    )
