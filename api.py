import os
import sqlite3
from flask import Blueprint
from flask import jsonify
from flask import request

api = Blueprint('api', __name__)


def dict_from_row(row):
    return dict(zip(row.keys(), row))


def needs_user_input(fn):
    def catch_missing(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except sqlite3.IntegrityError:
            return jsonify(error='missing or invalid data')
    return catch_missing


@api.route('/database/clear/')
def database_clear():
    try:
        os.remove('mese.db')
    except:
        pass
    with open('mese.schema', 'r') as schema:
        sql = schema.read()
        with sqlite3.connect('mese.db') as connection:
            cursor = connection.cursor()
            cursor.executescript(sql)
    return jsonify(result='database cleared')


@api.route('/user/list/')
def user_list():
    with sqlite3.connect('mese.db') as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute('SELECT id, name FROM User')
        return jsonify(result=[dict_from_row(row) for row in cursor.fetchall()])


@api.route('/user/new/')
@needs_user_input
def user_new():
    name = request.args.get('name')
    with sqlite3.connect('mese.db') as connection:
        cursor = connection.cursor()
        cursor.execute('INSERT INTO User(name) VALUES(?)', (name,))
        return jsonify(result='user created')


@api.route('/user/<_id>/')
def user_get(_id):
    with sqlite3.connect('mese.db') as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute('SELECT id, name FROM User WHERE id = ?', (_id, ))
        return jsonify(result=dict_from_row(cursor.fetchone()))


@api.route('/user/<_id>/delete/')
def user_delete(_id):
    with sqlite3.connect('mese.db') as connection:
        cursor = connection.cursor()
        cursor.execute('DELETE FROM User WHERE id = ?', (_id, ))
        return jsonify(result='user deleted')
