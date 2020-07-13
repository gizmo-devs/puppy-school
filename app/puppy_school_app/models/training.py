from flask import (
    Blueprint, redirect, render_template, request, session, url_for, jsonify
)
from ..core.auth import login_required
from ..core.database import get_db, query_db, upsert_query

import datetime, json

bp = Blueprint('training', __name__, url_prefix='/training')

@bp.route('/')
@login_required
def index():
    dog_data = []
    commands = query_db("SELECT * FROM dog_commands")
    for d in session['dogs']:
        # Get Dog Data
        dog = query_db("SELECT * FROM dogs WHERE id=?", [d['id'],], one=True)
        # Get Dog training Data
        dog_commands = query_db("""SELECT  *  FROM  dog_training_link JOIN dog_commands as DC ON command_id = DC.id
                    WHERE dog_id = ?""", [ d['id'] ] )

        dog_dict = dict(info=dog, dog_training=dog_commands)

        for c in dog_commands:
            tom_index = next((index for (index, d) in enumerate(dog_dict['dog_training']) if d["command_id"] == c['id']), None)
            #print(tom_index)
            dogs_progress = query_db("""SELECT * FROM dog_training_progress WHERE dog_id = ? and command_id = ? ORDER BY rec_date desc""", [ d['id'], c['id'] ])
            dog_dict['dog_training'][tom_index]['progress'] = dogs_progress


        dog_data.append(dog_dict)
    print(json.dumps(dog_data, default=myconverter))
    return render_template('training/index.html', dog_data=dog_data, commands=commands)


@bp.route('/upsert', methods=['POST'])
def upsert():
    print(request.form)
    dog_id = request.form['inputDog']
    now = datetime.datetime.now()
    params = []
    for v in request.form:
        if v != 'inputDog' and request.form[v] != '0':
            params += [(dog_id, v.split('_')[1], request.form[v], now)]
    print(params)
    query = "INSERT INTO dog_training_progress (dog_id, command_id, command_progress, rec_date) VALUES (?,?,?,?)"
    db = get_db()
    db.executemany(query, params)
    db.commit()
    db.close()
    return redirect(url_for('training.index'))


@bp.route('/<int:dog_id>/command-link', methods=['GET', 'POST'])
def command_link(dog_id):
    if request.method == 'POST':
        print(request.form)
        if request.form['action'] == 'add':
            query = "INSERT INTO dog_training_link (dog_id, command_id) VALUES (?,?)"
        else:
            query = "DELETE FROM dog_training_link WHERE dog_id=? and command_id=?"
        return jsonify(upsert_query(query, [request.form['dog_id'], request.form['command_id']]))
    else:
        dog = query_db("SELECT * FROM dogs WHERE id=?", [dog_id], one=True)
        query = 'SELECT * FROM dog_commands LEFT JOIN dog_training_link as DTL ON DTL.command_id = id WHERE dog_id = ? or dog_id is null'
        dog_training = query_db(query, [dog_id])
        for d in dog_training:
            tom_index = next((index for (index, d) in enumerate(dog_training) if d["dog_id"]), None)
            print(query_db("SELECT command_progress FROM dog_training_progress WHERE dog_id=? and command_id=? ORDER BY rec_date desc LIMIT 1", [d['dog_id'], d['command_id']]))

    return render_template('training/link_commands.html', dog_info=dog, dog_training=dog_training)

@bp.route('/dog/<dog_id>', methods=['GET', 'POST'])
def dog_training(dog_id):
    if request.method == 'GET':
        query = '''SELECT * FROM dog_commands
        LEFT JOIN
        dog_training_link as DTL
        ON DTL.command_id = id
        WHERE dog_id = ?'''
        return jsonify(query_db(query, dog_id))


def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

@bp.route('/chart/<dog_id>')
def get_chart_data(dog_id, chart_type="summary"):
    if chart_type == "summary":
        query = """SELECT 
            command, command_progress, rec_date
        FROM 
            dog_training_progress
            join dog_commands on command_id = dog_commands.id
        WHERE 
            dog_id = ?
        group by 
            command_id"""
    else:
        pass

    return jsonify(query_db(query, [dog_id]))