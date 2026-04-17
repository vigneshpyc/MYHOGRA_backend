from fastapi import APIRouter, Response, Request, HTTPException
from jose import jwt, JWTError
from app.schemas.auth import LoginRequest
from app.services.auth_services import authenticate_user, generate_tokens
from app.core.config import SECRET_KEY, ALGORITHM
import json
from app.db.db_operation import product_fetch

router = APIRouter(prefix="/auth", tags=["Auth"])

# with open("app/db/sampledata.json",'r') as file:
#     data = json.load(file)

@router.post("/login")
def login(user: LoginRequest, response: Response):
    userdata = authenticate_user(user.email, user.password)
    print(userdata)
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
    else:
        purchased = userdata['purchased']
    
    return {"username":username,"userID":userdata['userID'],"access_token": access_token, "purchased":purchased, "notPurchased":userdata["notPurchased"]}


@router.post("/refresh")
async def refresh_token(request: Request):
    token = request.cookies.get("refresh_token")
    print(request)

    if not token:
        raise HTTPException(status_code=401, detail="No refresh token")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("payload : ", payload)
        username = payload.get("sub")
        userID = payload.get("userID")
        access_token, _ = generate_tokens(username,userID)
        # body = await request.json()
        # print(body)
        # userID = body['userID']
        print(userID)
        purchased, notPurchased = product_fetch(userID)
        if notPurchased.count(None) == len(notPurchased):
            purchased = []
        print("✅purchased from refresh",purchased)
        print("✅not purchased from refresr", notPurchased)
        return {"username":username,"userId":userID, "access_token": access_token, "purchased":purchased, "notPurchased":notPurchased}

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("refresh_token")
    return {"message": "Logged out"}