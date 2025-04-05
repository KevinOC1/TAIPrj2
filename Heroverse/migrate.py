from sqlalchemy import create_engine, text
import os

def reset_database():
    # Path to your SQLite database
    db_path = 'heroverse.db'
    
    # Remove existing database file
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Removed existing database: {db_path}")

def create_database():
    # Import your models and base
    from app.database import engine
    from app import models
    
    # Create all tables defined in your models
    models.Base.metadata.create_all(bind=engine)
    print("Database and tables created successfully")

def add_limite_minimo_column():
    # Import database session
    from app.database import SessionLocal
    from app import models
    
    # Create a new database session
    db = SessionLocal()
    
    try:
        # Add the limite_minimo column to comics table
        db.execute(text('ALTER TABLE comics ADD COLUMN limite_minimo INTEGER DEFAULT 10'))
        db.commit()
        print("Added limite_minimo column to comics table")
    except Exception as e:
        db.rollback()
        print(f"Error adding column: {e}")
    finally:
        db.close()

def init_initial_data():
    # Import database session
    from app.database import SessionLocal
    from app import models
    
    # Create a new database session
    db = SessionLocal()
    
    try:
        # Call the init_db function to populate initial data
        models.init_db(db)
        print("Initial data added successfully")
    except Exception as e:
        db.rollback()
        print(f"Error adding initial data: {e}")
    finally:
        db.close()

def main():
    # Run migration steps
    reset_database()
    create_database()
    add_limite_minimo_column()
    init_initial_data()
    print("Migration completed successfully")

if __name__ == "__main__":
    main()