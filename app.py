from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify
from components.graph_creation.id_mapper import bridgedb_xref
from components.graph_creation.id_input import process_identifiers
import pandas as pd

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def index():
    # flash('Welcome to BioDataFuse!')
    return render_template('about.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/graph_creation', methods=['GET', 'POST'])
def gc_id_input():
    if request.method == 'POST':
        text_input = request.form.get('text_input')
        file_upload = request.files.get('file_upload')

        ids_df, warnings = process_identifiers(file_upload, text_input)

        if ids_df:
            session['ids_df'] = ids_df
            ids_df = pd.DataFrame(ids_df)
            no_input_ids = len(ids_df['identifier'].unique())
            session['no_input_ids'] = no_input_ids

        if warnings:
            return jsonify({'error': warnings})

        return redirect(url_for('gc_id_type'))
   
    return render_template('gc_id_input.html')

@app.route('/graph_creation/gc_id_type', methods=['GET', 'POST'])
def gc_id_type():
    ids_df = session.get('ids_df')

    if request.method == 'POST':
        id_type = request.form.get('identifier_type')
        if not id_type:
            return jsonify({'error': 'Please select an identifier type'})
        if id_type:
            session['id_type'] = id_type

        return redirect(url_for('gc_id_mapper'))
 
    return render_template(
        'gc_id_type.html',
        ids_df=ids_df,
        no_input_ids=session.get('no_input_ids')
        )

@app.route('/graph_creation/gc_id_mapper', methods=['GET', 'POST'])
def gc_id_mapper():
    ids_df = pd.DataFrame(session.get('ids_df'))
    id_type = session.get('id_type')
    bridgdb_df, bridgdb_metadata = bridgedb_xref(
        identifiers=ids_df,
        input_species="Human",
        input_datasource=id_type
    )

    session['bridgdb_df'] = bridgdb_df.to_dict('records')
    session['bridgdb_metadata'] = bridgdb_metadata

    if request.method == 'POST':
        return redirect(url_for('gc_datasource'))

    return render_template(
        'gc_id_mapper.html',
        ids_df=session['ids_df'],
        id_type=session['id_type'],
        no_input_ids=session['no_input_ids'],
        bridgdb_df_empty = bridgdb_df.empty)
  
@app.route('/graph_creation/gc_datasource',  methods=['GET', 'POST'])
def gc_datasource():
    if request.method == 'POST':
        datasource = request.form.getlist('datasource_selected')
        if not datasource:
            return jsonify({'error': 'Please select at least one datasource'})
        if datasource:
            session['datasource'] = datasource

        return redirect(url_for('gc_annotators'))
 
    return render_template('gc_datasource.html')    

@app.route('/graph_creation/gc_annotators', methods=['GET', 'POST'])
def gc_annotators():
    print('I am here')
    return render_template('gc_annotators.html')

@app.route('/graph_analysis')
def graph_analysis():
    return render_template('graph_analysis.html')

@app.route('/clear_session', methods=['POST'])
def clear_session():
    session.clear()
    return 'Session cleared'

if __name__ == '__main__':
    app.run(debug=True)
