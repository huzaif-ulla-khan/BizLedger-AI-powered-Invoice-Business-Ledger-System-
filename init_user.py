# init_user.py
from app import SessionLocal, User, get_password_hash

# Create DB session
db = SessionLocal()

# Default user credentials
username = "admin"
password = "admin123"

# Check if user already exists
existing = db.query(User).filter(User.username == username).first()

if not existing:
    hashed_password = get_password_hash(password)
    new_user = User(username=username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    print(f"✅ Default user created: {username} / {password}")
else:
    print("⚠️ User already exists")

db.close()
