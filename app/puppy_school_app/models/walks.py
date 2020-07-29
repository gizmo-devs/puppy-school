from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for
)
from ..core.auth import login_required
from ..core.database import query_db, upsert_query

import datetime

bp = Blueprint('walks', __name__, url_prefix='/walks')

@bp.route('/')
@login_required
def index():
    dogs = query_db("""
SELECT 
    * 
FROM 
    dogs 
    LEFT JOIN 
        dog_habbits AS dh ON dogs.id=dh.dog_id 
WHERE 
    id IN (
    SELECT 
        dog_id 
    FROM 
        dog_owners 
    WHERE 
        user_id = ?
        )
""", [session['user_id']])
    data = []
    for dog in session['dogs']:
        dog_info = query_db(
            """SELECT id, name, dob FROM dogs WHERE id = ?""",
            [dog['id'],],
            one=True
        )
        dog_walks = query_db("""
        SELECT 
            dog_walks.*
        FROM 
            dog_walks 
            WHERE dog_id = ?
        ORDER BY walked_date desc
        """, [dog['id'],])
        #x =
        dog_data = dict(info=dog_info, walks=dog_walks) #, chart_colour=get_random_colour())
        dog_data['chart_data'] = get_chart_data(dog_data)

        data.append(dog_data)
    return render_template('walks/index.html', dog_data=data)


@bp.route('/upsert', defaults={'walk_id': None}, methods=['GET', 'POST'])
@bp.route('/upsert/<int:walk_id>', methods=['GET', 'POST'])
def upsert(walk_id):
    print (request.form)
    # collect data
    dog_id = request.form['inputDog']
    loc = request.form['inputLoc']
    behaviour = request.form['behaviour_options']
    social = request.form['socialised_options']
    callback = request.form['callback_options']
    notes = request.form['inputNotes']

    now = datetime.datetime.now()

    print(dog_id, behaviour, social, callback, loc, notes)

    total_score = sum([int(behaviour), int(social), int(callback)])

    print (total_score)

    if walk_id:
        query = "UPATE dog_walks SET dog_id=?, behaviour_score=?, callback_score=?, socialised_score=?, total_score=?, loc=, notes=?)"
        params = [dog_id, behaviour, callback, social, total_score, loc, notes]
    else:
        query = "INSERT INTO dog_walks (dog_id, behaviour_score, callback_score, socialised_score, total_score, loc, notes, walked_date) VALUES (?,?,?,?,?,?,?,?)"
        params = [dog_id, behaviour, callback, social, total_score, loc, notes, now]

    if upsert_query(query, params):
        pass
    else:
        flash("Walk could not be written to Database")
    return redirect(url_for('walks.index'))


def get_chart_data(data):
    # print("Printing GET CHART DATA")
    print(data)
    x = []
    rec = []
    #data['weights'].reverse()
    if len(data['walks']) > 0:
        for item in data['walks']:
            x.append(item['walked_date'])
            rec.append(item['total_score'])

    return x, rec
