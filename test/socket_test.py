#!/usr/bin/env python3
import socketio
import time
import logging
import requests
import json
import datetime
import uuid
import threading

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class UserClient:
    """Represents a user client"""
    def __init__(self, name):
        self.name = name
        self.email = None
        self.token = None
        self.user_id = None
        self.sio = socketio.Client()
        self.connected = False
        self.conversation_id = None
        self.real_user_id = None  # Real user ID returned by the server
        
        # Register event handlers
        @self.sio.event
        def connect():
            logger.info(f"User {self.name} connected successfully!")
            self.connected = True
        
        @self.sio.event
        def disconnect():
            logger.info(f"User {self.name} disconnected!")
            self.connected = False
        
        @self.sio.event
        def connect_error(data):
            logger.error(f"User {self.name} connection error: {data}")
        
        @self.sio.on('user_online')
        def on_user_online(data):
            logger.info(f"User {self.name} received user online notification: {data}")
            # Store the real user ID
            if not self.real_user_id:
                user_id = data.get('user_id')
                if user_id:
                    logger.info(f"User {self.name} using real ID assigned by server: {user_id}")
                    self.real_user_id = user_id
        
        @self.sio.on('online_users')
        def on_online_users(data):
            logger.info(f"User {self.name} received online users list: {data}")
        
        @self.sio.on('private_message')
        def on_private_message(data):
            logger.info(f"User {self.name} received private message: {data}")
        
        @self.sio.on('conversation_message')
        def on_conversation_message(data):
            logger.info(f"User {self.name} received conversation message: {data}")
        
        @self.sio.on('message_delivered')
        def on_message_delivered(data):
            logger.info(f"User {self.name} message delivered: {data}")
        
        @self.sio.on('user_typing')
        def on_user_typing(data):
            logger.info(f"User {self.name} received user typing notification: {data}")
        
        @self.sio.on('error')
        def on_error(data):
            logger.error(f"User {self.name} received error: {data}")
        
        @self.sio.on('message')
        def on_message(data):
            logger.info(f"User {self.name} received server message: {data}")
    
    def register(self):
        """Register new user"""
        try:
            # Generate email with timestamp
            timestamp = int(time.time())
            email = f"{self.name}_{timestamp}@gmail.com"
            
            # Build registration request data
            register_data = {
                "first_name": self.name,
                "last_name": "User",
                "email": email,
                "password": "password123"
            }
            
            logger.info(f"User {self.name} registering with email {email}")
            
            # Send registration request
            register_url = "http://localhost:5001/api/auth/register"
            register_response = requests.post(register_url, json=register_data)
            
            # Check registration result
            if register_response.status_code == 201:
                logger.info(f"User {self.name} registered successfully!")
                self.email = email
                return True
            else:
                logger.error(f"User {self.name} registration failed: {register_response.status_code} - {register_response.text}")
                return False
        except Exception as e:
            logger.error(f"Error during registration for user {self.name}: {str(e)}")
            return False
    
    def login(self):
        """Login user and get token"""
        try:
            # Build login request data
            login_data = {
                "email": self.email,
                "password": "password123"
            }
            
            # Send login request
            login_url = "http://localhost:5001/api/auth/login"
            login_response = requests.post(login_url, json=login_data)
            
            # Check login result
            if login_response.status_code == 200:
                # Extract token and user ID
                response_data = login_response.json()
                self.token = response_data.get("access_token")
                
                if "user" in response_data and isinstance(response_data["user"], dict):
                    self.user_id = response_data["user"].get("user_id")
                
                logger.info(f"User {self.name} logged in successfully!")
                if self.user_id:
                    logger.info(f"User {self.name} ID: {self.user_id}")
                else:
                    # If user ID not received, wait for server-assigned ID
                    logger.info(f"User {self.name} waiting for server-assigned ID")
                
                return True
            else:
                logger.error(f"User {self.name} login failed: {login_response.status_code} - {login_response.text}")
                return False
        except Exception as e:
            logger.error(f"Error during login for user {self.name}: {str(e)}")
            return False
    
    def connect_socket(self):
        """Connect to WebSocket server"""
        try:
            # Build URL with token
            socket_url = f'http://localhost:5002?token={self.token}'
            
            logger.info(f"User {self.name} connecting to: {socket_url}")
            
            # Connect to socket service
            self.sio.connect(
                socket_url,
                socketio_path='socket',
                transports=['websocket'],
                wait_timeout=15
            )
            
            # Wait for connection and real user ID
            time.sleep(2)
            return self.connected
        except Exception as e:
            logger.error(f"Error during connection for user {self.name}: {str(e)}")
            return False
    
    def disconnect_socket(self):
        """Disconnect WebSocket connection"""
        try:
            self.sio.disconnect()
            return True
        except Exception as e:
            logger.error(f"Error disconnecting for user {self.name}: {str(e)}")
            return False
    
    def send_private_message(self, recipient_id, content):
        """Send private message"""
        # Use real user ID
        sender_id = self.real_user_id if self.real_user_id else self.user_id
        
        try:
            logger.info(f"User {self.name} sending private message to {recipient_id}: {content}")
            logger.info(f"Using sender ID: {sender_id}")
            
            self.sio.emit('private_message', {
                'sender_id': sender_id,
                'recipient_id': recipient_id,
                'content': content
            })
            return True
        except Exception as e:
            logger.error(f"Error sending private message for user {self.name}: {str(e)}")
            return False
    
    def send_typing_status(self, recipient_id, is_typing=True):
        """Send typing status"""
        # Use real user ID
        user_id = self.real_user_id if self.real_user_id else self.user_id
        
        try:
            status = "started" if is_typing else "stopped"
            logger.info(f"User {self.name} {status} typing to {recipient_id}")
            logger.info(f"Using user ID: {user_id}")
            
            self.sio.emit('typing', {
                'user_id': user_id,
                'recipient_id': recipient_id,
                'is_typing': is_typing
            })
            return True
        except Exception as e:
            logger.error(f"Error sending typing status for user {self.name}: {str(e)}")
            return False

def test_conversation_between_users(user1, user2):
    """Test conversation between two users"""
    # Ensure both users have real user IDs
    if not user1.real_user_id or not user2.real_user_id:
        logger.error("Cannot conduct chat test: users don't have real IDs")
        return
    
    # User 1 sends typing status to user 2
    user1.send_typing_status(user2.real_user_id, True)
    time.sleep(1)
    
    # User 1 sends message to user 2
    user1.send_private_message(user2.real_user_id, f"Hello {user2.name}, I'm {user1.name}")
    time.sleep(2)
    
    # User 1 stops typing
    user1.send_typing_status(user2.real_user_id, False)
    time.sleep(1)
    
    # User 2 sends typing status to user 1
    user2.send_typing_status(user1.real_user_id, True)
    time.sleep(1)
    
    # User 2 replies to user 1
    user2.send_private_message(user1.real_user_id, f"Hello {user1.name}, nice to meet you!")
    time.sleep(2)
    
    # User 2 stops typing
    user2.send_typing_status(user1.real_user_id, False)

def main():
    # Create two user clients
    user1 = UserClient("Alice")
    user2 = UserClient("Bob")
    
    # Register and login user 1
    if not user1.register() or not user1.login():
        return
    
    # Register and login user 2
    if not user2.register() or not user2.login():
        return
    
    # Connect both users to WebSocket
    if not user1.connect_socket() or not user2.connect_socket():
        return
    
    # Wait to get real user IDs
    logger.info("Waiting 5 seconds to get real user IDs...")
    time.sleep(5)
    
    # Test conversation between users
    test_conversation_between_users(user1, user2)
    
    # Keep connection for a while
    logger.info("Keeping connection for 10 seconds...")
    time.sleep(10)
    
    # Disconnect
    logger.info("Disconnecting all connections...")
    user1.disconnect_socket()
    user2.disconnect_socket()

if __name__ == "__main__":
    main() 