from fastapi import APIRouter, Request, Form, HTTPException, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from typing import List, Optional

from . import crud, models, schemas
from .database import get_db

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/inventario", response_class=HTMLResponse)
async def get_inventory(request: Request, db: Session = Depends(get_db)):
    comics = crud.get_comics(db)
    return templates.TemplateResponse(
        "inventario.html", 
        {"request": request, "comics": comics}
    )

# Mover la definición de la ruta genérica al final para evitar conflictos
@router.get("/comics/{comic_id}", response_class=HTMLResponse)
async def get_comic(request: Request, comic_id: int, db: Session = Depends(get_db)):
    comic = crud.get_comic(db, comic_id)
    if not comic:
        raise HTTPException(status_code=404, detail="Comic not found")
    return templates.TemplateResponse(
        "comic_detail.html", 
        {"request": request, "comic": comic}
    )

@router.get("/comics/{comic_id}/editar", response_class=HTMLResponse)
async def edit_comic_form(request: Request, comic_id: int, db: Session = Depends(get_db)):
    comic = crud.get_comic(db, comic_id)
    if not comic:
        raise HTTPException(status_code=404, detail="Comic not found")
    return templates.TemplateResponse(
        "edit_comic.html", 
        {"request": request, "comic": comic}
    )

@router.post("/comics/{comic_id}/editar")
async def update_comic(
    comic_id: int,
    price: float = Form(...),
    stock: int = Form(...),
    db: Session = Depends(get_db)
):
    comic_data = schemas.ComicUpdate(price=price, stock=stock)
    updated_comic = crud.update_comic(db, comic_id, comic_data)
    if not updated_comic:
        raise HTTPException(status_code=404, detail="Comic not found")
    return RedirectResponse(url="/inventario", status_code=303)

@router.get("/pedidos", response_class=HTMLResponse)
async def get_orders(request: Request, db: Session = Depends(get_db)):
    pedidos = crud.get_pedidos(db)
    return templates.TemplateResponse("pedidos.html", {"request": request, "pedidos": pedidos})

@router.get("/clientes", response_class=HTMLResponse)
async def get_clients(request: Request, db: Session = Depends(get_db)):
    clientes = crud.get_clientes(db)
    return templates.TemplateResponse("clientes.html", {"request": request, "clientes": clientes})

@router.get("/proveedores", response_class=HTMLResponse)
async def get_providers(request: Request, db: Session = Depends(get_db)):
    proveedores = crud.get_proveedores(db)
    return templates.TemplateResponse("proveedores.html", {"request": request, "proveedores": proveedores})

# Rutas para comics
@router.get("/comics-crear", response_class=HTMLResponse)
async def create_comic_form(request: Request):
    return templates.TemplateResponse(
        "create_comic.html", 
        {"request": request}
    )

@router.post("/comics-crear")
async def create_comic(
    title: str = Form(...),
    image_url: str = Form(...),
    price: float = Form(...),
    stock: int = Form(...),
    db: Session = Depends(get_db)
):
    comic_data = schemas.ComicCreate(
        title=title,
        image_url=image_url,
        price=price,
        stock=stock
    )
    crud.create_comic(db, comic_data)
    return RedirectResponse(url="/inventario", status_code=303)

# Rutas para clientes
@router.get("/clientes-crear", response_class=HTMLResponse)
async def create_cliente_form(request: Request):
    return templates.TemplateResponse(
        "create_cliente.html", 
        {"request": request}
    )

@router.post("/clientes-crear")
async def create_cliente(
    nombre: str = Form(...),
    email: str = Form(...),
    telefono: str = Form(None),
    direccion: str = Form(None),
    db: Session = Depends(get_db)
):
    cliente_data = schemas.ClienteCreate(
        nombre=nombre,
        email=email,
        telefono=telefono,
        direccion=direccion
    )
    crud.create_cliente(db, cliente_data)
    return RedirectResponse(url="/clientes", status_code=303)

# Rutas para proveedores
@router.get("/proveedores-crear", response_class=HTMLResponse)
async def create_proveedor_form(request: Request):
    return templates.TemplateResponse(
        "create_proveedor.html", 
        {"request": request}
    )

@router.post("/proveedores-crear")
async def create_proveedor(
    nombre: str = Form(...),
    email: str = Form(...),
    telefono: str = Form(None),
    direccion: str = Form(None),
    db: Session = Depends(get_db)
):
    proveedor_data = schemas.ProveedorCreate(
        nombre=nombre,
        email=email,
        telefono=telefono,
        direccion=direccion
    )
    crud.create_proveedor(db, proveedor_data)
    return RedirectResponse(url="/proveedores", status_code=303)
# Rutas para pedidos
@router.get("/pedidos-crear", response_class=HTMLResponse)
async def create_pedido_form(request: Request, db: Session = Depends(get_db)):
    clientes = crud.get_clientes(db)
    comics = crud.get_comics(db)
    return templates.TemplateResponse(
        "create_pedido.html", 
        {"request": request, "clientes": clientes, "comics": comics}
    )

@router.post("/pedidos-crear")
async def create_pedido(
    cliente_id: int = Form(...),
    comic_ids: List[int] = Form(...),
    cantidades: List[int] = Form(...),
    db: Session = Depends(get_db)
):
    # Crear el pedido
    pedido_data = schemas.PedidoCreate()
    nuevo_pedido = crud.create_pedido(db, pedido_data, cliente_id)
    
    # Agregar los detalles del pedido
    for i in range(len(comic_ids)):
        if cantidades[i] > 0:
            detalle_data = schemas.DetallePedidoCreate(
                comic_id=comic_ids[i],
                cantidad=cantidades[i]
            )
            crud.add_detalle_pedido(db, detalle_data, nuevo_pedido.id)
    
    return RedirectResponse(url="/pedidos", status_code=303)

# Rutas para ver y editar proveedores
@router.get("/proveedores/{proveedor_id}", response_class=HTMLResponse)
async def get_proveedor(request: Request, proveedor_id: int, db: Session = Depends(get_db)):
    proveedor = crud.get_proveedor(db, proveedor_id)
    if not proveedor:
        raise HTTPException(status_code=404, detail="Proveedor not found")
    return templates.TemplateResponse(
        "view_proveedor.html", 
        {"request": request, "proveedor": proveedor}
    )

@router.get("/proveedores/{proveedor_id}/editar", response_class=HTMLResponse)
async def edit_proveedor_form(request: Request, proveedor_id: int, db: Session = Depends(get_db)):
    proveedor = crud.get_proveedor(db, proveedor_id)
    if not proveedor:
        raise HTTPException(status_code=404, detail="Proveedor not found")
    return templates.TemplateResponse(
        "edit_proveedor.html", 
        {"request": request, "proveedor": proveedor}
    )

@router.post("/proveedores/{proveedor_id}/editar")
async def update_proveedor(
    proveedor_id: int,
    nombre: str = Form(...),
    email: str = Form(...),
    telefono: str = Form(None),
    direccion: str = Form(None),
    db: Session = Depends(get_db)
):
    proveedor_data = schemas.ProveedorUpdate(
        nombre=nombre,
        email=email,
        telefono=telefono,
        direccion=direccion
    )
    updated_proveedor = crud.update_proveedor(db, proveedor_id, proveedor_data)
    if not updated_proveedor:
        raise HTTPException(status_code=404, detail="Proveedor not found")
    return RedirectResponse(url=f"/proveedores/{proveedor_id}", status_code=303)

# Rutas para ver y editar clientes
@router.get("/clientes/{cliente_id}", response_class=HTMLResponse)
async def get_cliente(request: Request, cliente_id: int, db: Session = Depends(get_db)):
    cliente = crud.get_cliente(db, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente not found")
    return templates.TemplateResponse(
        "view_cliente.html", 
        {"request": request, "cliente": cliente}
    )

@router.get("/clientes/{cliente_id}/editar", response_class=HTMLResponse)
async def edit_cliente_form(request: Request, cliente_id: int, db: Session = Depends(get_db)):
    cliente = crud.get_cliente(db, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente not found")
    return templates.TemplateResponse(
        "edit_cliente.html", 
        {"request": request, "cliente": cliente}
    )

@router.post("/clientes/{cliente_id}/editar")
async def update_cliente(
    cliente_id: int,
    nombre: str = Form(...),
    email: str = Form(...),
    telefono: str = Form(None),
    direccion: str = Form(None),
    db: Session = Depends(get_db)
):
    cliente_data = schemas.ClienteUpdate(
        nombre=nombre,
        email=email,
        telefono=telefono,
        direccion=direccion
    )
    updated_cliente = crud.update_cliente(db, cliente_id, cliente_data)
    if not updated_cliente:
        raise HTTPException(status_code=404, detail="Cliente not found")
    return RedirectResponse(url=f"/clientes/{cliente_id}", status_code=303)

# Rutas para ver y editar pedidos
@router.get("/pedidos/{pedido_id}", response_class=HTMLResponse)
async def get_pedido_detail(request: Request, pedido_id: int, db: Session = Depends(get_db)):
    pedido = crud.get_pedido(db, pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido not found")
    return templates.TemplateResponse(
        "view_pedido.html", 
        {"request": request, "pedido": pedido}
    )

@router.get("/pedidos/{pedido_id}/editar", response_class=HTMLResponse)
async def edit_pedido_form(request: Request, pedido_id: int, db: Session = Depends(get_db)):
    pedido = crud.get_pedido(db, pedido_id)
    comics = crud.get_comics(db)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido not found")
    return templates.TemplateResponse(
        "edit_pedido.html", 
        {"request": request, "pedido": pedido, "comics": comics}
    )

@router.post("/pedidos/{pedido_id}/editar")
async def update_pedido(
    pedido_id: int,
    estado: str = Form(...),
    detalle_ids: List[int] = Form(...),
    cantidades: List[int] = Form(...),
    db: Session = Depends(get_db)
):
    # Actualizar el estado del pedido
    pedido_data = schemas.PedidoUpdate(estado=estado)
    updated_pedido = crud.update_pedido(db, pedido_id, pedido_data)
    
    if not updated_pedido:
        raise HTTPException(status_code=404, detail="Pedido not found")
    
    # Actualizar cantidades de los detalles del pedido
    for i in range(len(detalle_ids)):
        detalle_data = schemas.DetallePedidoUpdate(cantidad=cantidades[i])
        crud.update_detalle_pedido(db, detalle_ids[i], detalle_data)
    
    return RedirectResponse(url=f"/pedidos/{pedido_id}", status_code=303)

@router.get("/pedidos/{pedido_id}/estado")
async def update_pedido_estado(
    pedido_id: int, 
    estado: str,
    db: Session = Depends(get_db)
):
    # Verificar que el estado sea válido
    if estado not in ["pendiente", "completado", "cancelado"]:
        raise HTTPException(status_code=400, detail="Estado no válido")
    
    # Actualizar el estado del pedido
    pedido_data = schemas.PedidoUpdate(estado=estado)
    updated_pedido = crud.update_pedido(db, pedido_id, pedido_data)
    
    if not updated_pedido:
        raise HTTPException(status_code=404, detail="Pedido not found")
    
    return RedirectResponse(url=f"/pedidos/{pedido_id}", status_code=303)

@router.post("/pedidos/{pedido_id}/agregar-producto")
async def add_product_to_pedido(
    pedido_id: int,
    comic_id: int = Form(...),
    cantidad: int = Form(...),
    db: Session = Depends(get_db)
):
    # Verificar que el pedido existe
    pedido = crud.get_pedido(db, pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido not found")
    
    # Agregar el producto al pedido
    detalle_data = schemas.DetallePedidoCreate(
        comic_id=comic_id,
        cantidad=cantidad
    )
    crud.add_detalle_pedido(db, detalle_data, pedido_id)
    
    return RedirectResponse(url=f"/pedidos/{pedido_id}/editar", status_code=303)

@router.get("/pedidos/{pedido_id}/detalles/{detalle_id}/eliminar")
async def remove_product_from_pedido(
    pedido_id: int,
    detalle_id: int,
    db: Session = Depends(get_db)
):
    # Eliminar el detalle del pedido
    result = crud.delete_detalle_pedido(db, detalle_id)
    if not result:
        raise HTTPException(status_code=404, detail="Detalle not found")
    
    return RedirectResponse(url=f"/pedidos/{pedido_id}/editar", status_code=303)