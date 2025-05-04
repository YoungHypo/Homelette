from flask import request
from flask_socketio import emit, join_room, leave_room
from flask_jwt_extended import decode_token
from app.models.message import Message, Conversation
from app.models.user import User
from app import socketio, db
import uuid
from datetime import datetime

# mapping of online users and their socket ids
online_users = {}

@socketio.on('connect')
def handle_connect():
    try:
        # get token from query parameters
        token = request.args.get('token')
        if not token:
            return False  # reject connection
        
        # parse JWT token
        decoded_token = decode_token(token)
        user_id = decoded_token['sub']
        
        # validate user
        user = User.query.get(user_id)
        if not user:
            return False  # reject connection
        
        # mark user as online
        online_users[user_id] = request.sid
        
        # join user's own room (for receiving private messages)
        join_room(user_id)
        
        print(f"user {user_id} connected")
        
        # broadcast user online message to all connected clients
        emit('user_online', {'user_id': user_id}, broadcast=True)
        
        # send current online users list to user
        emit('online_users', {'users': list(online_users.keys())})
        
        return True
    except Exception as e:
        print(f"connection error: {str(e)}")
        return False

@socketio.on('disconnect')
def handle_disconnect():
    for user_id, sid in list(online_users.items()):
        if sid == request.sid:
            del online_users[user_id]
            print(f"user {user_id} disconnected")
            emit('user_offline', {'user_id': user_id}, broadcast=True)
            break

@socketio.on('join_conversation')
def handle_join_conversation(data):
    conversation_id = data.get('conversation_id')
    if not conversation_id:
        return
    
    join_room(conversation_id)
    print(f"user {request.sid} joined conversation {conversation_id}")

@socketio.on('leave_conversation')
def handle_leave_conversation(data):
    conversation_id = data.get('conversation_id')
    if not conversation_id:
        return
    
    leave_room(conversation_id)
    print(f"user {request.sid} left conversation {conversation_id}")

@socketio.on('private_message')
def handle_private_message(data):
    sender_id = data.get('sender_id')
    recipient_id = data.get('recipient_id')
    content = data.get('content')
    
    if not all([sender_id, recipient_id, content]):
        emit('error', {'message': 'missing required fields'})
        return
    
    # confirm sender is the user who is connected
    sender_sid = online_users.get(sender_id)
    if sender_sid != request.sid:
        emit('error', {'message': 'unauthorized'})
        return
    
    # create new message and save it
    try:
        message = Message(
            message_id=str(uuid.uuid4()),
            sender_id=sender_id,
            recipient_id=recipient_id,
            content=content
        )
        db.session.add(message)
        db.session.commit()
        
        # format message
        message_data = message.to_dict()
        
        # send message to recipient (if online)
        if recipient_id in online_users:
            emit('private_message', message_data, room=recipient_id)
        
        # confirm message delivered
        emit('message_delivered', message_data, room=sender_id)
    
    except Exception as e:
        db.session.rollback()
        emit('error', {'message': str(e)})

@socketio.on('conversation_message')
def handle_conversation_message(data):
    sender_id = data.get('sender_id')
    conversation_id = data.get('conversation_id')
    content = data.get('content')
    
    if not all([sender_id, conversation_id, content]):
        emit('error', {'message': 'missing required fields'})
        return
    
    # confirm sender is the user who is connected
    sender_sid = online_users.get(sender_id)
    if sender_sid != request.sid:
        emit('error', {'message': 'unauthorized'})
        return
    
    # validate conversation exists and user is a participant
    conversation = Conversation.query.get(conversation_id)
    if not conversation:
        emit('error', {'message': 'conversation not found'})
        return
    
    participant_ids = [p.user_id for p in conversation.participants]
    if sender_id not in participant_ids:
        emit('error', {'message': 'unauthorized to send message in this conversation'})
        return
    
    # create new message and save it
    try:
        message = Message(
            message_id=str(uuid.uuid4()),
            sender_id=sender_id,
            conversation_id=conversation_id,
            content=content
        )
        db.session.add(message)
        
        # update conversation updated time
        conversation.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        # format message
        message_data = message.to_dict()
        
        # send message to all members of the conversation
        emit('conversation_message', message_data, room=conversation_id)
    
    except Exception as e:
        db.session.rollback()
        emit('error', {'message': str(e)})

@socketio.on('typing')
def handle_typing(data):
    user_id = data.get('user_id')
    recipient_id = data.get('recipient_id')
    conversation_id = data.get('conversation_id')
    is_typing = data.get('is_typing', False)
    
    if not user_id:
        return
    
    typing_data = {
        'user_id': user_id,
        'is_typing': is_typing
    }
    
    # private chat typing status
    if recipient_id:
        emit('user_typing', typing_data, room=recipient_id)
    
    # group chat typing status
    elif conversation_id:
        emit('user_typing', typing_data, room=conversation_id) 