from fastapi import FastAPI
from .read_models import ProductRead

app = FastAPI()

@app.get("/products")
def get_products():
    return ProductRead.get_all()