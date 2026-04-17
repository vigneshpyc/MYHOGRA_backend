from app.core.security import create_token
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES
from app.db.fake_db import get_data
from app.db.db_connect import connection


def authenticate_user(email, password):
    # user = fake_users.get(username)
    try:
        con = connection()
        cursor = con.cursor(dictionary=True)
        cursor.execute("select userid, user_name from users where email=%s and user_password=%s",(email,password))
        data = cursor.fetchone()
        print("data",data)
    except Exception as e:
        print("⚠️Error while fetching")
    
    if not data:
        print("error")
        return {"Status":"Fail", "message":"data is empty"}
    
    cursor.execute(f"select purchased, not_purchased from purchase_data where userid='{data['userid']}'")
    product_data = cursor.fetchall()
    
    purchased = [x['purchased'] for x in product_data]
    print("purchased : ",purchased)
    
    notPurchased = [x['not_purchased'] for x in product_data]
    print(purchased,notPurchased)
    
    return {"username":data['user_name'],"userID": data['userid'], "purchased":purchased, "notPurchased":notPurchased}

def generate_tokens(username, userID):
    access_token = create_token({"sub": username,"userID":userID}, int(ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_token = create_token({"sub": username, "userID":userID}, int(REFRESH_TOKEN_EXPIRE_MINUTES))

    return access_token, refresh_token