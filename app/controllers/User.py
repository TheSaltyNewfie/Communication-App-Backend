from flask import current_app as app, request, jsonify
from app.utils.database import Database
from ..utils.security import hashPassword, generateToken, checkPassword


@app.route('/users/create', methods=['POST'])
def createUser():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    token = generateToken(32)

    password_hash = hashPassword(password)

    Database('app/data.db').execute(f'insert into Users (username, email, password_hash, token) VALUES (?, ?, ?, ?)',
                                    username, email, password_hash, token)

    user = Database(
        'app/data.db').execute('SELECT * FROM Users WHERE username = ?', username)

    return jsonify({'token': token, 'sender_id': user[0][0]}), 201


@app.route('/users/authenticate', methods=['POST'])
def authenticateUser():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    password_hash = hashPassword(password)
    print(password_hash)

    user = Database(
        'app/data.db').execute('SELECT * FROM Users WHERE username = ?', username)

    isUser = checkPassword(password, user[0][3])

    token = generateToken(32)

    Database('app/data.db').execute('UPDATE Users SET token = ? WHERE username = ?', token, username)

    if isUser:
        return jsonify({'token': token, 'sender_id': user[0][0]}), 200
    else:
        return jsonify({'message': 'failed'}), 401


@app.route('/users/<id>', methods=['GET'])
def getUsers(id):
    users = Database('app/data.db').execute('select username, email from Users where user_id = ?', id)

    obj = {
        'username': users[0][0],
        'email': users[0][1]
    }

    if len(users) == 0:
        return jsonify({'message': 'no user found'}), 404

    return jsonify(obj)


@app.route('/account', methods=['GET'])
def getAccount():
    token = request.headers.get('Authorization')
    user = Database('app/data.db').execute('select username from Users where token = ?', token)

    if len(user) == 0:
        return jsonify({'message': 'invalid token'}), 401
    else:
        return jsonify({'username': user[0][0]})


@app.route('/users/reset', methods=['PUT'])
def resetPassword():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    try:
        Database('app/data.db').execute('update Users set password = ? WHERE username = ? and email = ?', password, username, email)
        
        return jsonify({'message': 'successful'})
    except Exception as e:
        return jsonify({'error': e})
