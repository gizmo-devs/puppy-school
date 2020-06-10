import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from puppy_school_app.core.database import get_db, query_db
from puppy_school_app.core.scheduler import set_session

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        # username = request.form['username']
        password = request.form['inputPassword']
        first_name = request.form['inputFirstName'].title()
        surname = request.form['inputLastName'].title()
        email = request.form['inputEmailAddress'].lower()
        db = get_db()
        error = None

        if not email:
            error = 'Email is required.'
        elif not first_name:
            error = 'First Name is required.'
        elif not surname:
            error = 'Last Name is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM users WHERE email = ?', (email,)
        ).fetchone() is not None:
            error = 'User with the email address: {} is already registered.'.format(email)

        if error is None:
            db.execute(
                'INSERT INTO users (first_name, surname, email, password) VALUES (?,?,?,?)',
                (first_name, surname, email, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['inputEmailAddress'].lower()
        password = request.form['inputPassword']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM users WHERE email = ?', (email,)
        ).fetchone()

        if user is None:
            error = 'Incorrect Email Address.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('dashboard'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = query_db(
            'SELECT * FROM users WHERE id = ?', [user_id,], one=True)
        session['dogs'] = query_db(
            'SELECT id FROM dogs WHERE id IN (SELECT dog_id FROM dog_owners WHERE user_id = ?)',
            [user_id]
        )
        set_session()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view