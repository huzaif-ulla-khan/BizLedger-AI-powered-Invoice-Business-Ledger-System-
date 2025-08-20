# init_db.py
from db import engine, SessionLocal, Base
from models import User, Transaction
from passlib.context import CryptContext
import datetime

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(p: str) -> str:
    return pwd.hash(p)

def init():
    Base.metadata.drop_all(bind=engine)   # safety for dev: start clean
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # default admin
    admin_user = db.query(User).filter(User.username == "admin").first()
    if not admin_user:
        admin = User(username="admin", hashed_password=get_password_hash("admin123"))
        db.add(admin)
        db.commit()
        db.refresh(admin)
        print("Created admin / admin123")

        # sample transactions
        samples = [
            Transaction(user_id=admin.id, date=datetime.date(2025,8,1), description="Invoice - Alpha Ltd", amount=50000, type="income", category="Sales"),
            Transaction(user_id=admin.id, date=datetime.date(2025,8,3), description="Office Rent", amount=15000, type="expense", category="Rent"),
            Transaction(user_id=admin.id, date=datetime.date(2025,8,5), description="Consulting Fee", amount=20000, type="income", category="Service"),
            Transaction(user_id=admin.id, date=datetime.date(2025,8,7), description="Stationery", amount=1200, type="expense", category="Office Supplies"),
            Transaction(user_id=admin.id, date=datetime.date(2025,8,12), description="Bank Interest", amount=500, type="income", category="Finance"),
        ]
        db.add_all(samples)
        db.commit()
        print("Inserted sample transactions")
    else:
        print("Admin already exists")

    db.close()

if __name__ == "__main__":
    init()
