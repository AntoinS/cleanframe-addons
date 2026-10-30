import hashlib,json
from pathlib import Path
from zoneinfo import ZoneInfo
from jsonschema import Draft7Validator
root=Path(__file__).resolve().parents[1]
validator=Draft7Validator(json.loads((root/'package.schema.json').read_text()))
catalog=json.loads((root/'catalog.json').read_text())
assert catalog['api']==1 and len(catalog['addons'])<=32
ids=set()
for entry in catalog['addons']:
    assert entry['id'] not in ids
    ids.add(entry['id'])
    assert entry['path']==f"packages/{entry['id']}/{entry['version']}.json"
    data=(root/entry['path']).read_bytes()
    assert len(data)<=65536 and hashlib.sha256(data).hexdigest()==entry['sha256']
    package=json.loads(data);validator.validate(package)
    for key in package:assert package[key]==entry[key]
for path in list((root/'packages').rglob('*.json'))+list((root/'examples').glob('*.json')):
    item=json.loads(path.read_text());validator.validate(item)
    if item['kind']=='spotify':assert item['id']=='spotify'
    if 'timeZone' in item:ZoneInfo(item['timeZone'])
print('Catalog, checksums and example packages validated.')
