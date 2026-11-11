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

# API 2 keeps all API 1 metadata complete and never mutates the legacy catalog.
v2=json.loads((root/'catalog-v2.json').read_text())
assert v2['api']==2 and len(v2['addons'])<=32
native_schema=json.loads((root/'native-package.schema.json').read_text())
native_validator=Draft7Validator(native_schema)
catalog_schema=json.loads((root/'catalog-v2.schema.json').read_text())
# Resolve the sole local reference without permitting schema network requests.
catalog_schema['properties']['addons']['items']['oneOf'][0]=native_schema
Draft7Validator(catalog_schema).validate(v2)
v2ids=set()
for entry in v2['addons']:
    assert entry['id'] not in v2ids
    v2ids.add(entry['id'])
    if entry['kind']=='native':
        native_validator.validate(entry)
    else:
        package={key:value for key,value in entry.items() if key not in ('path','sha256')}
        validator.validate(package)
        assert entry['path']==f"packages/{entry['id']}/{entry['version']}.json"
        data=(root/entry['path']).read_bytes()
        assert len(data)<=65536 and hashlib.sha256(data).hexdigest()==entry['sha256']
        assert json.loads(data)==package
for legacy in catalog['addons']:
    current=next((entry for entry in v2['addons'] if entry['id']==legacy['id']),None)
    assert current is not None, 'API 2 must retain every legacy package identity'
    assert (current['api'],current['kind'])==(legacy['api'],legacy['kind']), 'Legacy package API and kind must remain compatible'
    assert tuple(map(int,current['version'].split('.')))>=tuple(map(int,legacy['version'].split('.'))), 'API 2 must not downgrade legacy packages'
print('API 2 catalog validated; native entries require separate signed-artifact and device acceptance.')
