from pydantic import BaseModel

class Update_db_request(BaseModel):
    product:str

class FetchProduct(BaseModel):
    category : str

class Add_Product(BaseModel):
    userId:int
    product:str
