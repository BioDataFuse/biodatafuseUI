# cytoscape_bridge.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import py4cytoscape as p4c
import json
import logging
import os
from networkx.readwrite.json_graph import node_link_graph

app = Flask(__name__)
CORS(app, supports_credentials=True)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

try:
    import pyBiodatafuse.constants as const
    logger.info("Successfully imported constants from pyBiodatafuse.")

    _GENE_NODE_LABELS = const.GENE_NODE_LABEL
    _ANATOMICAL_NODE_LABELS = const.ANATOMICAL_NODE_LABEL
    _DISEASE_NODE_LABELS = const.DISEASE_NODE_LABEL
    _GO_BP_NODE_LABELS = const.GO_BP_NODE_LABEL
    _GO_MF_NODE_LABELS = const.GO_MF_NODE_LABEL
    _GO_CC_NODE_LABELS = const.GO_CC_NODE_LABEL
    _PATHWAY_NODE_LABELS = const.PATHWAY_NODE_LABEL
    _COMPOUND_NODE_LABELS = const.COMPOUND_NODE_LABEL
    _SIDE_EFFECT_NODE_LABELS = const.SIDE_EFFECT_NODE_LABEL
    _HOMOLOG_NODE_LABELS = const.HOMOLOG_NODE_LABEL

except AttributeError as e:
    logger.error(f"AttributeError: {e}. This likely means the expected constants are not directly available in 'pyBiodatafuse.constants'.")

except ImportError as e:
    logger.warning(f"Could not import constants from pyBiodatafuse: {e}. "
                   "Ensure 'pyBiodatafuse' is installed and its constants.py "
                   "contains the expected variable names. "
                   "Reverting to hardcoded values (styling may be inaccurate).")


def apply_cytoscape_style(network_name: str):
    default_style = {
        "title": "BioDataFuse_style",
        "defaults": [
            {"visualProperty": "NODE_FILL_COLOR", "value": "#FF0000"},
            {"visualProperty": "EDGE_COLOR", "value": "#000000"},
            {"visualProperty": "NODE_SIZE", "value": 30},
            {"visualProperty": "EDGE_WIDTH", "value": 2},
            {"visualProperty": "NODE_LABEL_FONT_SIZE", "value": 10},
        ],
        "mappings": [],
    }

    p4c.styles.create_visual_style(default_style)
    logger.info("Base Cytoscape style created.")

    column = "labels"
    values = [
        [_GENE_NODE_LABELS],
        [_ANATOMICAL_NODE_LABELS],
        [_DISEASE_NODE_LABELS],
        [_GO_BP_NODE_LABELS],
        [_GO_MF_NODE_LABELS],
        [_GO_CC_NODE_LABELS],
        [_PATHWAY_NODE_LABELS],
        [_COMPOUND_NODE_LABELS],
        [_SIDE_EFFECT_NODE_LABELS],
        [_HOMOLOG_NODE_LABELS],
    ]
    shapes = [
        "ELLIPSE",  # Genes
        "HEXAGON",  # Anatomical
        "VEE",  # Diseases
        "PARALLELOGRAM",  # GO BP
        "ROUND_RECTANGLE",  # GO MF
        "RECTANGLE",  # GO CC
        "OCTAGON",  # Pathways
        "DIAMOND",  # Compounds
        "TRIANGLE",  # Side Effects
        "Ellipse",  # Homologs
    ]
    colors = [
        "#42d4f4",  # Cyan for Genes
        "#4363d8",  # Blue for Anatomical
        "#e6194B",  # Red for Diseases
        "#ff7b00",  # Orange for GO BP
        "#ffa652",  # Orange for GO MF
        "#ffcd90",  # Orange for GO CC
        "#3cb44b",  # Green for Pathways
        "#ffd700",  # Gold for Compounds
        "#aaffc3",  # Mint for Side Effects
        "#9b59b6",  # Purple for Homologs
    ]

    p4c.set_node_color_mapping(
        table_column=column,
        table_column_values=values,
        colors=colors,
        mapping_type="d",
        style_name="BioDataFuse_style",
        network=network_name
    )
    logger.info("Node color mapping applied.")

    p4c.set_node_shape_mapping(
        table_column=column,
        table_column_values=values,
        shapes=shapes,
        style_name="BioDataFuse_style",
        network=network_name
    )
    logger.info("Node shape mapping applied.")

    p4c.layouts.apply_layout("force-directed", network=network_name)
    logger.info(f"Layout 'force-directed' applied to '{network_name}'.")

@app.route('/load_graph_local', methods=['POST'])
def load_graph_local():
    try:
        data = request.get_json()
        graph_data = data.get('graph_data')
        network_name = data.get('network_name', 'BioDataFuse Network')

        if not graph_data:
            return jsonify({"status": "error", "message": "No graph data provided"}), 400

        # Ensure the correct structure
        if "elements" not in graph_data:
            return jsonify({"status": "error", "message": "'elements' key missing in graph data."}), 400

        elements = graph_data["elements"]
        nodes = elements.get("nodes", [])
        edges = elements.get("edges", [])

        # Convert graph data into the correct structure for node_link_graph
        # This should be a dict with keys: nodes and links (without 'elements')
        nx_data = {
            "nodes": [],
            "links": []  # Use 'links' instead of 'edges'
        }

        # Extract nodes
        for node in nodes:
            nx_data["nodes"].append({
                "id": node["data"]["id"],  # Ensure that each node has an 'id' field
                **node["data"]  # Add any other properties from node["data"]
            })

        # Extract edges
        for edge in edges:
            nx_data["links"].append({
                "source": edge["data"]["source"],  # Ensure there is a source
                "target": edge["data"]["target"],  # Ensure there is a target
                **edge["data"]  # Add other edge properties
            })

        # Now call node_link_graph with the correct structure
        adj_g = node_link_graph(nx_data)

        # Call load_graph to apply style to the Cytoscape network
        load_graph(adj_g, network_name)

        return jsonify({"status": "success", "message": f"Graph '{network_name}' loaded into Cytoscape."}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

def load_graph(g, network_name):
    """Load the obtained graph into a running instance of Cytoscape."""
    adj_g = g

    # Step 1: Create the network in Cytoscape
    p4c.networks.create_network_from_networkx(
        adj_g,
        title=network_name,
        collection="BioDataFuse",
    )

    # Step 2: Define the visual style as a dictionary
    default = {
        "title": "BioDataFuse_style",
        "defaults": [
            {"visualProperty": "NODE_FILL_COLOR", "value": "#FF0000"},
            {"visualProperty": "EDGE_COLOR", "value": "#000000"},
            {"visualProperty": "NODE_SIZE", "value": 30},
            {"visualProperty": "EDGE_WIDTH", "value": 2},
            {"visualProperty": "NODE_LABEL_FONT_SIZE", "value": 10},
        ],
        "mappings": [],
    }

    # Step 3: Create the visual style if not already created
    try:
        p4c.styles.create_visual_style(default)
        print(f"Visual style 'BioDataFuse_style' created successfully.")
    except Exception as e:
        print(f"Error creating visual style: {e}")

    # Step 4: Set the visual style to the network
    style_name = "BioDataFuse_style"
    try:
        # Set visual style to the network
        p4c.styles.set_visual_style(style_name, network=network_name)
        print(f"Visual style '{style_name}' applied to network '{network_name}' successfully.")
    except Exception as e:
        print(f"Error applying visual style '{style_name}' to network '{network_name}': {e}")

    # Step 5: Define node shape and color mapping
    column = "label"  # Column name from the node data (adjust based on your data)
    values = [
        "GENE", "ANATOMICAL", "DISEASE", "GO_BP", "GO_MF", "GO_CC", "PATHWAY", 
        "COMPOUND", "SIDE_EFFECT", "HOMOLOG", "KEY_EVENT", "MIE", "AOP", "AO"
    ]
    shapes = [
        "ELLIPSE", "HEXAGON", "VEE", "PARALLELOGRAM", "ROUND_RECTANGLE", 
        "RECTANGLE", "OCTAGON", "DIAMOND", "TRIANGLE", "Ellipse", "TRIANGLE", 
        "TRIANGLE", "VEE", "OCTAGON"
    ]
    colors = [
        "#42d4f4", "#4363d8", "#e6194B", "#ff7b00", "#ffa652", "#ffcd90", 
        "#3cb44b", "#ffd700", "#aaffc3", "#9b59b6", "#aaffc3", "#3cb44b", 
        "#000075", "#e6194B"
    ]

    # Step 6: Apply node color mapping
    try:
        p4c.set_node_color_mapping(
            column,
            values,
            colors,
            mapping_type="d",  # Apply as discrete values
            style_name=style_name,  # Reference to the visual style
            network=network_name
        )
        print("Node color mapping applied successfully.")
    except Exception as e:
        print(f"Error applying node color mapping: {e}")

    # Step 7: Apply node shape mapping
    try:
        p4c.set_node_shape_mapping(
            column,
            values,
            shapes,
            style_name=style_name,  # Reference to the visual style
            network=network_name
        )
        print("Node shape mapping applied successfully.")
    except Exception as e:
        print(f"Error applying node shape mapping: {e}")

    # Step 8: Apply layout (optional)
    try:
        p4c.layouts.apply_layout("force-directed", network=network_name)
        print("Layout applied successfully.")
    except Exception as e:
        print(f"Error applying layout: {e}")



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
