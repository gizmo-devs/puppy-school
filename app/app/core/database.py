#from ..models.user import User
import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = make_dicts

    return g.db


def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))


def query_db(query, args=(), one=False):
    # if parse(query)[0].get_type() == 'UNKNOWN':
    #     print("Collect query from SQL_QUERIES")
    #     query = next((dict_item['query'] for dict_item in SQL_QUERIES if dict_item['name'] == query), None)

    cur = get_db().cursor()
    cur.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def upsert_query(query, args=()):
    err = False
    db = get_db()
    cur = db.cursor()
    cur.execute(query, args)
    try:
        db.commit()
    except sqlite3.Error as e:
        print(e)
        err = True
    except Exception as e:
        print(e)
        err=True
    if err:
        print("!!! FAILED TO WRITE TO DATABASE !!!")
        return False
    else:
        return True

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()
    with current_app.open_resource('data-files/schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)



def get_users():
    sql = "get_users"
    users = query_db(sql, ['Lemon',"5"])
    print(users)
    return [User(item[0],item[1]) for item in users]


# =================================
SQL_QUERIES = [
    {
        "name": "get_users",
        "description": "Get user details from the table user.",
        "query": "SELECT first_name, surname FROM dev.user WHERE surname=%s ORDER BY id LIMIT %s;"
    }
]
