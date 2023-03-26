from fastapi import FastAPI

from app.api import customers, products, users, auth

app = FastAPI()
app.include_router(customers.router)
app.include_router(products.router)
app.include_router(users.router)
app.include_router(auth.router)


@app.get("/ping", tags=['System'])
def pong():
    return {"ping": "pong!"}
