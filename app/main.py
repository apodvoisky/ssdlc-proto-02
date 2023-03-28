from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import customers, products, users, auth

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
    expose_headers=["*"],
)

app.include_router(customers.router)
app.include_router(products.router)
app.include_router(users.router)
app.include_router(auth.router)


@app.get("/ping", tags=['System'])
def pong():
    return {"ping": "pong!"}
