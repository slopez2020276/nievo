from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router.router import user, admin


app = FastAPI()

# Configuración de CORS (puedes ajustar según tus necesidades)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(user)
app.include_router(admin)