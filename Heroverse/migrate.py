from sqlalchemy import create_engine, text
import os

def add_cliente_frecuente_columns():
    from app.database import SessionLocal
    
    db = SessionLocal()
    try:
        # Agregar nuevas columnas a clientes
        db.execute(text('ALTER TABLE clientes ADD COLUMN fecha_nacimiento DATETIME'))
        db.execute(text('ALTER TABLE clientes ADD COLUMN nivel VARCHAR DEFAULT "bronze"'))
        db.execute(text('ALTER TABLE clientes ADD COLUMN puntos INTEGER DEFAULT 0'))
        db.execute(text('ALTER TABLE clientes ADD COLUMN notas TEXT'))
        db.execute(text('ALTER TABLE clientes ADD COLUMN newsletter BOOLEAN DEFAULT FALSE'))
        db.execute(text('ALTER TABLE clientes ADD COLUMN promociones BOOLEAN DEFAULT FALSE'))
        db.execute(text('ALTER TABLE clientes ADD COLUMN generos_interes TEXT'))
        db.commit()
        print("Agregadas columnas de cliente frecuente")
    except Exception as e:
        db.rollback()
        print(f"Error al agregar columnas: {e}")
    finally:
        db.close()

def main():
    print("Iniciando migración para añadir campos de cliente frecuente...")
    add_cliente_frecuente_columns()
    print("Migración completada.")

if __name__ == "__main__":
    main()