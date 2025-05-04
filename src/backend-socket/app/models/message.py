import uuid
from datetime import datetime
from app import db

class Message(db.Model):
    __tablename__ = 'messages'
    
    message_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    sender_id = db.Column(db.String(36), db.ForeignKey('users.user_id'), nullable=False)
    recipient_id = db.Column(db.String(36), db.ForeignKey('users.user_id'), nullable=True)
    conversation_id = db.Column(db.String(36), db.ForeignKey('conversations.conversation_id'), nullable=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)
    
    # relationships
    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_messages')
    recipient = db.relationship('User', foreign_keys=[recipient_id], backref='received_messages')
    conversation = db.relationship('Conversation', backref='messages')
    
    def to_dict(self):
        result = {
            'message_id': self.message_id,
            'sender_id': self.sender_id,
            'content': self.content,
            'timestamp': self.timestamp.isoformat(),
            'is_read': self.is_read
        }
        
        if self.recipient_id:
            result['recipient_id'] = self.recipient_id
        
        if self.conversation_id:
            result['conversation_id'] = self.conversation_id
            
        return result

class Conversation(db.Model):
    __tablename__ = 'conversations'
    
    conversation_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    title = db.Column(db.String(255), nullable=True)
    
    # many-to-many relationship through association table
    participants = db.relationship('User', secondary='conversation_participants', backref='conversations')
    
    def to_dict(self):
        return {
            'conversation_id': self.conversation_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'title': self.title,
            'participants': [user.to_dict(basic=True) for user in self.participants]
        }

class ConversationParticipant(db.Model):
    __tablename__ = 'conversation_participants'
    
    conversation_id = db.Column(db.String(36), db.ForeignKey('conversations.conversation_id'), primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.user_id'), primary_key=True)
    joined_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) 