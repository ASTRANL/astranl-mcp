# datasets/geo-countries issue 24

Independent request: France and other features are emitted with -99 country codes.

Pinned upstream state: datasets/geo-countries at 185beb1137f6e9f5d916c91916f0159c20fbab30.
Pinned Natural Earth archive SHA-256: ce1ac7036499a0edd641fbc093cd209a98f96a49d2eca8480aaacad35138a7f6.

The patch uses Natural Earth's ISO_A2_EH and ISO_A3_EH fields only as a fallback when the current field is -99; existing non-sentinel values stay unchanged. On the pinned 258-record source this changes 9 features, repairs France to FR/FRA and Norway to NO/NOR, and leaves 13 alpha-2 and 14 alpha-3 sentinel values where Natural Earth itself supplies no equivalent code.

Run python3 verify_natural_earth_eh.py to reproduce the field-level result. The upstream workflow's GDAL invocation remains the integration point.
