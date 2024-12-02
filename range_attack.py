import random

import sympy
import networkx as nx
import matplotlib.pyplot as plt
import time
import numpy as np
import tqdm


def fast_augment_responses(responses):
    responses = remove_duplicates(responses)
    seen  = set()
    frozen_responses = []

    for i in responses:
        frozen_responses.append(frozenset(i))
        seen.add(frozenset(i))

    todo = []
    for i in tqdm.tqdm(frozen_responses):
        for j in frozen_responses:
            inter = i.intersection(j)
            if len(inter) > 0 and frozenset(inter) not in seen:
                todo.append(frozenset(inter))
                seen.add(frozenset(inter))


    frozen_responses.extend(todo)

    return remove_duplicates(frozen_responses)




# Map each record to the smallest response we have observed 
def reduce_to_domain_points(responses):
    d = {}
    for r in tqdm.tqdm(responses):
        for i in r:
            if i in d and len(d[i]) > len(r):
                d[i] = r
            elif i not in d:
                d[i] = r

    d_responses = {}
    for record in tqdm.tqdm(d):
        for i in range(len(responses)):
            if record in responses[i]:
                if record in d_responses:
                    d_responses[record].append(i)
                else:
                    d_responses[record] = [i]




    for record in tqdm.tqdm(d):
        remove = set()
        for ind in d_responses[record]:
            #sr = set(response)
            response = responses[ind]
            if record in response:
                for i in d[record]:
                    if i not in response:
                        remove.add(i)
        if len(remove) > 0:
            new_record = set(list(d[record])[:])
            for k in remove:
                new_record.remove(k)

            d[record] = new_record

    d =  make_d_consisten(d)
    return d


def remove_duplicates(responses):
    new_responses = []
    d = {}
    for i in tqdm.tqdm(responses):
        if frozenset(i) not in d:
            new_responses.append(i)
            d[frozenset(i)] = 0
    return new_responses



# Elements with the same domain value are replaced together with an ID
def translate_responses_domain(responses,d, plaintext=False):
    new_responses = []
    go_back = {}

    randoms = {}

    for response in responses:
        
        new_response = set()
        for i in response:
            # Elements that correspond to the same domain value have the same value in d. 
            if not plaintext:
                if tuple(sorted(d[i])) in randoms:
                    val = randoms[tuple(sorted(d[i]))]
                else:
                    val = random.randrange(10000000)
                    randoms[tuple(sorted(d[i]))] = val
                new_response.add(val)
                go_back[i] = val
            else:
                if tuple(sorted(d[i])) in randoms:
                    val = randoms[tuple(sorted(d[i]))]
                else:
                    val = i
                    randoms[tuple(sorted(d[i]))] = i
                new_response.add(i)
                go_back[i] = i               

        new_responses.append(new_response)
        assert(len(response)>=len(new_response))

    return new_responses,go_back


def find_prime_responses(responses, max_primes=0):
    primes = []
    for i in responses:
        if sympy.isprime(len(i)):
            if max_primes == 0  or (len(i) <=max_primes) :
                primes.append(i)

    return primes






def make_translator(col1,col2, R):
    translator = {}

    for row in R:
        inter1 = set(row).intersection(set(col1))
        inter2 = set(row).intersection(set(col2))

        if len(inter1) != 1 or len(inter2) != 1:
            continue

        # Each intersection should have one element, these elements should be on the same "x" coordinate
        translator[list(inter1)[0]] = inter2
        translator[list(inter2)[0]] = inter1

    return translator

def translate_responses(elem1, elem2, Orthogonals, groups):

    translator = make_translator(elem1,elem2, Orthogonals)
    added = set()

    for (a,b) in [(elem1,elem2), (elem2,elem1)]:
        for response in groups[a]:
            translated_response = []
            for element in response:
                if type(element) is set:
                    element = list(element)[0]
                
                if element in translator:
                    translated_response.append(list(translator[element])[0])
            if len(translated_response) == len(response) and tuple(sorted(list(translated_response))) not in added:
                if translated_response not in groups[b]:
                    groups[b].append(translated_response)
                added.add(tuple(sorted(list(translated_response))))

    return groups



#Endure that all keys in a value point to that value
def make_d_consisten(d):
    todo2 = set()

    todo = list(d.keys())[:]
    while todo:
        i = todo.pop()
        for j in d[i]:
            if d[i] != d[j]:
                inter = set(d[i]).intersection(set(d[j]))
                a = set(d[i]).difference(set(d[j]))
                b = set(d[j]).difference(set(d[i]))

                for k in [i,j]:
                    if k in a:
                        d[k] = a
                    elif k in b:
                        d[k] = b
                    else:
                        d[k] = inter
                todo2.update(a)
                todo2.update(b)
                todo2.update(inter)
                continue
        if len(todo) == 2:
            todo.extend(list(todo2))
            todo2 = set()
        

    return d



def make_simple_graph(tuples, go_back):
    G = nx.Graph()
    num_edges = {}
    done = set()

    reverse_go_back = {}

    for i in go_back:
        if go_back[i] in reverse_go_back:
            reverse_go_back[go_back[i]].append(i)
        else:
            reverse_go_back[go_back[i]] = [i]

    for (i,j) in tuples:
        if (i,j) not in done and (j,i) not in done:
            if i in num_edges:
                num_edges[i] += 1
            else:
                num_edges[i] = 1

            if j in num_edges:
                num_edges[j] += 1
            else:
                num_edges[j] = 1

            done.add((i,j))

    for (i,j) in tuples:
        G.add_edge(tuple(reverse_go_back[i]), tuple(reverse_go_back[j]))
    return G



def leakage_augment(responses):
    print("Augmenting Responses")
    responses = fast_augment_responses(responses)
    print("Reduce collocated points")
    d = reduce_to_domain_points(responses)
    new_responses, go_back = translate_responses_domain(responses,d)
    return new_responses, go_back




def general(responses):
    new_responses, go_back = leakage_augment(responses)

    print("Pick pair responses")
    tuples = find_prime_responses(new_responses, 2)

    print("Make graph")
    G = make_simple_graph(tuples,go_back)    
    return G, len(tuples)


