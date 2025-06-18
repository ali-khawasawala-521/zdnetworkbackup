from backend import database, models  # Ensure models is imported
from backend.models import Device, Backup, User  # 👈 This forces model registration

def init_db():
    print("Creating database and tables...")
    database.Base.metadata.create_all(bind=database.engine)
    print("Done!")

if __name__ == "__main__":
    init_db()
