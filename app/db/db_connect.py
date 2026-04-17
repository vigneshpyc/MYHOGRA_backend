import mysql.connector as msqlcon
from app.core.config import USER, HOST, PASSWORD, PORT, DATABASE
def connection():
    try:
        con = msqlcon.connect(
            host=HOST,
            user = USER,
            password = PASSWORD,
            port = PORT,
            database=DATABASE,
        )
        return con
    except Exception as e:
        return {"status":"error", "message":"DB not connected"}