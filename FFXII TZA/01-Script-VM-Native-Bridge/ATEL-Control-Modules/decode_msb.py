"""Decode an ATEL control-module .msb message stream.

Derived charset (the-ctrl-module-debug-companions.md, `.msb` section):
  0x00        NUL terminator
  0x02        line break
  0x04        space
  0x0e t a b c  4-arg line header (type + three 0x80-biased fields)
  0x0f cmd ..  escape; arity per TZA interpreter 002AC5F0: '!' (0x21) is
               ZERO-arg (apply stored font); ')' (0x29) takes
               1+(a1&7) packed bytes (reader 003FFBC0); '*' (0x2A) takes
               2 args + (a2&7F) literal bytes (reader 003FFD6B); other
               cmd<0x40 take 2 arg bytes (packed 9-bit: a2&7F|(a1&C0)<<1),
               cmd>=0x40 take 1
  0x10..0x1f <b>  2-byte glyph codes; runtime formula (002AC2F0):
               glyph_index = LEADBASE[mode][lead&0xF] + (sub-0x20)
               mode0 tbl@00916570 = [e0 1c0 2a0 380 460 540 620 700 |
                                      0  e0 1c0 2a0 460 540 620 700]
               mode1 tbl@009165B0 = [e0 1c0 2a0 380 460 540 620 700 |
                                     7e0 8c0 9a0 a80   0  e0 1c0 2a0]
               mode/threshold chosen per language at 002AB7D0:
               [01E02814] in {7..0xA} (JP-family) -> thresh 0x1C + mode1;
               else 0x18 + mode0. lead < thresh -> font1 (font00.dat
               record order, VERIFIED); lead >= thresh -> font2
               (fontex_subtitle.dat order, VERIFIED on us events:
               "The complices of the Senate have been quelled, Your
               Honor."). font1's high range (idx >= font00 size) is the
               PS2 fontpack order — not shipped as a Unicode table.
  0x20..0xff  single glyphs — font1[c-0x20] (002AC376): the whole byte
               range indexes the font; 0x81 is NOT a lead. jp font00:
               0x1e.. kana (interleaved gojuon), 0xc4.. = ヴ学ヶＡ..Ｙ,
               0x33a.. = ASCII '0'..'9'. us font00 starts ASCII at 0.
Usage: decode_msb.py <file.msb> [msgindex ...] [--font <locale>]
  --font jp|us|ch|cn|kr|... loads <work>/SWE2-DATA/font-decode/<loc>_font00.glyphs.txt
  and decodes the primary plane through the real glyph table.
"""
import os
import re
import struct
import sys

HIRAGANA = (
    "ぁあぃいぅうぇえぉお"
    "かがきぎくぐけげこご"
    "さざしじすずせぜそぞ"
    "ただちぢっつづてでとど"
    "なにぬねの"
    "はばぱひびぴふぶぷへべぺほぼぽ"
    "まみむめも"
    "ゃやゅゆょよ"
    "らりるれろ"
    "ゎわゐゑをん"
)
KATAKANA = (
    "ァアィイゥウェエォオ"
    "カガキギクグケゲコゴ"
    "サザシジスズセゼソゾ"
    "タダチヂッツヅテデトド"
    "ナニヌネノ"
    "ハバパヒビピフブプヘベペホボポ"
    "マミムメモ"
    "ャヤュユョヨ"
    "ラリルレロ"
    "ヮワヲ"
)
GLYPH = {}
for i, ch in enumerate(HIRAGANA):
    GLYPH[0x3E + i] = ch
for i, ch in enumerate(KATAKANA):
    GLYPH[0x91 + i] = ch
GLYPH[0xE3] = "ン"  # verified in イベ[e3]ト; e1/e2 = rare voiced forms, unpinned
LEADS = set(range(0x10, 0x20))  # bytes <0x20 take the 2-byte lead path (002AC326)
# NOTE: 0x81 is NOT a lead — bytes >=0x20 are single glyphs (font1[c-0x20]).
# The old "81 34-3d = digits" pattern was marker-byte 81 + fullwidth digit.
# 12-plane: fullwidth ASCII. Verified vs evctrl msg0 ("Event Plan Menu" items).
FW = {}
for i in range(26):
    FW[0x1286 + i] = chr(ord("A") + i)   # A-Z
    FW[0x12A0 + i] = chr(ord("a") + i)   # a-z
for i in range(10):
    FW[0x12BA + i] = str(i)              # fullwidth digits
FW.update({0x12D7: ":", 0x12DB: "[", 0x12DC: "]", 0x12D0: "_", 0x12CF: "/"})
# more 12-plane symbols, context-verified: "P:[12d8]www[12d8]weB[12d8]plan..." dev path,
# "musicinfo[12d5]xls", "the numbers[12d4] please", "Test Event[12d2][12d2]Resident"
# 12d2 = fullwidth minus (MAP_BEHIND_LOOKUP[-1.0] matches the float table's -1.0,
# and [-999] in mapctrl msg30); doubled as an em-dash separator in titles
FW.update({0x12D2: "−", 0x12D4: ",", 0x12D5: ".", 0x12D8: "\\", 0x12CB: "%",
           0x12D9: "'",   # possessive: "Reks' Anxiety", "Basch's Apology", "Ba'Gamnan"
           0x12D3: ":"})  # option colon: [12dd]0:OFF&1:ON[12de]
# 10-plane low slots = symbols (unified (lead-0x10)<<8|low table): verified anchors
# 10c3-10c7 form a contiguous punctuation block (、。ー「」), 10e1 = ・, 112d = 罫線
FW.update({0x10C3: "、", 0x10C4: "。", 0x10C5: "ー", 0x10C6: "「", 0x10C7: "」",
           0x10E1: "・", 0x112D: "─"})
# kanji anchors: 137b = 閉 ([137b]じる = 閉じる, first item of every btlctrl submenu)
# 139c = 制, 10cd = 御 (source-verified: エントリー制御, //イベント制御 in btlctrl.sbn)
# mapctrl msg31 sentence-verified: "クリアするまで元に戻られません。其のために別の
# ファイルへセーブすることをお勧めし" -> 122f=元 1235=戻 1088=其 11f3=別 1138=勧
FW.update({0x137B: "閉", 0x139C: "制", 0x10CD: "御",
           0x122F: "元", 0x1235: "戻", 0x1088: "其", 0x11F3: "別", 0x1138: "勧"})
# kanji round-3, source/plaintext-verified:
# 1379=他 (其[1379] = その他 on 9 category items; source //罫線/その他)
# 1099=盗 ([1099]む = 盗む; source 初期設定メニュー::盗む)
# 124d/1241/1053 = 融合技 ([124d 1241 1053]その他; source 融合メニュー::融合技)
# 1343=込 ([1345]み[1343]み = 読み込み; parallel kana form 読みこみEVENT exists)
FW.update({0x1379: "他", 0x1099: "盗", 0x124D: "融", 0x1241: "合",
           0x1053: "技", 0x1343: "込"})
# kanji round-4, btlctrl msg0/msg13 source anchors:
# 1075/1051/1084+1096 = 初期設定 (first submenu of msg0; source 初期設定メニュー)
# 107f/123f = 成功 (盗む&ドロップ[107f][123f]100%; source //盗む/ドロップ成功100%)
# 1098 = 率 (盗むレア率設定; source btlAtelGetStealRateMaxRare)
# 1096 = 定 (X設定 suffix corpus-wide), 1345 = 読 ([1345]みなおし/読み込み)
FW.update({0x1075: "初", 0x1051: "期", 0x1084: "設",
           0x107F: "成", 0x123F: "功", 0x1098: "率",
           0x1096: "定", 0x1345: "読", 0x11C0: "指"})
# kanji round-5, context-verified:
# 10fe=倒 (ザコ其[10fe]し/ボス[10fe]し = 倒し), 1068=死 (みんな死ねモード)
# 124a=同 (技其他と同じか), 107a=上/133a=下 (レベルは上げるだけで下げることは
#   できません -- grammatical sentence), 1055=強 (エリア強制読みこみ,
#   ヒントマーカー強制ON/OFF), 105d=後 (ロード完了後に / INDEX変更後),
# 10a8=受 ([10a8]ける = 受ける, command list), 11c0=指 (ID指定ジャンプ)
FW.update({0x10FE: "倒", 0x1068: "死", 0x124A: "同", 0x107A: "上",
           0x133A: "下", 0x1055: "強", 0x105D: "後", 0x10A8: "受"})
# kanji/symbol round-6, context-verified:
# 12d1 = fullwidth + : mapctrl30 "ギルたんまり[[+999999]" vs "ギルからっぽ[−999999]"
#   (parallel construction against verified 12d2=−), and "+1さいだいセット"
# 12dd/12de = 【】 bracket pair (option-field wrapper: 【0:OFF&1:ON】,
#   【読みこみEVENT】 - x52 paired occurrences)
# 1267 = 現 : "[1267]のマップを読みなおす" = 現のマップを読みなおす
# 10be = 用 : "デバッグ[10be]フラグ" = デバッグ用フラグ
# 14c1/10bc = 完了 : "ロード[14c1][10bc]後にマップ読みなおし" = ロード完了後に
# 146c/10d1 = 位置, 1128/105e = 変更 : "エントリ[146c][10d1]を[1128][105e]"
# 1061=全 10d7=消 1159=立 : "オフラグ[1061][10d7]&[1061][1159]" = 全消&全立
FW.update({0x12D1: "＋", 0x12DD: "【", 0x12DE: "】",
           0x1267: "現", 0x10BE: "用", 0x14C1: "完", 0x10BC: "了",
           0x146C: "位", 0x10D1: "置", 0x1128: "変", 0x105E: "更",
           0x1061: "全", 0x10D7: "消", 0x1159: "立"})
# 10cc=発 10ec=連 : msg10 action items "01:5発 02:6連発 03:7連発" (chain counts)
FW.update({0x10CC: "発", 0x10EC: "連"})
# kanji round-7, source-verified:
# 103d/109c = 移動 : btlctrl.sbn "//マップINDEX移動" matches msg0/msg20
#   "マップINDEX[移動]後マップ読みなおし" / "[移動]したいINDEXばんごうをセット"
# 1083/108f = 切替 : btlctrl.sbn "//切替デバッグメニュー" + "//サブメニュー：
#   デバッグメニュー切替" matches both corpus orders verbatim
FW.update({0x103D: "移", 0x109C: "動", 0x1083: "切", 0x108F: "替"})

# ---------------------------------------------------------------------------
# Font-table decoding (verified 2026-09-23 against shipped TZA resources):
#   idx = LEADBASE[mode][lead & 0xF] + (sub - 0x20)  ->  <loc>/font00.dat[rec]
# LEADBASE tables lifted from the EXE (00916570 / 009165B0).
# in/jp corpus runs mode1+threshold 0x1C; us/latin mode0+0x18 (002AB7D0).
# ---------------------------------------------------------------------------
TBL0 = [0xE0, 0x1C0, 0x2A0, 0x380, 0x460, 0x540, 0x620, 0x700,
        0x000, 0x0E0, 0x1C0, 0x2A0, 0x460, 0x540, 0x620, 0x700]
TBL1 = [0xE0, 0x1C0, 0x2A0, 0x380, 0x460, 0x540, 0x620, 0x700,
        0x7E0, 0x8C0, 0x9A0, 0xA80, 0x000, 0x0E0, 0x1C0, 0x2A0]
GLYPH_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "..", "..", "..", "Tools", "work", "SWE2-DATA",
                         "font-decode")


def load_font(loc, name="font00"):
    p = os.path.normpath(os.path.join(GLYPH_DIR, f"{loc}_{name}.glyphs.txt"))
    if not os.path.exists(p):
        return None
    return open(p, encoding="utf-8").read().split("\n")


# Per-locale runtime state (002AB7D0): CJK languages {7,8,0xB} (mask
# (id-7)&~5==0, 0xC excluded; shipped default 0xA -> mode0) run
# mode1 + threshold 0x1C; everyone else mode0 + 0x18. Secondary font is
# fontex_subtitle (VERIFIED on us alc_a0100: opening cutscene decodes
# verbatim — "The complices of the Senate have been quelled, Your Honor.").
LOCALE_MODE = {"jp": (True, 0x1C), "kr": (True, 0x1C), "ch": (True, 0x1C),
               "cn": (True, 0x1C), "in": (True, 0x1C)}
# the archive's "in" channel is authored in the jp glyph space — there is
# no in_font00; use the jp tables for both .msb and event .ebp banks
FONT_LOC = {"in": "jp"}


def load_loc_fonts(loc):
    floc = FONT_LOC.get(loc, loc)
    return load_font(floc), load_font(floc, "fontex_subtitle")


# Expansion glyphs (18/19/1A/1B leads) are NOT a global font extension:
# they are per-event-file glyph slots.  fontex_subtitle.fex is a chained
# directory of per-scene cp tables:
#     {u32 magic; u32 count; u32 cps[count]}*
# cps = the event file's distinct expansion characters in first-use order
# (VERIFIED 2026-09-24: bhm_d0101's 257-slot table @0x20f8 decodes the
# whole Bahamut airship scene verbatim; alc_a0100's 66-entry chunk 0
# decodes verbatim).  fontex_expand.fex uses the same chunked structure
# for a second class.
#
# The magic is the engine path hash (00674A00: eax=0x1505; per byte
# eax=eax*0x21+movsx(c); final btr 0x1F) of the event's windows-style
# path "event\<dir>\<name>" — VERIFIED 2026-09-24 on 9 events, identical
# across locales:  alc_a0100=0x22949AE0, bhm_d0101=0x48196775,
# gil_z0100=0x419B382A, dor_c1200=0x147FACB0, rbn_a0980=0x6357FC94.
# Sibling scenes differ by +1 (name's last char lands at hash end).
# <dir> = name[:4] with '_' between letters and digits ("bhm_d0101" ->
# dir "bhm_d").  --fex-chunk overrides when the bank is not an event
# file or the magic is absent.
FEX_FILE = os.environ.get("FFXII_FEX_SUBTITLE")
FEX2_FILE = os.environ.get("FFXII_FEX_EXPAND")


def fex_magic(name):
    """Engine path hash of 'event\\<dir>\\<name>' — the fex chunk key."""
    d = name[:3] + "_" + name[4]
    h = 0x1505
    for c in f"event\\{d}\\{name}".encode("ascii"):
        h = (h * 0x21 + c) & 0xFFFFFFFF
    return h & 0x7FFFFFFF


# common JP substrings used to score fex-chunk candidates when the bank
# is not an event file — a correct binding yields real text; a wrong
# one scrambles the chunk's own cps
JP_SCORE = ("です", "ます", "した", "ない", "する", "いる", "ある", "から",
            "けど", "だが", "って", "この", "その", "あの", "お前", "俺",
            "私", "まで", "もの", "こと", "どう", "もう", "まだ", "そう",
            "ここ", "それ", "これ", "あれ", "くれ", "のは", "とは", "なる",
            "わけ", "よう", "ため", "など", "だけ", "ほど", "しか", "でも",
            "てる", "しま", "なっ", "った", "んだ", "なら", "たら", "きっ")


def load_fex_chunks(path=None, loc="jp", kind="subtitle"):
    p = path or (FEX_FILE if kind == "subtitle" else FEX2_FILE) \
        or os.path.join(GLYPH_DIR, f"{loc}_fontex_{kind}.fex")
    if not os.path.exists(p):
        return None
    d = open(p, "rb").read()
    out = []
    pos = 0
    while pos + 8 <= len(d):
        mg, cnt = struct.unpack_from("<II", d, pos)
        cps = [struct.unpack_from("<I", d, pos + 8 + 4 * i)[0]
               for i in range(cnt) if pos + 8 + 4 * i + 4 <= len(d)]
        out.append((mg, cps))
        pos += 8 + 4 * cnt
    return out


def msb_codes(msb):
    """Distinct 18..1B expansion indices used by a .msb bank."""
    nmsg = (struct.unpack_from("<I", msb, 0)[0] & 0xFFFF) // 4 - 1
    codes = set()
    for i in range(nmsg):
        off = struct.unpack_from("<I", msb, 4 * (i + 1))[0] & 0xFFFF
        if off >= len(msb):
            continue
        body = msb[off:msb.find(b"\x00", off)]
        j = 0
        while j < len(body):
            c = body[j]
            if c == 0x0F and j + 1 < len(body):
                cmd = body[j + 1]
                if cmd == 0x21:
                    n = 0
                elif cmd == 0x29 and j + 2 < len(body):
                    n = 1 + (body[j + 2] & 7)
                elif cmd == 0x2A and j + 3 < len(body):
                    n = 2 + (body[j + 3] & 0x7F)
                else:
                    n = 2 if cmd < 0x40 else 1
                j += 2 + n
            elif 0x18 <= c < 0x1C and j + 1 < len(body):
                codes.add((c - 0x18) * 0xE0 + body[j + 1] - 0x20)
                j += 2
            elif c == 0x0E:
                j += 5
            else:
                j += 1
    return codes


def decode(body, font=None, font2=None, mode1=True, thresh=0x1C, fex=None):
    tbl = TBL1 if mode1 else TBL0
    out = []
    i = 0
    while i < len(body):
        c = body[i]
        if c == 0x0F and i + 1 < len(body):
            cmd = body[i + 1]
            if cmd == 0x21:      # '!' zero-arg: apply stored font (002AD151)
                n = 0
            elif cmd == 0x29 and i + 2 < len(body):  # ')' 002AD3F7/003FFBC0:
                n = 1 + (body[i + 2] & 7)   # a1 = base<<3 | count(0-7)
            elif cmd == 0x2A and i + 3 < len(body):  # '*' 002AD47C/003FFD6B:
                n = 2 + (body[i + 3] & 0x7F)  # a1 word, a2 = str byte count
            else:
                n = 2 if cmd < 0x40 else 1
            out.append(f"<{body[i + 1:i + 2 + n].hex()}>")
            i += 2 + n
        elif c == 0x02:
            out.append("|")
            i += 1
        elif c == 0x01:
            out.append("·")  # intra-item field separator (ctrl msg29 SE/Voice toggles)
            i += 1
        elif c == 0x04:
            out.append(" ")
            i += 1
        elif c == 0x0E:
            out.append(f"{{ln{body[i + 1:i + 5].hex()}}}")
            i += 5
        elif c in LEADS and i + 1 < len(body):
            code = (c << 8) | body[i + 1]
            if font is not None and 0x10 <= c < 0x20:
                idx = tbl[c & 0xF] + body[i + 1] - 0x20
                if c >= thresh:
                    if font2 is not None and idx < len(font2):
                        out.append(font2[idx])
                    else:
                        out.append(f"[g2:{code:04x}]")
                elif idx < len(font):
                    out.append(font[idx])
                elif fex is not None and idx - 0x7E0 < len(fex):
                    out.append(fex[idx - 0x7E0])  # font1 extension = .fex list
                else:
                    out.append(f"[g1h:{code:04x}]")  # primary font beyond font00 records
            else:
                out.append(FW.get(code) or f"[{code:04x}]")
            i += 2
        elif font is not None and c >= 0x20:
            # every byte >=0x20 is a single glyph: font1[c-0x20] (002AC376)
            idx = c - 0x20
            out.append(font[idx] if idx < len(font) else f"[{c:02x}]")
            i += 1
        elif c in GLYPH:
            out.append(GLYPH[c])
            i += 1
        elif 0x20 <= c <= 0x3D:
            out.append(chr(c))
            i += 1
        elif c >= 0xE4:
            out.append(f"{{icon{c:02x}}}")
            i += 1
        else:
            out.append(f"·{c:02x}·")
            i += 1
    return "".join(out)


def decode_bank(msb, font, font2, mode1, thresh, fex):
    """Decode every message body in the bank; returns list of (flag, text)."""
    nmsg = (struct.unpack_from("<I", msb, 0)[0] & 0xFFFF) // 4 - 1
    out = []
    for i in range(nmsg):
        entry = struct.unpack_from("<I", msb, 4 * (i + 1))[0]
        off, flag = entry & 0xFFFF, entry >> 16
        end = msb.find(b"\x00", off)
        out.append((flag, decode(msb[off:end], font, font2, mode1,
                                 thresh, fex)))
    return out


def bind_fex(msb, chunk_sets, need, font, font2, mode1, thresh):
    """Score every candidate chunk by decoding the bank and counting
    common-JP bigram hits.  chunk_sets = [(src_name, chunks), ...].
    Returns (src, magic, cps, score, n_candidates)."""
    cands = []
    for src, chunks in chunk_sets:
        for mg, cps in chunks or ():
            if len(cps) >= need:
                cands.append((src, mg, cps))
    # the per-file table is dense — count == max slot + 1.  Score only
    # exact-count candidates when they exist; a larger chunk contains
    # the right glyphs at wrong positions and can win on score alone
    # (dor_c1200: need 35, a count-71 chunk outscored the real one).
    exact = [c for c in cands if len(c[2]) == need]
    pool = exact or cands
    best = (None, 0, [], -1)
    for src, mg, cps in pool:
        fex = [chr(c) if c < 0x30000 else "?" for c in cps]
        text = "".join(t for _, t in
                       decode_bank(msb, font, font2, mode1, thresh, fex))
        sc = sum(text.count(bg) for bg in JP_SCORE)
        if sc > best[3]:
            best = (src, mg, cps, sc)
    return best[0], best[1], best[2], best[3], len(pool)


def main(path, indices=None, loc=None, fex_chunk=None):
    mode1, thresh = LOCALE_MODE.get(loc, (False, 0x18))
    font = font2 = fex = None
    if loc:
        font, font2 = load_loc_fonts(loc)
    msb = open(path, "rb").read()
    if loc:
        floc = FONT_LOC.get(loc, loc)
        subs = load_fex_chunks(loc=floc, kind="subtitle")
        exps = load_fex_chunks(loc=floc, kind="expand")
        codes = msb_codes(msb)
        if codes:
            need = max(codes) + 1
            stem = os.path.splitext(os.path.basename(path))[0]
            mg = fex_magic(stem) if re.fullmatch(
                r"[a-z]{3}_[a-z]\d{4}", stem) else None
            src = cps = None
            if fex_chunk is not None and subs:
                src, mg, cps = "subtitle", subs[fex_chunk][0], \
                    subs[fex_chunk][1]
            elif mg is not None:
                for s, chs in (("subtitle", subs), ("expand", exps)):
                    hit = [c for c in chs or () if c[0] == mg]
                    if hit and (len(hit[0][1]) >= need or src is None):
                        src, cps = s, hit[0][1]
                        if len(cps) >= need:
                            break
            if cps is None:
                src, _m, cps, sc, nc = bind_fex(
                    msb, (("subtitle", subs), ("expand", exps)),
                    need, font, font2, mode1, thresh)
                print(f"fex: scored fallback {src} score {sc} "
                      f"({nc} candidates >= {need})", file=sys.stderr)
            if cps:
                fex = [chr(c) if c < 0x30000 else "?" for c in cps]
                print(f"fex {src} chunk magic "
                      f"{mg if mg is None else f'{mg:08x}'} "
                      f"count {len(cps)} ({len(codes)} slots used)",
                      file=sys.stderr)
            else:
                print(f"fex: no chunk for {stem} magic "
                      f"{mg if mg is None else f'{mg:08x}'} "
                      f"({len(codes)} slots used)", file=sys.stderr)
    for i, (flag, text) in enumerate(
            decode_bank(msb, font, font2, mode1, thresh, fex)):
        if indices and i not in indices:
            continue
        print(f"msg{i:3d} flag={flag}: {text}")


if __name__ == "__main__":
    loc = None
    chunk = None
    if "--font" in sys.argv:
        i = sys.argv.index("--font")
        loc = sys.argv[i + 1]
        sys.argv.pop(i + 1)
        sys.argv.pop(i)
    if "--fex-chunk" in sys.argv:
        i = sys.argv.index("--fex-chunk")
        chunk = int(sys.argv[i + 1])
        sys.argv.pop(i + 1)
        sys.argv.pop(i)
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    main(args[0], {int(a) for a in args[1:]} or None, loc, chunk)
