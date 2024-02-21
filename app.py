from flask import Flask, render_template, request, session, redirect, url_for
from pyBiodatafuse.id_mapper import bridgedb_xref

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/graph_creation', methods=['GET', 'POST'])
def gc_id_input():
    if request.method == 'POST':
        ids = request.form.get('text_input')
        if not ids:
            return render_template('gc_id_input.html', warnings='Please enter at least one identifier')
        session['ids_df'] = ids
        return redirect(url_for('gc_id_type'))
    return render_template('gc_id_input.html')

@app.route('/graph_creation/gc_id_type', methods=['GET', 'POST'])
def gc_id_type():
    if request.method == 'POST':
        id_type = request.form.get('identifier_type')
        if not id_type:
            return render_template('gc_id_type.html', warnings='Please select an identifier type')
        session['id_type'] = id_type
        return redirect(url_for('gc_id_mapper'))
    return render_template('gc_id_type.html')

@app.route('/graph_creation/gc_id_mapper', methods=['GET', 'POST'])
def gc_id_mapper():
    if 'ids' in session and 'id_type' in session:
        if request.method == 'POST':
            bridgdb_df, bridgdb_metadata = bridgedb_xref(
                identifiers=session['ids_df'], 
                input_datasource=['id_type'],
                input_species="Human")
            session['bridgdb_df'] = bridgdb_df
            session['bridgdb_metadata'] = bridgdb_metadata
            # Set session variable to indicate mapping step is done
            session['mapping_done'] = True
            return render_template('gc_datasource.html')
        return render_template('gc_id_mapper.html')

    else:
        return redirect(url_for('gc_id_input'))

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
    
if __name__ == '__main__':
    app.run(debug=True)
