#!/usr/bin/env python3
"""Verify conservative ISO-code fallback against the pinned Natural Earth input."""
import hashlib, io, json, struct, urllib.request, zipfile
URL = "https://naciscdn.org/naturalearth/10m/cultural/ne_10m_admin_0_countries.zip"
EXPECTED_SHA256 = "ce1ac7036499a0edd641fbc093cd209a98f96a49d2eca8480aaacad35138a7f6"
data = urllib.request.urlopen(URL, timeout=60).read()
assert hashlib.sha256(data).hexdigest() == EXPECTED_SHA256
archive = zipfile.ZipFile(io.BytesIO(data))
dbf = archive.read(next(n for n in archive.namelist() if n.lower().endswith(".dbf")))
count = struct.unpack("<I", dbf[4:8])[0]
header_len = struct.unpack("<H", dbf[8:10])[0]
record_len = struct.unpack("<H", dbf[10:12])[0]
fields, pos, offset = [], 32, 1
while dbf[pos] != 0x0D:
    name = dbf[pos:pos+11].split(b"\0", 1)[0].decode()
    length = dbf[pos+16]
    fields.append((name, offset, length)); offset += length; pos += 32
wanted = {"ADMIN", "ISO_A2", "ISO_A3", "ISO_A2_EH", "ISO_A3_EH"}
rows = []
for i in range(count):
    record = dbf[header_len+i*record_len:header_len+(i+1)*record_len]
    rows.append({n: record[o:o+l].decode("latin1").replace("\0", "").strip() for n, o, l in fields if n in wanted})
def fallback(row, old, equivalent):
    return row[equivalent] if row[old] == "-99" and row[equivalent] != "-99" else row[old]
changed = []
for row in rows:
    new_a2 = fallback(row, "ISO_A2", "ISO_A2_EH"); new_a3 = fallback(row, "ISO_A3", "ISO_A3_EH")
    if (new_a2, new_a3) != (row["ISO_A2"], row["ISO_A3"]):
        changed.append((row["ADMIN"], row["ISO_A2"], new_a2, row["ISO_A3"], new_a3))
assert count == 258
assert next(x for x in changed if x[0] == "France") == ("France", "-99", "FR", "-99", "FRA")
assert next(x for x in changed if x[0] == "Norway") == ("Norway", "-99", "NO", "-99", "NOR")
assert len(changed) == 9
assert sum(fallback(r, "ISO_A2", "ISO_A2_EH") == "-99" for r in rows) == 13
assert sum(fallback(r, "ISO_A3", "ISO_A3_EH") == "-99" for r in rows) == 14
print(json.dumps({"records": count, "changed": changed, "remaining_minus_99": {"a2": 13, "a3": 14}}, ensure_ascii=False, sort_keys=True))
