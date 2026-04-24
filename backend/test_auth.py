from database import init_db, User, SessionLocal
from routers.auth import hash_password

init_db()
db = SessionLocal()

try:
    user = User(
        username='testuser2',
        email='test2@test.com',
        password_hash=hash_password('test1234')
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    print('User created OK:', user.id, user.username)
except Exception as e:
    print('Error:', e)
finally:
    db.close()