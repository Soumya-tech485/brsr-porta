from app.database import SessionLocal
from app.models.core import User
db = SessionLocal()
db.query(User).update({User.password_hash: '$2b$12$lkKMYYWHUxS.vcmAqOjVre.otYYdXyFcU538c0FuVYjmH4e5OcHea'})
db.commit()
print("Updated passwords correctly!")
