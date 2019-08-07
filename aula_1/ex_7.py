#!/usr/bin/python3

import os
import sys
import hashlib
import bson

import flask
import pymongo
import jwt


client = pymongo.MongoClient()
db = client.frank

app = flask.Flask(__name__)

def extract(user):
        user['_id'] = str(user['_id'])
        del user['password']
        return user

@app.route('/users/auth', methods=[ 'POST' ])
def auth_users():

    form = flask.request.json

    required_attributes = [ 'email', 'password']

    for attr in required_attributes:
        if attr not in form:
            return flask.jsonify({
                'message': 'attribute {} required' .format(attr)
            }), 400

    email, password = [ form[key] for key in required_attributes ]
    user = db.users.find_one({ 'email': email })

    if not user:
        return flask.jsonify({
            'message': 'user not found'
            }), 404

    if user.get('password') == hashlib.sha256(password.encode()).hexdigest():

        user = extract(user)

        user['token'] = jwt.encode(user, 'secret')

        return flask.jsonify({
            'user': user
            }), 200

    return flask.jsonify({
        'message': 'wrong password'
        }), 400

@app.route('/users', methods=[ 'GET' ])
def get_users():

        params = dict(flask.request.args)
        for key in params.keys():
            try:
                params[key] = int(params[key])
            except ValueError:
                pass

        users = [
            extract(u) for u in db.users.find(params)
        ]

        return flask.jsonify({
                'users': users
        })

@app.route('/users', methods=[ 'POST' ])
def post_users():
    
        form = flask.request.json

        required_attributes = [ 'email', 'password', 'age']

        for attr in required_attributes:
                if attr not in form:
                        return flask.jsonify({
                                'message': 'attribute {} required' .format(attr)
                                }), 400

        user = db.users.find_one({'email': form.get('email')})

        if user:
             return flask.jsonify({
                'message': 'email already exists'
        }), 400

        form['password'] = hashlib.sha256(form['password'].encode()).hexdigest()

        db.users.insert_one(form)
        
        return flask.jsonify({
                'message': 'user created'
        }), 201

        print(form)
        
@app.route('/users/<userid>', methods=[ 'GET' ])
def get_user_by_id(userid):
    user = db.users.find_one({'_id': bson.ObjectId(userid)})

    if not user:
        return flask.jsonify({
            'message': 'user not found'
        }),404
    return flask.jsonify({
            'users': extract(user)
    }), 200

@app.route('/users/<userid>', methods=[ 'PUT', 'PATCH' ])
def update_user_by_id(userid):
    user = db.users.find_one({'_id': bson.ObjectId(userid)})

    if not user:
        return flask.jsonify({
            'message': 'user not found'
        }),404

    for key in flask.request.json:
        if key in user:
            user[key] = flask.request.json[key]
            if key == 'password':
                user[key] = hashlib.sha256(user[key].encode()).hexdigest()
                
    db.users.update({'_id': bson.ObjectId(userid) }, user)

    return flask.jsonify({
            'user': extract(user)
        })

@app.route('/users/<userid>', methods=[ 'DELETE' ])
def delete_user_by_id(userid):
    user = db.users.find_one({'_id': bson.ObjectId(userid)})

    if not user:
        return flask.jsonify({
            'message': 'user not found'
            }), 404

    db.users.remove({'_id': bson.ObjectId(userid) }, user)

    return flask.jsonify({
            'user': extract(user)
        }), 200

if __name__ == "__main__":
    
    root_module = os.path.abspath(os.path.curdir)
    sys.path.append(root_module)

    os.environ['FLASK_APP'] = 'ex_7.py'
    os.environ['FLASK_ENV'] = 'development'

    app.run(host='0.0.0.0', debug=True)