from passlib.context import CryptContext
from sqlalchemy.orm import Session
from backend import models

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)

def create_user(db: Session, username: str, password: str, role: str = "employee"):
    existing_user = db.query(models.User).filter(models.User.username == username).first()
    if existing_user:
        return None

    user = models.User(
        username=username,
        password_hash=hash_password(password),
        role=role
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(models.User).filter(models.User.username == username).first()

    if not user:
        return None

    if not verify_password(password, user.password_hash):
        return None

    return user