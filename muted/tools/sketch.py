
from __future__ import annotations

import json

from pathlib import Path
from pathlib import PosixPath

from config.config import CONFIG
from entity.entity import Entity

from component.component import Component

class Sketch:
    def __init__(self):
        self._components: Mapping[str, Type[Component]] = {}

        self._components['entity'] = Component.instance('entity')
        self._components['tag'] = Component.instance('tag')

    def draft(self, path: str) -> None:
        path = Path(f'{path}')

        assert(path.is_dir())

        for f in path.iterdir():
            if f.is_file():
                data = self._load_json(f)

                self._update_component(data)

                self._components['entity'].update(f.stem, data['entity'])
                self._components['tag'].update(data['entity'], f.stem)

    def save(self) -> None:
        for key, value in self._components.items():
            value.save(key)

    def _load_json(self, f: PosixPath) -> dict:
        data: dict = {}

        with f.open(encoding='utf-8') as fin:
            print(f'--- processing {f.stem} ---')
            data = json.load(fin)

        if not 'entity' in data:
            data['entity'] = Entity.eid()

            with f.open(mode='w', encoding='utf-8') as fout:
                json.dump(data, fout, ensure_ascii=False, indent=2)

        return data

    def _update_component(self, data: dict) -> None:
        for key, value in data.items():
            if not 'entity' == key:
                try:
                    self._components[key].update(data['entity'], value)
                except KeyError:
                    self._components[key] = Component.instance(key)
                    self._components[key].update(data['entity'], value)

if __name__ == '__main__':
    sketch = Sketch()

    sketch.draft('./tools/drafts')
    sketch.save()

# sketch.py
