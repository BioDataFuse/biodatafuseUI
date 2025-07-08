# cytoscape_bridge.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from networkx.readwrite.json_graph import node_link_graph
from pyBiodatafuse.graph import cytoscape as cytoscape_graph

app = Flask(__name__)
CORS(app, supports_credentials=True)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@app.route('/load_graph_local', methods=['POST'])
def load_graph_local():
    try:
        data = request.get_json()
        graph_data = data.get('graph_data')
        network_name = data.get('network_name', 'BioDataFuse Network')

        if not graph_data:
            return jsonify({"status": "error", "message": "No graph data provided"}), 400

        if "elements" not in graph_data:
            return jsonify({"status": "error", "message": "'elements' key missing in graph data."}), 400

        elements = graph_data["elements"]
        nodes = elements.get("nodes", [])
        edges = elements.get("edges", [])

        nx_data = {
            "nodes": [],
            "links": [] 
        }

        for node in nodes:
            nx_data["nodes"].append({
                "id": node["data"]["id"], 
                **node["data"]  
            })

        for edge in edges:
            nx_data["links"].append({
                "source": edge["data"]["source"],  
                "target": edge["data"]["target"],  
                **edge["data"]  
            })

        adj_g = node_link_graph(nx_data)

        cytoscape_graph.load_graph(adj_g, network_name)

        return jsonify({"status": "success", "message": f"Graph '{network_name}' loaded into Cytoscape."}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)