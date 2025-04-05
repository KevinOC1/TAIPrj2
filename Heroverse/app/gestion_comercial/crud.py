from sqlalchemy.orm import Session
from . import models, schemas
from typing import Optional
def delete_detalle_pedido(db: Session, detalle_id: int):
    db_detalle = db.query(models.DetallePedido).filter(models.DetallePedido.id == detalle_id).first()
    if db_detalle:
        db.delete(db_detalle)
        db.commit()
        return True
    return False

# Funciones de Control de Stock

def get_comic(db: Session, comic_id: int):
    """
    Obtener un cómic por su ID
    :param db: Sesión de base de datos
    :param comic_id: ID del cómic
    :return: Comic encontrado o None
    """
    return db.query(models.Comic).filter(models.Comic.id == comic_id).first()

def ajustar_stock(db: Session, comic_id: int, cantidad: int):
    """
    Ajustar el stock de un cómic (puede ser positivo o negativo)
    :param db: Sesión de base de datos
    :param comic_id: ID del cómic
    :param cantidad: Cantidad para ajustar (positiva para añadir, negativa para reducir)
    :return: Comic actualizado o None si no se encuentra
    """
    comic = get_comic(db, comic_id)
    if comic:
        # Calcular nuevo stock, asegurándose de no ir por debajo de 0
        nuevo_stock = max(0, comic.stock + cantidad)
        comic.stock = nuevo_stock
        db.commit()
        db.refresh(comic)
        return comic
    return None

def transferir_stock(db: Session, comic_origen_id: int, comic_destino_id: int, cantidad: int):
    """
    Transferir stock de un cómic a otro
    :param db: Sesión de base de datos
    :param comic_origen_id: ID del cómic de origen
    :param comic_destino_id: ID del cómic de destino
    :param cantidad: Cantidad a transferir
    :return: Tupla de comics actualizados o None si no se pueden encontrar
    """
    comic_origen = get_comic(db, comic_origen_id)
    comic_destino = get_comic(db, comic_destino_id)
    
    if comic_origen and comic_destino and comic_origen.stock >= cantidad:
        # Reducir stock del cómic de origen
        comic_origen.stock -= cantidad
        
        # Aumentar stock del cómic de destino
        comic_destino.stock += cantidad
        
        db.commit()
        db.refresh(comic_origen)
        db.refresh(comic_destino)
        
        return (comic_origen, comic_destino)
    return None

def generar_informe_stock(db: Session):
    """
    Generar un informe de stock
    :param db: Sesión de base de datos
    :return: Lista de cómics con stock bajo o agotado
    """
    # Definir un umbral de stock bajo (por ejemplo, menos de 10 unidades)
    umbral_stock_bajo = 10
    
    comics_con_stock_bajo = (
        db.query(models.Comic)
        .filter(models.Comic.stock <= umbral_stock_bajo)
        .order_by(models.Comic.stock.asc())
        .all()
    )
    
    return comics_con_stock_bajo

def registrar_entrada_stock(db: Session, comic_id: int, cantidad: int, proveedor_id: Optional[int] = None):
    """
    Registrar una entrada de stock para un cómic
    :param db: Sesión de base de datos
    :param comic_id: ID del cómic
    :param cantidad: Cantidad de entrada
    :param proveedor_id: ID opcional del proveedor
    :return: Entrada de stock registrada o None
    """
    comic = get_comic(db, comic_id)
    if comic:
        # Ajustar stock
        comic.stock += cantidad
        
        # Crear registro de entrada de stock (puedes extender esto con un modelo de MovimientoStock si lo deseas)
        entrada_stock = models.MovimientoStock(
            comic_id=comic_id,
            cantidad=cantidad,
            tipo='entrada',
            proveedor_id=proveedor_id
        )
        
        db.add(entrada_stock)
        db.commit()
        db.refresh(comic)
        
        return entrada_stock
    return None

def registrar_salida_stock(db: Session, comic_id: int, cantidad: int, razon: Optional[str] = None):
    """
    Registrar una salida de stock para un cómic
    :param db: Sesión de base de datos
    :param comic_id: ID del cómic
    :param cantidad: Cantidad de salida
    :param razon: Razón opcional de la salida (devolución, merma, etc.)
    :return: Salida de stock registrada o None
    """
    comic = get_comic(db, comic_id)
    if comic and comic.stock >= cantidad:
        # Ajustar stock
        comic.stock -= cantidad
        
        # Crear registro de salida de stock
        salida_stock = models.MovimientoStock(
            comic_id=comic_id,
            cantidad=cantidad,
            tipo='salida',
            razon=razon
        )
        
        db.add(salida_stock)
        db.commit()
        db.refresh(comic)
        
        return salida_stock
    return None

def establecer_limite_stock(db: Session, comic_id: int, limite_minimo: int):
    """
    Establecer el límite mínimo de stock para un cómic
    :param db: Sesión de base de datos
    :param comic_id: ID del cómic
    :param limite_minimo: Nuevo límite mínimo de stock
    :return: Cómic actualizado o None si no se encuentra
    """
    comic = get_comic(db, comic_id)
    if comic:
        comic.limite_minimo = limite_minimo
        db.commit()
        db.refresh(comic)
        return comic
    return None

def generar_informe_stock_critico(db: Session):
    """
    Generar un informe de cómics con stock crítico
    :param db: Sesión de base de datos
    :return: Lista de cómics con stock por debajo del límite mínimo
    """
    comics_stock_critico = (
        db.query(models.Comic)  # Use models.Comic instead of Comic
        .filter(models.Comic.stock < models.Comic.limite_minimo)
        .order_by(models.Comic.stock.asc())
        .all()
    )
    
    return comics_stock_critico



#cliente frecuente
def crear_cliente_frecuente(db: Session, cliente_data: dict):
    """
    Crear un nuevo cliente frecuente
    :param db: Sesión de base de datos
    :param cliente_data: Diccionario con datos del cliente
    :return: Nuevo cliente creado
    """
    # Validar que el email no esté duplicado
    existing_cliente = db.query(models.Cliente).filter(models.Cliente.email == cliente_data['email']).first()
    if existing_cliente:
        raise ValueError("Ya existe un cliente con este correo electrónico")
    
    # Crear nuevo cliente
    nuevo_cliente = models.Cliente(
        nombre=cliente_data['nombre'],
        email=cliente_data['email'],
        telefono=cliente_data.get('telefono'),
        # Otros campos según tu modelo
    )
    
    db.add(nuevo_cliente)
    db.commit()
    db.refresh(nuevo_cliente)
    
    return nuevo_cliente