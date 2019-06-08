
from __future__ import annotations

import json

from pathlib import Path

from config.config import CONFIG
from entity.entity import Entity

def to_spec():
    path = Path(f'.muted/data/spec')

    assert(path.is_dir())

    for f in path.iterdir():
        print(f'------{f}-------')
        if f.is_file():
            spec = ''

            with f.open(encoding='utf-8') as fin:
                spec = json.load(fin)

                for item in spec:
                    try:
                        entity = item['entity']
                    except KeyError:
                        item['entity'] = Entity.eid()

                print(json.dumps(spec, ensure_ascii=False, indent=2))

            with f.open(mode='w', encoding='utf-8') as fout:
                json.dump(spec, fout, ensure_ascii=False, indent=2)
#                fout.write(json.dumps(spec, indent=2))

if __name__ == '__main__':
    to_spec()
