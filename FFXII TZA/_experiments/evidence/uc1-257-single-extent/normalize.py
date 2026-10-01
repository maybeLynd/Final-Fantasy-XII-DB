"""Bounded extent normalization; input names cannot determine the byte count."""
def normalize(raw):
    obs = raw['observation']
    entry, length = int(obs['entry'], 16), obs['bytes']
    assert type(length) is int and length == 353
    assert entry == 0x712180 and int(obs['end'], 16) == entry + length
    assert len(bytes.fromhex(obs['raw_hex'])) == length
    flow = obs['flow']
    assert flow['full_linear'] and not flow['problems']
    assert len(flow['instructions']) == 82 and all(i[4] for i in flow['instructions'])
    assert flow['exits'] == [['0x7122e0', 'ret']]
    assert obs['short352']['flow']['problems']
    assert not obs['listed_entries'] and not obs['numeric_span_overlaps']
    assert raw['controls']['known-truncated-store48']['flow']['problems']
    assert not raw['controls']['known-complete-store57']['flow']['problems']
    return dict(method=raw['method'], reference=raw['reference'], verdict='PASS_BOUNDED_EXTENT',
        entry=hex(entry), bytes=length, end=hex(entry+length), reachable_instructions=len(flow['instructions']),
        unreachable_trailing_bytes='', external_or_indirect_exits=[],
        controls='Original353B complete;352B target cut and reused known48B cut rejected, known57B complete accepted by unchanged actualflow detector',
        limits='Only selected00712180; other49held rows notrun/classified. Calls not traversed; bothinternalconditional edges followed, no external/computedexit in selectedspan. Computed alternative entries/nativeABI/livein/semantics/normalreachability unresolved. Boundedextent notadmission/acceptance/population/parity; FABLErule/SPECcorroboration/FRONTIERGO stillrequired.',
        cleanup='Read-only canonical/image/tool inputs; ownW/E only. PC OFF/noFF12/input/memory/save/config/reference/peer writes; S19 budget unchanged/fullgoalNOT_MET')
