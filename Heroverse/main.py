from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import uvicorn
from app.routes import router

# Crear la aplicación FastAPI
app = FastAPI(title="HeroVerse Comics")

# Montar archivos estáticos (CSS, JS, imágenes)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
# Configurar plantillas
templates = Jinja2Templates(directory="app/templates")

# Incluir las rutas de la aplicación
app.include_router(router)

# Ruta principal
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Para ejecutar la aplicación directamente
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)