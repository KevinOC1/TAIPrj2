from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
import logging

# Reorganización de importaciones para evitar conflictos
from app.database import get_db
from app import models, schemas
from . import crud  # crud específico de gestión comercial

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# Ruta para el panel de Gestión Comercial
@router.get("/gestion", response_class=HTMLResponse)
async def gestion_comercial(request: Request, db: Session = Depends(get_db)):
    # Obtener estadísticas para el panel
    comics_count = db.query(models.Comic).count()
    low_stock = db.query(models.Comic).filter(models.Comic.stock < 5).count()
    
    stats = {
        "low_stock": low_stock,
        "overstocked": db.query(models.Comic).filter(models.Comic.stock > 20).count(),
        "total_proveedores": db.query(models.Proveedor).count(),
        "pending_orders": 3,  
        "total_clientes": db.query(models.Cliente).count(),
        "new_clients": 5,  
        "frequent_clients": 7,  
        "active_promos": 3, 
        "supplier_orders": 4,  
        "arriving_soon": 2,  
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
            "min_stock": getattr(comic, 'min_stock', 5),  # Usar 5 si no existe el atributo
            "max_stock": getattr(comic, 'max_stock', 20),  # Usar 20 si no existe el atributo
            "category": "General",  # Simulado - implementar categorías en BD
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
    # Estadísticas reales para el módulo
    stats = {
        "members": db.query(models.Cliente).count(),
        "vip_members": db.query(models.Cliente).filter(models.Cliente.nivel == "vip").count(),
        "active_promos": 3,  # Puedes modificar esto según tus promociones reales
        "vip_orders": db.query(models.Pedido).filter(models.Pedido.cliente.has(nivel="vip")).count()
    }
    
    # Obtener clientes con sus niveles reales
    clientes_db = db.query(models.Cliente).limit(10).all()
    frequent_clients = []
    
    for cliente in clientes_db:
        # Calcular número de pedidos
        num_pedidos = db.query(models.Pedido).filter(models.Pedido.cliente_id == cliente.id).count()
        
        # Encontrar la última compra
        ultima_compra = db.query(models.Pedido)\
            .filter(models.Pedido.cliente_id == cliente.id)\
            .order_by(models.Pedido.fecha.desc())\
            .first()
        
        frequent_clients.append({
            "id": cliente.id,
            "nombre": cliente.nombre,
            "email": cliente.email,
            "level": cliente.nivel or "bronze",  # Usar nivel real de la base de datos
            "points": cliente.puntos or 0,
            "orders": num_pedidos,
            "last_purchase": ultima_compra.fecha.strftime("%d/%m/%Y") if ultima_compra else "N/A"
        })
    
    # Mantener las promociones y campañas simuladas
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
    
    # Mantener las campañas simuladas
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

@router.get("/gestion/pedidos-proveedor", response_class=HTMLResponse)
async def pedidos_proveedor(request: Request, db: Session = Depends(get_db)):
    # Estadísticas simplificadas
    stats = {
        "pending_orders": 5,
        "processing_orders": 3,
        "shipping_orders": 2,
        "completed_orders": 12
    }
    
    # Obtener proveedores
    proveedores = []
    try:
        proveedores = db.query(models.Proveedor).all()
    except Exception as e:
        print(f"Error al obtener proveedores: {e}")
    
    # Crear pedidos simulados con datos fijos (sin objetos complejos)
    pedidos_proveedor = []
    
    # Crear solo tres pedidos simples
    for i in range(1, 4):
        # Proveedor por defecto si no hay ninguno en la base de datos
        proveedor_dict = {"nombre": f"Proveedor {i}", "email": "ejemplo@mail.com"}
        
        # Usar un proveedor real si existe
        if proveedores and i <= len(proveedores):
            proveedor = proveedores[i-1]
            proveedor_dict = {"nombre": proveedor.nombre, "email": proveedor.email}
        
        pedido = {
            "id": i,
            "proveedor": proveedor_dict,
            "fecha_pedido": datetime.now(),
            "estado": "pending",
            "total": 100.00 * i
        }
        
        pedidos_proveedor.append(pedido)
    
    # Paginación simple
    pagination = {
        "current": 1,
        "pages": [1],
        "prev_page": None,
        "next_page": None
    }
    
    return templates.TemplateResponse("pedidos_proveedor.html", {
        "request": request,
        "stats": stats,
        "proveedores": proveedores,
        "pedidos_proveedor": pedidos_proveedor,
        "pagination": pagination
    })

# Ruta para crear un nuevo pedido a proveedor
@router.get("/gestion/pedidos-proveedor/crear", response_class=HTMLResponse)
async def crear_pedido_proveedor(request: Request, db: Session = Depends(get_db)):
    # Obtener proveedores y cómics para los formularios
    proveedores = db.query(models.Proveedor).all()
    comics = db.query(models.Comic).all()
    
    return templates.TemplateResponse("crear_pedido_proveedor.html", {
        "request": request,
        "proveedores": proveedores,
        "comics": comics
    })

# Ruta para crear un pedido a proveedor con un cómic preseleccionado
@router.get("/gestion/crear-pedido-proveedor", response_class=HTMLResponse)
async def crear_pedido_proveedor_recomendado(
    request: Request, 
    comic_id: Optional[int] = None, 
    db: Session = Depends(get_db)
):
    """
    Crear un pedido a proveedor, opcionalmente preseleccionando un cómic específico
    """
    # Obtener proveedores y cómics para los formularios
    proveedores = db.query(models.Proveedor).all()
    comics = db.query(models.Comic).all()
    
    # Preparar los datos del contexto sin usar objetos complejos
    # Simplemente pasamos el ID del cómic preseleccionado si existe
    context = {
        "request": request,
        "proveedores": proveedores,
        "comics": comics,
        "comic_preseleccionado_id": comic_id
    }
    
    return templates.TemplateResponse("crear_pedido_proveedor.html", context)

# Ruta para ver detalles de un pedido a proveedor
@router.get("/gestion/pedidos-proveedor/{pedido_id}", response_class=HTMLResponse)
async def ver_pedido_proveedor(pedido_id: int, request: Request, db: Session = Depends(get_db)):
    # Simular un pedido para mostrar (en una implementación real, buscaríamos en la BD)
    proveedor = db.query(models.Proveedor).first()
    if not proveedor:
        proveedor = {"id": 1, "nombre": "Proveedor de ejemplo", "email": "proveedor@ejemplo.com", "telefono": "555-1234"}
    
    comics = db.query(models.Comic).limit(3).all()
    
    fecha_hoy = datetime.now()
    fecha_entrega = datetime(datetime.now().year, datetime.now().month + 1, 1)
    
    # Simular fechas de cambios de estado
    fechas_estado = {
        "fecha_confirmacion": fecha_hoy,
        "fecha_procesado": fecha_hoy,
        "fecha_envio": fecha_hoy,
        "fecha_entrega_real": None
    }
    
    # Simular detalles - IMPORTANTE: Asegúrate de que esto sea una lista, no un método
    detalles = []
    total = 0
    
    for i, comic in enumerate(comics):
        cantidad = i + 1
        precio = comic.price
        subtotal = cantidad * precio
        total += subtotal
        
        detalles.append({
            "comic": comic,
            "cantidad": cantidad,
            "precio_unitario": precio,
            "subtotal": subtotal
        })
    
    pedido = {
        "id": pedido_id,
        "proveedor": proveedor,
        "fecha_pedido": fecha_hoy,
        "fecha_entrega_esperada": fecha_entrega,
        "fecha_entrega_real": None,
        "estado": "processing",  # Puede ser: pending, confirmed, processing, shipping, completed, cancelled
        "notas": "Pedido de reposición de inventario para temporada alta",
        "total": total,
        "detalles": detalles,  # Asegúrate de que sea una lista normal, no un método
        **fechas_estado
    }
    
    return templates.TemplateResponse("detalle_pedido_proveedor.html", {
        "request": request,
        "pedido": pedido
    })
    
    
    
@router.get("/stock/entrada", response_class=HTMLResponse)
async def entrada_stock_form(request: Request, db: Session = Depends(get_db)):
    # Usamos el módulo crud local
    comics = db.query(models.Comic).all()  # O usar app.crud.get_comics si está disponible
    proveedores = db.query(models.Proveedor).all()  # O usar app.crud.get_proveedores si está disponible
    return templates.TemplateResponse(
        "stock_entrada.html", 
        {"request": request, "comics": comics, "proveedores": proveedores}
    )

@router.post("/stock/entrada")
async def entrada_stock(
    comic_id: int = Form(...),
    cantidad: int = Form(...),
    proveedor_id: Optional[int] = Form(None),
    db: Session = Depends(get_db)
):
    entrada = crud.registrar_entrada_stock(db, comic_id, cantidad, proveedor_id)
    if not entrada:
        raise HTTPException(status_code=404, detail="No se pudo registrar la entrada de stock")
    
    return RedirectResponse(url="/inventario", status_code=303)

@router.get("/stock/salida", response_class=HTMLResponse)
async def salida_stock_form(request: Request, db: Session = Depends(get_db)):
    comics = db.query(models.Comic).all()  # O usar app.crud.get_comics si está disponible
    return templates.TemplateResponse(
        "stock_salida.html", 
        {"request": request, "comics": comics}
    )

@router.post("/stock/salida")
async def salida_stock(
    comic_id: int = Form(...),
    cantidad: int = Form(...),
    razon: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    salida = crud.registrar_salida_stock(db, comic_id, cantidad, razon)
    if not salida:
        raise HTTPException(status_code=400, detail="No se pudo registrar la salida de stock")
    
    return RedirectResponse(url="/inventario", status_code=303)

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

# Rutas para Control de Stock

@router.get("/stock/ajustar", response_class=HTMLResponse)
async def ajustar_stock_form(request: Request, db: Session = Depends(get_db)):
    comics = db.query(models.Comic).all()  # O usar app.crud.get_comics si está disponible
    return templates.TemplateResponse(
        "stock_ajustar.html", 
        {"request": request, "comics": comics}
    )

@router.post("/stock/ajustar")
async def ajustar_stock(
    comic_id: int = Form(...),
    cantidad: int = Form(...),
    db: Session = Depends(get_db)
):
    comic = crud.ajustar_stock(db, comic_id, cantidad)
    if not comic:
        raise HTTPException(status_code=404, detail="Comic not found")
    
    return RedirectResponse(url="/inventario", status_code=303)

@router.get("/stock/transferir", response_class=HTMLResponse)
async def transferir_stock_form(request: Request, db: Session = Depends(get_db)):
    comics = db.query(models.Comic).all()  # O usar app.crud.get_comics si está disponible
    return templates.TemplateResponse(
        "stock_transferir.html", 
        {"request": request, "comics": comics}
    )

@router.post("/stock/transferir")
async def transferir_stock(
    comic_origen_id: int = Form(...),
    comic_destino_id: int = Form(...),
    cantidad: int = Form(...),
    db: Session = Depends(get_db)
):
    comics = crud.transferir_stock(db, comic_origen_id, comic_destino_id, cantidad)
    if not comics:
        raise HTTPException(status_code=400, detail="No se pudo transferir el stock")
    
    return RedirectResponse(url="/inventario", status_code=303)

@router.get("/stock/informe", response_class=HTMLResponse)
async def informe_stock(request: Request, db: Session = Depends(get_db)):
    comics_stock_bajo = crud.generar_informe_stock(db)
    return templates.TemplateResponse(
        "stock_informe.html", 
        {"request": request, "comics": comics_stock_bajo}
    )
    
    
    # Stock Limit Routes
@router.get("/gestion/stock/{comic_id}/establecer-limites", response_class=HTMLResponse)
async def establecer_limites_stock_form(
    request: Request, 
    comic_id: int, 
    db: Session = Depends(get_db)
):
    comic = crud.get_comic(db, comic_id)
    if not comic:
        raise HTTPException(status_code=404, detail="Comic not found")
    
    return templates.TemplateResponse(
        "establecer_limites.html", 
        {"request": request, "comic": comic}
    )

@router.get("/gestion/stock/establecer-limites", response_class=HTMLResponse)
async def establecer_limites_stock_global_form(request: Request, db: Session = Depends(get_db)):
    comics = db.query(models.Comic).all()  # O usar app.crud.get_comics si está disponible
    return templates.TemplateResponse(
        "establecer_limites.html", 
        {"request": request, "comics": comics}
    )

@router.post("/gestion/stock/{comic_id}/establecer-limites")
async def guardar_limites_stock_individual(
    comic_id: int,
    limite_minimo: int = Form(...),
    db: Session = Depends(get_db)
):
    try:
        comic = crud.establecer_limite_stock(db, comic_id, limite_minimo)
        if not comic:
            raise HTTPException(status_code=404, detail="Comic not found")
        
        return RedirectResponse(url="/inventario", status_code=303)
    except Exception as e:
        # Log the full error for server-side debugging
        print(f"Error estableciendo límite de stock: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.post("/gestion/stock/establecer-limites")
async def guardar_limites_stock_global(
    comic_ids: List[int] = Form(...),
    limites_minimos: List[int] = Form(...),
    db: Session = Depends(get_db)
):
    # Establecer límites para cada cómic
    for comic_id, limite_minimo in zip(comic_ids, limites_minimos):
        crud.establecer_limite_stock(db, comic_id, limite_minimo)
    
    return RedirectResponse(url="/inventario", status_code=303)

@router.get("/stock/critico", response_class=HTMLResponse)
async def informe_stock_critico(request: Request, db: Session = Depends(get_db)):
        comics_stock_critico = crud.generar_informe_stock_critico(db)
        return templates.TemplateResponse(
        "stock_critico.html", 
        {"request": request, "comics": comics_stock_critico}
    )
    
    
@router.get("/gestion/clientes-frecuentes/nuevo", response_class=HTMLResponse)
async def nuevo_cliente_frecuente_form(request: Request):
    return templates.TemplateResponse(
        "nuevo_cliente_frecuente.html", 
        {"request": request}
    )

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/gestion/clientes-frecuentes/nuevo")
async def crear_cliente_frecuente(
    request: Request,
    nombre: str = Form(...),
    email: str = Form(...),
    telefono: Optional[str] = Form(None),
    fecha_nacimiento: Optional[str] = Form(None),
    nivel: Optional[str] = Form("bronze"),
    puntos_iniciales: Optional[int] = Form(0),
    notas: Optional[str] = Form(None),
    newsletter: bool = Form(False),
    promociones: bool = Form(False),
    generos: List[str] = Form([]),
    db: Session = Depends(get_db)
):
    try:
        # Parse fecha_nacimiento if provided
        parsed_fecha_nacimiento = None
        if fecha_nacimiento and fecha_nacimiento.strip():
            try:
                parsed_fecha_nacimiento = datetime.strptime(fecha_nacimiento, "%Y-%m-%d")
            except ValueError:
                logger.warning(f"Invalid date format: {fecha_nacimiento}")
        
        # Log form data for debugging
        form_data = await request.form()
        logger.info(f"Received form data: {dict(form_data)}")
        
        # Process checkbox values
        newsletter_value = "newsletter" in form_data
        promociones_value = "promociones" in form_data
        
        # Process genres (multi-checkbox) - Método corregido
        # En lugar de getall, usamos la lista generos que ya recibimos como parámetro
        # o podemos acceder directamente al form_data para obtener valores individuales
        if isinstance(generos, list):
            generos_str = ",".join(generos)
        else:
            # Si solo es un valor (no lista), lo tratamos como cadena única
            generos_str = str(generos) if generos else None
        
        cliente_data = {
            "nombre": nombre,
            "email": email,
            "telefono": telefono,
            "fecha_nacimiento": parsed_fecha_nacimiento,
            "nivel": nivel,
            "puntos": puntos_iniciales,
            "notas": notas,
            "newsletter": newsletter_value,
            "promociones": promociones_value,
            "generos_interes": generos_str
        }
        
        logger.info(f"Processed client data: {cliente_data}")
        
        # Usamos el crud local para crear el cliente frecuente
        nuevo_cliente = crud.crear_cliente_frecuente(db, cliente_data)
        logger.info(f"Successfully created client with ID: {nuevo_cliente.id}")
        
        return RedirectResponse(url="/gestion/clientes-frecuentes", status_code=303)
    except Exception as e:
        # Log the full error
        logger.error(f"Error creating frequent customer: {e}", exc_info=True)
        
        # Return to the form with an error message
        return templates.TemplateResponse("nuevo_cliente_frecuente.html", {
            "request": request, 
            "error": str(e)
        })
        
        
@router.get("/gestion/clientes-frecuentes/{cliente_id}/historial", response_class=HTMLResponse)
async def cliente_frecuente_historial(
    request: Request, 
    cliente_id: int, 
    db: Session = Depends(get_db)
):
    # Obtener datos del cliente
    cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    # Para la demo, simulamos un nivel, puntos y pedidos
    nivel = "gold"  # En la implementación real, esto vendría del cliente
    puntos = 750    # En la implementación real, esto vendría del cliente
    
    # Obtener pedidos reales del cliente
    pedidos = db.query(models.Pedido).filter(models.Pedido.cliente_id == cliente_id).all()
    
    # Simular movimientos de puntos
    movimientos_puntos = [
        {
            "fecha": datetime.now() - timedelta(days=60),
            "concepto": "Compra inicial",
            "puntos": 100,
            "balance": 100
        },
        {
            "fecha": datetime.now() - timedelta(days=45),
            "concepto": "Compra de cómics Marvel",
            "puntos": 200,
            "balance": 300
        },
        {
            "fecha": datetime.now() - timedelta(days=30),
            "concepto": "Canje por descuento",
            "puntos": -150,
            "balance": 150
        },
        {
            "fecha": datetime.now() - timedelta(days=15),
            "concepto": "Compra de cómics DC",
            "puntos": 250,
            "balance": 400
        },
        {
            "fecha": datetime.now() - timedelta(days=5),
            "concepto": "Puntos por cumpleaños",
            "puntos": 350,
            "balance": 750
        }
    ]
    
    # Simular estadísticas de puntos
    puntos_canjeados = 150
    puntos_totales = puntos + puntos_canjeados
    
    # Simular promociones usadas
    promociones_usadas = [
        {
            "title": "Descuento 15% en Marvel",
            "description": "15% de descuento en todos los cómics de Marvel",
            "code": "MARVEL15",
            "value": "15% descuento",
            "used_date": datetime.now() - timedelta(days=30)
        },
        {
            "title": "Cómic gratis por puntos",
            "description": "Canje de 150 puntos por un descuento en tu compra",
            "code": "POINTS2023",
            "value": "150 puntos",
            "used_date": datetime.now() - timedelta(days=30)
        }
    ]
    
    return templates.TemplateResponse("cliente_frecuente_historial.html", {
        "request": request,
        "cliente": cliente,
        "nivel": nivel,
        "puntos": puntos,
        "pedidos": pedidos,
        "movimientos_puntos": movimientos_puntos,
        "puntos_canjeados": puntos_canjeados,
        "puntos_totales": puntos_totales,
        "promociones_usadas": promociones_usadas
    })

@router.get("/gestion/clientes-frecuentes/{cliente_id}/promocion", response_class=HTMLResponse)
async def cliente_frecuente_promocion_form(
    request: Request, 
    cliente_id: int, 
    db: Session = Depends(get_db)
):
    # Obtener datos del cliente
    cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    # Para la demo, simulamos un nivel y puntos
    nivel = "gold"  # En la implementación real, esto vendría del cliente
    puntos = 750    # En la implementación real, esto vendría del cliente
    
    return templates.TemplateResponse("cliente_frecuente_promocion.html", {
        "request": request,
        "cliente": cliente,
        "nivel": nivel,
        "puntos": puntos
    })

@router.post("/gestion/clientes-frecuentes/{cliente_id}/promocion")
async def cliente_frecuente_promocion_submit(
    request: Request,
    cliente_id: int,
    promo_type: str = Form(...),
    promo_title: str = Form(...),
    valid_from: str = Form(...),
    valid_until: str = Form(...),
    db: Session = Depends(get_db)
):
    # Aquí procesarías los datos del formulario
    # y enviarías la promoción al cliente
    
    # Redireccionar a la lista de clientes frecuentes
    return RedirectResponse(url="/gestion/clientes-frecuentes", status_code=303)

@router.get("/gestion/clientes-frecuentes/{cliente_id}/nivel", response_class=HTMLResponse)
async def cliente_frecuente_nivel_form(
    request: Request, 
    cliente_id: int, 
    db: Session = Depends(get_db)
):
    # Obtener datos del cliente
    cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    # Obtener nivel actual de la base de datos
    nivel_actual = cliente.nivel or "bronze"  # Valor por defecto si no tiene nivel
    
    # Calcular puntos y total de compras
    # En una implementación real, calcularías esto de la base de datos
    puntos = sum(pedido.total for pedido in cliente.pedidos) // 10  # Ejemplo simple de cálculo de puntos
    total_compras = sum(pedido.total for pedido in cliente.pedidos)
    
    return templates.TemplateResponse("cliente_frecuente_nivel.html", {
        "request": request,
        "cliente": cliente,
        "nivel": nivel_actual,  # Usar nivel de la base de datos
        "puntos": puntos,
        "total_compras": total_compras
    })

@router.post("/gestion/clientes-frecuentes/{cliente_id}/nivel")
async def cliente_frecuente_nivel_submit(
    request: Request,
    cliente_id: int,
    nuevo_nivel: str = Form(...),
    motivo: str = Form(...),
    comentarios: Optional[str] = Form(None),
    notificar: bool = Form(False),
    db: Session = Depends(get_db)
):
    try:
        # Obtener el cliente
        cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        
        # Actualizar nivel
        cliente.nivel = nuevo_nivel
        
        # Registrar cambio de nivel (podrías crear un modelo de historial de niveles)
        # Ejemplo de cómo podrías registrar el cambio
        cambio_nivel = models.CambioNivel(
            cliente_id=cliente_id,
            nivel_anterior=cliente.nivel,
            nivel_nuevo=nuevo_nivel,
            motivo=motivo,
            comentarios=comentarios,
            fecha=datetime.now()
        )
        
        db.add(cambio_nivel)
        db.commit()
        
        # Opcional: Enviar notificación si está marcado
        if notificar:
            # Lógica para enviar notificación (correo, SMS, etc.)
            pass
        
        return RedirectResponse(url="/gestion/clientes-frecuentes", status_code=303)
    
    except Exception as e:
        # Manejar cualquier error
        logger.error(f"Error actualizando nivel de cliente: {e}")
        raise HTTPException(status_code=500, detail="Error al actualizar el nivel del cliente")