from fastapi import FastAPI
from app.routers import authentication, user,product, inventory, order
from app.database import engine
import app.models as models
from app.config import settings



app = FastAPI(title="Simple E-Commerce System")

models.Base.metadata.create_all(engine) #create all table into the database

app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(product.router)
app.include_router(inventory.router)
app.include_router(order.router)


@app.get("/")
def root():
  return {
    "Message":"E-Commerce Backend API is Running","docs":"/docs"
  }
