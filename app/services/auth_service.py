from sqlalchemy.orm import Session
from app.models import User, Student
from datetime import datetime
import secrets
import logging

logger = logging.getLogger(__name__)

# Shared token storage across all instances (in production, use Redis or database)
_active_tokens = {}

class AuthService:
    def __init__(self):
        self.active_tokens = _active_tokens  # Reference to shared storage
    
    def signup(self, db: Session, email: str, username: str, password: str, full_name: str) -> User:
        """Create a new user account"""
        try:
            # Check if email already exists
            existing_user = db.query(User).filter(User.email == email).first()
            if existing_user:
                raise ValueError("Email already registered")
            
            # Check if username already exists
            existing_username = db.query(User).filter(User.username == username).first()
            if existing_username:
                raise ValueError("Username already taken")
            
            # Create user
            user = User(
                email=email,
                username=username,
                full_name=full_name,
                created_at=datetime.utcnow()
            )
            user.set_password(password)
            
            db.add(user)
            db.commit()
            db.refresh(user)
            
            # Create associated student profile
            student = Student(
                name=full_name,
                email=email,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.add(student)
            db.commit()
            db.refresh(student)
            
            logger.info(f"Created student profile {student.id} for user {username}")
            
            # Link student to user
            user.student_id = student.id
            db.commit()
            db.refresh(user)
            
            logger.info(f"Linked student {student.id} to user {user.id} (username: {username})")
            
            # Verify the link
            if not user.student_id:
                raise ValueError("Failed to link student profile to user")
            
            return user
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating user: {str(e)}")
            raise
    
    def login(self, db: Session, email: str, password: str) -> tuple[User, str]:
        """Authenticate user and return user with token"""
        try:
            # Find user by email or username
            user = db.query(User).filter(
                (User.email == email) | (User.username == email)
            ).first()
            
            if not user:
                raise ValueError("Invalid email/username or password")
            
            if not user.verify_password(password):
                raise ValueError("Invalid email/username or password")
            
            if not user.is_active:
                raise ValueError("Account is deactivated")
            
            # Update last login
            user.last_login = datetime.utcnow()
            db.commit()
            
            # Generate token
            token = secrets.token_urlsafe(32)
            self.active_tokens[token] = user.id
            
            logger.info(f"User {user.username} logged in")
            return user, token
            
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            raise
    
    def verify_token(self, token: str) -> int:
        """Verify token and return user_id"""
        return self.active_tokens.get(token)
    
    def logout(self, token: str):
        """Remove token"""
        if token in self.active_tokens:
            del self.active_tokens[token]
