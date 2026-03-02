import secrets
from werkzeug.security import generate_password_hash
# Wir importieren app UND db direkt aus deinen Quelldateien
from src.app import app
from src.db import db
from src.models.user import UserEntity


def seed_admin():
    # Der app_context ist essentiell, damit SQLAlchemy die Konfiguration (URI) kennt
    with app.app_context():
        print("Verbinde mit Datenbank...")

        # Sicherstellen, dass Tabellen existieren
        db.create_all()

        # Prüfen, ob schon ein Admin da ist
        existing_user = db.session.execute(db.select(UserEntity)).scalar_one_or_none()

        if existing_user:
            print(f"Abbruch: Nutzer '{existing_user.email}' existiert bereits.")
            return

        print("Erstelle Admin-Account...")

        admin_email = "admin@example.com"
        admin_password = "start-passwort-123"

        new_admin = UserEntity(
            email=admin_email,
            name="Initial Admin",
            password=generate_password_hash(admin_password),
            api_key=secrets.token_urlsafe(32)
        )

        db.session.add(new_admin)
        db.session.commit()

        print("=" * 30)
        print("ADMIN ERFOLGREICH ANGELEGT")
        print(f"Email:   {admin_email}")
        print(f"PW:      {admin_password}")
        print(f"API-Key: {new_admin.api_key}")
        print("=" * 30)


if __name__ == "__main__":
    seed_admin()