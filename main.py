from fastapi import FastAPI


from api import customer, product

app = FastAPI()
app.include_router(customer.router)
app.include_router(product.router)


@app.get("/ping", tags=['System'])
def pong():
    return {"ping": "pong!"}
