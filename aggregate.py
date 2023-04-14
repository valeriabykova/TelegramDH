import json

data = []

for news in ['mash', 'meduza', 'ria', 'varlamov']:
    with open("./data/" + news + "_ents.json", "r", encoding = "UTF-8",) as f:
        data += json.load(f)

with open("./data/total_ents.json", "w", encoding = "UTF-8",) as f:
    json.dump(data, f, indent = 2, ensure_ascii = False)