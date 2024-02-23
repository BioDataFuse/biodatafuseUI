from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify
from pyBiodatafuse.id_mapper import bridgedb_xref
from components.graph_creation.id_input import process_identifiers

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def index():
    # flash('Welcome to BioDataFuse!')
    return render_template('about.html')

@app.route('/about')
def about():
    return render_template('about.html')

ALLOWED_EXTENSIONS = {'txt', 'csv'}  # Define allowed file extensions

def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/graph_creation', methods=['GET', 'POST'])
def gc_id_input():
    if request.method == 'POST':
        text_input = request.form.get('text_input')
        file_upload = request.files.get('file_upload')

        ids_df, warnings = process_identifiers(file_upload, text_input)

        if ids_df:
            session['ids_df'] = ids_df

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
    
    return render_template('gc_id_type.html', ids_df=ids_df)


@app.route('/graph_creation/gc_id_mapper', methods=['GET', 'POST'])
def gc_id_mapper():
    ids_df = session.get('ids_df')
    id_type = session.get('id_type')
    if not (ids_df and id_type):
        return redirect(url_for('gc_id_input'))

    if request.method == 'POST':
        bridgdb_df, bridgdb_metadata = bridgedb_xref(
            identifiers=ids_df, 
            input_datasource=[id_type],  # You need to pass the actual id_type, not the string 'id_type'
            input_species="Human"
        )
        session['bridgdb_df'] = bridgdb_df
        session['bridgdb_metadata'] = bridgdb_metadata
        return redirect(url_for('gc_datasource'))
    return render_template('gc_id_mapper.html', ids_df=session['ids_df'], id_type=session['id_type'])

@app.route('/render_template')
def render_template_route():
    if 'bridgdb_df' in session and 'ids_df' in session and 'id_type' in session:
        bridgdb_df = session['bridgdb_df']
        ids_df = session['ids_df']
        id_type = session['id_type']
        bridgdb_df_empty = bridgdb_df["target"].str.strip().eq("").all()
        return render_template('gc_id_mapper.html', bridgdb_df=bridgdb_df, ids_df=ids_df, id_type=id_type, bridgdb_df_empty=bridgdb_df_empty)
    else:
        # If any of the required session variables are missing, redirect to the input page
        return redirect(url_for('gc_id_input'))
    
@app.route('/graph_analysis')
def graph_analysis():
    return render_template('graph_analysis.html')

@app.route('/clear_session', methods=['POST'])
def clear_session():
    session.clear()
    return 'Session cleared'

if __name__ == '__main__':
    app.run(debug=True)
