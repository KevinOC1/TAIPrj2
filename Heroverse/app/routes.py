from fastapi import APIRouter, Request, Form, HTTPException, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from app import models
from app import schemas

router = APIRouter()
import os
templates = Jinja2Templates(directory="app/templates")

@router.get("/inventario", response_class=HTMLResponse)
async def get_inventory(request: Request):
    comics = models.get_all_comics()
    return templates.TemplateResponse(
        "inventario.html", 
        {"request": request, "comics": comics}
    )

@router.get("/comics/{comic_id}", response_class=HTMLResponse)
async def get_comic(request: Request, comic_id: int):
    comic = models.get_comic_by_id(comic_id)
    if not comic:
        raise HTTPException(status_code=404, detail="Comic not found")
    return templates.TemplateResponse(
        "comic_detail.html", 
        {"request": request, "comic": comic}
    )

@router.get("/comics/{comic_id}/editar", response_class=HTMLResponse)
async def edit_comic_form(request: Request, comic_id: int):
    comic = models.get_comic_by_id(comic_id)
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
    stock: int = Form(...)
):
    updated = models.update_comic(comic_id, price=price, stock=stock)
    if not updated:
        raise HTTPException(status_code=404, detail="Comic not found")
    return RedirectResponse(url="/inventario", status_code=303)

@router.get("/pedidos", response_class=HTMLResponse)
async def get_orders(request: Request):
    orders = models.get_all_orders()
    return templates.TemplateResponse("pedidos.html", {"request": request, "orders": orders})

@router.get("/clientes", response_class=HTMLResponse)
async def get_clients(request: Request):
    return templates.TemplateResponse("clientes.html", {"request": request})

@router.get("/proveedores", response_class=HTMLResponse)
async def get_providers(request: Request):
    return templates.TemplateResponse("proveedores.html", {"request": request})