import json
import re

def get_abrevs():
    with open('./data/freqs.json') as f:
        temp = json.load(f)

    entities = list(temp.keys())
    prob_abr = []
    for el in entities:
        if re.fullmatch(r'[А-Я]{2,4}', el):
            prob_abr.append(el.lower())
    abrevs = dict()
    for ent in entities:
        word = ''
        abr = ent.split()
        word_lenght = len(abr)
        for i in range(word_lenght):
            word += abr[i][0]
        if word.lower() in prob_abr:
            abrevs[ent.lower()] = word.upper()
    return abrevs    

abrevs = get_abrevs()

def change_ent(ent):
    if ent['ent'] == 'РФ':
        return {'ent' : 'Россия', 'type' : 'LOC'}
    elif ent['type'] != 'PER' and ent['ent'].lower() in abrevs:
        return {'ent' : abrevs[ent['ent'].lower()], 'type' : ent['type']}
    elif ent['ent'] == "ДАННОЕ СООБЩЕНИЕ (МАТЕРИАЛ":
        return None
    else:
        return ent

def change_msg(message):
    message = [change_ent(ent) for ent in message]
    return [ent for ent in message if ent]

def fix_names(messages):
    #someting
    messages = [change_msg(message) for message in messages]

    return messages