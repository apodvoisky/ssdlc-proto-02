from fastapi import FastAPI


from api import customer

app = FastAPI()
app.include_router(customer.router)


@app.get("/ping")
def pong():
    return {"ping": "pong!"}
