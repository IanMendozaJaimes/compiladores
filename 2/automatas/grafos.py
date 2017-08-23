import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()

G.add_edge("1","1")

pos=nx.spring_layout(G)

# nodes
nx.draw_networkx_nodes(G, pos, node_size=500, node_color="blue")

# edges
nx.draw_networkx_edges(G, pos,
        width=2, alpha=0.5, edge_color='black')

# labels
nx.draw_networkx_labels(G, pos, font_size=5, font_family='sans-serif')

nx.draw_networkx_edge_labels(G, pos, {
    ('1','1'):'h'
}, label_pos=0.3, with_labels = True)

plt.show();
