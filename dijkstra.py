import networkx as nx
import math as m

def init(graph,s):
    n =graph.number_of_nodes()
    d=[m.inf]*(n+1)
    p=[None]*(n+1)
    d[s]=0
    return n,d,p

def relax(u,v,w,d,p):
    if d[v]>d[u]+w:
        d[v]=d[u]+w
        p[v]=u


def dijkstra(graph,s):
    n,d,p=init(graph,s)
    S=[]
    while len(S)!=n:
        u=min((v for v in graph.nodes if v not in S),key = lambda v:d[v])
        if d[u] == m.inf:
            print("Graf nie jest spojny")
            break
        S.append(u)
        for neighbor in graph.neighbors(u):
            if neighbor not in S:
                weight = graph[u][neighbor]['weight']
                relax(u,neighbor,weight,d,p)
    return d,p
    
def print_paths(d, p, s):
    print(f"START : s = {s}")
    for v in range(1, len(d)):
        path = []
        u = v
        while u is not None:
            path.append(u)
            u = p[u]
        path.reverse()
        path_str = " - ".join(map(str, path))
        print(f"d ({v}) = {d[v]} ==> [{path_str}]")

def matrix_d(graph):
    result=[]
    best_sum_value=m.inf
    best_sum_node=-1
    best_minmax_value=m.inf
    best_minmax_node=-1

    for i in sorted(graph.nodes()):
        temp=dijkstra(graph,i)[0][1:]
        result.append(temp)
        suma= sum(temp)
        minmax=max(temp)
        if suma<best_sum_value:
            best_sum_value=suma
            best_sum_node=i
        if minmax<best_minmax_value:
            best_minmax_value=minmax
            best_minmax_node=i
        print(temp,suma,minmax)
    print(f'Best sum is {best_sum_value} in node {best_sum_node} ')
    print(f'Best minmax is {best_minmax_value} in node {best_minmax_node}')
    return result
