# cytoscape_bridge.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import py4cytoscape as p4c
import json
import logging
import os

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
            logger.error("No graph data provided.")
            return jsonify({"status": "error", "message": "No graph data provided"}), 400

        logger.debug(f"Incoming raw graph_data: {json.dumps(graph_data, indent=2)}")
        processed_graph_data = {}

        if "elements" not in graph_data and "nodes" in graph_data and "edges" in graph_data:
            logger.info("Wrapping graph data with 'elements' key for Cytoscape.js format.")
            processed_graph_data = {"elements": graph_data}
        else:
            processed_graph_data = graph_data

        logger.info(f"Attempting to load network '{network_name}' into Cytoscape Desktop...")

        p4c.create_network_from_cytoscapejs(
            json.dumps(processed_graph_data), 
            title=network_name,
            collection="BioDataFuse"
        )
        logger.info(f"Graph '{network_name}' successfully loaded into Cytoscape Desktop.")
        return jsonify({"status": "success", "message": f"Graph '{network_name}' loaded into Cytoscape."}), 200

    except Exception as e:
        logger.error(f"Error loading graph into Cytoscape: {e}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
