from app import create_app
from app.models import User
from app.db import db
from werkzeug.security import generate_password_hash

ADMIN_ID = "admin_b"
ADMIN_NAME = "Admin B"
ADMIN_EMAIL = "b@b.com"
ADMIN_PASSWORD = "b"
ADMIN_ROLE = "admin"

def seed_admin():
    app = create_app()
    with app.app_context():
        # Check if admin already exists
        existing = User.query.filter_by(email=ADMIN_EMAIL).first()
        if existing:
            print(f"Admin with email {ADMIN_EMAIL} already exists.")
            return
        admin = User(
            id=ADMIN_ID,
            name=ADMIN_NAME,
            email=ADMIN_EMAIL,
            role=ADMIN_ROLE,
            password=generate_password_hash(ADMIN_PASSWORD)
        )
        db.session.add(admin)
        db.session.commit()
        print(f"Seeded admin: {ADMIN_EMAIL} / {ADMIN_PASSWORD}")

if __name__ == "__main__":
    seed_admin()
