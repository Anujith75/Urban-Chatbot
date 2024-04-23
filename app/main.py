from ast import While
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

user_id = None

def login(username:str,password:str):
    cursor.execute("SELECT id FROM customers WHERE username = %s AND password = %s",(username,password))
    user_id = cursor.fetchone()
    if not user_id:
        print("Wrong username or password")
    else:
        print("Login Successful")
        return user_id
    
while True:
    print("\nPlease Login")
    username = input("Enter username: ")
    password = input("Enter password: ")
    user_id = login(username=username,password=password)
    if user_id:
        break
while True:
    print("\nWelcome to the system, How can I help you?")
    print("1. Property Details")
    print("2. Add Property")
    print("3. Update Property")
    option = input("\nEnter your choice: ")
    if option == '1':
        cursor.execute("SELECT * FROM properties WHERE customer_id = %s",(user_id))
        print("\n")
        properties = cursor.fetchall()
        for  i in properties:
            print(f"Name: {i[1]}")
            print(f"Address: {i[2]}, {i[3]}, {i[4]}\n")
    elif option == '2':
        name = input("Enter property name: ")
        print("Enter property Address")
        street = input("Street: ")
        district = input("District: ")
        state = input("State: ")
        cursor.execute("INSERT INTO properties (property_name,street,district,state,customer_id) VALUES (%s,%s,%s,%s,%s) RETURNING property_id",(name,street,district,state,user_id))
        property_id = cursor.fetchone()
        print(property_id)
        cursor.execute("SELECT * FROM properties WHERE property_id = %s",(property_id))
        properties = cursor.fetchall()
        for  i in properties:
            print(f"Name: {i[1]}")
            print(f"Address: {i[2]}, {i[3]}, {i[4]}\n")
        conn.commit()
        print("Property added successfully")
    elif option == '3':
        cursor.execute("SELECT * FROM properties WHERE customer_id = %s",(user_id))
        properties = cursor.fetchall()
        print(properties)
        property_id = input("Enter property id to update: ")
        name = input("Enter property name: ")
        street = input("Street: ")
        district = input("District: ")
        state = input("State: ")
        property_id = cursor.execute("UPDATE properties SET name = %s, street = %s, district = %s, state = %s WHERE id = %s returning property_id",(name,street,district,state,property_id))
        conn.commit()
        print("Property updated successfully")
    else:
        print("Invalid option")