from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional,Text
from uuid import uuid4
app = FastAPI()
db = []

from uuid import uuid4

class Product(BaseModel):
    id: Optional[str] = None
    nameProduct: str
    cantProduct: int
    unitPrice: float
    routes: str

    def dict(self, *args, **kwargs):
        data = super().dict(*args, **kwargs)
        if self.id is None:
            self.id = str(uuid4())
        return data


@app.get("/")
def getProducts():
    if len(db) == 0:
        return {"message": "DB is empty"}
    else:
        return db

@app.post("/products", response_model=Product)
def postProducts(product: Product):
    product.id = str(uuid4())
    db.append(product.dict())
    return product

@app.put("/products/{post_id}", response_model=Product)
def updateProducts(post_id: str,product: Product):
    for pod in db:
        if pod["id"] == post_id:
            pod["nameProduct"] = product.nameProduct
            pod["cantProduct"] = product.cantProduct
            pod["unitPrice"] = product.unitPrice
            pod["routes"] = product.routes
            return product
    raise HTTPException(status_code=404, detail="Product not found")

@app.delete("/products/{id}")
def deleteProducts(id: str):
    for pod in db:
        if pod["id"] == id:
            db.remove(pod)
            return {"detail": "Product deleted successfully"}
    raise HTTPException(status_code=404, detail="Product not found")

@app.get("/products/{product_id}")
def getProduct(product_id: str):
    for prod in db:
        if prod["id"] == product_id:
            return prod
    raise HTTPException(status_code=404, detail="Product not found")