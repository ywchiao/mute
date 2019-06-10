
from __future__ import annotations

from typing import List
from typing import NamedTuple
from typing import Optional
from typing import Tuple

from  pathlib import Path
import json
import uuid

from random import randint

from bool_component import BoolComponent
from float_component import FloatComponent
from text_component import TextComponent
from value_component import ValueComponent

class Entity:
    @staticmethod
    def eid() -> str:
        return uuid.uuid4().hex

def fopen(fname: str) -> Mapping[string, dict]:
    f = Path(f'./{fname}.json')

    data = {}

    if f.is_file():
        with f.open(encoding='utf-8') as fin:
            data = json.load(fin)

            for key, value in data.items():
                if dict == type(value) and 'entity' in value:
                    continue

                entity = Entity.eid()

                if type(value) in ( bool, float, int ):
                    data[key] = {
                        'entity': entity,
                        'value': value
                    }
                else:
                    data[key] = {
                        'entity': entity,
                        'text': value
                    }

        with f.open(mode='w', encoding='utf-8') as fout:
            json.dump(data, fout, ensure_ascii=False, indent=2)

    return data

def to_spec(t):
    text_component = TextComponent.instance('text_component')
    int_component = TextComponent.instance('int_component')

    for key, value in t.items():
        if 'text' in value:
            text_component.update(value['entity'], value['text'])
        elif 'value' in value:
            value_component.update(value['entity'], value['value'])

    text_component.save()

#    f = Path(f'./room.json')
#    f = Path(f'./genus.json')
#    tf = Path(f'./text.json')
#    vf = Path(f'./value.json')
#    fo = Path(f'./tag.json')

#    print(f'------{f}-------')

#    data = fopen('./genus.json')

#    for key, value in data.items():
#        tag[key] = {}

#        for k, v in value.items():
#            if dict == type(v) and 'entity' in v:
#                e = v['entity']
#            else:
#                e = Entity.eid()

#            if type(v) in ( bool, float, int ):
#                vue[e] = v
#            else:
#                text[e] = v

#            tag[key][k] = e

#        with f.open(mode='w', encoding='utf-8') as fout:
#            json.dump(spec, fout, ensure_ascii=False, indent=2)

#        with fo.open(mode='w', encoding='utf-8') as fout:
#            json.dump(tag, fout, ensure_ascii=False, indent=2)

#        with tf.open(mode='w', encoding='utf-8') as fout:
#            json.dump(text, fout, ensure_ascii=False, indent=2)

#        with vf.open(mode='w', encoding='utf-8') as fout:
#            json.dump(vue, fout, ensure_ascii=False, indent=2)

if __name__ == '__main__':
     t = fopen('rabbit')

     print(json.dumps(t, ensure_ascii=False, indent=2))

     to_spec(t)

# craft.py
