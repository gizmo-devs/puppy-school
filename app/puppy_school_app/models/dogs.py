from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for
)
from ..core.database import get_db, query_db, upsert_query
from ..core.auth import login_required

import sqlite3
bp = Blueprint('dogs', __name__, url_prefix='/dogs')


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
    return render_template('dogs/index.html', dogs=dogs)


@bp.route('/upsert', defaults={'dog_id': None}, methods=['GET', 'POST'])
@bp.route('/upsert/<int:dog_id>', methods=['GET', 'POST'])
@login_required
def upsert(dog_id=None):
    if dog_id is not None:
        dog = query_db("SELECT * FROM dogs LEFT JOIN dog_habbits AS dh on dogs.id=dh.dog_id WHERE id = ?", [dog_id,], one=True)
    else:
        dog = None

    if request.method == 'POST':
        print(request.form)
        dog_name = request.form['inputDogName']
        dog_dob = "-".join([
            request.form['inputDogDOBYear'],
            request.form['inputDogDOBMonth'],
            request.form['inputDogDOBDay']
        ])
        dog_gender = request.form['genderOptions']
        dog_bread = request.form['inputDogBread']
        habbit_loo = request.form['inputLoo']
        habbit_walk = request.form['inputWalk']
        habbit_feed = request.form['inputFeeds']
        habbit_alone = request.form['inputAlone']
        weighin_interval = request.form['inputWeighin']
        error = None

        if not dog_name:
            error = "Please provide a Dog Name."
        elif not dog_dob:
            error = "Please provide a Dog DOB."
        elif not dog_gender:
            error = "No gender provided."

        if error is None:
            #db = get_db()
            #cur = db.cursor()

            if dog_id:
                query = "UPDATE dogs SET name=?, dob=?, gender=?, bread=? WHERE id = ?"
                params = [dog_name, dog_dob, dog_gender, dog_bread, dog_id]
                print('Updating dog record in Database')
                if upsert_query(query, params):
                    query = "UPDATE dog_habbits SET daily_feeds=?, loo_intervals=?, walk_intervals=?, alone_intervals=?, weight_intervals_in_weeks=? WHERE dog_id=?"
                    params = [habbit_feed, habbit_loo, habbit_walk, habbit_alone, weighin_interval, dog_id]
                    print('Updating dogs habbits in Database')
                    upsert_query(query, params)

            else:
                query = "INSERT INTO dogs (name, dob, gender, bread) VALUES (?, ?, ?, ?)"
                params = [dog_name, dog_dob, dog_gender, dog_bread]
                new_dog_id = upsert_query(query, params)
                # Get id to link to user
                if new_dog_id:
                    q = "INSERT INTO dog_owners (dog_id, user_id) VALUES (?, ?)"
                    params = [new_dog_id, session['user_id']]
                    upsert_query(q, params)
                    q = "INSERT INTO dog_habbits (dog_id, daily_feeds, loo_intervals, walk_intervals, alone_intervals, weight_intervals_in_weeks) VALUES (?,?,?,?,?,?)"
                    params = [new_dog_id, habbit_feed, habbit_loo, habbit_walk, habbit_alone, weighin_interval]
                    upsert_query(q, params)

            return redirect(url_for('dogs.index'))

        flash(error)

    return render_template('dogs/upsert.html', dog=dog)
