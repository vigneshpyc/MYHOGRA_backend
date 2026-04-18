from app.db.db_connect import connection
from datetime import date
def product_fetch(userID):
    con = connection()
    cursor = con.cursor(dictionary=True)
    cursor.execute(f"select purchased, not_purchased from purchase_data where userid='{userID}' ")
    data = cursor.fetchall()
    purchased = [x['purchased'] for x in data]
    notPurchased = [s['not_purchased'] for s in data]

    return purchased, notPurchased

def user_data(email):
    pass

def add_product(userId, product):
    if userId and product:
        Date = date.today().isoformat()
        con = connection()
        cursor = con.cursor(dictionary=True)        
        cursor.execute("insert into purchase_data(userid, purchased, not_purchased, purchased_date) values(%s,%s,%s,%s)",(userId, None, product, Date))
        con.commit()
        cursor.close()
        return {"status":True,"message":"Data Added Successfully"}
    else:
        return {"status":False,"message":"Data not Added"}


def reset(userid):
    con = connection()
    cursor = con.cursor()
    cursor.execute("delete from purchase_data where userid=%s",(userid,))
    con.commit()
    cursor.close()