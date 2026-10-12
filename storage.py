import json
from pathlib import Path

BASE = Path(__file__).resolve().parent / 'data'
BASE.mkdir(exist_ok=True)

def load(name, default):
    path = BASE / f'{name}.json'
    if not path.exists():
        save(name, default)
        return default
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except (ValueError, OSError):
        return default

def save(name, records):
    (BASE / f'{name}.json').write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding='utf-8')
