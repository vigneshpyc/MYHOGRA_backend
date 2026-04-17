from fastapi import APIRouter, Request
from app.db.db_connect import connection
from app.db.Fetchproduct import Fetchproduct
from app.schemas.update_db import Update_db_request, FetchProduct, Add_Product
from app.db.db_operation import add_product
from app.core.config import SECRET_KEY, ALGORITHM
from jose import jwt
db_api = APIRouter(prefix='/dbapi', tags=['Dbapi'])



@db_api.post('/addproduct')
async def add_product_db(request :Request):
    token = request.cookies.get("refresh_token")
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    userID = payload.get("userID")
    data = await request.json()

    print("Product : ", data['product'])
    res = add_product(userID, data['product'] )
    print(res['message'])
    return res

@db_api.post('/update')
def update_db(data:Update_db_request):
    try:
        con = connection()
        cursor = con.cursor()
        print("------------------------------------Db connected successfully, entering query execution👇-------------------------------")
    except Exception as e:
        print("Something went worng because ",e)
    # cursor.execute(f"update purchase_data set purchased='{data.product}', not_purchased='{""}' where userid={data.userID} and not_purchased='{data.product}'")
    cursor.execute("update purchase_data set purchased = %s, not_purchased=%s where userid=%s and not_purchased = %s",(data.product,None,data.userID,data.product))
    con.commit()
    cursor.close()
    print("✅ Db updated successfully")
    return {"status":"success"}

@db_api.post('/fetchproduct')
def fetch_product(Category:FetchProduct):
    product = Fetchproduct(Category.category)
    return product