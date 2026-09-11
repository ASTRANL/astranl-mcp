# datasets/s-and-p-500-companies-financials #17 verification

Prepared 2026-09-11 by an AI assistant for AstraNL.

Pinned upstream commit: `2f5811f022cc8b252ea15884903dee4dfecb088a`.
Pinned `scripts/constituents.py` blob: `52a5d03b09ce6f0c9d2fb1deddfac3fa60b6e7dd`.
Pinned HTML blob: `824fafc83b83bce0ee22baf4044c07cb7467d218`; SHA-256 `9968d27af7beff5bc49decf83a2d0c8f402d952aec93108e90c43dcf2074cfb0`.

The current tracked HTML is UTF-8. Emulating Windows' cp1252 default reproduces a `UnicodeDecodeError` at byte 26,682 (`0x8f`). The offset differs from the report because the tracked Wikipedia snapshot changed.

The minimal tested patch specifies UTF-8 for both the HTML input and generated CSV output. Input-only encoding avoids the read failure but emits cp1252 bytes on Windows, so it is not sufficient.

Verification:
- unmodified under emulated cp1252: exit 1;
- input-only fix: exit 0, output is not UTF-8;
- input+output UTF-8 fix: exit 0;
- 503 records, expected header, every row has three non-empty fields;
- regenerated CSV SHA-256 `abfc59c19af420188ede485e1b5f89299952aa691701b4717652942500995c9a`, exactly matching the tracked CSV;
- `git diff --check` passes.

This is independent verification, not upstream acceptance or merge.