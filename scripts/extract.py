from tqdm import tqdm
import json
import os
from .natasha_model import extract_ents


text_types = {'bold',
    'italic',
    'link',
    'strikethrough',
    'text_link'}

#сообщения могут быть списком где некоторые части текст, а некоторые словари
def from_list(msg):
    res = ""
    for part in msg:
        if isinstance(part, str):
            res += part
        elif part['type'] in text_types:
            res += part['text']
    return res

#проверяем является ли сообщение текстом
def get_text(msg):
    if isinstance(msg, str):
        return msg
    elif isinstance(msg, list):
        return from_list(msg)

#достает сущности из списка сообщений
def extract(data):
    messages = []
    for message in tqdm(data, leave=False):
        if message['type'] == 'message':
            try:
                message = get_text(message['text'])
                yield extract_ents(message)
            except:
                yield ""

def extract_from_json(fp, reload = False, limit=None):
    if not reload:
        if os.path.exists(fp[:-5] + "_ents.json"):
            with open(fp[:-5] + "_ents.json", "r", encoding = "UTF-8",) as f:
                return json.load(f)
        else:
            print("Сохранение не найдено, делаем все заново")

    with open(fp, encoding = "UTF-8") as f:
        data = json.load(f)['messages'][:limit]

    entities = [ent for ent in extract(data) if ent]

    with open(fp[:-5] + "_ents.json", "w", encoding = "UTF-8",) as f:
        json.dump(entities, f, indent = 2, ensure_ascii = False)

    return entities