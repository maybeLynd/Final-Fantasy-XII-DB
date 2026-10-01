# Validation correction

The first dependency-provenance check required raw working-tree JSON bytes to
equal `git cat-file` bytes from commit8e5c8d. It stopped on the first input before
writing `dependencies.json`: the existing repository normalizes CRLF to LF.

For `current-field-memory.json`, the working file has2,901,134bytes and581CRLF
pairs; its committed blob has2,900,553bytes and noCRLF. Replacing precisely those
line endings makes the bytes identical; independently parsed JSON is identical.
No captured memory byte, identity, address, sample, or outcome changed. This is
a provenance-comparison error, not a live instrument failure, so it does not
invalidate the underlying game observation or justify a new capture.

The corrected check records both hashes/lengths and the exact identity relation:
byte-identical binary, or CRLF-to-LF-only for text plus equal parsed JSON where
applicable. Any other change fails. A package-local `.gitattributes` preserves
the new package's exact tool/evidence bytes. The final checker verifies all11
dependencies against their specified committed blobs using that bounded rule.
