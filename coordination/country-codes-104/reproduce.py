#!/usr/bin/env python3
"""Run the exact helper added by parser.patch against observed source cells."""
import ast
import copy
import hashlib
import json
from pathlib import Path

from lxml import html

ROOT = Path(__file__).resolve().parent
patch = (ROOT / 'parser.patch').read_text()
lines = patch.splitlines()
start = lines.index('+def process_statoids_fifa_row(tr):')
added = []
for line in lines[start:]:
    if not line.startswith('+'):
        break
    added.append(line[1:])
helper_source = '\n'.join(added) + '\n'
tree = ast.parse(helper_source)
assert len(tree.body) == 1 and isinstance(tree.body[0], ast.FunctionDef)
scope = {'copy': copy}
exec(compile(tree, '<exact-helper-from-parser.patch>', 'exec'), scope)
parse = scope['process_statoids_fifa_row']
assert lines.count('+    row = process_statoids_fifa_row(tr)') == 2

results = []
for f in json.loads((ROOT / 'fixtures.json').read_text())['rows']:
    # Only FIFA cells are copied from the live source; all surrounding cells
    # are synthetic sentinels to check column isolation.
    tr = html.fromstring('<tr><td>sentinel</td><td>' + f['alpha2'] + '</td>'
                         + '<td>unchanged</td>' * 5 + f['fifa_html']
                         + '<td>tail</td></tr>')
    original = html.tostring(tr)
    before = [td.text_content() for td in tr]
    after = parse(tr)
    assert before[7] == f['before'] and after[7] == f['after']
    assert before[:7] == after[:7] and before[8:] == after[8:]
    assert html.tostring(tr) == original
    results.append({'alpha2':f['alpha2'], 'before':before[7], 'after':after[7]})

for cell in ['<td><code>AFG</code></td>', '<td>\u00a0</td>', '<td></td>',
             '<td><code>XX<a href="https://example.invalid">Y</a></code></td>']:
    tr = html.fromstring('<tr><td>sentinel</td><td>ZZ</td>' + '<td>x</td>'*5 + cell + '</tr>')
    assert parse(tr) == [td.text_content() for td in tr]
assert parse(html.fromstring('<tr><td>x</td></tr>')) == ['x']
print(json.dumps({'status':'PASS', 'source_cell_cases':results,
                  'preservation_cases':5, 'active_loop_replacements':2,
                  'patch_sha256':hashlib.sha256(patch.encode()).hexdigest(),
                  'meaning':'Source parsing only; no verified FIFA assignment for Antarctica.',
                  'external_acceptance':False}, indent=2))
