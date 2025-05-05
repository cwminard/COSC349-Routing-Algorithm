from flask import Flask, render_template, request
import networkx as nx
import matplotlib.pyplot as plt


#network = nx.Graph()
nodes_weights = {'A'}
app = Flask(__name__)

def id_shortest_path(network, source, target):
    try:
        path = nx.dijkstra_path(network, source=source, target=target)
        return path
    except nx.NetworkXNoPath:
        return None
    

def configure_graph(src, dest):
    client_edge_wt = 5
    client_edges = [('Client 1','Client 2', client_edge_wt),('Client 2','Client 3', client_edge_wt),('Client 4','Client 5',client_edge_wt), ('Client 5','Client 6', client_edge_wt)]
    client_server_wt = 4
    client_server_edges = [('Server 1','Client 1', client_server_wt),('Server 1','Client 4',client_server_wt),('Server 2','Client 1',client_server_wt)
                            ,('Server 2','Client 2',client_server_wt),('Server 2','Client 4',client_server_wt),('Server 2','Client 5',client_server_wt),
                            ('Server 3','Client 2',client_server_wt),('Server 3','Client 3',client_server_wt),('Server 3','Client 5',client_server_wt)
                            ,('Server 3','Client 6',client_server_wt),('Server 4','Client 3',client_server_wt),('Server 4','Client 6',client_server_wt)]
    server_edge_wt = 7
    server_edges = [('Server 1','Server 2',server_edge_wt),('Server 2','Server 3',server_edge_wt),('Server 3','Server 4',server_edge_wt)]


    network = nx.Graph()
    network.add_node('Server 1')
    network.add_node('Server 2')
    network.add_node('Server 3')
    network.add_node('Server 4')
    server_nodes = ['Server 1', 'Server 2', 'Server 3', 'Server 4']

    network.add_node('Client 1')
    network.add_node('Client 2')
    network.add_node('Client 3')
    network.add_node('Client 4')
    network.add_node('Client 5')
    network.add_node('Client 6')
    client_nodes = ['Client 1', 'Client 2', 'Client 3', 'Client 4', 'Client 5', 'Client 6']

    network.add_weighted_edges_from(client_server_edges) # Edges with weight 4
    network.add_weighted_edges_from(server_edges) # Edges with weight 7
    network.add_weighted_edges_from(client_edges) # Edges with weight 2
    
    position = nx.spring_layout(network)
    nx.draw(network, pos=position, with_labels=True, font_size=10, font_color='black', font_weight='bold')
    nx.draw_networkx_nodes(network, pos=position, nodelist=server_nodes, node_color='#728be8', node_size=1200)
    nx.draw_networkx_nodes(network, pos=position, nodelist=client_nodes, node_color='#eb6eeb', node_size=800)
    nx.draw_networkx_edges(network, pos=position, edgelist=server_edges,width=7, alpha=0.5, edge_color='#042291')
    nx.draw_networkx_edges(network, pos=position, edgelist=client_edges,width=7, alpha=0.5, edge_color='#cc37cc')
    nx.draw_networkx_edges(network, pos=position, edgelist=client_server_edges,width=7, alpha=0.5, edge_color='#abe02d')
    edge_labels = nx.get_edge_attributes(network, 'weight')
    nx.draw_networkx_edge_labels(network, pos=position, edge_labels=edge_labels, font_color='black')
    #plt.title("Network Graph", fontsize=20, fontweight='bold')
    #plt.show()
    
    path = id_shortest_path(network, src, dest)
    return path


@app.route('/', methods=['GET', 'POST'])
def generate_path():
    if request.method == 'POST':
        src = request.form.get('source')
        dest = request.form.get('destination')
        if not src or not dest:
            return render_template('graph.html', error="Source and destination must be provided.")
        path = configure_graph(src, dest)
        if path:
            path_str = " -> ".join(path)
        else:
            path_str = "No path found between the given nodes."
        return render_template('graph.html', source=src, destination=dest, path=path_str)
    return render_template('graph.html')
