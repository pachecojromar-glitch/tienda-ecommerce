from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import create_db
from routers import users,products,categories,comments

app=FastAPI(
    title="Store API",
    description="API básica de ecommerce para manipulación de productos, categorías, usuarios y comentarios",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    create_db()

api_prefix="/api"

app.include_router(users.router,prefix=api_prefix)
app.include_router(products.router,prefix=api_prefix)
app.include_router(categories.router,prefix=api_prefix)
app.include_router(comments.router,prefix=api_prefix)