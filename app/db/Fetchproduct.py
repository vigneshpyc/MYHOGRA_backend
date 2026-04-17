from app.db.db_connect import connection
def Fetchproduct(category):
    con = connection()
    cursor = con.cursor(dictionary=True)
    cursor.execute(f"select item_name from products where category='{category}'")
    data = cursor.fetchall()
    cursor.close()
    return data
