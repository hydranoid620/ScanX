import json
import math

import MySQLdb
import MySQLdb.cursors
import requests
from flask import Flask, render_template, jsonify, request, session

app = Flask(__name__, static_url_path='')
app.secret_key = b'A+jWl4h6wMkR7LcWBm85AO8q'


def get_db() -> MySQLdb.Connection:
    db = MySQLdb.connect(host='<hostnameOrIpOfOurDataBase>',
                         user='<username>',
                         passwd='<password>',
                         db='<databseName>')
    return db


def check_db_table():
    # Makes sure the table exists and has the right columns
    db = get_db()
    db.cursor().execute('CREATE TABLE IF NOT EXISTS `users` (`name` TINYTEXT, `password` TINYTEXT)')
    db.commit()
    db.close()


check_db_table()


# Serves the main HTML page
@app.route('/')
def index(name=None):
    return render_template('index.html', name=name)

# example of using sessions if we plan on it in the future 
"""
@app.route('/login', methods=['POST'])
def login():
    request_json = request.get_json(force=True)
    db = get_db()
    db_cursor = db.cursor()

    # Try and find the user in the database
    if db_cursor.execute('SELECT * FROM users WHERE username=%s', (request_json['username'],)) > 0:
        if db_cursor.fetchall()[0][1] != request_json['password']:
            # Incorrect password
            db.close()
            return jsonify(message='Invalid login'), 401
    else:
        # User does not exist in the database, register them
        try:
            db_cursor.execute('INSERT INTO users VALUES (%s, %s)', (request_json['username'], request_json['password']))
            db.commit()
            db.close()
            session['username'] = request_json['username']
            session['logged_in'] = True
            return jsonify(newAccount=True), 200
        except MySQLdb.Error as e:
            db.rollback()
            db.close()
            return jsonify(message=e.args), 500

    # Set session variables and return logged in user
    db.close()
    session['username'] = request_json['username']
    session['logged_in'] = True
    return jsonify(message='Logged in', newAccount=False), 200


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    session['logged_in'] = False
    return jsonify(message='OK'), 200
"""




# Delete user from database example
@app.route('/users', methods=['DELETE'])
def delete_user():
    db = get_db()
    try:
        db.cursor().execute('DELETE FROM users WHERE username=%s', (session['username'],))
        db.commit()
        db.close()
        # Clear the session cookie
        session.pop('username', None)
        session.pop('logged_in', None)
        return jsonify(message='OK'), 200
    except MySQLdb.Error as e:
        db.rollback()
        db.close()
        return jsonify(message=e.args), 500









# example of using a url param
@app.route('/ficsit/<mod_id>', methods=['GET'])
def mod_details(mod_id):
    response = make_query(json.dumps({'query': 'query {getMod(modId: "' + mod_id + '") {versions{link} full_description logo hotness downloads popularity}}'}))
    return jsonify(json.loads(response.text)['data']['getMod']), 200