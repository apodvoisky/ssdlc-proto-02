from fastapi import FastAPI

from api import customer

app = FastAPI()
app.include_router(customer.router, prefix='/t01')

