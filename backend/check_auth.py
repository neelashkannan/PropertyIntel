from database import SessionLocal
from models import User
from auth import verify_password

def check():
    db = SessionLocal()
    user = db.query(User).filter(User.email == 'admin@propertyintel.com').first()
    if not user:
        print("User not found")
        return
    
    password = "PropertyIntel2024!"
    match = verify_password(password, user.hashed_password)
    print(f"Password match: {match}")
    db.close()

if __name__ == "__main__":
    check()
