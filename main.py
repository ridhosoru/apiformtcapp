import os
import json
from dotenv import load_dotenv
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
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

class Log(BaseModel):
    username : str
    password : str

class LogUser(BaseModel):
    username : str
    password : str
    id       : int

class regUser(BaseModel):
    username :str
    password :str
    workNumber:int
    id : int

class wId(BaseModel):
    id          :int

class getRespon(BaseModel):
    id          :int
    datestart   :str
    status      :str

class Task(BaseModel):
    id    :Optional[int] = None
    status:Optional[str] = None
    datestart:Optional[str] = None
    timestart :Optional[str] = None
    timerespon:Optional[str] = None
    location :Optional[str] = None
    machine :Optional[str] = None
    problem:Optional[str] = None
    commenttxt:Optional[str] = None
    problemaftercheck:Optional[str] = None
    solve:Optional[str] = None
    timefinish:Optional[str] = None
    namemtc:Optional[str] = None

class TaskUpdate(BaseModel):
    id    :Optional[int] = None
    status:Optional[str] = None
    datestart:Optional[str] = None
    timestart :Optional[str] = None
    timerespon:Optional[str] = None
    commenttxt:Optional[str] = None

class TaskFinish(BaseModel):
    id    :Optional[int] = None
    status:Optional[str] = None
    datestart:Optional[str] = None
    timestart :Optional[str] = None
    timerespon:Optional[str] = None
    commenttxt:Optional[str] = None
    problemaftercheck:Optional[str] = None
    solve:Optional[str] = None
    timefinish:Optional[str] = None
    namemtc:Optional[str] = None

class getTasK(BaseModel):
    id : int
    datestart:str

@app.post("/registerAcc")
def registerAcc(reg:Reg):
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

@app.post("/loginAcc")
def login(log:Log):
    try:
        response = supabase.table("Account_Data").select("*").eq("username", log.username).eq("password", log.password).execute()
        if response.data:
            return response.data
        raise HTTPException(status_code=401, detail="Invalid username or password")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/loginUser")
def loginUser(log:LogUser):
    try:
        response = supabase.table("user_data").select("*").eq("username", log.username).eq("password", log.password).eq("id",log.id).execute()
        if response.data:
            return response.data
        raise HTTPException(status_code=409, detail="Invalid username or password")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.post("/RegisterUser")
def regUser(reguser:regUser):
    try:
        response = supabase.table("user_data").insert({
        "username" : reguser.username, 
        "password" : reguser.password,
        "worknumber" : reguser.workNumber,
        "id"    : reguser.id
        }).execute()
        if response.data:
            return response.data
        raise HTTPException(status_code=409, detail="Invalid username or password")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/machineName")
def getMachine(getmachine:wId):
    try:
        response = supabase.table("machinename").select("*").eq("id", getmachine.id).execute()
        if response.data: 
            return response.data
        raise HTTPException(status_code=404, detail="Machine ID not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/lineName")
def getLine(getline:wId):
    try:
        response = supabase.table("linename").select("*").eq("id", getline.id).execute()
        if response.data: 
            return response.data
        raise HTTPException(status_code=404, detail="ID not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/issueTable")
def getLine(getissue:wId):
    try:
        response = supabase.table("issuetable").select("*").eq("id", getissue.id).execute()
        if response.data: 
            return response.data
        raise HTTPException(status_code=404, detail="ID not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/TaskInput")
def taskInput(task:Task):
    try:
        response = supabase.table("tasktable").insert({
        "id"    : task.id,
        "status":task.status,
        "datestart":task.datestart,
        "timestart" :task.timestart,
        "timerespon":task.timerespon,
        "location" :task.location,
        "machine" :task.machine,
        "problem":task.problem,
        "commenttxt":task.commenttxt,
        "problemaftercheck":task.problemaftercheck,
        "solve":task.solve,
        "timefinish":task.timefinish,
        "namemtc":task.namemtc
        }).execute()
        if response.data:
            return response.data
        raise HTTPException(status_code=404, detail="id not founf")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/getTask")
def getTask(gettask:getTasK):
    try:
        response = supabase.table("tasktable").select("*").eq("id", gettask.id).eq("datestart",gettask.datestart).execute()
        if response.data: 
            return response.data
        raise HTTPException(status_code=404, detail="ID not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/getRespon")
def getTask(getrespon:getRespon):
    try:
        response = supabase.table("tasktable").select("*").eq("id", getrespon.id).eq("datestart",getrespon.datestart).eq("status",getrespon.status).execute()
        if response.data: 
            return response.data
        raise HTTPException(status_code=404, detail="ID not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/TaskUpdate")
def taskUpdate(task:TaskUpdate):
    try:
        response = supabase.table("tasktable").update({ 
        "status":task.status,
        "timerespon":task.timerespon,
        }).eq("id",task.id).eq("datestart",task.datestart).eq("commenttxt",task.commenttxt).eq("timestart",task.timestart).execute()
        if response.data:
            return response.data
        raise HTTPException(status_code=404, detail="id not founf")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/TaskFinish")
def taskfinsh(task:TaskFinish):
    try:
        response = supabase.table("tasktable").update({ 
        "status":task.status,
        "timefinish":task.timefinish,
        "problemaftercheck":task.problemaftercheck,
        "solve":task.solve,
        'namemtc':task.namemtc
        }).eq("id",task.id).eq("datestart",task.datestart).eq("timerespon",task.timerespon).eq("commenttxt",task.commenttxt).eq("timestart",task.timestart).execute()
        if response.data:
            return response.data
        raise HTTPException(status_code=404, detail="id not founf")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        