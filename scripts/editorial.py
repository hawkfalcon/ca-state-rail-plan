"""Apply the atlas author's explanatory prose without editing source evidence.

Narratives live in content/editorial.json. Only the explicitly allowed fields below
can be changed; original appendix entries are never passed through this module.
Run this file directly to refresh already processed data after editing the prose.
"""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
COPY = json.loads((ROOT / 'content/editorial.json').read_text())


def apply_copy(records, section, allowed):
    by_id = {item['id']: item for item in records}
    for identifier, fields in COPY[section].items():
        assert identifier in by_id, f'Unknown {section} identifier: {identifier}'
        assert set(fields) <= set(allowed), f'Non-editorial fields in {identifier}'
        by_id[identifier].update(fields)
    return records


def apply_projects(records):
    return apply_copy(records, 'projects', ('name', 'unlock', 'ask'))


def apply_routes(records):
    return apply_copy(records, 'corridors', ('why', 'action'))


def evidence_hash(records, omitted):
    data = [{k: v for k, v in item.items() if k not in omitted} for item in records]
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()


if __name__ == '__main__':
    audit = {'explanation': 'Only independent narrative fields changed. Equal evidence hashes include geometry, frequencies, source citations, original capital names and costs.', 'files': {}}
    for name, key, fn, omitted in [
        ('network.json', 'routes', apply_routes, ('why', 'action')),
        ('network-geo.json', 'routes', apply_routes, ('why', 'action')),
        ('projects.json', None, apply_projects, ('name', 'unlock', 'ask')),
    ]:
        path = ROOT / 'data' / name
        data = json.loads(path.read_text())
        records = data[key] if key else data
        before = evidence_hash(records, omitted)
        fn(records)
        after = evidence_hash(records, omitted)
        assert before == after
        path.write_text(json.dumps(data, separators=(',', ':')) if name == 'network-geo.json' else json.dumps(data, indent=2))
        audit['files'][name] = {'evidence_hash_before': before, 'evidence_hash_after': after, 'unchanged': before == after}
    audit['original_capital_register_sha256'] = hashlib.sha256((ROOT / 'data/capital-projects.json').read_bytes()).hexdigest()
    (ROOT / 'data/editorial-audit.json').write_text(json.dumps(audit, indent=2))
    print(f"Applied copy to {len(COPY['projects'])} projects and {len(COPY['corridors'])} corridors; all non-editorial data unchanged.")
