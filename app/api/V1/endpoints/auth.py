from fastapi import APIRouter, Response, Request, HTTPException
from jose import jwt, JWTError
from app.schemas.auth import LoginRequest, UserData
from app.services.auth_services import authenticate_user, generate_tokens
from app.core.config import SECRET_KEY, ALGORITHM
import json
from app.db.db_operation import product_fetch,reset
from app.db.db_connect import connection
from datetime import date

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
def login(user: LoginRequest, response: Response):
    userdata = authenticate_user(user.email, user.password)
    # print(userdata)
    username = userdata['username']


    if not username:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token, refresh_token = generate_tokens(username, userdata['userID'])

    # 🔐 Store refresh token in HttpOnly cookie
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,  # True in production (HTTPS)
        samesite="lax"
    )

    #line check for completed status, if incolmpleted get the incompleted list and send to user
    if userdata['notPurchased'].count(None) == len(userdata['notPurchased']):
         purchased = []
         reset(userdata['userID'])
    else:
        purchased = userdata['purchased']
    
    return {"username":username,"userID":userdata['userID'],"access_token": access_token, "purchased":purchased, "notPurchased":userdata["notPurchased"]}


@router.post("/refresh")
async def refresh_token(request: Request):
    token = request.cookies.get("refresh_token")

    if not token:
        raise HTTPException(status_code=401, detail="No refresh token")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        userID = payload.get("userID")
        access_token, _ = generate_tokens(username,userID)
        purchased, notPurchased = product_fetch(userID)
        if notPurchased.count(None) == len(notPurchased):
            purchased = []

       
        return {"username":username,"userId":userID, "access_token": access_token, "purchased":purchased, "notPurchased":notPurchased}

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("refresh_token")
    return {"message": "Logged out"}

@router.post('/newuser')
def create_new_user(UserData:UserData):
    Date = date.today()
    con = connection()
    cursor = con.cursor()
    cursor.execute("insert into users(user_name,email, user_password, created_date, user_status) values(%s,%s,%s,%s,%s)",(UserData.username, UserData.email,UserData.password, Date, 1))
    con.commit()
    cursor.close()
    return {"status":"ok","message":"New User Created Successfully"}