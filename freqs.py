import json
import numpy as np

def get_freqs(data):
    freqs = zip(*np.unique([el['ent'] for t in data for el in t], return_counts = True))
    freqs = dict(sorted(list(freqs), key = lambda x: x[1], reverse=True))
    return {k:int(v) for k, v in freqs.items() if v > 2}


def gen_freqs(fp):
    with open("./data/" + fp + "_ents.json", "r", encoding = "UTF-8") as f:
        data = json.load(f)

    with open("./data/freqs.json", "w", encoding = "UTF-8",) as f:
        json.dump(get_freqs(data), f, indent = 2, ensure_ascii = False)