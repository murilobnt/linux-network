# File: linux-network.py
# Author: Murilo Bento
#
# MIT License
#
# Copyright (c) 2020 Murilo Bento
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN

# --- IMPORTS ---

import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

from nxviz import CircosPlot

# ---------------

# --- DATA ACQUISITION AND REFINEMENT ---

edges = pd.read_csv('./input/edges.csv')
nodes = pd.read_csv('./input/nodes.csv')

nodes = nodes.iloc[:,[0]]

edges.columns = ["source", "target"]
nodes.columns = ["index"]

data = nodes.set_index('index').to_dict().items()
G = nx.from_pandas_edgelist(edges)
G.add_nodes_from(data)

# ---------------

# --- METRICS ---

deg_cen = nx.degree_centrality(G)

nodes = sorted(deg_cen.items(), key=lambda x:x[1], reverse=True)[0:25]
nodes_keys = []
for node in nodes:
    nodes_keys.append(node[0])

H = G.subgraph(nodes_keys)

cen_btw = nx.betweenness_centrality(H)
cen_ei = nx.eigenvector_centrality(H)
cen_clos = nx.closeness_centrality(H)
cc = nx.clustering(H)

for v in H.nodes():
    node = H.nodes[v]
    node['degree'] = deg_cen[v]
    node['betweeness'] = cen_btw[v]
    node['eigenvector'] = cen_ei[v]
    node['closeness'] = cen_clos[v]
    node['clustering'] = float(cc[v])

# ---------------

# --- PLOTTING ---

indexes = ['degree', 'betweeness', 'eigenvector', 'closeness', 'clustering']

for i in indexes:
    current = CircosPlot(H, title=i, node_color=i, node_order=i, node_labels=True)
    current.draw()

    plt.title(i.capitalize())
    plt.suptitle(i.capitalize())
    plt.savefig(f"output/{i}.png")

# ---------------
