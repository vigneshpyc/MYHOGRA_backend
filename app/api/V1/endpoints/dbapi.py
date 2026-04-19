from fastapi import APIRouter, Request
from app.db.db_connect import connection
from app.db.Fetchproduct import Fetchproduct
from app.schemas.update_db import FetchProduct
from app.db.db_operation import add_product, reset
from app.core.config import SECRET_KEY, ALGORITHM
from jose import jwt
db_api = APIRouter(prefix='/dbapi', tags=['Dbapi'])



@db_api.post('/addproduct')
async def add_product_db(request :Request):
    #get userid from tokens
    token = request.cookies.get("refresh_token")
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    userID = payload.get("userID")

    data = await request.json()
    res = add_product(userID, data['product'] )
    return res

@db_api.post('/update')
async def update_db(request:Request):
    token = request.cookies.get("refresh_token")
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    userID = payload.get("userID")
    data = await request.json()

    try:
        con = connection()
        cursor = con.cursor()
    except Exception as e:
        return {"status":"error", "message":"Something went wrong because of "+e}
    cursor.execute("update purchase_data set purchased = %s, not_purchased=%s where userid=%s and not_purchased = %s",(data['product'],None,userID,data['product']))
    con.commit()
    cursor.close()
    return {"status":"success"}

@db_api.post('/fetchproduct')
def fetch_product(Category:FetchProduct):
    product = Fetchproduct(Category.category)
    return product

@db_api.post('/reset')
def reset_list(request:Request):
    token = request.cookies.get("refresh_token")
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    userID = payload.get("userID")
    result = reset(userID)

    return result
