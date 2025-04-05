from app.database import get_db
from app import models, schemas, crud
from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# Ruta para el panel de Gestión Comercial
@router.get("/gestion", response_class=HTMLResponse)
async def gestion_comercial(request: Request, db: Session = Depends(get_db)):
    # Obtener estadísticas para el panel
    stats = {
        "low_stock": db.query(models.Comic).filter(models.Comic.stock < 5).count(),
        "overstocked": db.query(models.Comic).filter(models.Comic.stock > 20).count(),
        "total_proveedores": db.query(models.Proveedor).count(),
        "pending_orders": 3,  # Simulado - implementar lógica real
        "total_clientes": db.query(models.Cliente).count(),
        "new_clients": 5,  # Simulado - implementar lógica real
        "frequent_clients": 7,  # Simulado - implementar lógica real 
        "active_promos": 3,  # Simulado - implementar lógica real
        "supplier_orders": 4,  # Simulado - implementar lógica real
        "arriving_soon": 2,  # Simulado - implementar lógica real
        "customer_orders": db.query(models.Pedido).count(),
        "pending_delivery": db.query(models.Pedido).filter(models.Pedido.estado == "pendiente").count()
    }
    
    return templates.TemplateResponse("gestion_comercial.html", {
        "request": request,
        "stats": stats
    })

# Rutas para Gestión de Stock
@router.get("/gestion/stock", response_class=HTMLResponse)
async def gestion_stock(request: Request, db: Session = Depends(get_db)):
    # Preparar estadísticas
    low_stock = db.query(models.Comic).filter(models.Comic.stock < 5).count()
    normal_stock = db.query(models.Comic).filter(models.Comic.stock >= 5, models.Comic.stock <= 20).count()
    overstocked = db.query(models.Comic).filter(models.Comic.stock > 20).count()
    
    stats = {
        "low_stock": low_stock,
        "normal_stock": normal_stock,
        "overstocked": overstocked
    }
    
    # Obtener cómics con información adicional de stock
    comics_db = db.query(models.Comic).all()
    comics = []
    
    for comic in comics_db:
        stock_status = "normal"
        if comic.stock < 5:
            stock_status = "low"
        elif comic.stock > 20:
            stock_status = "high"
        
        comics.append({
            "id": comic.id,
            "title": comic.title,
            "image_url": comic.image_url,
            "price": comic.price,
            "stock": comic.stock,
            "min_stock": 5,  # Valores por defecto - implementar en BD
            "max_stock": 20,  # Valores por defecto - implementar en BD
            "category": "Marvel",  # Simulado - implementar categorías en BD
            "stock_status": stock_status
        })
    
    return templates.TemplateResponse("gestion_stock.html", {
        "request": request,
        "stats": stats,
        "comics": comics
    })

# Rutas para Clientes Frecuentes
@router.get("/gestion/clientes-frecuentes", response_class=HTMLResponse)
async def clientes_frecuentes(request: Request, db: Session = Depends(get_db)):
    # Estadísticas para el módulo
    stats = {
        "members": 25,  # Simulado
        "vip_members": 7,  # Simulado
        "active_promos": 3,  # Simulado
        "vip_orders": 12   # Simulado
    }
    
    # Obtener clientes frecuentes simulados
    # En implementación real, deberíamos tener un modelo ClienteFrecuente
    clientes_db = db.query(models.Cliente).limit(10).all()
    frequent_clients = []
    
    levels = ["bronze", "silver", "gold", "vip"]
    
    for i, cliente in enumerate(clientes_db):
        # Simular datos de cliente frecuente
        level = levels[i % 4]
        points = (i + 1) * 100
        orders = (i + 1) * 2
        
        frequent_clients.append({
            "id": cliente.id,
            "nombre": cliente.nombre,
            "email": cliente.email,
            "level": level,
            "points": points,
            "orders": orders,
            "last_purchase": datetime.now().strftime("%d/%m/%Y")
        })
    
    # Simular promociones
    promotions = [
        {
            "id": 1,
            "title": "Descuento 15% en Marvel",
            "description": "15% de descuento en todos los cómics de Marvel",
            "start_date": "01/01/2025",
            "end_date": "31/01/2025",
            "eligible_levels": "Silver, Gold, VIP",
            "status": "active",
            "sent": 15,
            "used": 8,
            "conversion_rate": 53
        },
        {
            "id": 2,
            "title": "Cómic gratis por 1000 puntos",
            "description": "Canjea 1000 puntos por un cómic gratis a elegir",
            "start_date": "01/01/2025",
            "end_date": "30/06/2025",
            "eligible_levels": "Todos",
            "status": "active",
            "sent": 20,
            "used": 5,
            "conversion_rate": 25
        },
        {
            "id": 3,
            "title": "Descuento 20% en DC Comics",
            "description": "20% de descuento en todos los cómics de DC",
            "start_date": "01/02/2025",
            "end_date": "28/02/2025",
            "eligible_levels": "Gold, VIP",
            "status": "active",
            "sent": 10,
            "used": 3,
            "conversion_rate": 30
        }
    ]
    
    # Simular campañas
    campaigns = [
        {
            "id": 1,
            "title": "Campaña de Reactivación",
            "description": "Campaña para reactivar clientes inactivos",
            "start_date": "01/01/2025",
            "end_date": "31/03/2025",
            "audience": "Clientes sin compras en 3 meses",
            "reach": 50,
            "progress": 65,
            "status": "active"
        },
        {
            "id": 2,
            "title": "Captación Nuevos Socios",
            "description": "Campaña para registrar nuevos clientes en programa de fidelidad",
            "start_date": "01/02/2025",
            "end_date": "31/05/2025",
            "audience": "Clientes no registrados en programa",
            "reach": 100,
            "progress": 30,
            "status": "active"
        },
        {
            "id": 3,
            "title": "Upgrade a VIP",
            "description": "Promocionar upgrade de nivel a clientes Gold",
            "start_date": "01/03/2025",
            "end_date": "30/04/2025",
            "audience": "Clientes nivel Gold",
            "reach": 15,
            "progress": 0,
            "status": "draft"
        }
    ]
    
    return templates.TemplateResponse("clientes_frecuentes.html", {
        "request": request,
        "stats": stats,
        "frequent_clients": frequent_clients,
        "promotions": promotions,
        "campaigns": campaigns
    })

# Rutas para Pedidos a Proveedores
@router.get("/gestion/pedidos-proveedor", response_class=HTMLResponse)
async def pedidos_proveedor(request: Request, db: Session = Depends(get_db)):
    # Estadísticas para el módulo
    stats = {
        "pending_orders": 5,    # Simulado
        "processing_orders": 3,  # Simulado
        "shipping_orders": 2,    # Simulado
        "completed_orders": 12   # Simulado
    }
    
    # Obtener proveedores para el filtro
    proveedores = db.query(models.Proveedor).all()
    
    # Simular pedidos a proveedores
    # En implementación real, deberíamos tener un modelo PedidoProveedor
    pedidos_proveedor = []
    
    estados = ["pending", "confirmed", "processing", "shipping", "completed"]
    
    for i in range(1, 11):
        proveedor_index = i % len(proveedores)
        estado_index = i % len(estados)
        
        # Simular items del pedido
        items = []
        for j in range(1, 4):
            items.append({
                "cantidad": j,
                "producto": f"Cómic {j}",
                "precio_unitario": 10.50 * j
            })
        
        total = sum(item["cantidad"] * item["precio_unitario"] for item in items)
        
        # Crear pedido simulado
        pedido = {
            "id": i,
            "proveedor": proveedores[proveedor_index],
            "fecha_pedido": datetime.now(),
            "estado": estados[estado_index],
            "items": items,
            "total": total
        }
        
        pedidos_proveedor.append(pedido)
    
    # Información de paginación
    pagination = {
        "current": 1,
        "pages": [1, 2, 3],
        "prev_page": None,
        "next_page": 2
    }
    
    return templates.TemplateResponse("pedidos_proveedor.html", {
        "request": request,
        "stats": stats,
        "proveedores": proveedores,
        "pedidos_proveedor": pedidos_proveedor,
        "pagination": pagination
    })

@router.get("/inventario", response_class=HTMLResponse)
async def get_inventory(request: Request, db: Session = Depends(get_db)):
    comics = crud.get_comics(db)
    return templates.TemplateResponse(
        "inventario.html", 
        {"request": request, "comics": comics}
    )

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