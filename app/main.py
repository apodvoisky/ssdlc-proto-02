from fastapi import FastAPI

from app.api import customers, products

app = FastAPI()
app.include_router(customers.router)
app.include_router(products.router)


@app.get("/ping", tags=['System'])
def pong():
    return {"ping": "pong!"}
