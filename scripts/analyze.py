from itertools import combinations
import numpy as np
from pyvis.network import Network
from tqdm import tqdm

def clean_data(data):
    data = [
        np.unique([ent['ent'] for ent in msg])
        for msg in data
    ]
    return [d for d in data if len(d)>1]

def get_freq_entities(data, cutoff):
    freqs = zip(*np.unique([el for t in data for el in t], return_counts = True))
    freqs = sorted(list(freqs), key = lambda x: x[1], reverse=True)[:cutoff]
    return {ent for ent, _ in freqs}

def filter_entities(data, good_ents):
    data = [[ent for ent in d if ent in good_ents] for d in data]
    return [d for d in data if len(d)>1]



def count_connections(data, entity_limit = 300):
    data = clean_data(data)
    good_ents = get_freq_entities(data, cutoff=entity_limit)
    data = filter_entities(data, good_ents)
    conns = {e:dict() for e in good_ents}

    for message in data:
        for a, b in combinations(message, 2):
            if a!=b:
                conns[a][b] = conns[a].get(b, 0) + 1
                conns[b][a] = conns[b].get(a, 0) + 1

    return conns

def drop_connections_iter(conns, n):

  for e in conns:
    to_leave = []
    for q in conns[e]:
      if q in conns and e in conns[q]:
        to_leave.append((q, conns[e][q]))
    to_leave = [k for k, v in sorted(to_leave, key=lambda x: x[1], reverse=True)]
    conns[e] = {k:v for k, v in conns[e].items() if k in to_leave[:n]}

  return {k:v for k, v in conns.items() if len(v)>1}

def drop_connections(conns, connection_limit = 5):
    for i in range(10):
        conns = drop_connections_iter(conns, connection_limit)
    return conns

def get_nodes(conns):
    nodes = list(conns.keys())
    index = {e:i for i, e in enumerate(nodes)}
    return nodes, index

def get_edges(conns, index):
    return list({
        (index[k], index[e], w) 
        for k, v in conns.items() 
        for e, w in v.items() 
        })

def make_graph(conns):
    nodes, nodes_index = get_nodes(conns)
    edges = get_edges(conns, nodes_index)

    net = Network(
        height='750px', 
        width='100%', 
        bgcolor='#222222', 
        font_color='white'
        )
    
    net.add_nodes(range(len(nodes)), label = nodes)

    for (e, q, w) in tqdm(edges, leave = False):
        net.add_edge(e, q, weigth = w)

    return net
