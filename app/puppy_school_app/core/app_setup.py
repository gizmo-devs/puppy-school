# from main import app
# from api import api
from ..core import database as db, auth, scheduler
from ..models import feeds, weight, training, dogs, loo, commands, walks

from flask import render_template, current_app as app

import os
print(app.instance_path)
app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'puppy-school.sqlite'),
    )
try:
    os.makedirs(app.instance_path)
    db.init_db()
except OSError:
    pass


@app.errorhandler(404)
def page_not_found(e):
    print(e)
    return render_template('layout/e404.html')
@app.errorhandler(500)
def page_not_found(e):
    print(e)
    return render_template('layout/e500.html')

db.init_app(app)
app.register_blueprint(auth.bp)
app.register_blueprint(dogs.bp)
app.register_blueprint(weight.bp)
app.register_blueprint(walks.bp)
app.register_blueprint(training.bp)
app.register_blueprint(commands.bp)
app.register_blueprint(loo.bp)
app.register_blueprint(feeds.bp)
app.register_blueprint(scheduler.bp)

@app.route("/")
@auth.login_required
def dashboard():
    # This could also be returning an .html
    scheduler.set_session()
    return render_template('dashboard.html')
