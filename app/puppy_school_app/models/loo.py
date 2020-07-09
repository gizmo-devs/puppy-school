from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for
)
from ..core.scheduler import set_session
from ..core.auth import login_required
from ..core.database import query_db, upsert_query

import datetime

bp = Blueprint('loo', __name__, url_prefix='/loo')

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
        dog_loos = query_db("""
        SELECT 
            lb.*
        FROM 
            loo_breaks AS lb 
            WHERE dog_id = ?
        ORDER BY break_time desc
        """, [dog['id'],])
        last_break = query_db("""
        SELECT 
            break_time
        FROM 
            loo_breaks AS lb 
            WHERE dog_id = ?
        ORDER BY break_time desc
        """, [dog['id'],], one=True)
        dog_data = dict(info=dog_info, last_break=last_break, loo_breaks=dog_loos) #, chart_colour=get_random_colour())
        data.append(dog_data)
    return render_template('loo/index.html', dog_data=data)


@bp.route('/upsert', defaults={'loo_id': None}, methods=['GET', 'POST'])
@bp.route('/upsert/<int:loo_id>', methods=['GET', 'POST'])
def upsert(loo_id):
    # collect data
    dog_id = request.form['inputDog']
    type = [request.form[x] for x in request.form if str(x).endswith('_options')] # if x.endswith('_options')
    notes = request.form['inputNotes']

    now = datetime.datetime.now()

    print(dog_id, type, notes)

    if loo_id:
        query = "UPDATE loo_breaks SET dog_id=?, loo_type=?"
        params = [dog_id, type]
    else:
        for each in type:
            query = "INSERT INTO loo_breaks (dog_id, break_time, loo_type) VALUES (?,?,?)"
            params = [dog_id, now, each]

            if upsert_query(query, params):
                if upsert_query("UPDATE dog_last SET last_loo_break=? WHERE dog_id=?", [now, dog_id]):
                    pass
                set_session()
            else:
                flash("Loo Break could not be written to Database", "Error")
    return redirect(url_for('loo.index'))


def get_chart_data(data):
    # print("Printing GET CHART DATA")
    print(data)
    x = []
    rec = []
    #data['weights'].reverse()
    if len(data['loos']) > 0:
        for item in data['walks']:
            x.append(item['walked_date'])
            rec.append(item['total_score'])

    return x, rec
