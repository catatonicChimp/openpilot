"""Read vendor matrices without modifying files or evaluating workbook formulas."""
import hashlib
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path('/Volumes/nas/devel/vw-mib/datasets/Volkswagen/03_CAN_KMatrix/kmatrix_all')
NS = {'s': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
REVISIONS = ['V7.15F_20150527', 'V7.16F_20151104', 'V7.17F_20160602']
MESSAGES = {'ACC_06', 'ACC_07', 'TSK_06', 'ESP_08'}
result = {'root': str(ROOT), 'sources': []}
for bus in ['0850_Antrieb', '0854_Fahrwerk']:
    for path in sorted((ROOT / bus / 'Archiv').glob('*')):
        if path.suffix not in {'.dbc', '.xlsx'}:
            continue
        if path.suffix == '.xlsx' and not any(r in path.name for r in REVISIONS + ['V7.25F_20210601']):
            continue
        raw = path.read_bytes()
        source = {'path': str(path.relative_to(ROOT)), 'sha256': hashlib.sha256(raw).hexdigest()}
        if path.suffix == '.dbc':
            text = raw.decode('cp1252')
            messages = {}
            for match in re.finditer(r'^BO_ (\d+) (\w+):[^\n]*\n((?:[ \t]+SG_[^\n]*\n)*)', text, re.M):
                if match[2] in MESSAGES:
                    messages[match[2]] = {'id': int(match[1]), 'line': text[:match.start()].count('\n') + 1,
                                           'definition': match[0]}
            source['messages'] = messages
            ids = {m['id'] for m in messages.values()}
            source['annotations'] = [{'line': n, 'text': line} for n, line in enumerate(text.splitlines(), 1)
                                     if any(re.match(rf'(?:VAL_|CM_ SG_|BA_ "[^"]+" BO_) {i}\b', line) for i in ids)]
        else:
            sheets = []
            with zipfile.ZipFile(path) as archive:
                strings = [''.join(t.text or '' for t in si.findall('.//s:t', NS))
                           for si in ET.fromstring(archive.read('xl/sharedStrings.xml')).findall('s:si', NS)]
                book = ET.fromstring(archive.read('xl/workbook.xml'))
                rels = {r.get('Id'): r.get('Target') for r in ET.fromstring(archive.read('xl/_rels/workbook.xml.rels'))}
                for sheet in book.findall('s:sheets/s:sheet', NS):
                    target = rels[sheet.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')]
                    entry = target.lstrip('/') if target.startswith('/') else 'xl/' + target
                    rows = []
                    for row in ET.fromstring(archive.read(entry)).findall('.//s:sheetData/s:row', NS):
                        cells = {}
                        for c in row.findall('s:c', NS):
                            v = c.find('s:v', NS)
                            if v is not None:
                                value = strings[int(v.text)] if c.get('t') == 's' else v.text
                                cells[c.get('r')] = value
                            elif c.get('t') == 'inlineStr':
                                cells[c.get('r')] = ''.join(t.text or '' for t in c.findall('.//s:t', NS))
                        msg = cells.get('A' + row.get('r'))
                        if msg in MESSAGES or int(row.get('r')) <= 4:
                            rows.append({'row': int(row.get('r')), 'cells': cells})
                    if rows:
                        sheets.append({'name': sheet.get('name'), 'xml': entry, 'rows': rows})
            source['sheets'] = sheets
        result['sources'].append(source)
out = Path(__file__).with_name('vendor-extract.json')
out.write_text(json.dumps(result, indent=2, ensure_ascii=True) + '\n')
print(f'{len(result["sources"])} sources -> {out}')
