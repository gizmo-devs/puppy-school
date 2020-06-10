from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from core.database import get_db, query_db
from core.auth import login_required

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


@bp.route('/upsert', defaults={'dog_id': 'empty'}, methods=['GET', 'POST'])
@bp.route('/upsert/<int:dog_id>', methods=['GET', 'POST'])
@login_required
def upsert(dog_id=None):
    if dog_id is not None:
        dog = query_db("SELECT * FROM dogs LEFT JOIN dog_habbits AS dh on dogs.id=dh.dog_id WHERE id = ?", [dog_id,], one=True)

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
        error = None

        if not dog_name:
            error = "Please provide a Dog Name."
        elif not dog_dob:
            error = "Please provide a Dog DOB."
        elif not dog_gender:
            error = "No gender provided."

        if error is None:
            db = get_db()
            cur = db.cursor()
            print("Hello", dog_id)
            if dog_id:
                cur.execute("UPDATE dogs SET name=?, dob=?, gender=?, bread=? WHERE id = ?",
                    [dog_name, dog_dob, dog_gender, dog_bread, dog_id]
                )
                cur.execute(
                    "UPDATE dog_habbits SET food_intervals=?, loo_intervals=?, walk_intervals=?, alone_intervals=? "
                    "WHERE dog_id=?", [habbit_feed, habbit_loo, habbit_walk, habbit_alone, dog_id])

            else:
                cur.execute("INSERT INTO dogs (name, dob, gender, bread) VALUES (?, ?, ?, ?)",
                    [dog_name, dog_dob, dog_gender, dog_bread]
                )
                # Get id to link to user
                dog_id = cur.lastrowid
                cur.execute("INSERT INTO dog_owners (dog_id, user_id) VALUES (?, ?)", [dog_id, session['user_id']])

                print(type(x) for x in [dog_id, habbit_feed, habbit_loo, habbit_walk, habbit_alone])
                cur.execute("INSERT INTO dog_habbits (dog_id, food_intervals, loo_intervals, walk_intervals, alone_intervals) "
                         "VALUES (?,?,?,?,?)", [dog_id, habbit_feed, habbit_loo, habbit_walk, habbit_alone])

            try:
                db.commit()
            except sqlite3.Error as e:
                print(e)
            except Exception as e:
                print(e)

            return redirect(url_for('dogs.index'))

        flash(error)

    return render_template('dogs/upsert.html', dog=dog)
