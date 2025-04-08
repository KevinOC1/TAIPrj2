from sqlalchemy import create_engine, text
import os

def add_proveedor_columns():
    from app.database import SessionLocal
    
    db = SessionLocal()
    try:
        db.execute(text('ALTER TABLE proveedores ADD COLUMN contacto_nombre VARCHAR'))
        db.execute(text('ALTER TABLE proveedores ADD COLUMN contacto_telefono VARCHAR'))
        db.execute(text('ALTER TABLE proveedores ADD COLUMN notas TEXT'))
        db.commit()
        print("Columnas añadidas a la tabla proveedores correctamente")
    except Exception as e:
        db.rollback()
        print(f"Error al añadir columnas: {e}")
    finally:
        db.close()

def main():
    print("Iniciando migración para añadir campos a proveedores...")
    add_proveedor_columns()
    print("Migración completada.")

if __name__ == "__main__":
    main()