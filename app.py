from flask import Flask, render_template, request, session, redirect, url_for, jsonify, send_file
from components.graph_creation.id_mapper import bridgedb_xref
from components.graph_creation.id_input import process_identifiers
from components.graph_creation.id_annotator import process_selected_sources
import pandas as pd

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route("/")
def index():
    return render_template("about.html")

@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/graph_creation", methods=["GET", "POST"])
def gc_id_input():
    if request.method == "POST":
        text_input = request.form.get("text_input")
        file_upload = request.files.get("file_upload")
        ids_df, warnings = process_identifiers(file_upload, text_input)
        if ids_df:
            session["ids_df"] = ids_df
            ids_df = pd.DataFrame(ids_df)
            no_input_ids = len(ids_df["identifier"].unique())
            session["no_input_ids"] = no_input_ids
        if warnings:
            return jsonify({"error": str(warnings)})

        id_type = request.form.get("identifier_type")
        if id_type:
            session["id_type"] = id_type

        return render_template("gc_id_mapper.html", ids_df=ids_df, id_type=id_type, no_input_ids=no_input_ids)
    
    return render_template(
        "gc_id_input.html",
        no_input_ids=session.get("no_input_ids")
    )

@app.route("/graph_creation/gc_id_mapper/", methods=["GET", "POST"])
def gc_id_mapper():
    ids_df = pd.DataFrame(session.get("ids_df"))
    id_type = session.get("id_type")
    bridgedb_df, bridgedb_metadata = bridgedb_xref(
        identifiers=ids_df,
        input_species="Human",
        input_datasource=id_type
    )
    session["bridgedb_df"] = bridgedb_df.to_dict("records")
    session["bridgedb_metadata"] = bridgedb_metadata

    if request.method == "POST":
        return redirect(url_for("gc_datasource"))

    return render_template(
        "gc_id_mapper.html",
        ids_df=session["ids_df"],
        id_type=session["id_type"],
        no_input_ids=session["no_input_ids"],
        bridgedb_df_empty = bridgedb_df.empty)
  
@app.route("/graph_creation/gc_datasource/", methods=["GET", "POST"])
def gc_datasource():
    if request.method == "POST":
        datasource = request.form.getlist("datasource_selected")
        if not datasource:
            return jsonify({"error": "Please select at least one datasource"})
        
        session["datasource"] = datasource
        return redirect(url_for("gc_annotator"))
    else:
        return render_template("gc_datasource.html")  

@app.route("/graph_creation/gc_annotator/", methods=["GET", "POST"])
def gc_annotator():
    datasource = session["datasource"]
    bridgedb_df = pd.DataFrame(session["bridgedb_df"])
    combined_data, combined_metadata = process_selected_sources(bridgedb_df, datasource)
    session["combined_data"] = combined_data.to_dict("records")
    session["combined_metadata"] = combined_metadata

    if request.method == "POST":
        return redirect(url_for("gc_graph_generator"))
    else: 
        return render_template(
            "gc_annotator.html",
            datasource = datasource,
            combined_data = session["combined_data"],
            combined_metadata = combined_metadata 
            )

@app.route("/graph_creation/get_combined_data/")
def get_combined_data():
    combined_data = session.get("combined_data")
    combined_data = pd.DataFrame(combined_data)
    temp_file_path = "temp_combined_data.tsv"
    combined_data.to_csv(temp_file_path, sep="\t", index=False)
    
    return send_file(temp_file_path, as_attachment=True, download_name="combined_data.tsv")

@app.route("/graph_creation/get_metadata/")
def get_metadata():
    combined_metadata = session.get("combined_metadata")
    return combined_metadata

@app.route("/graph_creation/gc_graph_generator/", methods=["GET", "POST"])
def gc_graph_generator():
    combined_data = session["combined_data"]
    combined_data = pd.DataFrame(combined_data)

    if request.method == "POST":
        return redirect(url_for("ga_graph_statistics.html"))
    
    return render_template("gc_graph_generator.html")

@app.route("/graph_analysis/")
def graph_analysis():
    return render_template("graph_analysis.html")

@app.route("/clear_session/", methods=["POST"])
def clear_session():
    session.clear()
    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(debug=True)
