from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import session,engine
import database_models
from models import Product
from sqlalchemy.orm import Session

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:3000"],
    allow_methods = ["*"]
)
database_models.Base.metadata.create_all(bind=engine)

@app.get("/")
def greet():
    
    return {"message": "Wellcome to FastAPI learning!"}

products = [
    Product(id = 1,   name = "phone",    description = "A smartphone",    price = 9994,    quantity =10 ),
    Product(id = 2,   name = "Laptop",    description = "A laptop",       price =3433 ,    quantity =12 ),
    Product(id = 3,   name = "Pen",    description = "A pen",             price = 2323,    quantity = 21),
    Product(id = 5,   name = "Table",    description = "A Wooden Chair",  price = 23232,   quantity = 44)

]

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


##
def init_db():
    db = session()
    count = db.query(database_models.Product).count
    if count == 0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))

    db.commit()

init_db()
## all data get
@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):
    ## amader database connection lagbe
    ## jekhane query lekha lagbe
    # db = session()
    # db.query()
    db_products = db.query(database_models.Product).all()
    return db_products

###  record alada alada dekhar jonno id er maddhome
@app.get("/products/{id}")
def get_product_by_id(id: int ,db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        return db_product
    return "sorry not found"


## adding records
@app.post("/products")
def add_product(product : Product,db: Session = Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return product



## update
@app.put("/products/{id}")
def update_product(id: int, product : Product,db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product :
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        db.commit()
        return "Product Updated"

    else: 
        "No product found"



## dlt
@app.delete("/products/{id}")
def delete_product(id: int,db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product   :
        db.delete(db_product)
        db.commit()   
        return "product deleted"
      
    else:
        return "No product Found"