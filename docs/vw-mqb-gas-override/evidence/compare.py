"""Compare relevant archived DBC layouts and value tables chronologically."""
import json
from pathlib import Path
import re

base = Path(__file__).parent
data = json.loads((base / 'vendor-extract.json').read_text())
out = ['# MQB Revision Comparison', '', 'Generated from vendor-extract.json. DBC layout/value-table comparison only; not behavioral validation.', '']
for bus in ['ACAN', 'FCAN']:
    out += ['## ' + bus, '']
    sources = [s for s in data['sources'] if s['path'].endswith('.dbc') and 'MQB_' + bus + '_' in s['path']]
    sources.sort(key=lambda s: (re.search(r'_(\d{8})_', s['path'])[1], s['path']))
    previous = None
    for source in sources:
        current = {}
        for name, message in source['messages'].items():
            if name == 'ESP_08':
                continue
            current[name + '.id'] = message['id']
            for line in message['definition'].splitlines()[1:]:
                match = re.match(r' SG_ (\w+) : (\d+)\|(\d+)@(\d)([+-]) \(([^,]+),([^\)]+)\)', line)
                if match:
                    current[name + '.' + match[1]] = [*match.group(2, 3, 4, 5), float(match[6]), float(match[7])]
            for annotation in source['annotations']:
                match = re.match(r'VAL_ ' + str(message['id']) + r' (\w+) (.*)', annotation['text'])
                if match:
                    current[name + '.' + match[1] + '.values'] = match[2]
        out += ['### ' + Path(source['path']).name, '']
        if previous is None:
            out += ['Baseline; no earlier revision compared.', '']
        else:
            changes = [f'- `{key}`: `{previous.get(key, "ABSENT")}` -> `{current.get(key, "ABSENT")}`'
                       for key in sorted(set(previous) | set(current)) if previous.get(key) != current.get(key)]
            out += changes or ['No compared layout, message-ID, or value-table differences.']
            out += ['']
        previous = current
(base / 'revision-comparison.md').write_text('\n'.join(out) + '\n')
print('Wrote', base / 'revision-comparison.md')
