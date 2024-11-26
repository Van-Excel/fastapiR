from typing import List, Optional
from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, HTTPException, Request, status
from pydantic import BaseModel
from random import randrange
import uvicorn
from app.schema.posts import PostsResponse
from app.schema.products import CreateProduct, ProductResponse


from app.config.database import get_DB_connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_connection = (
        get_DB_connection()
    )  # Or just `get_DB_connection()` if it's synchronous.
    app.state.db_connection = db_connection
    print("Database connection established")
    try:
        yield 
    finally:
        db_connection.close()  # Close the connection
        print("Database connection closed")



app = FastAPI(
    lifespan=lifespan,
    title="fastAPI revision",
    description="Application to implement Production based practices",
    version="0.1.0",
)

# returns DB connection
def get_db(request:Request):
    return request.app.state.db_connection


@app.get("/", tags=["Home"])
async def root():

    return {"message": "Hello World Programmers"}



@app.get('/products', response_model=List[ProductResponse], status_code=status.HTTP_200_OK, tags=["Products"]) 
async def get_posts(db= Depends(get_db)):
    with db.cursor() as cur:
        cur.execute("SELECT * FROM products")
        products = cur.fetchall()
    return [ProductResponse(**product) for product in products]


@app.get('/posts', response_model=List[PostsResponse], status_code=status.HTTP_200_OK, tags=["Posts"]) 
async def get_posts(db= Depends(get_db)):
    with db.cursor() as cur:
        cur.execute('SELECT * FROM public."Posts"')
        posts = cur.fetchall()
    return [PostsResponse(**post) for post in posts]




# create new products

@app.post("/products", status_code=status.HTTP_201_CREATED, response_model= ProductResponse, tags=["Products"])
async def create_post(payload: CreateProduct, db= Depends(get_db)):
    payload = payload.model_dump()
    try:
        
        with db.cursor() as cur:
            query = '''INSERT INTO products (name, price, is_sale, inventory) VALUES (%s, %s, %s, %s) RETURNING *; '''
            values = (payload["name"], payload["price"] , payload["is_sale"], payload["inventory"])
            cur.execute(query, values)
            
            # Commit the transaction to save changes to the database
            db.commit()
            
            # fetch the created post since the transaction is committed
            new_post = dict(cur.fetchone())
            
        return ProductResponse(**new_post)
    except Exception as e:
        # Rollback the transaction if any error occurs
        db.rollback()
        print(f"Error occurred: {e}")
        # You can raise an HTTP exception or return an error message
        raise HTTPException(status_code=500, detail="Failed to create product")
            
        
    
   




@app.get("/posts/{id}", status_code=status.HTTP_200_OK, tags=["Post"])
async def get_specific_user(id: str):
    filtered_data = [post for post in data if post["id"] == id]
    if not filtered_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": f"Post with id of {id} not found"},
        )
    return {"data": filtered_data}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Post"])
async def delete_post(id: str):
    global data
    print(data[0])
    indexed = [index for index, post in enumerate(data) if post["id"] == id]
    print(indexed)
    if not indexed:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": f"Post with id of {id} not found"},
        )
    index_a = indexed[0]
    # del data[index]
    data = data.pop(index_a)
    print(data)

    return


if __name__ == "__main__":
    setting = uvicorn.Config(
        "app.main:app", port=8000, log_level="info", reload=True, use_colors=True
    )
    server = uvicorn.Server(config=setting)
    server.run()
