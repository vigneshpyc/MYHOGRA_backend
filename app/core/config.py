from dotenv import load_dotenv
import os
load_dotenv()

# SECRET_KEY = "supersecretkey" #os.getenv("SECRET_KEY")
# ALGORITHM = "HS256"

# ACCESS_TOKEN_EXPIRE_MINUTES = 1
# REFRESH_TOKEN_EXPIRE_MINUTES = 5

#Security credentials values
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

#JWT credentials values
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
REFRESH_TOKEN_EXPIRE_MINUTES = os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES")


#DB credentials values
HOST=os.getenv("HOST")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
PORT = os.getenv("PORT")
DATABASE=os.getenv("DATABASE")
