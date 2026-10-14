from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from .config import settings
from .routers import juridica

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION,
              openapi_url=f"{settings.API_V1_STR}/openapi.json")
# No usar CORS abierto con credenciales: definir orígenes permitidos tras configurar despliegue.
app.include_router(juridica.router, prefix=settings.API_V1_STR)

@app.get("/health")
def health_check():
    return {"status": "healthy", "version": settings.VERSION}
