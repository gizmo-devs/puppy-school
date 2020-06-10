from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for, jsonify
)
from core.auth import login_required
from core.database import get_db, query_db, upsert_query

import datetime

bp = Blueprint('weight', __name__, url_prefix='/weight')

@bp.route('/')
@login_required
def index():
    data = []
    for dog in session['dogs']:
        dog_info = query_db(
            """SELECT id, name FROM dogs WHERE id = ?""",
            [dog['id'],],
            one=True
        )
        dog_weights = query_db("""
        SELECT 
            dog_weights.*
            , u.first_name
            , u.surname
        FROM 
            dog_weights 
            JOIN users as u ON measured_by=u.id WHERE dog_id = ?
        ORDER BY dog_weights.date_measured desc
        """, [dog['id'],])
        #x =
        dog_data = dict(info=dog_info, weights=dog_weights, chart_colour=get_random_colour())

        dog_data['chart_data'] = get_chart_data(dog_data)

        data.append(dog_data)


    print(data)

    x=None
    return render_template('weight/index.html', dog_data=data)


@bp.route('/upsert', defaults={'weight_id': None}, methods=['GET', 'POST'])
@bp.route('/upsert/<weight_id>', methods=['GET', 'POST'])
@login_required
def upsert(weight_id=None):
    if request.method == 'POST':
        print(request.form)
        dog_id = request.form['inputDog']
        dog_weight = request.form['inputWeight']
        user_id = session['user_id']

        db = get_db()
        cur = db.cursor()
        if weight_id:
                query = "UPDATE dog_weight SET dog_id=?, weight=?, date_measured=?, measured_by=? WHERE id = ?"
                params = [dog_id, dog_weight, datetime.date.today(), user_id, weight_id]

        else:
            query = "INSERT INTO dog_weights (dog_id, weight, date_measured, measured_by) VALUES (?, ?, ?, ?)"
            params = [dog_id, dog_weight, datetime.date.today(), user_id]

        if upsert_query(query, params):
            if upsert_query("UPDATE dog_last SET last_weighed=? WHERE dog_id=?", [datetime.datetime.now(), dog_id]):
                pass
        else:
            flash("Weight could not be written to the Database", "Error")

        return redirect(url_for('weight.index'))


@bp.route('record/get/<id>')
def get_weight_record(id):
    return jsonify(query_db("SELECT * FROM dog_weights WHERE id = ?", [id,], one=True))


@bp.route('record/get/dog/<dog_id>')
def get_dogs_weights(dog_id):
    return jsonify(query_db("SELECT weight, date_measured FROM dog_weights WHERE dog_id=? LIMIT 12", [dog_id,]))


def get_chart_data(data):
    # print("Printing GET CHART DATA")
    # print(data)
    x = []
    rec = []
    #data['weights'].reverse()
    if len(data['weights']) > 0:
        for item in data['weights']:
            x.append(item['date_measured'])
            rec.append(item['weight'])

    return x, rec



def get_random_colour(opacity=0.6):
    from random import randrange
    return "rgba({}, {}, {}, {})".format(randrange(0, 255), randrange(0, 255), randrange(0, 255), opacity)
