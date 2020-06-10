from main import app
from api import api
from core import database as db, auth, scheduler
from models import dogs, weight, walks, training, loo, commands, feeds

from flask import render_template, session

import os

app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'puppy-school.sqlite'),
    )
try:
    os.makedirs(app.instance_path)
except OSError:
    pass


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
