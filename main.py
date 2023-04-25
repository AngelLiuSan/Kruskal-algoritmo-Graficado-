import networkx as nx
import matplotlib.pyplot as plt


def kruskal(G):
    edges = list(G.edges.data('weight'))
    edges.sort(key=lambda x: x[2])  # ordenar las aristas por peso
    mst = nx.Graph()
    parent = dict()
    rank = dict()

    def make_set(node):
        parent[node] = node
        rank[node] = 0

    def find(node):
        if parent[node] != node:
            parent[node] = find(parent[node])
        return parent[node]

    def union(node1, node2):
        root1 = find(node1)
        root2 = find(node2)
        if root1 != root2:
            if rank[root1] > rank[root2]:
                parent[root2] = root1
            else:
                parent[root1] = root2
                if rank[root1] == rank[root2]: rank[root2] += 1

    for node in G.nodes:
        make_set(node)
        pos = nx.spring_layout(G)
        nx.draw_networkx_nodes(G, pos, node_size=2000, nodelist=None, node_color="tab:orange", alpha=0.75)
        nx.draw_networkx_nodes(G, pos, nodelist=node, node_color="green", alpha=0.75)
        nx.draw_networkx_edges(G, pos, alpha=0.5, width=6)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'))
        label_options = {"ec": "k", "fc": "white", "alpha": 0.7}
        nx.draw_networkx_labels(G, pos, font_size=14, bbox=label_options)
        ax = plt.gca()
        ax.margins(0.20)
        plt.axis("off")
        plt.show()
    for edge in edges:
        node1, node2, weight = edge
        if find(node1) != find(node2):
            union(node1, node2)
            mst.add_edge(node1, node2, weight=weight)

    return mst


datos = []
lineas = []
l = []
n = []
nodos = int(input("no de nodos: "))
for i in range(nodos):
    l.append(i)
i = 0
with open("in2.txt") as archivo:
    for linea in archivo:
        if i in l:
            lineas.append(linea)
        i = i + 1

for i in lineas:
    n.append(i.rstrip('\n'))

G = nx.Graph()
for i in n:
    G.add_node(i)

G.add_edge(n[2], n[1], weight=3)
G.add_edge(n[0], n[1], weight=2)
G.add_edge(n[2], n[0], weight=4)
G.add_edge(n[0], n[3], weight=1)

origen = input("Ingresa un nodo origen: ")
destino = input("Ingresa un nodo destino: ")

mst = kruskal(G)
total_cost = sum([w for _, _, w in mst.edges.data('weight')])
print("El costo total del árbol generador mínimo es:", total_cost)

pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True)
nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'))
nx.draw(mst, pos, edge_color='r', with_labels=True)
nx.draw_networkx_edge_labels(mst, pos, edge_labels=nx.get_edge_attributes(mst, 'weight'))
nx.draw_networkx_nodes(G, pos, node_size=2000, nodelist=None, node_color="tab:orange", alpha=0.75)
nx.draw_networkx_nodes(G, pos, nodelist=None, node_color="green", alpha=0.75)
plt.show()

