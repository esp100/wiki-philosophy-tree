from pyvis.network import Network
import networkx as nx
from IPython.display import HTML
from src.node import Node
from src.scrapping import all_the_ways_lead_to


def add_to_tree(branch, tree=None):
  if tree is None:
    root = Node(branch[-1])
    
    node = root
    for value in reversed(branch[:-1]):
      child = Node(value)
      node.child[value] = child
      node = child 

    return root
  else:
    node = tree 

    for value in reversed(branch[:-1]):
      if value not in node.child:
        node.child[value] = Node(value)

      node = node.child[value]
    return tree 


def build_networkx_graph(node, G=None, level=0):
    if G is None:
        G = nx.DiGraph()
    
    node_id = str(node.value)
    
    if level == 0:
        G.add_node(
            node_id,
            level=level,
            size=30,
            color="#FF5733",
            font={"size": 18, "bold": True}
        )
    else:
        G.add_node(node_id, level=level)

    for child in node.child.values():
        child_id = str(child.value)
        G.add_edge(node_id, child_id)
        build_networkx_graph(child, G, level=level + 1)
        
    return G

def plot_tree(root_node):
    G = build_networkx_graph(root_node)
    
    net = Network(height="600px", width="100%", directed=True, notebook=True, cdn_resources='in_line')
    net.from_nx(G)
    
    for edge in net.edges:
        edge['arrows'] = 'from'  
    
    net.set_options("""
    {
      "layout": {
        "hierarchical": {
          "enabled": true,
          "direction": "DU",
          "sortMethod": "directed",
          "levelSeparation": 90,
          "nodeSpacing": 140,
          "treeSpacing": 160
        }
      },
      "interaction": {
        "dragNodes": true,
        "zoomView": true,
        "dragView": true
      },
      "physics": {
        "hierarchicalRepulsion": {
          "centralGravity": 0.0,
          "springLength": 80,
          "nodeDistance": 130
        },
        "solver": "hierarchicalRepulsion"
      },
      "edges": {
        "arrows": {
          "to": { "enabled": false },
          "from": { "enabled": false }
        },
        "smooth": {
          "enabled": true,
          "type": "cubicBezier",
          "forceDirection": "vertical",
          "roundness": 0.5
        }
      }
    }
    """)
    return HTML(net.generate_html())

def leaf_page_to_graph(leaf_page, reset=False):

    if reset or not hasattr(leaf_page_to_graph, "tree"):
        leaf_page_to_graph.tree = None

    path = all_the_ways_lead_to(leaf_page)
    
    leaf_page_to_graph.tree = add_to_tree(path, leaf_page_to_graph.tree)
    
    return plot_tree(leaf_page_to_graph.tree)
