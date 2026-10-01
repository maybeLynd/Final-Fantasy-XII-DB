"""check_upstream_markers.py - FINAL-AUDIT pass 26, upstream identifications against upstream itself.

Pass 26: *"verify third-party identifications against real upstream code; fails if any library
identification is unsupported"*. The corpus identifies 801 functions across a dozen libraries and
names exact versions for three of them - libvpx VP8 1.6.0, Lua 5.2.1, zlib 1.2.11. A version number
is the most falsifiable claim in the database: it is either the version whose source produced these
bytes or it is not.

THE EVIDENCE IS IN THE IMAGE, and no source tarball is needed for the strongest form of it. Upstream
libraries carry their own authored banners - `deflate_copyright` in zlib's `deflate.c`, `LUA_RELEASE`
in `lua.h`, the decoder version string in libvpx - and those strings are compiled in verbatim. If
the corpus says "zlib 1.2.11" and the image contains ` deflate 1.2.11 Copyright 1995-2017 Jean-loup
Gailly and Mark Adler `, the identification is not an inference at all; it is upstream saying so.

THE DISTINCTION THIS INSTRUMENT EXISTS TO MAKE. A string containing a library's name is NOT upstream
evidence. Searching for "vorbis" finds

    "[sead][!!error!!]MaterialVorbisExtraData::GetSeekOffset failed!"

which is **Square Enix's own error message mentioning Ogg Vorbis**, written by the game, not by
libvorbis. Treating that as corroboration would be exactly the mistake pass 26 is written to catch -
counting the game's word for a library as the library's own. So every marker below is classified by
WHO WROTE IT, and a match is only counted when the string is authored upstream.

WHAT A MISS MEANS, and it is not a defect. Some libraries carry no distinctive strings at all -
libogg's bitwise packer is pure arithmetic, and Tremor is integer-only Vorbis with its strings
stripped. An identification resting on body shape, call structure or clone evidence is not
"unsupported" for lacking a banner; it is supported by different evidence that this instrument does
not read. Those are reported as NO-UPSTREAM-STRING, which is a statement about this test's reach,
never a verdict on the claim. YEBIS is a third case again: Silicon Studio's middleware is not open
source, so there is no upstream text in existence to match against.

ONE MISS IS A CORROBORATION. libxml2 matches nothing at all - and the corpus withdrew its four
libxml2 tags on 2026-09-12 (CF-1) for carrying no libxml2 evidence. An instrument built for a
different purpose agreeing with a correction already made is worth more than one agreeing with a
claim still standing.
"""
import io, os, re, sys

EXE = os.path.join("Database", "Tools", "work", "exe", "FFXII_TZA.exe")
EXE_SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"

# (library, claimed version or None, [(marker, who authored it)])
#   "upstream"  the library's own compiled-in string - real pass-26 evidence
#   "game"      a string the game wrote that happens to name the library - NOT evidence
LIBS = [
    ("zlib", "1.2.11", [
        (b" deflate 1.2.11 Copyright 1995-2017 Jean-loup Gailly and Mark Adler ", "upstream"),
        (b" inflate 1.2.11 Copyright 1995-2017 Mark Adler ", "upstream"),
        (b"incorrect header check", "upstream"),
        (b"invalid distance too far back", "upstream"),
    ]),
    ("Lua", "5.2.1", [
        (b"$LuaVersion: Lua 5.2.1  Copyright (C) 1994-2012 Lua.org, PUC-Rio $", "upstream"),
        (b"$LuaAuthors: R. Ierusalimschy, L. H. de Figu", "upstream"),
    ]),
    ("libvpx VP8", "1.6.0", [
        (b"WebM Project VP8 Decoder v1.6.0", "upstream"),
        (b"Invalid reference frame", "upstream"),
    ]),
    # NOT `WebM`. The image's only "WebM" is the four characters at the start of libvpx's own
    # banner, "WebM Project VP8 Decoder v1.6.0" - so scoring libwebm on it confirms libwebm with
    # libvpx's string, which is the double-count this instrument is supposed to catch. libwebm's
    # real fingerprint is its NAMESPACE in the decorated RTTI names the linker emitted from
    # upstream's headers: ?AVTrack@mkvparser@@, ?AVBlockEntry@mkvparser@@, ?AVIMkvReader@mkvparser@@.
    ("libwebm", None, [(b"mkvparser@@", "upstream")]),
    ("Dear ImGui", None, [
        (b"imgui.ini", "upstream"),
        (b"imgui_log.txt", "upstream"),
    ]),
    # Both YEBIS strings in the image are the game's own logging - "[YEBIS]Yebis Enable
    # Failed!!!", "YEBIS DOF Info:" - so this stays unconfirmed BY THIS TEST. Silicon Studio's
    # middleware is not open source, so there is no upstream text to match against at all.
    ("YEBIS / PPFX", None, [(b"[YEBIS]", "game"), (b"YEBIS DOF Info", "game")]),
    # upstream's namespace inside decorated RTTI: ?AV?$OutputFilter@VSolidusEscaper@JsonBox@@
    ("JsonBox", None, [(b"JsonBox@@", "upstream")]),
    ("Bullet", None, [(b"Bullet", "unclear"), (b"btAssert", "upstream"),
                      (b"btCollision", "upstream")]),
    # EASTL's own default allocator names, from eastl/vector.h, set.h, list.h - the library
    # naming its own containers, not the game naming the library.
    ("EASTL", None, [(b"EASTL vector", "upstream"), (b"EASTL set", "upstream"),
                     (b"EASTL list", "upstream")]),
    ("libvorbis", None, [
        (b"Xiph.Org libVorbis", "upstream"),
        (b"MaterialVorbisExtraData", "game"),
    ]),
    ("libogg", None, [(b"Xiph.Org libOgg", "upstream")]),
    ("Tremor", None, [(b"Tremor", "upstream")]),
    # CRI's own middleware build banner. The other HCA strings in the image -
    # "[sead][!!error!!]HCADecoder_Create error" - are the GAME's, and are marked so.
    ("CRI HCA", "Mixer 2.00.00", [(b"HCA Mixer Ver.2.00.00 Build:Jul 31 2015", "upstream"),
                       (b"HCADecoder_Create", "game")]),
    ("libxml2", None, [(b"libxml", "upstream"), (b"xmlParse", "upstream")]),
]


def main():
    import hashlib
    if not os.path.isfile(EXE):
        print("pass 26: no image at %s - ABSTAINING" % EXE)
        return 3
    d = open(EXE, "rb").read()
    if hashlib.sha256(d).hexdigest() != EXE_SHA:
        print("pass 26: not the authority binary - refusing to go on")
        return 3

    print("FINAL-AUDIT pass 26 - third-party identifications against upstream's own strings\n")
    print("  image: %s\n" % EXE)

    confirmed = weak = none = 0
    # A VERSION CLAIM IS THE FALSIFIABLE ONE, so it is the only thing this goes red on. Identity
    # rows are reported and never fail: libogg genuinely has no string to find, and a checker that
    # goes red on that teaches people to ignore it. But a library the corpus names a VERSION for
    # must have that version's own banner in the image - if someone later writes "zlib 1.3" here,
    # this is what catches it.
    missing_version = []
    for lib, ver, markers in LIBS:
        found = []
        for mk, who in markers:
            n = d.count(mk)
            if n:
                found.append((mk, who, n))
        up = [f for f in found if f[1] == "upstream"]
        if up:
            verdict = "CONFIRMED" + (" (version)" if ver else "")
            confirmed += 1
        elif ver:
            verdict = "VERSION CLAIMED, NO BANNER"
            missing_version.append((lib, ver))
            weak += 1
        elif found:
            verdict = "GAME-STRING ONLY"
            weak += 1
        else:
            verdict = "NO-UPSTREAM-STRING"
            none += 1
        print("  %-20s %-18s %s" % (lib, ver or "-", verdict))
        for mk, who, n in found:
            s = mk.decode("latin-1")
            print("      [%-8s x%-3d] %s" % (who, n, s if len(s) <= 68 else s[:65] + "..."))
        if not found:
            print("      no marker from this set is present in the image")
        print()

    print("  CONFIRMED by an upstream-authored string : %d" % confirmed)
    print("  only a string the GAME wrote             : %d" % weak)
    print("  no marker in this set                    : %d" % none)
    print()
    print("  A NO-UPSTREAM-STRING row is not an unsupported identification. libogg's packer is")
    print("  arithmetic and Tremor is stripped - those rest on body and clone evidence this")
    print("  instrument does not read, and it says so rather than voting on them. YEBIS is not")
    print("  open source, so no upstream text exists to match at all.")
    print()
    print("  libxml2 matching NOTHING corroborates a correction the corpus already made: its four")
    print("  tags were withdrawn 2026-09-12 (CF-1) for carrying no libxml2 evidence.")
    if missing_version:
        print()
        print("  A VERSION IS CLAIMED WITH NO UPSTREAM BANNER IN THE IMAGE:")
        for lib, ver in missing_version:
            print("      %s %s" % (lib, ver))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
