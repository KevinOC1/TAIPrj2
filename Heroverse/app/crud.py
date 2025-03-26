from sqlalchemy.orm import Session
from . import models, schemas

# Funciones CRUD para comics

def get_comics(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Comic).offset(skip).limit(limit).all()

def get_comic(db: Session, comic_id: int):
    return db.query(models.Comic).filter(models.Comic.id == comic_id).first()

def create_comic(db: Session, comic: schemas.ComicCreate):
    db_comic = models.Comic(**comic.dict())
    db.add(db_comic)
    db.commit()
    db.refresh(db_comic)
    return db_comic

def update_comic(db: Session, comic_id: int, comic_data: schemas.ComicUpdate):
    db_comic = get_comic(db, comic_id)
    if db_comic:
        # Actualizar solo los campos proporcionados
        for key, value in comic_data.dict(exclude_unset=True).items():
            setattr(db_comic, key, value)
        db.commit()
        db.refresh(db_comic)
    return db_comic

def delete_comic(db: Session, comic_id: int):
    db_comic = get_comic(db, comic_id)
    if db_comic:
        db.delete(db_comic)
        db.commit()
        return True
    return False

# Funciones CRUD para clientes

def get_clientes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Cliente).offset(skip).limit(limit).all()

def get_cliente(db: Session, cliente_id: int):
    return db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()

def create_cliente(db: Session, cliente: schemas.ClienteCreate):
    db_cliente = models.Cliente(**cliente.dict())
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

# Funciones CRUD para proveedores

def get_proveedores(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Proveedor).offset(skip).limit(limit).all()

def get_proveedor(db: Session, proveedor_id: int):
    return db.query(models.Proveedor).filter(models.Proveedor.id == proveedor_id).first()

def create_proveedor(db: Session, proveedor: schemas.ProveedorCreate):
    db_proveedor = models.Proveedor(**proveedor.dict())
    db.add(db_proveedor)
    db.commit()
    db.refresh(db_proveedor)
    return db_proveedor

# Funciones CRUD para pedidos

def get_pedidos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Pedido).offset(skip).limit(limit).all()

def get_pedido(db: Session, pedido_id: int):
    return db.query(models.Pedido).filter(models.Pedido.id == pedido_id).first()

def create_pedido(db: Session, pedido: schemas.PedidoCreate, cliente_id: int):
    db_pedido = models.Pedido(**pedido.dict(), cliente_id=cliente_id)
    db.add(db_pedido)
    db.commit()
    db.refresh(db_pedido)
    return db_pedido

def add_detalle_pedido(db: Session, detalle: schemas.DetallePedidoCreate, pedido_id: int):
    # Obtener el cómic para obtener el precio
    comic = get_comic(db, detalle.comic_id)
    if not comic:
        return None
    
    # Crear el detalle del pedido
    db_detalle = models.DetallePedido(
        pedido_id=pedido_id,
        comic_id=detalle.comic_id,
        cantidad=detalle.cantidad,
        precio_unitario=comic.price
    )
    db.add(db_detalle)
    
    # Actualizar el stock del cómic
    comic.stock -= detalle.cantidad
    
    # Actualizar el total del pedido
    pedido = get_pedido(db, pedido_id)
    pedido.total += comic.price * detalle.cantidad
    
    db.commit()
    db.refresh(db_detalle)
    return db_detalle