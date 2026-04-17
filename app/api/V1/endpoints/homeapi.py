from fastapi import APIRouter
from app.services.add import First
router = APIRouter()

@router.get('/home')
def homepage(a,b):
    result = First.add(int(a),int(b))
    return {"status":"success","answer":result}