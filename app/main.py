import logging
import uuid
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import customers, products, users, auth


logname = str(uuid.uuid4())
logging.basicConfig(filename=f'{logname}.log', level=logging.INFO)
logging.info("SSDLC Proto Service")

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
