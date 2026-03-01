from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
import config

app = FastAPI(
    title="API Controle de Luminosidade",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS para React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotas
app.include_router(router)


@app.get("/")
def root():
    return {
        "name": "API Controle de Luminosidade",
        "version": "1.0.0",
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=config.HOST, port=config.PORT, reload=config.DEBUG)

