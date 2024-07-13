from flask import current_app as app, request, jsonify
from app.utils.database import Database


@app.route('/conversations/create', methods=['POST'])
def createConversation():
    data = request.get_json()
    name = data.get('name')
    token = request.headers.get('Authorization')
    print(token)
    print(data)
    print(request.headers)
    user = Database('app/data.db').execute('select * from Users where token = ?', token)
    print(user)

    if len(user) == 0:
        return jsonify({'message': 'You are not authorized to see this'}), 401

    Database('app/data.db').execute('insert into Conversations (name) values (?)', name)

    result = Database('app/data.db').execute('select * from Conversations where name = ?', name)

    return jsonify({'id': result[0][0]}), 200


@app.route('/conversation/<name>', methods=['GET'])
def getConversation(name):
    token = request.headers.get('Authorization')

    user = Database('app/data.db').execute('select * from Users where token = ?', token)

    if len(user) == 0:
        return jsonify({'message': 'You are not authorized to see this'}), 401

    result = Database('app/data.db').execute('select conversation_id from Conversations where name = ?', name)
    
    return jsonify({'message': result[0][0]})


@app.route('/conversations', methods=['GET'])
def getConversations():
    token = request.headers.get('Authorization')

    user = Database('app/data.db').execute('select * from Users where token = ?', token)

    if len(user) == 0:
        return jsonify({'message': 'You are not authorized to see this'}), 401

    result = Database('app/data.db').execute('select * from Conversations')

    obj = []

    for conversation in result:
        print(conversation)
        obj.append({
            'conversation_id': conversation[0],
            'name': conversation[1]
        })

    print(obj)

    return jsonify(obj)
