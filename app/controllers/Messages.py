from flask import current_app as app, request, jsonify
from app.utils.database import Database


@app.route('/messages/<conversation>', methods=['GET'])
def getConversationMessages(conversation):
    token = request.headers.get('Authorization')
    user = Database(
        'app/data.db').execute('select * from Users where token = ?', token)

    if len(user) == 0:
        return jsonify({'message': 'You are not authorized to see this'}), 401

    result = Database('app/data.db').execute(
        'SELECT content, message_id, sent_at, sender_id FROM Messages where conversation_id = ?', conversation)

    obj = []

    for message in result:
        user = Database(
            'app/data.db').execute('select username from Users where user_id = ?', message[3])
        obj.append({
            'content': message[0],
            'message_id': message[1],
            'sent_at': message[2],
            'sender': user[0][0]
        }
        )

    return jsonify(obj)


@app.route('/messages/create', methods=['POST'])
def createMessage():
    data = request.get_json()
    conversation_id = data.get('conversation_id')
    content = data.get('content')
    token = request.headers.get('Authorization')
    print(token)
    user = Database(
        'app/data.db').execute('select * from Users where token = ?', token)
    print(user)

    if len(user) == 0:
        return jsonify({'message': 'You are not authorized to see this'}), 401

    Database('app/data.db').execute('insert into Messages (conversation_id, sender_id, content) values (?, ?, ?)',
                                    conversation_id, user[0][0], content)

    return jsonify({'message': 'created message'})
