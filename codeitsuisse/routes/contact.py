import logging
import json
import numpy as np

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/contact_trace', methods=['POST'])
def evaluate_contact():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    result = contact(**data)
    logging.info("My result :{}".format(result))
    return result


def get_dist(gene1, gene2):
    pos = 0
    dist = 0
    while (pos<len(gene1)):
        dist += 1*(gene1[pos:pos+4]!=gene2[pos:pos+4])
        pos += 4
    return dist
    

def contact(infected, origin, cluster):
    inf_gene = infected["genome"]
    og_gene = origin["genome"]
    
    dim = len(cluster) + 2
    dists = np.zeros((dim, dim))
    genes = [inf_gene, og_gene] + [i["genome"] for i in cluster]
    # create array of distances
    for g in range(len(genes)):
        base = genes[g]
        for h in range(g, len(genes)):
            if h == g:
                dists[h][g] = 999
            else:
                dists[g][h] = get_dist(base, genes[h])
                dists[h][g] = dists[g][h]
    
    paths = [[0]]
    visited = {0:0}
    complete_paths = []

    # treat paths as a stack
    while len(paths) > 0:
        added = 0
        path = paths[0]
        paths = paths[1:]
        gene_no = path[-1]
        min_val = dists[gene_no].min()
        for i in range(len(genes)):
            if (dists[gene_no][i] == min_val) and (visited.get(i) is None):
                dists[gene_no][i] += 1
                paths.append(path + [i])
                visited[i] = 0
                added += 1
        
        if added == 0:
            complete_paths.append(path)
    
    # convert the complete paths into strings
    for p in range(len(complete_paths)):
        path = complete_paths[p]
        path_str = ""
        while len(path)>0:
            i = path[0]
            if i>1:
                name = cluster[i-2]["name"]
            elif i==1:
                name = origin["name"]
            else:
                name = infected["name"]
            
            if len(path)>2:
                name += "* -> "
            elif len(path)>1:
                name += " -> "
            path_str += name
            path = path[1:]
        complete_paths[p] = path_str
    return complete_paths



