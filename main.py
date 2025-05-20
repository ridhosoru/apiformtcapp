import os
import json
from dotenv import load_dotenv
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
import psycopg2
from typing import Optional
from dotenv import load_dotenv
from supabase import create_client, Client
from postgrest import APIError
import ast

load_dotenv()
db_url = os.getenv("db_url")
db_key = os.getenv("db_key")
app = FastAPI()
supabase: Client = create_client(db_url, db_key)

class Reg(BaseModel):
    username : str
    password : str
    email    : str

@app.post("/registerAcc")
def registerUser(reg:Reg):
    try :
        response = supabase.table("Account_Data").insert({
            "username" : reg.username, 
            "password" : reg.password,
            "email" : reg.email
        }).execute()
        if response.data is not None:
            account_id = response.data[0]["id"]
            # return account_id
            try :
                responseadm = supabase.table("user_data").insert({
                    "id"       : account_id,
                    "username" : "admin",
                    "password" : "admin",
                    "worknumber": 1
                }).execute()
                return response.data
            except Exception as e :
                raise HTTPException(status_code=500, detail=str(e))
    except Exception as e :
        detail = str(e)
        detail_dict = ast.literal_eval(detail)
        message_e = detail_dict['message']
        if message_e == "duplicate key value violates unique constraint \"Account_Data_username_key\"":
            raise HTTPException(status_code=409, detail="username already used")
        elif message_e == "duplicate key value violates unique constraint \"Account_Data_email_key\"":
            raise HTTPException(status_code=400, detail="email already used")
        else :
            raise HTTPException(status_code=500, detail=str(e))
        