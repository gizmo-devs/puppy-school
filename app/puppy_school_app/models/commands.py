from flask import (
    Blueprint, render_template, request
)
from ..core.auth import login_required
from ..core.database import query_db, upsert_query

bp = Blueprint('command', __name__, url_prefix='/command')

@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == "POST":
        print(request)
        command = request.form['inputNewCommandName']
        level = request.form['inputNewCommandLevel']
        desc = request.form['inputNewCommandDesc']

        query = "INSERT INTO dog_commands (command, level, description) VALUES(?,?,?)"
        if not upsert_query(query, [command, level, desc]):
            print("Cannot write to Database")

    commands = query_db("SELECT * FROM dog_commands")
    return render_template('commands/index.html', dog_commands=commands)