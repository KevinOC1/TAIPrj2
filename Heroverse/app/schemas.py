from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Esquemas para Comic
class ComicBase(BaseModel):
    title: str
    image_url: str
    price: float
    stock: int

class ComicCreate(ComicBase):
    pass

class ComicUpdate(BaseModel):
    title: Optional[str] = None
    image_url: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None

class Comic(ComicBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Esquemas para Cliente
class ClienteBase(BaseModel):
    nombre: str
    email: str
    telefono: Optional[str] = None
    direccion: Optional[str] = None

class ClienteCreate(ClienteBase):
    pass

class Cliente(ClienteBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Esquemas para Proveedor
class ProveedorBase(BaseModel):
    nombre: str
    email: str
    telefono: Optional[str] = None
    direccion: Optional[str] = None

class ProveedorCreate(ProveedorBase):
    pass

class Proveedor(ProveedorBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Esquemas para DetallePedido
class DetallePedidoBase(BaseModel):
    comic_id: int
    cantidad: int

class DetallePedidoCreate(DetallePedidoBase):
    pass

class DetallePedido(DetallePedidoBase):
    id: int
    pedido_id: int
    precio_unitario: float

    class Config:
        from_attributes = True

# Esquemas para Pedido
class PedidoBase(BaseModel):
    estado: Optional[str] = "pendiente"

class PedidoCreate(PedidoBase):
    pass

class PedidoUpdate(BaseModel):
    estado: Optional[str] = None

class Pedido(PedidoBase):
    id: int
    cliente_id: int
    fecha: datetime
    total: float
    detalles: List[DetallePedido] = []

    class Config:
        from_attributes = True

# Esquema extendido para Cliente con sus pedidos
class ClienteConPedidos(Cliente):
    pedidos: List[Pedido] = []

    class Config:
        from_attributes = True