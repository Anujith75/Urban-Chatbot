from sys import deactivate_stack_trampoline
import time
from fastapi import FastAPI, HTTPException
from fastapi import status
import psycopg2
from pydantic import BaseModel

app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(database="postgres", user="postgres.cidsbhqdqcupmmfgovdb", password="brainalyst@123", host="aws-0-ap-south-1.pooler.supabase.com", port="5432")
        cursor = conn.cursor()
        print("Connected to DB")
        break
    except Exception as error:
        print("Unable to connect to DB")
        time.sleep(2)

class User_login(BaseModel):
    username : str
    password : str

@app.post("/",status_code=status.HTTP_201_CREATED)
def login(user : User_login):
    cursor.execute("SELECT id FROM customers WHERE username = %s AND password = %s",(user.username,user.password))
    user_id = cursor.fetchone()
    if not user_id:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail="Wrong username and password"
        )
    print("User Validated")
    return user_id

@app.get("/customers")
async def root():
    cursor.execute("SELECT name FROM customers")
    customers = cursor.fetchall()
    print(customers)
    return customers