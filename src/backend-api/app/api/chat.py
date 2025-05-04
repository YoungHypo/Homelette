from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.message import Message, Conversation, ConversationParticipant
from app.models.user import User
from app import db
from datetime import datetime
import uuid

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/conversations', methods=['GET'])
@jwt_required()
def get_conversations():
    """get all conversations for the current user"""
    user_id = get_jwt_identity()
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "user not found"}), 404
    
    conversations = user.conversations
    
    return jsonify({
        "success": True,
        "data": [conv.to_dict() for conv in conversations]
    }), 200

@chat_bp.route('/conversations', methods=['POST'])
@jwt_required()
def create_conversation():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data or 'participants' not in data:
        return jsonify({"error": "missing participant information"}), 400
    
    # ensure creator is also in the participants list
    participants = data['participants']
    if user_id not in participants:
        participants.append(user_id)
    
    # validate all participants exist
    for participant_id in participants:
        if not User.query.get(participant_id):
            return jsonify({"error": f"user {participant_id} not found"}), 404
    
    # create conversation
    conversation = Conversation()
    if 'title' in data:
        conversation.title = data['title']
    db.session.add(conversation)
    
    # add participants
    for participant_id in participants:
        user = User.query.get(participant_id)
        conversation.participants.append(user)
    
    db.session.commit()
    
    return jsonify({
        "success": True,
        "data": conversation.to_dict()
    }), 201

@chat_bp.route('/conversations/<conversation_id>', methods=['GET'])
@jwt_required()
def get_conversation(conversation_id):
    user_id = get_jwt_identity()
    
    # validate conversation exists and user is a participant
    conversation = Conversation.query.get(conversation_id)
    if not conversation:
        return jsonify({"error": "conversation not found"}), 404
    
    if user_id not in [p.user_id for p in conversation.participants]:
        return jsonify({"error": "unauthorized to access this conversation"}), 403
    
    return jsonify({
        "success": True,
        "data": conversation.to_dict()
    }), 200

@chat_bp.route('/conversations/<conversation_id>/messages', methods=['GET'])
@jwt_required()
def get_messages(conversation_id):
    user_id = get_jwt_identity()
    
    # validate conversation exists and user is a participant
    conversation = Conversation.query.get(conversation_id)
    if not conversation:
        return jsonify({"error": "conversation not found"}), 404
    
    if user_id not in [p.user_id for p in conversation.participants]:
        return jsonify({"error": "unauthorized to access this conversation"}), 403
    
    # get messages, sorted by timestamp
    messages = Message.query.filter(
        Message.conversation_id == conversation_id
    ).order_by(Message.timestamp.asc()).all()
    
    return jsonify({
        "success": True,
        "data": [msg.to_dict() for msg in messages]
    }), 200

@chat_bp.route('/messages/direct', methods=['GET'])
@jwt_required()
def get_direct_messages():
    """get messages with a specific user"""
    user_id = get_jwt_identity()
    other_user_id = request.args.get('user_id')
    
    if not other_user_id:
        return jsonify({"error": "missing user ID parameter"}), 400
    
    # validate user exists
    if not User.query.get(other_user_id):
        return jsonify({"error": "user not found"}), 404
    
    # get all messages between the two users
    messages = Message.query.filter(
        ((Message.sender_id == user_id) & (Message.recipient_id == other_user_id)) |
        ((Message.sender_id == other_user_id) & (Message.recipient_id == user_id))
    ).order_by(Message.timestamp.asc()).all()
    
    return jsonify({
        "success": True,
        "data": [msg.to_dict() for msg in messages]
    }), 200

@chat_bp.route('/messages/<message_id>/read', methods=['PUT'])
@jwt_required()
def mark_as_read(message_id):
    user_id = get_jwt_identity()
    
    message = Message.query.get(message_id)
    if not message:
        return jsonify({"error": "message not found"}), 404
    
    if message.recipient_id != user_id:
        return jsonify({"error": "unauthorized to modify this message"}), 403
    
    message.is_read = True
    db.session.commit()
    
    return jsonify({
        "success": True,
        "message": "message marked as read"
    }), 200 