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
            return jsonify(error='missing or invalid data'), 400
    return catch_missing


@api.route('/database/clear/')
def database_clear():
    try:
        os.remove('mese.db')
    except:
        pass
    with open('schema.sql', 'r') as schema:
        sql = schema.read()
        with sqlite3.connect('mese.db') as connection:
            cursor = connection.cursor()
            cursor.executescript(sql)
    return jsonify(result='database cleared')


@api.route('/users/', methods=['POST'])
@needs_user_input
def user_create():
    name = request.args.get('name')
    with sqlite3.connect('mese.db') as connection:
        cursor = connection.cursor()
        cursor.execute('INSERT INTO User(name) VALUES(?)', (name,))
        return jsonify(result='user created')


@api.route('/users/')
def user_retrieve_all():
    with sqlite3.connect('mese.db') as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute('SELECT id, name FROM User')
        return jsonify(result=[dict_from_row(row) for row in cursor.fetchall()])


@api.route('/users/<_id>/')
def user_retrieve(_id):
    with sqlite3.connect('mese.db') as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute('SELECT id, name FROM User WHERE id = ?', (_id, ))
        return jsonify(result=dict_from_row(cursor.fetchone()))


@api.route('/users/<_id>/', methods=['PUT'])
@needs_user_input
def user_update(_id):
    name = request.args.get('name')
    with sqlite3.connect('mese.db') as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute('UPDATE User SET name = ? WHERE id = ?', (name, _id, ))
        return jsonify(result=dict_from_row(cursor.fetchone()))


@api.route('/users/<_id>/', methods=['DELETE'])
def user_delete(_id):
    with sqlite3.connect('mese.db') as connection:
        cursor = connection.cursor()
        cursor.execute('DELETE FROM User WHERE id = ?', (_id, ))
        return jsonify(result='user deleted')
