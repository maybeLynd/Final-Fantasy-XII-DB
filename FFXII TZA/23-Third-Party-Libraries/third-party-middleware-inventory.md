---
system: Third-party middleware inventory
category: 23-Third-Party-Libraries
status: DOCUMENTED - was REOPENED; both triggers (the 2026-09-02 census scope defect and CF-1's libxml2 reopening) are resolved, and a non-author falsification pass on 2026-10-01 CORRECTED the census totals at GN162 (EASTL 97, bare-name 136, total 827; ThirdParty 691 exact) with its regression applied (owner re-status 2026-10-01, OPUS, on SWE2-STRUCT's swe2struct-reopened3-0930)
owner_layer: CodeDomain:ThirdParty.* + the bare-name families Bullet.* / Lua.* / EASTL.*
evidence_tier: 2
verified_against:
  gzf_sha256: 2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9
  snapshot_sha256: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation across GN160 -> GN161 - the records this document rests on are unchanged except for `001E5C40`, `0029E3B0`, `002A5020`, `002A86A0`, `00573BE0`, which gained a plate comment and CodeDomain tags in batch R109 and lost nothing; voided by any delta that removes or rewrites a comment, tag, name, prototype or body range; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-02
audit:
  passes: 3
  last_pass: 2026-10-01
  last_pass_kind: falsification
  last_pass_state: swe2struct-falsification-2026-10-01 - tag census CORRECTED at GN162 (EASTL 97, bare-name 136, total 827; ThirdParty 691 exact); both triggers resolved; CF-2 corrected to G-23
  crossref_clean: true
  reopened_count: 2
function_families:
  - "libogg framing.c object | C | members/libogg-framing.tsv | 22 | Xiph libogg 1.3 framing.c, not FFXII code: the 22 census entries 007B9D70-007BA970, linked inside the SEAD span in alphabetical order of their libogg names. Identified body by body (sec. libogg): ogg_page_bos / continued / eos are the 11-byte header[5] tests for bits 2 / 1 / 4 (asserted byte-exact by 18-Audio/members/select_audio_libraries.py), ogg_page_checksum_set zeroes header bytes 22-25 and runs the CRC table 01CB5380, ogg_sync_pageseek 007BA7E0 compares the OggS capture pattern at 01CB5780, and allocation goes through the four _ogg_ hooks 01F41CF8-01F41D10 that SEAD's init 007A4D50 installs. Boundary: framing.c only; bitwise.c (oggpack, e.g. 0017CAE0), Tremor and vorbisfile are NOT covered"
  - "Tremor with vorbisfile.c | C | members/tremor-vorbisfile.tsv | 99 | Xiph Tremor, the integer Vorbis decoder, with its vorbisfile.c, statically linked beside SEAD, not FFXII code: every census entry in 007F41A0 up to 007F6FB0 (exclusive) (vorbisfile) and 007F7680 up to 007FFBC0 (exclusive) (decoder) less two entries since measured as A (007F41A0, 007F7FF0 - A beats a declaration, selector regenerated 2026-09-16) (18-Audio/members/select_audio_libraries.py). Identified by ov_pcm_tell / ov_raw_tell returning OV_EINVAL -131 below ready_state OPENED (byte-exact), the codec registry 01F41E58-01F41F60 whose three residue bundles share four functions and differ only in inverse (res0 / res1 / res2), the vorbis signature compare at 007F7FF0 and the integer MDCT. Closure control: no member is called from outside the object except by SEAD span bodies, and every entry is joined to the object by a call, lea, registry slot or _ogg_ hook. Boundary: the two ranges; the SEAD objects and MS ADPCM decoder between them (007F6FB0 up to 007F7680 (exclusive)), libogg bitwise.c (0017CAE0) and the unreached libvorbis at 0088xxxx are NOT covered 007FF1C0 left the family 2026-09-17, since measured as A (A beats a declaration). One member left the family on the 2026-09-17 re-sweep, since measured as A: 007F5CC0; a second, 007FE0F0, went A on the 2026-09-18 re-sweep. 2026-10-01 (OPUS for SWE2-EC7, A-drift round 5, record _index/candidates/opus-adrift-round5-1001): 3 member(s) left the family, since measured as A (A beats a declaration) after OPUS re-statused the third-party middleware inventory (6d9fb5a1f) DOCUMENTED; ../18-Audio/members/select_audio_libraries.py re-run on a clean HEAD export drops exactly these three and admits nothing; the members file is the selector's output; its other library files are unchanged; addresses and causing pages in the record."
  - "CRI HCA decoder | C | members/cri-hca-decoder.tsv | 53 | CRI Middleware HCA audio decoder, statically linked and driven by SEAD, not FFXII code: every census entry in 00121000 up to 00125740 (exclusive) (the start of .text) except the ICF-folded ret-0 body 001243B0 that FFXII code shares (18-Audio/members/select_audio_libraries.py). Identified by 00121DB0's reference to the Copyright (c) 2009-2010 CRI Middleware Co., Ltd. string at 01CBA610 and the tables that follow it, read by 00123140 / 00123250 / 001234A0; SEAD's Voice::Initialize, which emits the HCADecoder_ errors, is among its callers. Closure control: no member is called from outside the object except by SEAD span bodies; the next entry 00125740 is called from 0016xxxx and fails it. Boundary: the decoder bodies; SEAD's wrappers are NOT covered"
  - "libvorbis float codec | C | members/libvorbis.tsv | 115 | Xiph libvorbis, the floating-point Vorbis codec linked for the video audio path and REACHED FROM THE MOVIE PLAYER IN TWO HOPS (corrected 2026-09-16, OPUS, on FABLE-CONTRA-LIBVORBIS-IS-REACHED-BY-THE-MOVIE-PLAYER; the note previously read 'reached by nothing (CF-2)' and that was false - the chain is 001B7F30 -> 0067A480 -> 00679A50 -> 008800C0/00880AF0/00880BF0, each hop verified from edges.tsv, and 0067A480 is the movie player FR-1 names), not FFXII code: every census entry from 008800C0 up to 008958B0 (exclusive) less three A-measured entries and 00887630, which nothing references and no fingerprint identifies (18-Audio/members/select_audio_libraries.py). Identified by the 8-field codec registry at 01CEB070-01CEB190 whose three residue bundles share unpack / look / free_info / free_look and differ in class / forward / inverse, the vorbis signature compare at 008800C0, _float32_unpack 00882AC0 (mask 0x1FFFFF, exponent 0x3FF, bias -788) and its own const allocator slots 01CEB618-01CEB630 that only this object and bitwise.c use. Closure control: members are called only from the object and the three Boundary.Audio wrapper functions 00679600 / 00679A50 / 00679F40, and every member is joined by a call, lea, registry slot, allocator slot or bitwise.c call; the entry before, 00880020, is Bullet's and fails. Boundary: the object; its client wrappers at 0067xxxx and the CRT cosine after it (008958B0) are NOT covered 2 members left the family 2026-09-17, since measured as A (A beats a declaration): 008845A0 and one more, dropped by re-running 18-Audio/members/select_audio_libraries.py. 1 member(s) left the family 2026-09-20, since measured as A (A beats a declaration): 00893E80. 2026-10-01 (OPUS for SWE2-EC7, A-drift round 5, record _index/candidates/opus-adrift-round5-1001): 1 member(s) left the family, since measured as A (A beats a declaration) after OPUS re-statused the third-party middleware inventory (6d9fb5a1f) DOCUMENTED; ../18-Audio/members/select_audio_libraries.py re-run on a clean HEAD export drops exactly it and admits nothing; the members file is the selector's output; addresses and causing pages in the record."
  - "libogg bitwise.c object | C | members/libogg-bitwise.tsv | 4 | Xiph libogg bitwise.c as linked, not FFXII code: the four census entries from 0017C890 up to 0017CC70 (exclusive) - oggpack_write (bits over 32 rejected, buffer grown by 256 through the realloc slot 01CEB620), oggpack_look, oggpack_adv, oggpack_read - identified by the 33-entry mask table (1 << k) - 1 at 01CEB590 that look and read index (asserted by 18-Audio/members/select_audio_libraries.py). Callers are libvorbis and Tremor only; the neighbours fail the closure test (0017C2F0 is libvpx, 0017CC70 joins nothing). Boundary: the four bodies; the inlined or stripped rest of bitwise.c does not exist in the image"
  - "Bullet physics library | C | members/bullet.tsv | 467 | Bullet physics (collision, shapes, narrowphase, LinearMath hull library and the simulation island manager), statically linked, not FFXII code: every census entry from 00830760 up to 00861E90 and from 0087F180 up to 008800C0 less 64 already in OPUS's generated families, one entry whose RTTI is not Bullet's and two stubs called only from game code (members/select_bullet.py). Evidence: 276 entries at vtable slots of bt* classes or Bullet's helper structs; btCollisionWorld::updateSingleAabb 00840DF0 references Bullet's own 'Overflow in AABB, object removed from simulation' text with its continuousphysics.com address; the entries before the ranges are CRT (008306C0) and zlib (0087EBF0), the entry after the first is an import thunk. Controls: 20 outbound targets, all CRT and math imports except three LinearMath header bodies emitted into Phyre's physics object; inbound callers are Phyre's physics client (0068-006A), unwind thunks and game call sites (most into the excluded malloc stub); shared globals only the TLS index and a static zone. Boundary: the library bodies; Phyre's physics integration (PPhysics, 0069-006A) and the LinearMath bodies emitted there are NOT covered 5 members left the family 2026-09-17, since measured as A (A beats a declaration): 0084B320 and four more, dropped by re-running members/select_bullet.py. A further member left on the same-day re-sweep: 00837880, A-measured; another, 0083F850, went A on 2026-09-18. 1 member(s) left the family 2026-09-20, since measured as A (A beats a declaration): 00861D30. 5 member(s) left the family 2026-09-29, since measured as A (A beats a declaration), after 08afb6b02 re-statused their citing page DOCUMENTED: removed by re-running members/select_bullet.py, which drops exactly these five and admits nothing (identical on a clean extract of HEAD); addresses in _index/candidates/ec7-family-ruling-exec-0929 (SWE2-EC7)."
  - "Lua 5.2.1 library | C | members/lua.tsv | 600 | PUC-Rio Lua 5.2.1, statically linked C, not FFXII code: every census entry from 0080F2E0 up to 00830760 (exclusive) less 13 in OPUS's Lua math-adapter family and 5 A-measured (members/select_lua.py). Cardinality went 606 -> 605 on 2026-09-13 when FABLE's luaL_testudata/lua_settop reading made 00811130 A-measured; A beats a declaration, so the selector's own A-exclusion moved it out. The family was REFUSED in between, which is the checker working, not a regression. Evidence: the '$LuaVersion: Lua 5.2.1 Copyright (C) 1994-2012 Lua.org, PUC-Rio' banner heads its string pool 01CCA080-01CCD37F, 303 entries reference that pool, luaopen_base 00814F90 leas 'Lua 5.2' and '_VERSION'; no entry carries RTTI and every entry is joined to the object by a call, lea, table slot or pool reference. Edges: zlib (crc32_z 0080E910) and four import thunks below, Bullet (00830760, called from Bullet) above, the pool's end marked by Bullet's serialisation names. Controls: 29 outbound targets, all CRT and math imports (longjmp among them) or inlined printf wrappers; 32 entries are called from outside, the Lua API, by the Phyre scripting bindings; no .data global is shared with outside code. Boundary: the interpreter, compiler and standard libraries; the Phyre binding layer and FFXII's loader are NOT covered One member left the family 2026-09-17, since measured as A: 008216A0, dropped by re-running members/select_lua.py; two more, 008162F0 and 00827600, went A on the 2026-09-18 re-sweep."
  - "zlib 1.2.11 | C | members/zlib.tsv | 54 | zlib 1.2.11 (Gailly and Adler), statically linked, not FFXII code: every census entry from 0080C5A0 up to 0080F2BC (inflate side) and from 0087AF40 up to 0087F180 (deflate side) less one entry in OPUS's forwarder family (members/select_zlib.py). Evidence: both version banners; inflate 0080C750 references 'incorrect header check'; uncompress 0080C5A0 is the 24-byte shim into uncompress2; crc32 and adler32 are 'mov r8d,r8d; jmp' widening shims into their _z bodies; the deflate side calls the inflate side's checksums 14 times, so the two ranges are one library. Edges: ATL below the first range, import thunks at both other edges, Bullet above the second. Controls: outbound only memcpy and memset; inbound only uncompress from 0019AA20 and the save reader 00865D90, and compress2 from the save writer 00866200; no shared .data. Boundary: zlib bodies only; the save container code that drives them is NOT covered. 2026-09-18: 57→56 - 0080C750 (stock inflate(), interior-read by SWE2-FRONTIER 2026-09-17) is now measured as A (A beats a declaration). 2026-09-30 (SWE2-EC7, DD re-status A-drift, record _index/candidates/ec7-dd-adrift-pairing-0930): 1 member(s) left the family, since measured as A (A beats a declaration) after OPUS re-statused the save-image buffers page (e696ef86e) DOCUMENTED; the selector re-run on a clean HEAD export drops exactly these and admits nothing; the members file is the selector's output; addresses and causing pages in the record. 2026-10-01 (OPUS for SWE2-EC7, A-drift round 5, record _index/candidates/opus-adrift-round5-1001): 1 member(s) left the family, since measured as A (A beats a declaration) after OPUS re-statused the third-party middleware inventory (6d9fb5a1f) DOCUMENTED; members/select_zlib.py re-run on a clean HEAD export drops exactly it and admits nothing; the members file is the selector's output; addresses and causing pages in the record."
  - "libvpx VP8 decoder object | C | members/libvpx-vp8-decoder.tsv | 116 | libvpx 1.6.0 (WebM Project), its VP8 decoder object, statically linked, not FFXII code: census entries from 0016DDD0 up to 0017C890 joined to the decoder - reached from the entries that reference its string pool or carry the LibVPX tag, held in its interface or control-map tables, or called only by the video client - less the folded return-4 body 0016EE70, the sprintf wrapper 001744F0 (now declared by the MSVC runtime tail row), and three entries since measured as A (0016EEC0, 0016FE80, 00174790 - A beats a declaration, selector regenerated 2026-09-16) (members/select_libvpx.py). Fingerprint: vpx_codec_vp8_dx_algo at 01CDB290 names 'WebM Project VP8 Decoder v1.6.0', ABI 5, and holds init / destroy / peek / get_si / decode / get_frame inside the range; its control map 01CDB320 carries ids 1-7 and 0x100-0x103. Controls: inbound callers only the video client at 0067xxxx; outbound only CRT and the decoder's own assembly DSP kernels. Boundary: the C decoder object; those kernels (00125740-00129xxx, 001481D0-0014Cxxx, 00158B40..) and the client are NOT covered One member left on the same-day re-sweep: 0016E4A0, A-measured. 2 member(s) left the family 2026-09-29, since measured as A (A beats a declaration); every removed address and its reason is in _index/candidates/ec7-refused-family-repair-0929/removed-members.tsv. Re-derived by re-running members/select_libvpx.py, which now leaves the UC-1 frontier bodies out of its population (UC-1 series break 2026-09-28); its output equals this file and leaves the DSP kernel list unchanged."
  - "libvpx VP8 decoder object, UC-1 bodies in its span | C | members/libvpx-vp8-decoder-uc1.tsv | 4 | not this game's code: libvpx 1.6.0 decoder bodies, declared apart from the parent row under FABLE family ruling R1 (4e32dd8df) by SWE2-EC7, record _index/candidates/ec7-uc1-span-rows-0929. 4 UC-1 bodies admitted to frontier 2026-09-28, dispositioned by span 2026-09-29. TEST 1: strictly inside 0016DDD0 up to 0017C890 between listed decoder members. TEST 2: select_libvpx.py re-run with them in its population admits all 4, its interface-table and control-map assertions and the DSP-kernel fixpoint hold, and its outbound and inbound controls are unchanged. TEST 3: each is held in the decoder's control map at 01CDB320 (the documented vpx_codec_control entry mechanism the parent row names), one is also branched to from inside the span, and none reaches anything outside the span that the listed members do not. Generator: _index/candidates/ec7-uc1-span-rows-0929/uc1_span_tests.py --write."
  - "libvpx VP8 DSP kernels | C | members/libvpx-vp8-dsp-kernels.tsv | 63 | libvpx 1.6.0 VP8 DSP kernels (hand-written SIMD assembly and intrinsics the decoder dispatches to), not FFXII code: every census entry outside the decoder object whose every direct caller and every lea referencer is a member of the libvpx VP8 decoder row or another such kernel, iterated to a fixpoint, held in no .rdata or .data table and not an import thunk (members/select_libvpx.py) - 27 at 00125740-00128FB3 directly after the CRI HCA decoder, one at 00133B40, 32 at 001481D0-0014C221, two at 00158B40 / 00158C09. Regenerated 2026-09-16: 001294D0 left as A-measured, and 001292C0/00129312/001297DE lost their only member referencers in the same pass (cascade, not position). The runtime-dispatch setup 0016F080 leas four of them. Control: the same rule rejects every CRT body the decoder also calls, because other code references those too. Boundary: kernels with no reference at all (e.g. 001274D0, 00129870, 0012A290) are NOT covered; their attribution would rest on position alone 2 members left the family 2026-09-17, since measured as A (A beats a declaration): 00149DC0 and one more, dropped by re-running members/select_libvpx.py. On the same-day re-sweep the decoder-object rule was repaired: members whose only referencers had drifted to A *inside the decoder object* came back, restoring 001292C0/00129312/001297DE (+3)."
  - "libwebm mkvparser | C | members/libwebm-mkvparser.tsv | 104 | WebM Project libwebm mkvparser (the Matroska/WebM container parser), statically linked, not FFXII code: every joined census entry in the contiguous run 007FFBC0 up to 00808888 (exclusive) - ending where the import-thunk field begins - plus the three vtable bodies the linker scattered into the audio region (007AD440 Track::EOSBlock, 007BD590 SimpleBlock, 007E3260 BlockGroup), each carrying mkvparser:: RTTI (members/select_mkvparser.py). Fingerprint: the eight mkvparser:: class vtables 01CC6A68-01CC6B28 and IMkvReader 00D89AE0, and the Matroska element IDs compiled into the parse switch (18538067 Segment, 114D9B74 SeekHead, 1654AE6B Tracks, 1F43B675 Cluster, 1C53BB6B Cues, 1043A770 Chapters, 1254C367 Tags, 4DBB/53AB/53AC Seek); no mkvmuxer:: RTTI exists, so only the parse side is linked. The count went 100 -> 105 under FABLE's T2 adjudication (FABLE-ADJ-MKV): the five destructor bodies 007FFCD0-00800150 are reached only through unwind funclets 008A5B30-008A5B70 whose FuncInfos (01CC6880/858/830/8A8/8D0) hang off MEMBER frames (008041F0, 00804860, 00804BE0, 00804CF0, 00807650) - the selector now walks .pdata -> UNWIND_INFO -> FuncInfo -> unwind-map action RVA -> funclet mechanically. Controls: inbound only the video client at 0067xxxx (25 call sites into the public API and member getters); outbound only CRT (free/delete, memcpy, the eh_vector iterators, the security cookie, _guard_check_icall). NOT covered: the game's IMkvReader implementation and movie client (VbfMkvReader / WebM_VbfMkv.Runtime at 006Cxxxx and 001Bxxxx), the shared CRT tail 00808850 called by _Facet_Register (declared by the MSVC runtime tail row), the _purecall stub 00861EC6, the folded bodies already dispositioned elsewhere (00800140, 008005C0/008006D0/00800710, 007B6C40), the two A-measured bodies 00801210/00806F20 and IMkvReader's deleting destructor 006CC9F0 (also A-measured). 2026-09-18: 105→104 - 00801550 has since been measured as A (A beats a declaration)."
  - "MSVC runtime tail | C | members/msvc-runtime-tail.tsv | 52 | Microsoft Visual C++ runtime residue (vcruntime/CRT + ATL), statically linked into the game, not FFXII code: the joined census entries 008087C4 up to 0080C5A0 (exclusive) - less 23 A-measured bodies, the two declared NativeAdapter bodies, the 20 declared basic_streambuf import thunks 00808888-008088FA and the three declared tail-call forwarders - plus 14 stdio members the linker scattered through .text as COMDATs (members/select_msvc_runtime.py). Evidence: census names are used only where the body matches - 00808C90 is the __scrt_common_main_seh sequence (_set_app_type, _configure_narrow_argv, _initialize_narrow_environment, __setusermatherr, atexit); 00808C64 installs type_info::vftable; a qword to 00808D5C sits at .rdata 008C31D8 inside the _initterm range 008C31D0-008C5678 walked by A-measured 00808D78; 00809B44 leas 00809B54 (the 0xE06D7363 'msc' filter) into SetUnhandledExceptionFilter; A-measured 00809124 registers 00809244 through atexit; the vdecl math kernels 0080A270/0080A720/0080AFE0 are reached only through the declared thunk block inside 00809920's slot; the CAtlBaseModule trio 0080C440-0080C51C ends the block. COMDAT rule: a scattered body joins only when its ENTIRE callee set is __local_stdio_printf_options 0016D670, __stdio_common_* / __acrt_iob_func thunks and already-declared thunk entries - 005CDAA0 (16 KiB format buffer, then a virtual logger dispatch) fails and stays game code. Controls: outbound targets are the shared allocator 00210EC0, memset/free thunks, CRT config imports and the game-side entry/init bodies the CRT startup invokes; inbound callers span the whole image - CRT leaf utilities are universal; no member is admitted on position alone. NOT covered: 008098D4 the shared allocator adapter (mkvparser members and game code call it - no runtime-exclusive witness), the post-thunk strays 00861EAE-008620E0 including the FFXII-authored exit stub 008620C0, the 23 A-measured bodies inside the block Two members left the family on the 2026-09-17 re-sweep, since measured as A: 0080A270 and 0080B8A0."
  - "JsonBox JSON library | C | members/jsonbox.tsv | 54 | JsonBox (anhero/JsonBox), the JSON Value/Object/parser/serializer object linked for the game's JSON consumers, statically linked, not FFXII code: census entries in the two link runs 001FE0E0 up to 00202B10 (exclusive) and 002161C0 up to 00216540 (exclusive) joined to the object by a call or lea edge, with every external caller in the 001Cxxxx JSON-client band or a declared/EH/static-life convention (members/select_jsonbox.py). Evidence: RTTI names JsonBox::OutputFilter<JsonBox::VSolidusEscaper / VIndentCanceller / VIndenter> whose vtables at 00905070 / 009050F0 / 00905170 are basic_streambuf-derived and carry JsonBox-specific bodies only at slot 0 (deleting destructors 001FF930/001FF870/001FF8D0) and slot 3 (the write overrides 002016F0/00201690/002016C0) - slot 6 is 00660570, ICF-folded across hundreds of Phyre descriptor vtables, and is NOT a member - plus the upstream Value.cpp error-literal pool 00904FE8-00905038 ('Expected '\"', got '', 'Expected a digit, '.', 'e' or 'E', got '') referenced only by members 002008F0/00201890/00201C40/00201EB0, and nine bodies that lea the vtables. Controls: 26 distinct inbound client callers, all in 001Cxxxx (Presentation/ItemsEquipment JSON consumers), plus four convention callers (declared EH wrappers 001FE990/001FEA00, static-lifetime bodies 008A6E90/008A6F10); excluded inside the runs: declared bodies 001FE990/001FEA00/002164D0 and seven bodies joined by nothing; positive rejections 002164D0 (PhyreCore-declared) and 00660570 (ICF-folded). Edges: 001FE080 below is A-measured Presentation.EffectFont, 00202B10 above is foreign SIMD called from outside; 00216160 below the helper island is A-measured, 00216540 above is declared PhyreCore. Boundary: the member bodies; the 001Cxxxx client bodies, the declared PhyreCore filter-policy helpers and the shared basic_streambuf slots are NOT covered. 2026-09-30 (SWE2-EC7, DD re-status A-drift, record _index/candidates/ec7-dd-adrift-pairing-0930): 2 member(s) left the family, since measured as A (A beats a declaration) after OPUS re-statused the EASTL strings page (8c8406bfd) and the CL2 menu colour tables page (9bda44687) DOCUMENTED; exact A removal. select_jsonbox.py did not re-run then (it excluded rows named 'JsonBox' rather than this row's name, and treated the two departed bodies, which call members from inside the runs, as foreign callers); repaired later the same day under FABLE's accounting-state ruling (record _index/candidates/ec7-accounting-predicate-audit-0930): the row name is matched and A status no longer feeds its predicate, and its re-run on a clean HEAD export reproduces this file exactly; addresses and causing pages in the record. 2026-10-01 (OPUS for SWE2-EC7, A-drift paired with owner re-status batch 19, record _index/candidates/opus-dd-restatus-19-1001): 1 member(s) left the family, since measured as A (A beats a declaration) after OPUS re-statused the @FTR node table page DOCUMENTED (owner batch 19); exact A removal in the same publish (select_jsonbox.py does not re-run at HEAD, as EC7 recorded); addresses and causing pages in the record."
  - "Dear ImGui context object | C | members/imgui.tsv | 9 | Dear ImGui (ocornut), a minimal dormant context object shipped in the retail build, not FFXII code: census entries in the four runs 00791D80 up to 00792350, 00795F10 up to 00796180, 00796E70 up to 007973D0 and 00798D70 up to 00798E90 joined to the object by a call or lea edge, called by nothing outside declared static-init and atexit-teardown stubs (members/select_imgui.py). Evidence: 00791D80 is ImGuiIO::ImGuiIO() - memset 0xB88, IniFilename 'imgui.ini' (01CB3990) and LogFilename 'imgui_log.txt' (01CB39A0) stored at +0x10/+0x18, the upstream default constants (DeltaTime 1/60, IniSavingRate 5.0, MouseDoubleClickTime 0.3, MouseDoubleClickMaxDist 6.0) and the three default platform-callback bodies 00796E70/00798D70/00797360 stored at +0xA0/+0xA8/+0xC0. Controls: the only inbound callers are conventions - the A-measured static-object ctor 00791E70 and the declared atexit teardown 008B7D40 - so the object is dormant, no live caller; outbound targets are four CRT bodies; the foreign Input body 00796FC0 inside run 3 is the positive rejection; .data globals touched are the allocator table 01F40380, the context global 02EA54F0 and two more. Edges: 00791CD0/00792350 (Phyre.Reflection, Phyre.Framework), 00795DC0/00796180, 00796E30/007973D0, 00798AC0/00798E90 - all independently non-ImGui. Boundary: the member bodies; the Phyre wrapper PImGuiDynamicMesh (vtable 01CB3950), the static-init/teardown machinery and the shared globals are NOT covered. 2026-10-01 (OPUS for SWE2-EC7, A-drift round 5, record _index/candidates/opus-adrift-round5-1001): 1 member(s) left the family, since measured as A (A beats a declaration) after OPUS re-statused the third-party middleware inventory (6d9fb5a1f) DOCUMENTED; exact A removal. select_imgui.py does not re-run at HEAD: it asserts the departed context-object body is a member, so its assertion has to admit an A body before the selector can reproduce this file - recorded as follow-up work; addresses and causing pages in the record."
---

# Third-party middleware inventory

> FFXII: The Zodiac Age is built from **at least twelve third-party libraries** totalling ~~**801**
> tagged functions~~ **827** tagged functions in the certified parent's tag census *(corrected 2026-10-01,
> SWE2-STRUCT for OPUS: §2's corrected totals)* — including a **commercial post-effect middleware that checks a licence expiry
> date every time the game starts**.

> **REOPENED 2026-09-02 — this document's census had a scope defect.** It counted the
> `CodeDomain.ThirdParty.*` tag family and reported the result as the inventory of third-party code.
> **111 further functions carry bare-name library tags** (`EASTL.*` 72, `Lua.*` 21, `Bullet.*` 18)
> with no `ThirdParty` token at all, so the census could not see them — and **EASTL, a twelfth
> library, appeared nowhere in this document** even though this category's own `README.md` names it
> as a classification source. Falsification pass 3 in section 11. The `ThirdParty.*` figures below
> remain exact for that family; the totals and the library list did not.

## 1. What the player sees

Nothing directly, but almost every part of the experience is somebody else's code.

The cinematics play through a video codec. The music streams through an audio codec. Physics
objects tumble through a physics library. The bloom and lens effects come from a bought-in
post-processing package. The engine even embeds a full scripting language.

The one place this nearly becomes visible is a failure message the developers left in:

```
[YEBIS]Yebis Enable Failed!!!
The YEBIS library passed over the expiration date : %s
```

**A licensed component in the shipping game can refuse to start.** If that ever fired, the player
would simply see the game render without its post-effects.

## 2. Native mechanism

### The inventory — the `ThirdParty.*` tag family, 691 functions

**This is one of two tag families.** It is complete and exact for itself; the bare-name families
follow below and bring the true total to ~~802~~ **827** *(corrected 2026-10-01, SWE2-STRUCT for OPUS: GN162 tag census, checks N3-N5)*.

> *GN161 note, 2026-09-14: R109 added one `ThirdParty.XML.ConfigParse` member — the tag family
> is now 691 and the true total ~~802~~. The per-library table below is otherwise unchanged; the new
> member is an XML-family function, not assigned to a named library row pending identification.*
> *Corrected 2026-10-01 (SWE2-STRUCT for OPUS): at the certified GN162 parent the true total is 827.
> 25 functions were re-tagged from `CxxStandardLibrary.OrderedContainerRuntime` to `EASTL.OrderedContainerRuntime`
> (checks N3-N5). The 691 and every row of the table below re-measure exactly (check N2).*

| Library | Functions | Purpose |
|---|---:|---|
| **PPFX** | 348 | post-processing framework |
| **Bullet** | 120 | rigid-body physics |
| **libvpx (VP8 1.6.0)** | 73 | video **decoding** — the decoder only |
| **Lua 5.2.1** | 90 | embedded scripting |
| **zlib 1.2.11** | 25 | compression |
| **libvorbis** | 11 | audio decoding |
| **Dear ImGui** | 7 | debug UI |
| **Tremor** | 4 | integer-only Vorbis decoder |
| **libxml2** | 4 | XML parsing — **withdrawn 2026-09-12 (CF-1):** the four tagged functions carry no libxml2 evidence; see the reopened section |
| **JsonBox** | 4 | JSON parsing |
| **YEBIS** | 3 | commercial post-effects |
| **zlib adapter** | 1 | `0080C5A0`, a 24-byte shim; distinct tag from zlib proper — *corrected 2026-09-13: it is zlib's own `uncompress` (§zlib 1.2.11 below)* |
| **Subtotal — `ThirdParty.*`** | **691** | exact for this tag family |

**Corrected 2026-09-02.** This table previously read Bullet 119, libvpx 70, no zlib-adapter row, and
a `(audit-tag residue) 5` line. The total was right; the attribution was not — see section 10.

### The bare-name families the census above could not see

Measured 2026-09-02 against a freshly regenerated `DumpFullCoverageGraph.java` at the GN checkpoint
(38,161 rows, 0 duplicate entry addresses). Every function below carries a **single** tag in a
bare-name namespace and **no `ThirdParty` token**, which is exactly why a `ThirdParty.*` census
returns none of them:

| Library | Functions | Breakdown |
|---|---:|---|
| **EASTL** | ~~**72**~~ **97** | `BasicString` 58, `ContainerRuntime` 14, `OrderedContainerRuntime` 25 *(corrected 2026-10-01, SWE2-STRUCT for OPUS: GN162 tag census, checks N3-N5)* |
| **Lua** (additional) | **21** | `Math` 15, `Runtime` 4, `StringPattern` 2 |
| **Bullet** (additional) | **18** | `Collision` 11, `Dynamics` 5, `Physics` 1, `LinearMath` 1 |
| **Subtotal** | ~~**111**~~ **136** | |

*Re-measured 2026-10-01 (SWE2-STRUCT for OPUS) at the certified GN162 parent with the same selector.* The 2026-09-02
export reproduces this table's original figures exactly (check N1, the control). At GN162 the only change is EASTL:
- the 25 `OrderedContainerRuntime` rows are re-tags of functions that were `CxxStandardLibrary.OrderedContainerRuntime.*`
  at GN, among them the red-black insert `0016D840` of [the ordered-container page](../24-Compiler-And-CRT-Runtime/Cxx-Runtime-Families/the-ordered-container-runtime.md)
  (check N4);
- that page identified the tree as EASTL's on 2026-09-15.

### Corrected totals

| Library | `ThirdParty.*` | bare-name | **True total** |
|---|---:|---:|---:|
| Bullet | 120 | 18 | **138** |
| Lua | 90 | 21 | **111** |
| **EASTL** | 0 | ~~72~~ 97 | ~~**72**~~ **97** |
| all others | 481 | 0 | 481 |
| **Total** | **691** | ~~**111**~~ **136** | ~~**802**~~ **827** |

*(Corrected 2026-10-01, SWE2-STRUCT for OPUS: GN162 tag census, checks N3-N5)*

**EASTL — Electronic Arts' STL — is the twelfth library**, and it was missing entirely. It is
unambiguously third-party, this category's `README.md` already lists it as a classification source,
and `_index/EVIDENCE-STANDARD.md` cites `std/EASTL mangled names` as tier-3 evidence. Its 58
`BasicString` functions are the largest single bare-name group in the image.

Note that 58 EASTL static initializers are already analysed in
[`../24-Compiler-And-CRT-Runtime/Static-Initialization-And-Lifetime/static-initialization-order-and-injection-timing.md`](../24-Compiler-And-CRT-Runtime/Static-Initialization-And-Lifetime/static-initialization-order-and-injection-timing.md)
as contributors to the static-init table. That is a different question — *when they run* — and does
not constitute a library document. EASTL still owes one.
*(Pointer 2026-10-01 (SWE2-STRUCT for OPUS): the library document exists,
[EASTL strings, containers and the logging allocator](EASTL/eastl-strings-containers-and-the-logging-allocator.md).)*

Versions are pinned in the GFZ tags where the evidence supported it: `LibVPX_VP8_1_6_0`,
`Zlib_1_2_11`. Lua's version is established at **5.2.1** from its own authored banner.

### YEBIS — commercial middleware with an expiry check

Authored strings, verbatim:

```
EnableYebis
Yebis enable: 
[YEBIS]Yebis Enable Failed!!!
YEBIS DOF Info: 
YEBIS DOF Info (2ndScreen): 
YEBIS_D3D11
FeatureId = YEBIS_D3D11, BeginYear = 0, BeginMonth = 0, BeginDay = 0, EndYear = 0, EndMont...
.................. YEBIS Expiration Problem ...............
YEBIS Expiration Problem
The YEBIS library passed over the expiration date : %s
```

And two RTTI class names in a `Yebis` namespace:

```
.?AVYebisPfxMemoryAllocatorD3D11@Yebis@@
.?AVPfxShimD3D11@Yebis@@
```

Three things this establishes:

**YEBIS is genuinely linked, not a leftover.** It has RTTI classes, a D3D11 memory allocator, and
GFZ-tagged functions (`Rendering.Yebis.YebisPfxMemoryAllocatorD3D11.TrackedAllocate` /
`.TrackedFree`).

**It carries a feature-licence record** with Begin/End year-month-day fields. The retail values
visible in the format string are **all zero**, which for a licence window conventionally means
*no expiry* — so the check exists and passes. That reading is not proven; see **X-2**.

*Answered 2026-09-14 (FABLE), X-2:* **no expiry, and by an explicit branch rather than by the
convention.** The verifier `006DFF40` checks the decoded licence in `0071D9E0`: the six signed date
fields must equal the plain-text ones or the licence is *not valid*; when all six are zero it jumps
**past the date test** to success (`0071E0F4`–`0071E11A`); otherwise it compares `_time64` against
a `_mktime64` window (begin 00:00:00, end 23:59:59) and sets *expired*. The shipped record is all
zeros, so it takes the first path. The sentence above is kept as the limit it was when written.

**It owns depth of field.** `YEBIS DOF Info` explains the `mDofApertureFnumber` parameter found in
the render-parameter document: YEBIS models a physical camera lens, which is why FFXII's DOF is
parameterised by f-number rather than blur radius.

The `(2ndScreen)` variant indicates a second render target — consistent with the `_2ndScreen.json`
config and the `2ndScreen` string found alongside it.

### Two Vorbis decoders

Both `libvorbis` (11 functions, including `VorbisSynthesisBlockin`) and **Tremor** (4 functions:
`VorbisApplyWindow`, `MdctBackward`, `MdctBitreverse`, `MdctButterflyGeneric`) are present.

Tremor is the **integer-only** Vorbis decoder, written for platforms without fast floating point.
Its presence in a PC build is a strong sign of **console heritage carried forward** — the same
pattern as the `PS2DepthOfField.fx` shader name.


### libogg — a library this inventory did not list, found inside the SEAD span (2026-09-13, FABLE)

**Correction to the library count.** Neither **libogg** nor the **CRI HCA decoder** appears in the
tables above — neither carries a `ThirdParty.*` or bare-name tag; both were grouped under the topic tag
`Audio`. The lead's "at least twelve" remains true as a lower bound; the two are recorded here, and
the audio split as a whole is on [SEAD function identification §13](../18-Audio/sead-function-identification.md).

**libogg 1.3 `framing.c` is the 22 census entries `007B9D70`–`007BA970`** (EC-7 letter C, frontmatter
`function_families`, selector `18-Audio/members/select_audio_libraries.py`). The linker placed them in
**alphabetical order of their libogg names**, which the identifications confirm end to end:

| Entry | libogg function | Identifying body |
|---|---|---|
| `007B9D70` | `_os_body_expand` | reallocates through the `_ogg_realloc` hook |
| `007B9DE0` | `_os_lacing_expand` | reallocates two arrays through the same hook |
| `007B9E70` | `_packetout` | the common body of the two wrappers below |
| `007B9F70` | `ogg_page_bos` | `mov rax,[rcx]; movzx eax,byte [rax+5]; and eax,2; ret` |
| `007B9F80` | `ogg_page_checksum_set` | zeroes header bytes 22–25, CRC over header and body with the table at `01CB5380` |
| `007BA050` | `ogg_page_continued` | the same 11-byte body with `and eax,1` |
| `007BA060` | `ogg_page_eos` | … with `and eax,4` |
| `007BA070` | `ogg_page_granulepos` | assembles header bytes 6–13 into 64 bits |
| `007BA0D0` | `ogg_page_serialno` | assembles header bytes 14–17 |
| `007BA100` | `ogg_stream_clear` | frees body, lacing and granule arrays through `_ogg_free` |
| `007BA160` | `ogg_stream_init` | `memset`, three allocations |
| `007BA230` / `007BA250` | `ogg_stream_packetout` / `ogg_stream_packetpeek` | tail-call `_packetout` with advance 1 / 0 |
| `007BA270` | `ogg_stream_pagein` | the 897-byte page absorber, `memcpy` |
| `007BA600` / `007BA650` | `ogg_stream_reset` / `ogg_stream_reset_serialno` | identical resets, the second also stores the serial at `+0x160` |
| `007BA6A0` | `ogg_sync_buffer` | malloc / realloc / free through the hooks |
| `007BA770` | `ogg_sync_clear` | one free |
| `007BA7B0` | `ogg_sync_init` | zeroes the four-field sync state |
| `007BA7E0` | `ogg_sync_pageseek` | compares the `OggS` capture pattern at `01CB5780` |
| `007BA950` | `ogg_sync_reset` | `storage < 0` check, then zeroes fill / returned / unsynced |
| `007BA970` | `ogg_sync_wrote` | `fill + bytes > storage` → −1 |

**Allocation is re-plumbed.** libogg's `_ogg_malloc` / `_ogg_calloc` / `_ogg_realloc` / `_ogg_free` are
the four function pointers `01F41CF8` / `01F41D00` / `01F41D08` / `01F41D10`, statically initialised to the CRT `malloc` /
`calloc` / `realloc` / `free` and overwritten by SEAD's
init `007A4D50`; Tremor and `vorbisfile` (`007F41A0` onward) call through the same four.

**Correction to CF-2 above (2026-09-12, FABLE's own answer).** That answer called `007F8220`,
`007F8600`, `007F8FD0` "driver functions" and the table at `01F41E58` the driver's decoder core, and
said the 62-function upward closure lies "all inside the sound driver". **The lower part of that
closure is Xiph code linked beside SEAD, not SEAD:** `007F41A0`–≈`007FF1C0` is Tremor (`vorbisfile.c`,
then the decoder; `007F7FF0` checks the `vorbis` signature), and the table at `01F41E58`–`01F41F60` is Tremor's own
codec registry — `01F41E58` is `_mapping_P`, pointing at the mapping0 bundle `01F41F40` (unpack `007FDA10`,
look `007FD880`, free_info `007FD780`, free_look `007FD7B0`, inverse `007FDC60`); the three residue bundles at
`01F41EC8` / `01F41EF0` / `01F41F18` share unpack `007FCD80`, look `007FCF80`, free_info `007FCC80` and free_look
`007FCCB0` and differ only in inverse (`007FD190` / `007FD200` / `007FD270`) — exactly `res0` / `res1` / `res2`;
the floor bundles start at `01F41E60` and `01F41E98`. **The conclusion stands** — Tremor is the wired-in
decoder, reached from the SEAD stream vtables `01CB9130` / `01CB90D8` / `01CB92B8` / `01CB92D8` /
`01CB92C0`, which are SEAD; libvorbis is unreached — only the attribution of the path's lower half is
corrected. ~~**Not yet declared:** Tremor / `vorbisfile` and the CRI HCA decoder, whose exact object
boundaries are still open;~~ *Both declared the same day, next section;* `bitwise.c` (`oggpack_*`, e.g. `0017CAE0`) is not in this row.


### Tremor with `vorbisfile.c`, and the CRI HCA decoder — declared (2026-09-13, FABLE)

The two objects §libogg left open now have exact boundaries (EC-7 letter C, frontmatter
`function_families`; both lists regenerate from `18-Audio/members/select_audio_libraries.py`, which
asserts every fingerprint below).

**Tremor, 106 members — `007F41A0` up to `007F6FB0` (exclusive) (`vorbisfile.c`) and `007F7680` up to `007FFBC0` (exclusive) (the decoder).**

| evidence | where |
|---|---|
| `ov_pcm_tell` / `ov_raw_tell`: `cmp [rcx+0x80], 2` / `mov rax, -131` / return `+0x78` or `+0x10` — Tremor's `OV_EINVAL` below `ready_state` `OPENED` (byte-exact) | `007F6280`, `007F6730` |
| `ov_open_callbacks`, `ov_pcm_seek`, `ov_read` — the three the SEAD voice code calls (`ov_read` reaches `_fetch_and_process_packet` `007F4710` and the synthesis pcmout / read pair `007F8EE0` / `007F8F60`) | `007F5970`, `007F59C0`, `007F6750` |
| `_bisect_forward_serialno` — the first `vorbisfile` body, self-recursive, driving libogg's `ogg_page_serialno` / `ogg_sync_pageseek` | `007F41A0` |
| the `vorbis` signature compare of the header parser | `007F7FF0`, `007F8140` → `01CEBB50` |
| the codec registry: `_mapping_P` at `01F41E58` → mapping0 `01F41F40`; three residue bundles at `01F41EC8` / `01F41EF0` / `01F41F18` sharing unpack `007FCD80`, look `007FCF80`, free_info `007FCC80`, free_look `007FCCB0`, differing only in inverse `007FD190` / `007FD200` / `007FD270` — `res0` / `res1` / `res2`; floor bundles from `01F41E60` and `01F41E98` | `.data` |
| `qsort` comparators passed by `lea` (`sharedbook`'s from `007F9EC0`, `floor1`'s from `007FBF00` / `007FC320`) | `007FA650`, `007FCB30` |
| the integer MDCT the classifier did tag (`VorbisApplyWindow`, `MdctBitreverse`, `MdctButterflyGeneric`, `MdctBackward`) | `007FB180`–`007FFBB8` |

**What sits between the two ranges is not Tremor:** `007F6FB0` is a **Microsoft ADPCM block decoder**
(the standard adaptation table 230 … 768 and coefficient pairs 256/0, 240/0, 460/−208, 392/−232 are
loaded as immediates and constants; samples per block `2 × align / channels − 12`, the same formula as
the helper `007F7350`), called only by SEAD's voice code `007EAA60`; then SEAD's own `SoundObject`
vtable installers and methods and three SSE geometry helpers (`007F7360`–`007F7570`, [SEAD §13](../18-Audio/sead-function-identification.md)).
~~These 14 entries stay undeclared~~ *Corrected 2026-09-13: the gap is 11 entries, not 14.* The nine SEAD ones are now declared on the SEAD row (RTTI and only-caller evidence, [SEAD §13](../18-Audio/sead-function-identification.md)); the ADPCM decoder `007F6FB0` and its helper `007F7350` stay undeclared, because their upstream — SEAD's or a third party's — is not
established.

**The CRI HCA decoder, 53 members — `00121000` up to `00125740` (exclusive), the first bytes of `.text`,** less `001243B0`,
a 3-byte `ret 0` that identical-code folding shares with FFXII's own code. `00121DB0` references
`Copyright (c) 2009-2010 CRI Middleware Co., Ltd.` at `01CBA610`; `00123140`, `00123250` and `001234A0`
read the tables stored immediately after it; SEAD's `Voice::Initialize` `007EBAD0` — the function that
emits every `HCADecoder_*` diagnostic — and the voice functions `007EAA60`, `007ED580`, `007DC730`–
`007DD040`, `007EDE90`, `007EE500` are its callers.

**Closure control, for both.** No member is called directly from anywhere except its own object and
SEAD's span, and every entry is joined to its object by a call, a `lea`, a registry slot or an `_ogg_`
hook. **The test discriminates at both edges:** the entry after Tremor, `007FFBC0`, is called from
`00801210`, and the entry after the decoder, `00125740`, from `0016E4A0` — each fails it. **Its blind
spot:** a function SEAD calls, placed inside a range, would pass; the MS ADPCM decoder is such a
function, and it was separated by its tables, not by this test.

**Correction to the Tremor count.** The tag census above lists Tremor at **4** functions; the linked
object is **107** entries. The classifier tagged only the four MDCT / window bodies and filed the other
103 under the topic tag `Audio`.


### libvorbis and libogg `bitwise.c` — declared (2026-09-13, FABLE)

**libvorbis is 122 linked entries, not 11.** The float codec CF-2 found unreached occupies **`008800C0` up
to `008958B0`**, between Bullet's last call chain (`0087F410` → `0087F7F0` → `00880020` → `0087FD80`) and
the CRT cosine (`008958B0`, a 5-byte forwarder to `00895DC0`); the classifier tagged eleven of its bodies
`ThirdParty.Audio.LibVorbis` and filed the rest under `Audio`. **119 are declared** (EC-7 letter C);
three are A-measured and one, `00887630` — a float routine that nothing calls, `lea`s or tabulates — is
left out because nothing but its position says what it is.

| evidence | where |
|---|---|
| the codec registry in libvorbis's **8-field** form: three residue bundles at `01CEB0D0` / `01CEB110` / `01CEB150` share unpack `00891F40`, look `00891C80`, free_info `008923B0`, free_look `008922D0` and differ in class / forward / inverse (one with a null pack slot); floor and mapping bundles around them at `01CEB070`–`01CEB0C8` and a further table at `01CE3080`–`01CE30A8` | `.rdata` |
| the `vorbis` signature compare — the same six bytes at `01CEBB50` that Tremor's parser compares | `008800C0` |
| `_float32_unpack`: mantissa `& 0x1FFFFF`, exponent `(v >> 21) & 0x3FF`, bias −788 (`VQ_FMAN − 1 + VQ_FEXP_BIAS`) | `00882AC0` |
| its **own const allocator slots** `01CEB618` calloc / `01CEB620` realloc / `01CEB628` malloc / `01CEB630` free — used by no code outside libvorbis and `bitwise.c` (whole-image scan) | `.rdata` |
| `vorbis_book_encode`, smallft's factor-table initialiser — this copy carries the encoder side too | `00884100`, `0088D500` |

**Clients.** Every direct caller from outside the object is one of three `Boundary.Audio` wrappers,
`00679600`, `00679A50`, `00679F40`; CF-2's reachability (the root `00679A40` is called by nothing) is
unchanged. **Upper edge, stated plainly:** the closure test does *not* decide it — the CRT cosine is
called only from libvorbis, so it would pass; that edge rests on the forwarder-and-cosine bodies being
the MSVC math runtime.

**libogg `bitwise.c` is four entries, `0017C890` up to `0017CC70`,** placed after libvpx in the `0017xxxx`
zone: `oggpack_write` (`bits > 32` rejected, `storage − 4` test, growth by 256 through the realloc slot
`01CEB620`), `oggpack_look`, `oggpack_adv`, `oggpack_read`; look and read index the 33-entry mask table
`(1 << k) − 1` at `01CEB590`. Its callers are libvorbis and Tremor (`007FA670` calls `oggpack_adv`). The
rest of `bitwise.c` is inlined or stripped. Its realloc slot is libvorbis's, so it was built with that
copy; Tremor reuses it through identical-code linking rather than carrying its own.

**Corrections.** The table at the top counts libvorbis at 11 and Tremor at 4 (fixed above to 107); the
linked objects are 122 and 107. "Two Vorbis decoders" below is right that both ship; its function counts
are the classifier's, not the objects'.


### Bullet — the linked library, 480 functions declared (2026-09-13, FABLE)

The tag census counts Bullet at 120 (`ThirdParty.Physics.Bullet`) plus 18 bare-name functions. **The
linked library is two ranges, 547 entries:** **`00830760` up to `00861E90`** (collision world, shapes,
convex / GJK narrowphase, the LinearMath hull library) and **`0087F180` up to `008800C0`**
(`btSimulationIslandManager` with its union-find and sort), the second placed between zlib and
libvorbis. **480 are declared** (EC-7 letter C; `members/select_bullet.py`).

| evidence | where |
|---|---|
| 276 entries sit at vtable slots of `bt*` classes — including function-local callback classes decorated with a Bullet method, such as `btBvhTriangleMeshShape::performConvexcast`'s — or of Bullet's helper structs `DebugDrawcallback` and `SupportVertexCallback` | `rtti/methods.tsv` |
| `btCollisionWorld::updateSingleAabb` references Bullet's own diagnostic, `Overflow in AABB, object removed from simulation` … `If you can reproduce this, please email bugs@continuousphysics.com` | `00840DF0` → `01CCE6A0` |
| lower edges: `008306C0` is called from the CRT at `0082EDA0`; `0087EBF0` is zlib's, called from zlib's `0087E970`. Upper edge of the first range: `00861E90` is a 6-byte import thunk; `00861900`–`00861D30`, the hull library's last helpers, are called only from Bullet | selector asserts |

**Left out:** 64 entries already in OPUS's generated families (vtable installers, deleting destructors,
forwarders, the `malloc` import stub `0085E730` that game code also calls); `008478A0`, whose folded body
is also a `Phyre::VTS` slot; and `00834D40` / `00848C20`, 6- and 5-byte stubs that only game code calls.

> **Crossing into Movement — FINAL-AUDIT pass 22 (FABLE, 2026-09-14).** `00834D40` is `mov eax, 0x40; ret`. Its game
> caller is `0026EB30`, which the ledger files under Movement. That caller takes the stub's result as a count, clamps
> it to at most `0x40`, and skips its loop when the count is not positive (`0026ECF3`–`0026ED06`). The stub supplies a
> constant loop bound and nothing third-party. That is consistent with leaving it out of the library span.

**Controls.** Outbound: 20 targets — the CRT (`free`, the cookie, `_guard_check_icall`, the thread-safe
static header / footer) and math imports, and **three LinearMath header bodies emitted into Phyre's
physics object** (`006A3E20` — a basis-trace routine Phyre's own `006A2600` / `006A4A60` also call —
`006A57C0`, and the callback body `0069F490`), which are Bullet code by origin but not by placement and
are not claimed. Inbound: Phyre's physics client (`0068xxxx`–`006Axxxx`, 62 call sites), unwind / teardown
thunks, 42 game call sites at `0018xxxx` that all reach the excluded `malloc` stub, and about a dozen other game call sites. Shared `.data`: only the TLS index and one static-lifetime slot.


### Lua 5.2.1 — the linked interpreter, 606 functions declared (2026-09-13, FABLE)

The tables above count Lua at 90 (`ThirdParty.Scripting.Lua*`) plus 21 bare-name functions. **The linked
interpreter is 623 entries, `0080F2E0` up to `00830760`** — the VM, compiler, garbage collector and the
standard libraries — and **606 are declared** (EC-7 letter C; `members/select_lua.py`).

| evidence | where |
|---|---|
| `$LuaVersion: Lua 5.2.1  Copyright (C) 1994-2012 Lua.org, PUC-Rio $$LuaAuthors: …` heads Lua's string pool, which runs to `01CCD37F` (base, string, table, os, io, debug and package library names, the opcode names `LOADK` … `EXTRAARG`, the parser's messages) | `01CCA080` |
| 303 of the 623 entries reference that pool | selector |
| `luaopen_base` stores `_VERSION = "Lua 5.2"` | `00814F90` → `01CCA898` / `01CCA8A0` |
| `lua_settop` — `L->top` adjusted from `ci->func`, new slots nil-tagged; **864 direct callers**, the most-called body in the range | `00811130` |
| no entry in the range carries RTTI, and every one is joined to the object by a call, a `lea`, a registration-table slot or a pool reference | selector |

**Edges.** Below: a zlib object (`inflateInit2` `0080DF50` … `crc32_z` `0080E910`) and four 6-byte import
thunks (`MiniDumpWriteDump`, the D3D11 and DXGI creators, `0080F2BC`–`0080F2CE`). Above: Bullet — `00830760`
is called from Bullet's `0083B580`, and Lua's pool ends exactly where Bullet's serialisation names start
(`01CCD380` `btCollisionShapeData`). The last bodies of the range, `00830410`–`008306C0`, reference `control structure too long` —
Lua's code generator (`01CCD308`), easily mistaken for the MSVC runtime beside it.

**Controls.** Outbound: 29 targets, every one a CRT or math import (`longjmp` among them, which Lua's C error
handling needs) or an inlined `printf`-family wrapper (`001744F0`, `001CCAC0`, `0017D2E0`). Inbound: 32 entries
are called from outside — the Lua API — by some 1,300 call sites in the Phyre scripting bindings
(`005Bxxxx`–`006Axxxx`, `0087xxxx`). Shared `.data`: **none** — Lua keeps its state in `lua_State`.
**Left out:** 13 entries already in OPUS's *Lua math unary-function adapter* family, 4 A-measured.


### zlib 1.2.11 — two link ranges, 58 functions declared (2026-09-13, FABLE)

**zlib is 59 linked entries in two ranges**: the inflate side **`0080C5A0` up to `0080F2BC`** (`uncompress`,
`uncompress2`, `inflate`, `inflateInit2`, `adler32`, `crc32` / `crc32_z`, `inflate_fast`, `inflate_table`) and the
deflate side **`0087AF40` up to `0087F180`** (`compress2`, `deflate`, `deflateInit_`, the Huffman trees). **58 are
declared** (EC-7 letter C; `members/select_zlib.py`); one is in OPUS's forwarder family.

| evidence | where |
|---|---|
| `inflate 1.2.11 Copyright 1995-2017 Mark Adler` and `deflate 1.2.11 Copyright 1995-2017 Jean-loup Gailly and Mark Adler` | `01CC9F51`, `01CDA261` |
| `inflate` references `incorrect header check`; `deflate` reads the `z_errmsg` table | `0080C750` → `01CC7C58`; `0087BD60` → `01CC9E90` … |

Interior read 2026-09-17 (SWE2-FRONTIER): `0080C750` is stock zlib `inflate()` — the body carries the full inflate error table (`invalid window size`, `unknown compression method`, `invalid stored block lengths`, `too many length or distance symbols`, `invalid distance too far back`, `unknown header flags set`), opens with `inflateResetKeep` `0080E1C0` at [`0080C76A`](../_index/ADDRESS-INDEX.md), and its 12 `0080E5F0` calls are the `updatewindow`/`inflate_fast` inner loop; nothing FFXII-specific is interposed — the save container can be reconstructed against upstream zlib 1.2.11 source directly.
| `crc32` and `adler32` are 8-byte `mov r8d, r8d; jmp` widening shims into `crc32_z` / `adler32_z` | `0080E5F0`, `0080E300` |
| the deflate side calls the inflate side's checksums 14 times — one library in two places | selector |

**Correction to the tag table above:** the row *zlib adapter — `0080C5A0`, a 24-byte shim; distinct tag from zlib
proper* is **zlib's own `uncompress`**: it passes `&sourceLen` and calls `uncompress2` `0080C5C0` (`0080C5A9`–`0080C5AE`),
exactly as zlib 1.2.11 defines it. It is not an FFXII adapter.

**Controls.** Outbound: `memcpy` and `memset` only. Inbound: `uncompress` from `0019AA20` and from the save reader
`00865D90`, and `compress2` from the save writer `00866200` — the [SAFH pipeline](../19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/save-image-buffers-header-and-payload.md)'s
two ends — and nothing else. Shared `.data`: none.


### libvpx 1.6.0 — the VP8 decoder object, 122 functions declared (2026-09-13, FABLE)

The tag census counts libvpx at 73. **The decoder's C object is 124 entries from `0016DDD0` up to `0017C890`** — ending
exactly where libogg's `oggpack_write` begins — and **122 are declared** (EC-7 letter C; `members/select_libvpx.py`).

| evidence | where |
|---|---|
| the codec interface `vpx_codec_vp8_dx_algo`: name → `WebM Project VP8 Decoder v1.6.0`, ABI version 5, then `init` `0016E110`, `destroy` `0016E210`, the control-map pointer, `peek` `0016E380`, `get_si` `0016E3A0`, `decode` `0016E4A0`, `get_frame` `0016EA80` | `01CDB290` |
| its control map: ids 1, 2, 3, 4–7 (all four on the folded `return VPX_CODEC_INCAPABLE` body `0016EE70`), `0x100`–`0x103`, then `−1` | `01CDB320` |
| the decoder's diagnostics (`Invalid frame width`, `Failed to allocate (pbi->mt_yabove_row)`, `Truncated packet or corrupt partition %d length`, `A stream must start with a complete key frame` …), referenced by nine entries | `01CEB640`–`01CEBB3F` |

**Membership is by joining, not position:** an entry counts when the call / `lea` closure grown from the pool
referencers and the tagged bodies reaches it, when the interface or control map holds it, or when only the video
client calls it. **Left out:** `001744F0`, an inlined `sprintf` wrapper that Lua calls too, and `0016EE70`, the
folded constant return that seven other slots share.

**Controls.** Inbound: the video client at `0067xxxx` only. Outbound: the CRT, and — the decoder's other half — **its
hand-written assembly DSP kernels**, unaligned entries at `00125740`–`001297DE` (beginning with the MMX-state reset
`00125740` directly after the CRI HCA decoder), `001481D0`–`0014C221` and `00158B40`. Those kernels are a separate
package and are not in this row.

**The kernels — 66 declared the same day (second row).** An entry is a kernel when **every** direct caller and every `lea` referencer is a decoder member or another kernel (iterated to a fixpoint), and no `.rdata` / `.data` slot holds it: 31 at `00125740`–`001297DE`, `00133B40`, 32 at `001481D0`–`0014C221`, `00158B40` / `00158C09`. The run-time dispatch setup `0016F080` `lea`s four of them (`001260E7`, `001263AD`, `00126E10`, `00127104`). **The rule is not blind to foreign code:** every CRT body the decoder calls (the cookie, `memcpy`, `memset`, the stdio options getter …) is rejected by it, because other code references them too. Kernels nothing references at all (`001274D0`, `00129870`, `0012A290`) are left undeclared.

### libwebm mkvparser — the WebM/Matroska container parser, 105 functions declared (2026-09-13, SWE2-EC7; count corrected 2026-09-16 under FABLE-ADJ-MKV)

The movie path's third library (after libvpx and libvorbis): **libwebm's `mkvparser`**, the WebM
Project's Matroska container parser. The `.webm` files are EBML — this is the code that walks them.
No `mkvmuxer` RTTI exists anywhere in the image; **only the parse half is linked**, which is what a
game that plays pre-rendered video needs.

| evidence | where |
|---|---|
| eight `mkvparser::` class vtables: `IMkvReader`, `BlockEntry`, `SimpleBlock`, `BlockGroup`, `Track::EOSBlock`, `Track`, `VideoTrack`, `AudioTrack` | `00D89AE0`, `01CC6A68`–`01CC6B28` |
| Matroska element IDs compiled into the parse switch: `18538067` Segment, `114D9B74` SeekHead, `1549A966` SegmentInfo, `1654AE6B` Tracks, `1F43B675` Cluster (9×), `1C53BB6B` Cues (5×), `1043A770` Chapters, `1254C367` Tags, `4DBB`/`53AB`/`53AC` Seek | immediates inside the run |
| `00801550`, the element-walk core: reads an element ID (`00802910`), bounds-checks it, reads its size (`00807E20`), iterates, and pulls data through `m_pReader->Read` — an indirect call through the `IMkvReader` vtable; interior verified 2026-09-17 (SWE2-FRONTIER): `008019A0` first at [`00801569`](../_index/ADDRESS-INDEX.md), `00802910` ×2 | inside the run |

**Membership** (`members/select_mkvparser.py`): the contiguous run `007FFBC0`–`00808888` (the
import-thunk field ends it) is the parser's emitted object — an entry counts when the downstream
call/`lea` closure from the tagged `WebM_MKV` bodies and the vtable targets reaches it, when a
`mkvparser::` vtable holds it, or when only the `0067xxxx` movie client calls it (the public API and
the track getters). **Left out, each for a named reason:** `00801210`/`00806F20` are A-measured;
`00800140` (`CxxObjectLifecycle.VtableInstallStub`), `008005C0`/`008006D0`/`00800710` (scalar
deleting destructors) and `007B6C40` (`NativeLeaf.MemberAddressAccessor`) are already dispositioned
by the generated families — folded bodies the parser shares with other classes; `00808850` is the
shared CRT tail `_Facet_Register` calls (declared by the MSVC runtime tail row, as is `008087C4`,
the CRT destructor called by `~_Fac_tidy_reg_t` `008B905C`); `00861EC6` is `_purecall`.
`007FFCD0`/`007FFD00`/`007FFD80`/`007FFDA0`/`00800150` were once listed here as excluded unwind
thunks; they are members — see the repair note below.
Three RTTI-marked bodies the linker scattered into the audio region are declared — `007AD440`
(`Track::EOSBlock`, `return 0`), `007BD590` (`SimpleBlock`), `007E3260` (`BlockGroup`) — and two are
not: `006CC9F0` (`IMkvReader`'s out-of-line deleting destructor) is already A-measured, `007B6C40`
is already declared as above.

**Repaired under T2 adjudication (FABLE-ADJ-MKV, 2026-09-13):** the five bodies
`007FFCD0`/`007FFD00`/`007FFD80`/`007FFDA0`/`00800150` were first excluded as "serving
`006Exxxx` frames" — that frame attribution was wrong. Each is reached by exactly one reference:
the `jmp` of an unwind funclet at `008A5B30`/`40`/`50`/`60`/`70` (`lea rcx,[rdx+off]; jmp body`).
The selector now walks the chain mechanically — `.pdata` `RUNTIME_FUNCTION` → `UNWIND_INFO` →
handler-data `FuncInfo` (magic `0x19930522`) → unwind-map action RVA → funclet — and admits a body
when **every** code referrer is a funclet owned by a member frame. All five map: `01CC6880` →
`008041F0`, `01CC6858` → `00804860`, `01CC6830` → `00804BE0`, `01CC68A8` → `00804CF0`,
`01CC68D0` → `00807650` (the last under `__GSHandlerCheck_EH`, whose handler data points at the
FuncInfo directly). They are the parser's own member destructors run during unwind — members.
Three of the named frames (`00804860`, `00804BE0`, `00804CF0`) call `008083D0`, a
CxxRuntime-tagged body that is itself a member of this family — an intra-parser edge, not a
crossing into game code.

**Controls.** Inbound: the movie client at `0067xxxx` only — 25 call sites into the public API and
the member getters. Outbound: CRT only (`free`/`delete`, `memcpy`, the eh_vector iterators,
`__security_check_cookie`, `_guard_check_icall`). The game's `IMkvReader` implementation — the
`VbfMkvReader`/`WebM_VbfMkv` bodies at `006Cxxxx` and `001Bxxxx` — is the client and is **not**
covered.

### MSVC runtime tail — the statically linked CRT/vcruntime residue, 54 functions declared (2026-09-14, SWE2-EC7)

Between the libwebm mkvparser object and zlib sits the tail the linker emitted for the **MSVC
runtime itself**: the `__scrt_*` startup machinery, `_Init_thread_*` condition-variable support,
the security-cookie / GS-handler bodies, the `__isa_available`-gated math dispatch with its
SSE/libm kernels, and the ATL `CAtlBaseModule` residue. Microsoft's own code compiled into the
game, not FFXII code — `00808C90` is the canonical `__scrt_common_main_seh` sequence
(`_set_app_type`, `_configure_narrow_argv`, `_initialize_narrow_environment`, `__setusermatherr`,
`atexit`).

| evidence | where |
|---|---|
| `__scrt_common_main_seh` body | `00808C90` |
| CRT initializer — a qword to it sits inside the `_initterm` range `008C31D0`–`008C5678` that A-measured `00808D78` walks | `00808D5C` (`.rdata 008C31D8`) |
| `type_info::vftable` install — scalar deleting destructor of the CRT RTTI support class | `00808C64` |
| the `0xE06D7363` 'msc' exception filter; `00809B44` `lea`s it into `SetUnhandledExceptionFilter` | `00809B54` |
| `_Init_thread` teardown registered through `atexit` in A-measured `00809124` | `00809244` |
| `__isa_available`-gated math dispatch → SSE/libm kernels `0080A270`/`0080A720`/`0080AFE0`, scalar fallbacks `00809D20`/`00809D80` | `008098C0`/`00809900` |
| ATL `CAtlBaseModule` ctor / dtor / `GetHInstanceAt` | `0080C440`–`0080C51C` |
| two CRT bodies the linker emitted inside the mkvparser run | `008087C4` (`_Fac_tidy_reg_t` deleting dtor, sole caller `~_Fac_tidy_reg_t` `008B905C`), `00808850` (`_Facet_Register`) |

**Membership** (`members/select_msvc_runtime.py`): an in-block entry joins when a member or an
A-measured in-block body calls it or `lea`s it (callback registration — `atexit`,
`SetUnhandledExceptionFilter`), when it calls a member, when a pointer to it sits in the `.CRT$XI`
`_initterm` table, or when every code referrer is a declared thunk entry — the vdecl kernels are
`jmp`ed to by the stubs inside `00809920`'s census slot. **Left out, each for a named reason:**
`008098D4` is a shared allocator adapter — eight mkvparser members and game code call it, so no
runtime-exclusive witness exists; the six post-thunk strays `00861EAE`–`008620E0` carry no CRT
witness edge (`008620C0`'s own string marks it FFXII-authored); the 23 A-measured bodies, two
NativeAdapter bodies, 20 `basic_streambuf` import thunks and three tail-call forwarders inside the
span are already dispositioned.

**COMDAT stdio wrappers.** Fourteen members sit scattered through `.text`: `sprintf` `0017D2E0`
(FID-identified VS2019) and twelve `printf`/`vfprintf`/`vsprintf`/`vsnprintf`/`vswprintf`-family
wrappers, plus the shared accessor `__local_stdio_printf_options` `0016D670`. The purity test
admits a scattered body only when **every** callee is the stdio machinery or a declared thunk —
`005CDAA0` calls `__stdio_common_vsnprintf_s` but then formats into a 16 KiB stack buffer and
virtual-dispatches to a logger; it stays game code.

**Controls.** Outbound: the shared allocator `00210EC0`, the `memset`/`free` thunks, the CRT
config imports (`_set_app_type`, `_configthreadlocale`, `__setusermatherr`…) and the game-side
entry/init bodies (`005C5230`, `0053DD10`, `0061ECF0`) that `__scrt_common_main_seh` invokes — the
CRT startup calling `main` is the expected edge. Inbound callers span the whole image: CRT leaf
utilities are called by everyone, which is itself the check — nothing is admitted on position.
Boundary: the entry before `008087C4` is `00808770`, a declared mkvparser member; the entry after
`0080C51C` is `0080C5A0`, the declared zlib `uncompress` shim.

### JsonBox — the JSON library the 001Cxxxx consumers parse through — declared (2026-09-17, SWE2-EC7)

JsonBox (anhero/JsonBox) is the JSON `Value`/`Object` tree plus the recursive-descent parser and the
indenting serializer behind the game's `JsonData/*.json` consumers — **57 members declared** in two
link runs, `001FE0E0`–`00202B10` (the Value.cpp machinery: tagged-variant/Object/Array operations,
the 1527-byte parser `00200E60`, its client-facing entry `00200BF0`, and the serializer bodies that
construct the output filters) and the `002161C0`–`00216540` helper island (`members/jsonbox.tsv`,
`members/select_jsonbox.py`).

The upstream identity rests on three independent witnesses. The RTTI names
`JsonBox::OutputFilter<JsonBox::VSolidusEscaper / VIndentCanceller / VIndenter>` resolve to three
`basic_streambuf`-derived vtables at `00905070` / `009050F0` / `00905170`, which carry JsonBox-specific
code only at slot 0 (the deleting destructors `001FF930`/`001FF870`/`001FF8D0`) and slot 3 (the
`write` overrides `002016F0`/`00201690`/`002016C0`) — every other slot is the shared streambuf
implementation, and slot 6 is `00660570`, an ICF-folded body carried by hundreds of Phyre descriptor
vtables, which is therefore **not** a member. Nine member bodies lea those vtables. And the parser's
error-literal pool at `00904FE8`–`00905038` (`Expected '"', got '`, `' instead, ignoring it.`,
`Expected a digit, '.', 'e' or 'E', got '`, `\u00`, the four-space indent) is upstream Value.cpp
wording, referenced only by members `002008F0`/`00201890`/`00201C40`/`00201EB0`.

The client boundary is sharp: every inbound caller from outside the object is either in the
`001Cxxxx` JSON-consumer band (26 distinct callers — Presentation/ItemsEquipment native-support
bodies) or a declared/EH/static-life convention (the declared EH wrappers `001FE990`/`001FEA00`, the
static-lifetime bodies `008A6E90`/`008A6F10`). Inside the runs the declared bodies `001FE990`,
`001FEA00`, `002164D0` and seven bodies joined by nothing are excluded; the positive rejections are
`002164D0` (PhyreCore-declared) and `00660570` (ICF-folded).

### Dear ImGui — a debug UI shipped in the retail build — declared (2026-09-17, SWE2-EC7)

What ships is a **minimal, dormant ImGui context object — 10 members** in four scattered link runs,
not the full upstream library (`members/imgui.tsv`, `members/select_imgui.py`). The upstream identity
is airtight: `00791D80` is `ImGuiIO::ImGuiIO()` — it memsets `0xB88` bytes, stores the upstream
default filenames `"imgui.ini"` (`01CB3990`) and `"imgui_log.txt"` (`01CB39A0`) at `+0x10`/`+0x18`,
writes the upstream default constants (`DeltaTime` 1/60, `IniSavingRate` 5.0,
`MouseDoubleClickTime` 0.3, `MouseDoubleClickMaxDist` 6.0) and stores the three default
platform-callback bodies `00796E70` / `00798D70` / `00797360` at `+0xA0`/`+0xA8`/`+0xC0`.

The four runs are `00791D80`–`00792350` (the IO ctor plus the `00792090` context-construction mass —
their outer static-object ctor `00791E70` is A-measured, its interior cited by the group-wipe page,
so it is a convention caller, not a member), `00795F10`–`00796180` (the
teardown/clear trio `00795FC0`/`00795F10`/`007960E0`, reached at exit through the declared teardown
stub `008B7D40`), `00796E70`–`007973D0` (two callbacks plus their helpers, with the foreign Input
body `00796FC0` between them excluded) and the singleton `00798D70`. **No live game code calls into
the object** — the only inbound edges are the static initializer and the atexit stubs, which settles
the earlier open question: the debug UI's context is created before main but is never pumped. The
Phyre-side wrapper `PImGuiInternal::PImGuiDynamicMesh` (vtable `01CB3950`) and the shared static at
`02EA54C0` are integration machinery, not members.

### Where the two "post-processing" systems sit

The binary contains **three** distinct post-processing layers, which is easy to conflate:

| Layer | Functions | Nature |
|---|---:|---|
| `Phyre.PostProcessing` | 72 | PhyreEngine's own |
| `ThirdParty.Rendering.PPFX` | 348 | a separate framework |
| `ThirdParty.Rendering.Yebis` | 3 | commercial, owns DOF/lens |

## 3. Key addresses

| Address / symbol | Role | Verified |
|---|---|---|
| `.?AVYebisPfxMemoryAllocatorD3D11@Yebis@@` | YEBIS D3D11 allocator RTTI | ✅ string |
| `.?AVPfxShimD3D11@Yebis@@` | YEBIS D3D11 shim RTTI | ✅ string |
| `008119F0` | `lua_type` — proven Lua 5.2 | ✅ read |
| `00684D10` / `00686280` | `lua_pcall` call sites | not read |
| — | Bullet `btSequentialImpulseConstraintSolver`, `btHashedOverlappingPairCache`, `btTriangleRaycastCallback` | GFZ-tagged |
| — | libvpx `Vp8FilterBlock1d16V6Ssse3` (SSSE3 path) | GFZ-tagged |
| — | `Zlib_1_2_11.InflateInit2` | GFZ-tagged |

*Pointer 2026-10-01 (SWE2-STRUCT for OPUS), for the "not read" row: `00684D10` and `00686280` are function entries,
not call sites. They are the Phyre script callers, `PScripting::PClassCallableMethodScript::PCallerScript` among
them ([the vtable method index](../00-Engine-Core-Runtime/Object-Model/vtable-method-index.md)). They are read on
[the embedded-Lua page](../22-Middleware-PhyreEngine/Embedded-Lua-And-Object-Bindings/embedded-lua-and-phyre-object-bindings.md)
§12 (`EXP-110` ran both from shipped bytes); that page owns them.*

## 4. Data structures and formulas

```
YEBIS feature licence record   (from the format string)
  FeatureId    string      "YEBIS_D3D11"
  BeginYear    int         0 in the retail build
  BeginMonth   int         0
  BeginDay     int         0
  EndYear      int         0
  EndMonth     int         0
  (EndDay presumably follows; the string is truncated in the extraction)

Licence gate (as described by the strings, not read from a body)
  if (today > expiry)  ->  "The YEBIS library passed over the expiration date : %s"
                       ->  "[YEBIS]Yebis Enable Failed!!!"
```

*Pointer 2026-10-01 (SWE2-STRUCT for OPUS): both "not read" notes in this block are answered by X-2 in §7, which reads
the body.* The verifier `006DFF40` checks six signed date fields: begin and end year, month and day. So EndDay is the
sixth field. When all six are zero, the date test is skipped, which is what the shipped record does.

**No formula is asserted for any library's internals.** These are inventory facts.

## 5. Call chain

```
startup
  -> EnableYebis
     -> licence/feature check (FeatureId = YEBIS_D3D11, Begin/End date)
        -> pass : post-effects available
        -> fail : "[YEBIS]Yebis Enable Failed!!!"

render frame
  -> Phyre.PostProcessing (72)   engine-native effects
  -> PPFX (348)                  framework effects
  -> YEBIS (3+)                  DOF / lens, "YEBIS DOF Info"

audio  -> libvorbis / Tremor
video  -> libvpx VP8 1.6.0
physics-> Bullet
config -> JsonBox (JsonData/*.json)~~, libxml2~~
save   -> zlib 1.2.11 (~~linked; not proven to encode the save container~~ compress2 level 9, then RC4: V-9)
script -> Lua 5.2.1
debug  -> Dear ImGui + JsonData/debugMenuSettings.json
```

*Corrected 2026-10-01 (SWE2-STRUCT for OPUS), in the block above:* libxml2 is struck from the config line, because
the identification is withdrawn (`CF-1`, `X-6`). The save line now gives V-9's answer, from §6's own note: the save
body is `compress2` level 9 followed by RC4.

**Do not confuse with:** `ff12-trampoline.dll` and its `x64\scripts\*.lua`, which are a
third-party *mod loader* present in a modded install, not part of the shipping game.

## 6. Modding notes

- **YEBIS owns depth of field and lens effects.** Changing DOF means engaging YEBIS parameters, not
  a Phyre shader.
- **`EnableYebis` is a named toggle** — it appears in the same string table as the JSON-backed
  render parameters, so it is plausibly a config key. Not proven; **X-3**.
- **zlib 1.2.11 is linked**, which makes it the first candidate for the `SAFH` save body — but no
  DEFLATE stream was found in a save file, so linkage is *not* proof (see the save document, V-9). *(2026-09-13: it is
  the codec — the stream is RC4-encrypted after `compress2` level 9, `0087AF40`; decrypting first exposes it. V-9 answered.)*
- **A Dear ImGui debug menu is compiled in**, with `JsonData/debugMenuSettings.json`. Whether it can
  be re-enabled is **X-4** and would be a significant modding capability.
- **Two Vorbis decoders exist.** Audio work should confirm which path actually runs.
  *(Pointer 2026-10-01 (SWE2-STRUCT for OPUS): confirmed. Tremor serves the sound driver's streams (`CF-2`), and
  libvorbis is the movie player's audio path (register `G-23`; checks G1-G3).)*
- **XIIOnline:** Bullet is the physics authority. Any shared-world simulation must decide whether
  physics is authoritative or cosmetic — two clients running Bullet independently will diverge, and
  nothing in this layer reconciles them.

## 7. What is not known

- [x] Bodies of every third-party function — this is an inventory, not an analysis. **X-1.**
      *SUPERSEDED 2026-09-26 (FABLE, Claude Opus 5.5) under FRONTIER's class-1 ruling: a population-coverage statement; the population is carried by 23-Third-Party-Libraries/third-party-middleware-inventory.md. See the register row.*
- [x] Whether the YEBIS all-zero Begin/End dates mean "no expiry" or "unset". **X-2.**
      *Answered on the page 2026-09-14 (FABLE), box left for the ledger mirror (X-2; also register BO-4):* **no expiry, by
      an explicit branch.** The licence verifier is `006DFF40` (strings `License is not valid.` / `License is expired.`
      / `Unexpected License Error.`, source `..\src\UT\ppfxLicense.cpp`). It decodes the licence through `0071C550`
      and checks it in `0071D9E0`:
      1. **The text must match the signed record.** The six date fields decoded from the signed licence (begin
         year / month / day, end year / month / day) must equal the plain-text fields of
         `FeatureId = YEBIS_D3D11, BeginYear = 0, …` field by field (`0071DC87`–`0071DCDB`). Any mismatch sets status 1,
         *not valid* (`0071E209`).
      2. **All six zero skips the date test.** `0071E0F4`–`0071E11A` compare each with 0 and jump straight to the
         success exit `0071E216`.
      3. **Otherwise it tests a window.** It builds `struct tm`s: begin at `year − 1900`, `month − 1`, `day` and 00:00:00;
         end at 23:59:59. It converts both with `_mktime64` (`0071E169`, `0071E1EB`), reads `_time64` (`0071E176`), and
         sets status 2, *expired* (`0071E1FF`), when now is before begin or after end.

      The shipped record is all zeros (`00D86C51`), so the window is never evaluated. The verifier's outcome for this
      build is decided by step 1, the signature and field match, which this reading does not re-derive.
- [x] Whether `EnableYebis` is a JSON config key or a compile-time switch. **X-3.**
- [x] **UQ-314.** Whether the Dear ImGui debug menu can be re-enabled at runtime. **X-4 — high modding value.**
      *Narrowed 2026-09-12 (FABLE) — the gates are runtime data, not a compile-out; the ImGui
      context is created before `main`.* **(1) ImGui is initialised in the shipped build:**
      `00169620` — a CRT static initialiser whose pointer sits at `008C4110` inside the initializer
      table `008C31D8`–`008C5678` ([static initialization](../24-Compiler-And-CRT-Runtime/Static-Initialization-And-Lifetime/static-initialization-order-and-injection-timing.md)) — calls `00791E70` on a static ImGui object and
      registers the destructor with `atexit`; `00791E70` is the only caller of `00791D80`, the
      function that owns the `imgui.ini` / `imgui_log.txt` names. **(2) The in-game debug menu is
      compiled in and gated by runtime state only.** Its input drivers are the widget procs
      `0023B330` and `0023B6F0` (built by the debug widget factory `0023BD40`), which read the raw
      pad words `02F9736C` / `02F9736A` and feed the 0x11A-item handler `001D1660` through
      `0017DB90`; its text overlay `001CD0E0` is drawn through `001D0190`, whose gate is
      `0022A550()` — **frame mode byte `02064AD3` == 2 (the field frame) and draw mode 1's
      render-pass mask `[022C7F94]` (`00358330(1)`) non-zero** — or the latch singleton
      `01F81258`'s byte `+9`, or its `+0xA74 == 2`; and the field frame itself calls the debug draw
      `0017DAA0` at `0022A844` under the same mask test ([what happens between two frames](../22-Middleware-PhyreEngine/The-Frame/what-happens-between-two-frames.md) §4.3, [the application root](../00-Engine-Core-Runtime/Application-Root/game-application.md)). The
      pass masks live in a `.data` table that is zero at load and is written only by the ten
      setters `00358450`–`00358780`, whose call sites pass mode 0 or a register — so whether mode
      1 ever receives a non-zero mask in shipped play is the one thing not settled statically.
      **Intervention points for a mod:** write a non-zero low word at `022C7F94` (draw mode 1)
      while the frame mode is 2, or set byte `+9` of the object behind `001C0DA0`; nothing in the
      image needs patching. *Not established:* whether ImGui's per-frame begin / render is ever
      pumped by game code (the game's calls into the ImGui region resolve to CRT and input-backend
      functions), and whether the pad words carry a real device. Live discriminator: set
      `022C7F94` and watch for the overlay.
      **ANSWERED 2026-09-27 (FABLE, Claude Opus 5.5), static: no.** Only the dormant context ships: none of ImGui's
      frame/window literals is in the image, the context object is touched only by its initializer and atexit stub, and
      no shipped script calls the draw-mask verbs. The debug menu the image does have is the game's own renderer (UQ-14),
      not ImGui. [The UQ-314 record](../_index/candidates/uq314-imgui-dormant/README.md) (4 checks).
- [x] ~~**Which Vorbis decoder actually runs.** *Half answered 2026-09-07:* **both really do ship**, confirmed by body evidence the tags cannot encode — Tremor 4 functions / **0** float SSE ops, libvorbis 11 / **121**. **Which one the audio streaming path reaches is still unknown** and needs call-graph reachability, not a body property.~~
  **CF-2 ANSWERED 2026-09-12 (FABLE): Tremor is the one wired in; ~~libvorbis is linked and reached
  by nothing.~~** *(Corrected 2026-10-01 (SWE2-STRUCT for OPUS), after register `G-23` (FABLE, 2026-09-16):
  libvorbis is reached, from the movie player, see the end of this item.)* Reachability was run on the raw `E8`/`E9` index (function-list-independent), the
  gap-code operand index and a whole-image pointer scan. **Tremor:** its four bodies are called only
  from the driver's own decoder core (`007FDC60`, `007FE530`, `007FF1C0`), and that core is the
  13-entry function table at `01F41F00`–`01F41F60` (with two more entries at `01F41ED8`) whose base
  `01F41E58` three driver functions take (`007F8220` at `007F83C4`, `007F8600` at `007F86AB`,
  `007F8FD0` at `007F9156`) — *and **two MORE index the same table** without ever taking its base,
  found 2026-09-15 (FABLE): `007F7680` (`mov r8, [r12 + rax*8 + 0x1E21E58]`) and `007F7DF0`
  (`mov rax, …`), where `r12` holds the **image base** `00120000`, so `0x00120000 + 0x1E21E58` is
  `01F41E58`. **An address scan cannot see these** — the table's address is never materialised — which
  is the blind spot measured at `UQ-382`; the list of takers was short by two for that reason and not
  through any error in the scan that produced it.* The upward closure from those three is 62 functions, all inside the
  sound driver, rooted at six entry points of which five are `.rdata` vtable slots of the driver's
  stream objects (`007E9340` → `01CB9130`, `007E96A0` → `01CB90D8`, `007EA37C` → `01CB92B8`, `007EA388`
  → `01CB92D8`, `007ED4C0` → `01CB92C0`). **libvorbis:** nine of its eleven functions have **no caller
  in any form** — no `E8`/`E9` site, no gap-code reference, and their three vtables at `01CEB0A8`–
  `01CEB178` are referenced only by two of the eleven themselves (`008923E0`, `00893860`, through
  `01CEB190`); the other two (`00880DF0` ← `00679600` ← `00679A40`) end at a root that no site calls
  and no pointer slot holds. So the streaming path (the driver's stream vtables) reaches Tremor,
  ~~and libvorbis is dead weight carried by the link — consistent with the console heritage the
  section reads.~~ Which driver object owns which vtable is the residue. **X-5**, tracked as **CF-2**.
  *Corrected 2026-10-01 (SWE2-STRUCT for OPUS): libvorbis is not dead weight.*
  - The movie player `0067A480` (`001B7F30`'s callee, the one `FR-1` names) calls `00679A50`, its only caller.
  - `00679A50` calls the libvorbis bodies `008800C0`, `00880AF0` and `00880BF0` inside the library's span
    `008800C0`-`008958B0` (register `G-23`, re-measured by checks G1-G3 of [the 2026-10-01 record](../_index/candidates/swe2struct-reopened3-0930/README.md)).
  - The count of "nine of eleven with no caller" is about the eleven *tagged* bodies, none of which `00679A50`
    calls. It is not about the library. So Tremor runs the sound driver's streams, and libvorbis decodes the movie
    audio.
  - *Reached* means a static caller exists, not that it runs in a given scene.
- [x] **X-6 ANSWERED 2026-09-15 (OPUS) — the JsonBox half stands as FABLE left it; the
      libxml2 half is not an open question, because **libxml2 is not in this image**.**
      - **This document had already withdrawn the identification.** The `libxml2` row above reads
        *“withdrawn 2026-09-12 (`CF-1`): the four tagged functions carry no libxml2 evidence”*.
        A question asking *what libxml2 parses* cannot outlive that withdrawal, and it did.
      - **Independent marker probe, and it finds nothing.** Eight libxml2-specific symbols —
        `libxml`, `xmlParse`, `xmlFree`, `xmlNode`, `xmlMalloc`, `XML_PARSE`, `xmlreader`, `XPath`
        — return **zero hits across the whole image**.
      - **The controls hit, which is what makes the zero mean something.** Five banners this
        document itself names — `inflate 1.2.11`, `deflate 1.2.11`, `LuaVersion: Lua 5.2.1`,
        `WebM Project VP8 Decoder v1.6.0`, `CRI Middleware` — each return exactly one hit by the
        same search.
      - **The only XML in the binary is the manifest.** `<?xml` and `encoding=` appear once each and
        both land in **`.rsrc`**, the Windows resource section — the application manifest every
        MSVC binary embeds. That is not a parser, and nothing reads it as one.
      - ⚠ **A correction to my own first attempt at this, because it nearly weakened the answer
        wrongly.** I first used the literal string `zlib` as a control; it returns **zero**, and I
        was about to report that string-absence can miss a library. It cannot, here — zlib *is*
        present and §X-8 above names its banner, `inflate 1.2.11 Copyright 1995-2017 Mark Adler`
        at `01CC9F50`. **The control was badly chosen, not the method**, and the corrected controls
        are the five above.
      - **So X-6 closes as: JsonBox parses `JsonData/*.json` (FABLE's half, unchanged), and the
        libxml2 half is retired as premise-withdrawn rather than answered.** `X-8`'s request for a
        libxml2 *version* is void for the same reason and is its owner's to retire. **X-6.**
- [x] ~~Whether PPFX is Sony's or another vendor's.~~ **X-7 ANSWERED 2026-09-13 (FABLE): another vendor's — PPFX is the core of Silicon Studio's Yebis.** `ppfx.cpp`'s licence checks and its string pool (`YEBIS_D3D11`, the YEBIS expiry messages, and `TjmjdpoTuvejp` = `SiliconStudio` shifted by one, unreferenced), `Yebis::YebisPfxMemoryAllocatorD3D11` sharing `PPFX::CPfxMemoryAllocator`'s body, and the `yeblic-ppfxlic` build workspace; the 1,660-function object is declared on [the Yebis/PPFX source map §11](PostEffects-Yebis-PPFX/yebis-ppfx-source-map.md).
- [x] Exact versions for Bullet, libvorbis, libxml2, JsonBox, Dear ImGui and YEBIS. **X-8.**
      ***CLOSED 2026-09-27: five versions answered, and ~~NO ADMISSIBLE SOURCE~~ OUT OF EVIDENCE BOUNDARY (relabelled the same day; FRONTIER's batch-K Extension 2026-09-27b) for YEBIS's product version, REVIEWED AND SIGNED by OPUS (lost build, the BS-5 test; FABLE, Claude Opus 5.5, author).** Bullet 2.77, libvorbis 1.3.5, Dear ImGui v1.35, JsonBox 0.6.2 ([record](../_index/candidates/x8-jsonbox-062/README.md)), libxml2 not linked. YEBIS: the image carries the build line `yeblic-ppfxlic-bl2015` and the date Feb 18 2016 but no version in either string width, its resources or any shipped module; the vendor's internal release is unpublished and its only public release list starts after the build. [Package](../_index/candidates/nas-package-6-2026-09-27/README.md), [review](../_index/candidates/nas6-review-opus/README.md).*
      *Narrowed 2026-09-18 (FABLE): no version literal exists for any of them, so the exact versions cannot come from strings.* A case-insensitive sweep of every printable run in the image for `bullet`, `vorbis`, `xiph`, `ogg`, `libxml`, `jsonbox`, `imgui` and `yebis` finds: **Bullet** — only class and RTTI names, among them the serializer structs `btCollisionObjectFloatData` / `btCollisionShapeData` (~~`01BAC180`, `01BAD1D8`~~ `01CCD380`, `01CCE3D8` *(corrected 2026-09-27, FABLE, Claude Opus 5.5: file offsets, not addresses)*), which exist only from the 2.76 serializer onward, so **≥ 2.76** is the bound; **libvorbis / Tremor** — no `Xiph.Org libVorbis I` banner and no `vorbis_` / `ogg_` symbol string at all (the only `vorbis` runs are the SEAD layer's own error strings, ~~`01B973D0`~~ `01CB85D0` *(corrected 2026-09-27, FABLE, Claude Opus 5.5: file offsets, not addresses)* onward), so the codec was linked without its info banner; the sibling **libogg** is already dated **1.3** by its `framing.c` layout in the members table; **libxml2** — withdrawn 2026-09-12 (CF-1), and the sweep confirms no XML-parser string exists, so its version is moot; **JsonBox** — RTTI only (`OutputFilter<SolidusEscaper>`, `<IndentCanceller>`, `<Indenter>`, ~~`01E26F40`~~ `01F48940` *(corrected 2026-09-27, FABLE, Claude Opus 5.5: file offsets, not addresses)*), a library that ships no version string; **Dear ImGui** — only `imgui.ini`, `imgui_log.txt` and Phyre's `PImGuiDynamicMesh`, no `IMGUI_VERSION` literal within `0x400` bytes of any of them; **YEBIS** — the licence string `FeatureId = YEBIS_D3D11, BeginYear = 0 …` and its expiration check (~~`00C65A00`, `00C6E490`~~ `00D86C00`, `00D8F690` *(corrected 2026-09-27, FABLE, Claude Opus 5.5: file offsets, not addresses)*), which names the D3D11 build and not a version. What would settle a version is a structural fingerprint per library (a function-layout match against a known release), which no page has run.
      **PARTLY ANSWERED 2026-09-27 (FABLE, Claude Opus 5.5), static against upstream history - the fingerprints are run.** **Bullet 2.77** (`BN-1`, corroborated by the ray-test adder's hit-fraction write-back, the cylinder still using the box inertia body, and the 0x30-byte mesh part with no `PHY_UCHAR` branch). **libvorbis 1.3.5**: the single-entry codebook branch at `00882F50` arrived in 1.3.5, and `_book_maptype1_quantvals` `00882850` has none of 1.3.6's divide guards. **Dear ImGui v1.35**: the context object is 0x3AC0 bytes with InputTextState / Tooltip / LogAutoExpandMaxDepth / FramerateSecPerFrame at `+0xFA8` / `+0x34B0` / `+0x38D4` / `+0x38D8` (`00791E70`), a layout upstream has only from 2015-03-08 to 03-13, and v1.35 is the one tag in that window. **JsonBox: the 0.6 line**, as an EASTL port - its `OutputFilter` vtables have 15 slots, where 0.5's `setbuf(char*, int)` would add a 16th; ~~which 0.6.x tag it was forked from cannot be read, because the port replaced the only containers that differ~~ *(corrected 2026-09-27, FABLE, Claude Opus 5.5: it is **0.6.2** - `String32` changed from `basic_string<int32_t>` to `vector<int32_t>` in 0.6.2, and the image's backslash-u append in `00201EB0` is a vector push with no terminator; later master changes only `getToString`, which is not linked. [Record](../_index/candidates/x8-jsonbox-062/README.md))*. **libxml2**: not linked (`X-6`), so no version. **YEBIS**: the image carries a `Feb 18 2016` build stamp and the build line `yeblic-ppfxlic-bl2015`, but no product version, and the vendor publishes no history - class 3, like `MH-1`. Also: the CRI HCA **decoder** banner is `Ver.2.05.00` (`01CBA5D1`), beside the mixer's 2.00.00. [Record and control](../_index/candidates/x8-library-versions/README.md) (FAILS 0).

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| ~~Eleven libraries, 690 functions~~ ~~**Twelve libraries, 801 functions**~~ **827 functions** in the certified GN162 tag census (691 + 136). The census names eleven libraries once libxml2 is withdrawn (`CF-1`); the declared families add libogg, the CRI HCA decoder and libwebm *(corrected 2026-10-01, SWE2-STRUCT for OPUS, checks N2-N5)* | ~~GFZ `CodeDomain.ThirdParty.*` tag census~~ — **that census was scope-limited and missed 111 functions.** Corrected figure from a `CodeDomain` census over **all** tag families, on a freshly regenerated graph at GN | 3 |
| YEBIS is linked | two RTTI class names in namespace `Yebis`, plus GFZ-tagged allocator functions | 4 / 3 |
| YEBIS has a licence expiry check | authored strings naming FeatureId, Begin/End date fields and an expiry failure message | 2 |
| YEBIS owns DOF | authored strings `YEBIS DOF Info` / `YEBIS DOF Info (2ndScreen)` | 2 |
| Lua is 5.2.1 | authored `$LuaVersion` banner; corroborated structurally in `008119F0` | 2 / 1 |
| libvpx is VP8 1.6.0 | **the library's own banner in the EXE**: `WebM Project VP8 Decoder v1.6.0` | 2 |
| Only the VP8 **decoder** is linked | that banner says `Decoder`; no encoder banner exists in the image | 2 |
| zlib is 1.2.11 | **the library's own banners**: `deflate 1.2.11 Copyright 1995-2017 Jean-loup Gailly and Mark Adler` and `inflate 1.2.11 Copyright 1995-2017 Mark Adler` | 2 |
| Per-library function counts, `ThirdParty.*` family | full `CodeDomain.ThirdParty.*` census, grouped by library with **no truncation** (2026-09-02). **Exact for that family — but the family is not the whole of third-party code** | 3 |
| Bare-name families: EASTL 72, Lua +21, Bullet +18 | `CodeDomain` census over all 38,161 rows of a freshly regenerated `DumpFullCoverageGraph.java` at GN, selecting rows whose tag contains no `ThirdParty` token; 0 duplicate entry addresses | 3 |
| Tremor is present | four GFZ-tagged MDCT/window functions under `Audio.Tremor` | 3 |
| Dear ImGui ships in retail | GFZ tag + `JsonData/debugMenuSettings.json` string | 3 / 2 |

**Why tier 2 overall.** The load-bearing YEBIS claims come from authored strings — text the
developers wrote — which is strong. The counts come from GFZ tags, which is tier 3 and inherits
whatever that classification got right. No third-party function body was read in this pass, and
§7 says so as **X-1** rather than implying analysis that did not happen.

**One inference explicitly withheld.** All-zero Begin/End dates in the YEBIS format string are
*conventionally* a perpetual licence. That is a reasonable reading and it is not proof — the string
is a `printf` template, and the zeros may be the template's placeholder values rather than the
runtime record. Recorded as **X-2**.
*(Pointer 2026-10-01 (SWE2-STRUCT for OPUS): X-2 was answered on 2026-09-14 from the verifier's body (§7). All-zero
dates take an explicit branch past the date test, so the zeros are the runtime record's, not a template's.)*

## 9. Related

- [`../22-Middleware-PhyreEngine/Embedded-Lua-And-Object-Bindings/embedded-lua-and-phyre-object-bindings.md`](../22-Middleware-PhyreEngine/Embedded-Lua-And-Object-Bindings/embedded-lua-and-phyre-object-bindings.md) — the 90 Lua functions in detail
- [`../17-Presentation-Rendering/Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md`](../17-Presentation-Rendering/Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md) — the parameters YEBIS and PPFX consume
- [`../19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/save-image-buffers-header-and-payload.md`](../19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/save-image-buffers-header-and-payload.md) — where zlib is a candidate but unproven

## 10. Falsification pass 2026-09-02

**Attack chosen.** This document's version pins — `libvpx VP8 1.6.0` and `zlib 1.2.11` — rested on
**tier 3 evidence: the GFZ's own version-pinned tags**. The mission standard is that the GFZ can be
wrong and must be audited rather than deferred to, so an inherited version number that nothing
independent confirms is the weakest load-bearing claim here. The killer looked for was a version
string in the binary that **disagreed** with the tag.

**Result: SURVIVED, and the evidence tier improved.** Every library states its own version inside
the image:

```
deflate 1.2.11 Copyright 1995-2017 Jean-loup Gailly and Mark Adler
inflate 1.2.11 Copyright 1995-2017 Mark Adler
WebM Project VP8 Decoder v1.6.0
$LuaVersion: Lua 5.2.1  Copyright (C) 1994-2012 Lua.org, PUC-Rio
```

The GFZ tags were right. Those three claims move from **tier 3 (a tag) to tier 2 (an authored
string)**, and one new fact falls out: the banner says **Decoder**, and no encoder banner exists —
so only the VP8 *decode* path is linked, which is what a game that plays pre-rendered video needs.

**Result: the attribution table was OVERTURNED in part.** Re-running the tag census over all 38,161
functions reproduces the headline total of **690 exactly**, but not the per-library split:

| Library | Document said | Census | |
|---|---:|---:|---|
| Bullet | 119 | **120** | short by 1 |
| libvpx | 70 | **73** | short by 3 |
| zlib adapter | *(absent)* | **1** | omitted entirely |
| everything else | — | — | matches exactly |

The document balanced its total with a line reading `(audit-tag residue) 5`. **There is no residue.**
Those five functions are attributable, and four of them carry names that state their library
outright:

```
Video.LibVPX_VP8_1_6_0.Vp8FilterBlock1d16V6Ssse3    0012696A  (545 B)
Video.LibVPX_VP8_1_6_0.Vp8MbPostProcAcrossIpC       00149BCE  (487 B)
Video.LibVPX_VP8_1_6_0.Vp8MbPostProcDownC           00149983  (587 B)
Compression.ZlibAdapter                             0080C5A0  ( 24 B)
```

*(Qualified 2026-09-27, FABLE, Claude Opus 5.5, on OPUS-NOTICE-FABLE-UC3-INVENTORY-NAMES: the two `…C` strings are GFZ tags and stay as data, but the bodies are libvpx's SSE2 assembly, not C - `00149983` is `vp8_mbpost_proc_down_xmm` and `00149BCE` is `vp8_mbpost_proc_across_ip_xmm` from `vp8/common/x86/postproc_sse2.asm`, byte-matched in [the UC-3 record](../_index/candidates/uc3-libvpx-bytematch/README.md) and accepted by OPUS in UC-3's answer.)*

plus one Bullet function among the seven that carry `btSequentialImpulseConstraintSolver`,
`btHashedOverlappingPairCache`, `btTriangleRaycastCallback` and `btTriangleShape` names.

**Why the error was reachable.** The counts were taken per *exact tag string*. A library's functions
carry both a base tag (`ThirdParty.Video.LibVPX_VP8_1_6_0`) and, where the GFZ identified a specific
routine, a longer one (`…LibVPX_VP8_1_6_0.Vp8MbPostProcDownC`). Counting exact strings puts the
base-tag functions in the library's row and drops the individually-*better-identified* ones into a
remainder — so **the most precisely known functions were the ones that went missing**. That is a
counter-intuitive failure mode worth naming: a grouping key finer than the concept being counted
loses exactly the best-attributed members.

**A method note.** The first run of this census printed only the top 40 tag strings, and its
per-library sums disagreed with the document. Those sums were **not** reported, because a
disagreement computed from a truncated list is not evidence of anything. The census was re-run
ungrouped and complete before any correction was made here.

**Not attacked, still tier 3 or 4:** the claim of "at least eleven libraries" rests on the same tag
census; the YEBIS licence-expiry behaviour rests on strings, not on a read of the checking function.

---

## 11. Falsification pass 2026-09-02 (pass 3)

**Attack chosen.** Pass 2 ended by naming its own untested claim: *"the claim of 'at least eleven
libraries' rests on the same tag census."* A claim that a pass explicitly declines to attack is the
correct next target, and the killer observation was easy to state: **a third-party library present
in the image but absent from this table.**

**Result: BROKEN. The claim was false, and the defect is methodological, not arithmetic.**

Both this document's original census and pass 2's re-census enumerated the `CodeDomain.ThirdParty.*`
tag family. Pass 2 reproduced the total of 690 exactly and read that agreement as confirmation. It
was not: **re-running the same scoped query reproduces the same blind spot.** Support is not proof.

A `CodeDomain` census over *all* tag families, on a freshly regenerated `DumpFullCoverageGraph.java`
at the GN checkpoint, finds **111 third-party functions with no `ThirdParty` token**:

| Family | Functions | Why invisible |
|---|---:|---|
| `EASTL.*` | 72 | tag begins `GFZ.V121.CodeDomain.EASTL.` |
| `Lua.*` | 21 | tag begins `GFZ.V121.CodeDomain.Lua.` |
| `Bullet.*` | 18 | tag begins `GFZ.V121.CodeDomain.Bullet.` |

Verified distinct, not duplicates: each is a single-tag row at a unique entry address, and the
regenerated graph has **0 duplicate entry addresses** across 38,161 rows. The selection excluded any
row containing `ThirdParty` anywhere in its tag field, so no row is counted twice.

**What this changes.** Eleven libraries → **twelve**; 690 functions → **801**; Bullet 120 → **138**;
Lua 90 → **111**; and **EASTL enters the document for the first time at 72 functions**.

**Why the error was reachable — and why it is worse than pass 2's.** Pass 2's defect was a grouping
key *finer* than the concept counted. This one is a **filter narrower than the concept counted**,
and it is more dangerous for two reasons. First, it is silent: a narrow filter returns a clean,
plausible, internally consistent answer with no remainder to notice. Second, it was
**self-confirming**: the document stated its scope as `CodeDomain:ThirdParty.*` in its own
front-matter, so every later check inherited the scope from the artefact it was meant to test.

**The contradiction was already on disk.** This category's `README.md` states its classification
source as *"CodeDomain: Bullet / Lua / EASTL / Media / Math"* — the bare-name families — while this
document censused `ThirdParty.*`. Two documents in one category disagreed about what the category
contains, and neither noticed. `_index/COVERAGE.md` independently estimates *"Named third-party
(Bullet, Lua, EASTL, media codecs) ~1,000"*, which is closer to 801 than to 690. **Three artefacts
disagreed and the disagreement went unread for want of anyone comparing them.**

**What was tried that did NOT break it.** The `ThirdParty.*` per-library figures were re-derived
from the fresh graph and **every one reproduced exactly**, including the pass-2 corrections
(Bullet 120, the composite-tagged `btSequentialImpulseConstraintSolver.VirtualIterationStage` row at
`0085CDC0` included). The 690 subtotal is exact. The version pins and the YEBIS strings were not
re-attacked and stand as pass 2 left them. **The document's arithmetic was never wrong; its
boundary was.**

**Standing lesson for this database.** A census is only as wide as its selector, and a selector
copied from the document under test cannot falsify that document. Any count claim should record the
selector it used, and a later pass should re-derive the *selector*, not just re-run it.

**Still owed:** an EASTL library document; a read of the YEBIS licence-check function; and a check
of whether any *other* category's census inherited the same `ThirdParty.*` scope.
*(Pointer 2026-10-01 (SWE2-STRUCT for OPUS): all three are done.*
- *The EASTL document is [EASTL strings, containers and the logging allocator](EASTL/eastl-strings-containers-and-the-logging-allocator.md).*
- *The licence check is read as X-2 in §7.*
- *The other-category check is `BO-2`. SWE2-DATA executed it on 2026-09-27
  ([record](../_index/candidates/census-rederive-2026-09-27/disposition.md)): eight tag-prefix selectors were swept,
  and two that select their own taxonomy were flagged.)*

## Falsification pass 2026-09-07 — versions recovered, two Vorbis decoders confirmed, libxml2 challenged

`xiionline-61`, GN160 `fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708`, read from
the authorized EXE `73461d08…d89721f8`.

**Why this document needed attacking.** Its §8 evidence rows cite **GFZ tag names** — *"four
GFZ-tagged MDCT/window functions under `Audio.Tremor`"*. Tag names are a prior session's claim about
the binary, at the same error rate as today's. **This is a census of what the GFZ called things, and
it was being read as a census of what ships.**

### X-8 — exact versions, three recovered from the image's own banners

| library | version | the string that says so | at |
|---|---|---|---|
| **zlib** | **1.2.11** (2017) | `inflate 1.2.11 Copyright 1995-2017 Mark Adler` | `01CC9F50` |
| | | `deflate 1.2.11 Copyright 1995-2017 Jean-loup Gailly and Mark Adler` | `01CDA260` |
| **Lua** | **5.2.1** | `$LuaVersion: Lua 5.2.1  Copyright (C) 1994-2012 Lua.org, PUC-Rio $` | `01CCA080` |
| **libvpx** | **VP8 decoder v1.6.0** | `WebM Project VP8 Decoder v1.6.0` | `01CEB698` |

**A modder can now read the real upstream source for these three** instead of decompiled output —
which is the entire point of knowing a version.

**Honest negative for the rest.** Bullet, JsonBox, Dear ImGui and YEBIS carry **no version banner
anywhere in the image**. That is a fact about the build, not a gap in the search: every printable
run of ≥6 bytes was scanned and matched against each library's markers. **X-8 stays open for those
four, and it may not be answerable from this binary at all.** *(2026-09-27, FABLE, Claude Opus 5.5: the banner negative stands; the versions were then read structurally instead - Bullet 2.77, Dear ImGui v1.35, JsonBox the 0.6 line, with YEBIS's the one not recoverable. See the X-8 box in §7.)*

### X-5 — both Vorbis decoders really do ship, and the bodies prove it

The tags claim `Audio.Tremor` (4 functions) and `Audio.LibVorbis` (11). **Tremor is the integer-only
Vorbis decoder; libvorbis is the floating-point one.** That is a property of the *code*, not of the
name, so it is a test the tags cannot have been copied from.

Counted float SSE opcodes (`F3 0F 10/11/58/59/5C/5E`, `F2 0F …`, `0F 58/59/5C/5E`) across each
family's exact bodies:

| family | functions | bytes | **float SSE ops** |
|---|---:|---:|---:|
| `Audio.Tremor` | 4 | 5,791 | **0** |
| `Audio.LibVorbis` | 11 | 7,498 | **121** |

**Zero against 121.** The four Tremor bodies are pure integer arithmetic — `>> 0x1f & 3`, `>> 2`,
integer division — and `FUN_007FB180`'s window/MDCT loop contains no floating-point instruction of
any kind. They also occupy a different link region (`007Fxxxx`) from the libvorbis family
(`0088xxxx`–`0089xxxx`).

> **The tag split survived a test built from a property it does not encode.** Both decoders ship,
> and which one *runs* is still open — that needs a call-graph reachability read from the audio
> streaming path, not a body property.
>
> *(Pointer 2026-10-01 (SWE2-STRUCT for OPUS): answered since. Tremor runs the sound driver's streams (`CF-2`, §7), and
> libvorbis is the movie player's audio path (register `G-23`).)*

**A negative result worth recording:** the image contains **no `Xiph.Org`, no `libVorbis`, no
`vorbis_` and no version banner** — a single `OggS` page magic is all. **String absence was not
evidence of absence here**, because a decoder is tables and arithmetic. Had this pass stopped at the
string scan it would have wrongly refuted a true claim.

### libxml2 — the claim does not survive, and is reopened

**Six independent markers, zero hits:** `libxml`, `xmlParse`, `xmlFree`, `XML_PARSE`, `xmlNode`,
`encoder error`. A real libxml2 build emits error and encoding strings in quantity.

The four functions tagged `ThirdParty.XML.Libxml2` were read:

- **`002B39A0`, named `xmlStrchr`** — the body is a **generic `strchr`**: walk until NUL, return the
  first match or null. **Every C library contains this function.** The name is not asserted anywhere
  in the binary (`xmlStrchr` appears **0** times as a string), so it is a prior session's
  identification of a body that carries no library-specific evidence. **A shape match, not an
  identification.**
- **`002A3730`** — a state machine over a large record (`+0x44` masked `0x180000`, a byte switch at
  `+0x180`, writes `+0x3c5`, calls `002ABEC0`/`002B3950`). **Nothing in it is XML.**

> **CF-1 answered 2026-09-12 (FABLE): not libxml2 — nothing XML is in the image.** The four tagged
> functions (`002A2C00` 1,113 B, `002A3250` 853 B, `002A3730` 220 B, `002B39A0` 34 B) reference **no
> string at all**, nor do their direct callees; their callees are game helpers (`002A2C00` calls the
> UI routines `00244F50` / `00246790` / `00246AD0` / `002470D0` / `00247730` / `0024ABC0` /
> `00254A10`; `002A3250` calls the text-region helpers `002ABF20` / `002AC2A0` / `002B2880` /
> `002B28F0` / `002B2930` and `002A3730`); their callers, by a function-list-independent `E8`/`E9`
> index, are game functions (`002A3090`, `002E16B0` for the first; `002A35B0`; `002A38C0`), and the
> `strchr` at `002B39A0` is called by the text and menu helpers `002A5590`, `002A6C40`, `002A70B0` and
> `00573BE0`. No libxml2 constant — no entity table, no encoding name, no parser-context shape — is
> reachable from any of them. The label was a shape match on one function propagated to its
> neighbours; the inventory row is withdrawn, and X-6's libxml2 half and X-8's libxml2 version have
> no subject.
>
> **Reopened as `CF-1`.** The honest position is that **four functions were labelled libxml2 and the
> evidence for the label has not been located.** They may be libxml2 with the strings stripped by
> selective linking; they may be something else. **They are not confirmed, and this document listed
> them as a shipped library.**

### What survived unchanged

**JsonBox and Dear ImGui are confirmed by evidence outside the tags** — JsonBox by six genuine RTTI
type descriptors (`.?AV?$OutputFilter@VIndenter@JsonBox@@@JsonBox@@` and siblings), Dear ImGui by the
authored filenames `imgui.ini` and `imgui_log.txt` plus Phyre's `PImGuiDynamicMesh@PImGuiInternal`.
**Bullet is confirmed by its own symbols** — `btCollisionObject`, `btRigidBody`, `btDbvt`,
`btVector3`, `btDiscreteDynamicsWorld`. **YEBIS is confirmed** by its licence-feature strings.

## Residual placements — 2026-09-14 (SWE2-FRONTIER, residual-placement package)

| function | size | role (call-signature read) |
|---|---:|---|
| `001E5C40` | 1021 | middleware-side record walk on `[rcx+0x250]`: `001C0DA0`, `001E6040`, `00861EBA` x8 (CRT math helper), `0018A9E0`; caller `001A53F0` |
| `0029E3B0` | 759 | record copy over `[r8+0xCC..0x3F0]`/`[r15+0xD0]`: `0029DF20` x2, `0029CD90`, `0029DCE0`, `00246AD0` |
| `002A5020` | 783 | field-block copier over `rcx+0x10..0x80`: `0017F880` x6, `002B2880`/`002B28F0`/`002B2930` alternating |
| `002A86A0` | 1364 | UI text/layout body on `[r14+0x38..0x148]`: `005C5230`, `002B3400` x3, `002DD7E0`, `002F9860`, `002B4090`, `002D8BB0` x2, `002B0280`, `00244070` |

## FINAL-AUDIT pass 26 — 2026-09-14 (OPUS): identity and version separated, a fourth banner found

Pass 26 is *"verify third-party identifications against real upstream code; fails if any library
identification is unsupported"*. Run against the authorised image
`73461d08…d89721f8`, instrument `Tools/work/OPUS/pass26_upstream_match.py`.

**X-8's three versions reproduce exactly.** `zlib 1.2.11`, `Lua 5.2.1` and `libvpx VP8 1.6.0` were
recovered here on 2026-09-07 from the image's own banners; an independent search run without
reference to those addresses lands on the same four strings, and the recomputed addresses agree with
the published ones to the byte. The two zlib rows differ by exactly 1 because **the zlib banners
begin with a leading space** — ` inflate 1.2.11 Copyright…` — and §X-8 correctly recorded the
address of the space. That is a reproduction, not a new result.

**A FOURTH VERSION BANNER, which X-8 did not cover.** The inventory carries a CRI HCA decoder family
(`members/cri-hca-decoder.tsv`) and no version for it anywhere in this database:

| library | version | the string that says so | at |
|---|---|---|---|
| **CRI HCA** | **Mixer 2.00.00, build 2015-07-31 16:45:20** | `HCA Mixer Ver.2.00.00 Build:Jul 31 2015 16:45:20` | `01CB7AC1` |
| | | `right (c) 2009-2010 CRI Middleware Co., Ltd.` | `01CBA629` |

**IDENTITY AND VERSION ARE DIFFERENT CLAIMS, and §X-8 answered only the second.** Its honest
negative — *"Bullet, JsonBox, Dear ImGui and YEBIS carry no version banner anywhere in the image"* —
remains true and is not weakened here. But **three of those four** — Bullet, JsonBox and Dear
ImGui, not YEBIS — **are** confirmed *as themselves* by strings upstream wrote, and so are **two
more that the negative never named**, libwebm and EASTL. **Five in all**, which is what pass 26
asks. *(This sentence read "four of those libraries" until 2026-09-15 above a table of five, and
two of the five were not in the "those" it pointed back to. Found by
`check_counts_vs_tables.py`.)*

| library | upstream-authored string | what it is |
|---|---|---|
| **libwebm** | `?AVTrack@mkvparser@@`, `?AVBlockEntry@mkvparser@@`, `?AVIMkvReader@mkvparser@@` | upstream's own namespace, in decorated RTTI the linker emitted from libwebm's headers |
| **EASTL** | `EASTL vector`, `EASTL set`, `EASTL list` | EASTL's default allocator names, from its own container headers |
| **JsonBox** | `…@JsonBox@@` ×6 | upstream's namespace in decorated RTTI |
| **Bullet** | `btCollision…` ×27 | upstream's own class names |
| **Dear ImGui** | `imgui.ini`, `imgui_log.txt` | ImGui's default filenames, written by ImGui |

**The distinction this pass exists to enforce.** A string *containing* a library's name is not
upstream evidence. Searching for "vorbis" finds
`[sead][!!error!!]MaterialVorbisExtraData::GetSeekOffset failed!` — **Square Enix's error message
mentioning Ogg Vorbis, written by the game.** Counting that as corroboration would be taking the
game's word for a library as the library's own, and it is exactly the failure pass 26 is written to
catch. libvorbis is therefore **not confirmed by this test**, consistent with §X-5's own recorded
negative that the image contains no `Xiph.Org` and no `libVorbis` string.

**Not confirmed here, and why that is not a defect.** `libogg` (pure arithmetic bit-packing),
`Tremor` (integer Vorbis, strings stripped) and `libvorbis` carry no upstream text to match. Their
identifications rest on body shape and the float-SSE split §X-5 measured — 0 float ops against 121 —
which is evidence this instrument does not read. **YEBIS is a third case: Silicon Studio's middleware
is not open source, so there is no upstream text in existence to match against.** These are
statements about this test's reach, not verdicts on the claims.

> **One miss is a corroboration.** `libxml2` matches **nothing at all** — no `libxml`, no `xmlParse`.
> The corpus withdrew its four libxml2 tags on 2026-09-12 (**CF-1**) for carrying no libxml2
> evidence. An instrument built for a different purpose agreeing with a correction already made is
> worth more than one agreeing with a claim still standing.

**Result: 9 identifications confirmed by upstream-authored strings, 2 resting only on strings the
game wrote, 3 with no marker in this set. No identification is contradicted.**

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Resource — CLIENT (5 edges through 5 of this page's functions).** The Resource layer reaches this page at `0019AA20`, `001CD0E0`, `001D1660`, `0080C5A0` and 1 more. `FUN_002eeee0` is the worked example, read in full - it is a 295-byte step through a packed `(kind << 16) | index` id: when the index goes negative it looks the kind up in the **eight-entry `.rdata` table** at `00D0F870`, steps to the neighbouring kind modulo eight, and restarts the index at zero - so the id wraps across kinds rather than running off the end; **1 of the 5 bodies on that layer are read, the rest are counted**. The crossing is that those functions are consulted by that layer, not a shared responsibility. Edge count and subject list from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

**Story_Event_Quest_Hunt — SERVICE.** `002E16B0` on this page calls `PersistentFlag_SetBank2048`, owned by that layer. What it reaches is the 2,048-bit bank setter, refusing any id above **`0x7FF`** before it touches the bank - the same range its query enforces; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Developer — CLIENT (2 edges through 2 boundary bodies this page names).** `001C2F50` calls `00796E20` — the shared input-manager singleton getter (`mov rax, [02EA5368]; ret`, 55 callers, read from the shipping bytes) — and `001FEA00`, the EH-guard wrapper the JsonBox row excludes (`sub rsp, 0x38; mov [rsp+0x20], -2; call 002001F0; add rsp, 0x38; ret` — the `-2` scope-state marker over a call into JsonBox member `002001F0`). This page names both bodies to bound the JsonBox run and the `001D5260` subtree's callee list; the Developer body consuming them is that body's relationship with the input manager and the JSON machinery, not a shared responsibility of the middleware inventory. Edge list from `edges.tsv`; both callee bodies read from the shipping bytes 2026-09-17 (SWE2-EC7).

**Gameplay — CLIENT (1 edge).** `00339630` calls `00202B10`, the foreign SIMD transform body the JsonBox row names as the upper boundary of run 1 — one of the `0033xxxx` locomotion callers already dispositioned on the transform-primitives page. The inventory cites `00202B10` only to bound the run; the crossing is Gameplay consulting the transform primitive, not a shared responsibility. Edge from `edges.tsv`; `00339630` prologue read from the shipping bytes 2026-09-17 (SWE2-EC7).

## The `0017DAA0` exclusive subtree — all 3 members bound (SWE2-FRONTIER, followup queue)

`0017DAA0` (21 B) is the entry adapter the frame page cites at `0022A844`:
`001D50D0()` fetches the page context, tail `001D5260(rax)` (`0017DAA4`–
`0017DAB0`). The subtree is the **information-page builder**.

`001D5260` (704 B) gates on `byte[rcx+0xA70]`, memsets via `00861EC0`, seeds
with `0019C5D0` ×2, `001EADB0`, `00796E20`, `xmm0 = 1.0` (`01CEBBF0`,
`001D5300`), then fills rows: `001EA990` twice (`001D5366`, `001D5423`),
`001D0190` (`001D53C2`), `esi == 9` vs `0xA` kind split (`001D53CB`–
`001D53DE`), `001EA380` per row, `rdi` bounded at `0x16` (22 rows,
`001D540C`/`001D54DA`), `001EAEA0`, `00808C40` cookie. Row strings include
`"tent!!"`, `"None content!!"` and a `<Inf…` format run at `008FF950`–
`008FF95E` (`001D548E`–`001D54AC`).

| member | role | interior |
| --- | --- | --- |
| `001D0190` (251 B) | the row-command dispatcher — `edx` split at `0xDD`/`0x122` ranges, `jmp rcx` table (`001D01E0`), `[01DFE40C]` mode index ×4 into `rdx + 0x1E632B0`, `0022A550`, `001CD0E0`/`001C0DA0` record ops, `[rax+9]` flag byte, `[rdi+0xA74]` mode-2 check (`001D0266`) | [`001D01E0`](../_index/ADDRESS-INDEX.md) |
| `001D5260` (704 B) | the page builder, above | [`001D527B`](../_index/ADDRESS-INDEX.md) |
| `001EA990` (242 B) | the string-row materializer — `eax = [rcx+0x28] & 0x7FFFFFFF` rows over `rbx = [r15+0x30]`; per row, strlen on `01CEB638`, `0017D260` alloc, `00861EBA` copy, `~cl` byte op on `[rbx+rsi]` (`001EAA2A`) | [`001EAA06`](../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `001D50D0`, `0019C5D0`, `001EADB0`,
`00796E20`, `001EA380`, `001EAEA0`, `0022A550`, `001CD0E0`, `001C0DA0`,
`0017D260`, `00861EBA`/`00861EC0`, `00808C40`.

## The `00679A40` exclusive subtree — all 2 members bound (SWE2-FRONTIER, followup queue)

`00679A40` (15 B) — `call 00679600; return 0` (`00679A44`/`00679A49`): the
root of the `00679A40 → 00679600 → 00880DF0` Boundary.Audio wrapper chain
the inventory already traces into the libvorbis residue bundle.

| member | role | interior |
| --- | --- | --- |
| `00679600` (large) | Boundary.Audio client wrapper — `dword[rcx+0x324]` selects the instance, `imul ×0x17700` and `×0xBB80` stride the two backing arrays, `qword[rcx+0x4E8]` is the channel list (`0067960C`/`00679616`/`00679636`) | [`00679616`](../_index/ADDRESS-INDEX.md) |
| `0067A240` (163 B) | round-robin list append — `005CD840(rcx+0x48, …)` (`0067A255`), stores `r8` at `[rbx+0x58]` (`0067A26B`), then `dword[rbx+0x28] mod 3` via the `0x55555556` magic (`imul`/`shr 0x1F`/fixup, `0067A264`–`0067A278`) selects one of three sub-list heads `[rbx+0x10]`/`+0x18`/`+0x20` for the `00861EBA` insert (`0067A291`–`0067A297`); on the first append (`byte[rbx+0x40]==0`, `0067A29C`) it vcalls `[rbx+0x8]`'s slot 1 with the `+0x10` list, `005CD5E0(rbx+0x30)`, `inc` the `+0x28` counter and latches `+0x40` (`0067A2A2`–`0067A2CF`) | [`0067A264`](../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `005CD840`, `00861EBA` (362 callers —
the generic insert), `005CD5E0`, `00880DF0` (the vorbis
residue entry the wrapper chain reaches).

## The `008958B0` exclusive subtree — all 2 members bound (SWE2-FRONTIER, followup queue)

`008958B0` (5 B) — `jmp 00895DC0` thunk. The subtree binds the CRT
transcendental pair the inventory uses as the vorbis-object boundary
marker:

| member | role | interior |
| --- | --- | --- |
| `00895DC0` (large) | CRT `cos` — `andpd` with `0x7FFF…` (abs), Cody-Waite reduction against `π/2` (`0x3FF921FB54442D18`) and the `0xC338000000000000` two-power constant (`00895DD7`/`00895DDF`) | [`00895DD7`](../_index/ADDRESS-INDEX.md) |
| `008958C0` (large) | CRT `sin` twin — polynomial seeded with the `-0.1666…` (`0xBFC5555555555555`) coefficient pair (`008958C9`) | [`008958C9`](../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none — leaf CRT math. `008958B0` is
the first address after the libvorbis object; nothing FFXII-authored
references it.

## The `00791E70` exclusive subtree — all 2 members bound (SWE2-FRONTIER, followup queue)

`00791E70` (540 B — corrected 2026-09-17 on
AUDITSEM-CONTRA-FRONTIER-SUBTREE-791E70-SIZE; the earlier ~40 B
described only the ctor head) — the Dear ImGui context constructor:
`00791D80(rbx+8)` initialises the context body (`00791E81`), then
`00792090(rbx+0xB90)` constructs the trailing member object
(`00791E8D`). The body continues for ~500 B more: ~60 immediate
field writes plus three further `00861EC0` memsets — `0x24E0` at
`rbx+0xFA8` (`00791EAB`/`00791F4B`), `0x400` at `+0x34B0`
(`00791F7F`/`00792032`) and `0x1E0` at `+0x38D8`
(`0079206C`/`00792072`) — before `ret` at `0079208B`.

| member | role | interior |
| --- | --- | --- |
| `00791D80` (large) | context init — `memset` `0xB88` bytes via `00861EC0` (`00791D88`/`00791D91`), then loads the `"imgui.ini"` default filename (`00791D9E`) | [`00791D91`](../_index/ADDRESS-INDEX.md) |
| `00792090` | member-object ctor at `+0xB90` (the `ImGuiIO`/settings block) | [`00792090`](../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `00861EC0`. The `0xB88` zero-fill plus
`"imgui.ini"` identifies this as Dear ImGui's `ImGui::CreateContext`
path — middleware, not FFXII-authored code.

`00793140` (258 B) is the child-pointer release sweep the `008B7D40` teardown region calls on the dormant ImGui context's owner record: nine qword fields (`+0x34A0`, `+0xFA0`, `+0xF88`, `+0xF48`, `+0xF30`, `+0xF18`, `+0xF00`, `+0xEB0`, `+0xE90` ...) are each tested and, when non-null, passed to `call qword ptr [[01F40380] + 0xC0]` - the function-pointer slot inside the `02EA58C0` object the uq314 record identifies as the ImGui context.

Interior anchor `00793165` (function `00793140`).

## Falsification pass 2026-10-01 (SWE2-STRUCT for OPUS)

*Run by a Claude session in the SWE2-STRUCT lane for OPUS, a non-author of this page. Record and checker:
[`swe2struct-reopened3-0930`](../_index/candidates/swe2struct-reopened3-0930/README.md), [`p3_inventory.py`](../_index/candidates/swe2struct-reopened3-0930/p3_inventory.py) (10 checks, FAILS 0).*

**Attack chosen: the census totals.** These are the lede's function count, §2's *Corrected totals* (691 + 111 = 802)
and §8's first evidence row. They are the page's most load-bearing claim: the page reopened on them (pass 3), and
the inventory's headline and its consumers repeat them.

Pass 3's own lesson was to re-derive the selector, not just re-run it. So this pass reran the page's selector on the
certified parent, after first proving it is the page's selector. The killer looked for was a family whose count moved
between the 2026-09-02 measurement and the parent the page transfers to.

**Method.** Two exports were used:
- `Tools/work/graph/functions.tsv`, stamped as the certified GN162 parent (`59629b9b…`, 38,161 functions);
- the 2026-09-02 GN export that pass 3 measured, as the **positive control**.

The selector is the page's own:
- `ThirdParty.*` rows are grouped by the first two tag components;
- bare-name rows are those whose tags hold no `ThirdParty` token and carry a `GFZ.V121.CodeDomain.EASTL.*`,
  `GFZ.V121.CodeDomain.Lua.*` or `GFZ.V121.CodeDomain.Bullet.*` tag.

**Result: CORRECTED.**

| figure | page | GN export (control) | GN162 | checks |
|---|---:|---:|---:|---|
| `ThirdParty.*`, every row of §2's table | 691 (690 before R109) | 690 | **691, every row exact** | N1, N2 |
| EASTL (bare-name) | 72 | 72 | **97** (+25 `OrderedContainerRuntime`) | N3, N4 |
| Lua / Bullet (bare-name) | 21 / 18 | 21 / 18 | **21 / 18** | N3 |
| bare-name subtotal | 111 | 111 | **136** | N5 |
| total | 802 (801 in the lede and §8) | 801 | **827** | N5 |

**Why it moved, and why the transfer did not catch it.** Between the two exports, 25 functions were re-tagged from
`CxxStandardLibrary.OrderedContainerRuntime` to `EASTL.OrderedContainerRuntime`. That is consistent with OPUS's 2026-09-15
identification of the tree as EASTL's. No function was added: each row exists in both exports (N4, N6).

The front matter carries the page to GN162 on *"the records this document rests on are unchanged"*. That basis covers
the functions the page cites. It cannot cover a census over all 38,161 rows, and the census is what moved.

### The reopening triggers are resolved (SWE2-STRUCT for OPUS)

`reopened_count: 2` matches the page's two reopenings, and both are resolved.

1. **2026-09-02, pass 3: the census scope defect.** The bare-name families are on the page. The corrected totals are
   now re-measured at the parent and corrected again above. The pass's three "still owed" items are done (pointer in
   §11).
2. **2026-09-07: libxml2 "reopened as `CF-1`".** `CF-1` was answered on 2026-09-12: four functions carried no
   libxml2 evidence, and the row is withdrawn. `X-6` and `X-8` retired its version. This pass strikes the last
   libxml2 mention, in §5's call chain.

**Also corrected:** §7's `CF-2` box still said libvorbis is *"reached by nothing … dead weight"*. Register `G-23`
overturned that on 2026-09-16, and the front matter's libvorbis family row already carried the correction. Checks
G1-G3 re-measure the chain: the movie player `0067A480` calls `00679A50`, which calls `008800C0`, `00880AF0` and
`00880BF0`.

**What this pass did not attack:** the version table (pass 26 re-measured it), the YEBIS strings and licence branch
(X-2), and the function-family rows in the front matter, which have their own selectors.
