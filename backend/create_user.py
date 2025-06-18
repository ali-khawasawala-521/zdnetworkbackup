import sys
import getpass
from sqlalchemy.orm import Session
from backend import crud, database

def main():
    # Simple input for email and password
    email = input("Enter user email: ").strip()
    password = getpass.getpass("Enter password: ").strip()

    if not email or not password:
        print("Email and password cannot be empty.")
        sys.exit(1)

    db: Session = database.SessionLocal()
    try:
        existing_user = crud.get_user(db, email)
        if existing_user:
            print(f"User with email '{email}' already exists.")
            sys.exit(1)

        user = crud.create_user(db, email, password)
        print(f"User created with ID: {user.id}, Email: {user.email}")
    except Exception as e:
        print(f"Error creating user: {e}")
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    main()
