import os
import json
from dotenv import load_dotenv
from fastapi import FastAPI,Depends,HTTPException
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv
from supabase import create_client, Client
from postgrest import APIError
import ast
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

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

class addNote(BaseModel):
    id : int
    username:str
    subject: str
    notetext:str
    datenote:str

class getNote(BaseModel):
    id:int
    username:str

class getAlltask(BaseModel):
    id : int

class regProd(BaseModel):
    id:int
    name:str

class addstore(BaseModel):
    id : int
    namepart:str
    codepart: str
    typepart:str
    stockpart:int
    imgpath : str

class takestock(BaseModel):
    id:int
    namepart:str
    codepart:str
    stockpart:int


class getID(BaseModel):
    id : int

class takestorelist(BaseModel):
    id :int
    namepart:str
    codepart: str
    typepart:str
    stocktake:int
    date : str
    nameuser:str
    location:str
    machine:str
    status:str

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/getCred")
def get_cred():
    return {
        "email": os.getenv("email"),
        "password": os.getenv("password")
    }

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
    
@app.post("/problemName")
def getLine(getissue:wId):
    try:
        response = supabase.table("problemname").select("*").eq("id", getissue.id).execute()
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

@app.post("/addnote")
def taskInput(note:addNote):
    try:
        response = supabase.table("notemtc").insert({
        "id"    : note.id,
        "username"    : note.username,
        "subject"    : note.subject,
        "notetext"    : note.notetext,
        "datenote"     :note.datenote
        }).execute()
        if response.data:
            return response.data
        raise HTTPException(status_code=404, detail="id not founf")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/getNote")
def getnote(note:getNote):
    try:
        response = supabase.table("notemtc").select("*").eq("id", note.id).eq("username",note.username).execute()
        if response.data:
            return response.data
        raise HTTPException(status_code=404, detail="id not founf")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/getAllTask")
def getTask(getalltask:getAlltask):
    try:
        response = supabase.table("tasktable").select("*").eq("id", getalltask.id).execute()
        if response.data: 
            return response.data
        raise HTTPException(status_code=404, detail="ID not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/regMachine")
def getMachine(regprod:regProd):
    try:
        response = supabase.table("machinename").insert({
        "id"    : regprod.id,
        "name"  : regprod.name
        }).execute()
        if response.data:
            return response.data
        raise HTTPException(status_code=404, detail="id not founf")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/regLoc")
def getMachine(regprod:regProd):
    try:
        response = supabase.table("linename").insert({
        "id"    : regprod.id,
        "name"  : regprod.name
        }).execute()
        if response.data:
            return response.data
        raise HTTPException(status_code=404, detail="id not founf")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/regProb")
def getMachine(regprod:regProd):
    try:
        response = supabase.table("problemname").insert({
        "id"    : regprod.id,
        "name"  : regprod.name
        }).execute()
        if response.data:
            return response.data
        raise HTTPException(status_code=404, detail="id not founf")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/addstore")
def taskInput(adstore:addstore):
    try:
        response = supabase.table("store").insert({
        "id"    : adstore.id,
        "namepart"    : adstore.namepart,
        "codepart"    : adstore.codepart,
        "typepart"    : adstore.typepart,
        "stockpart"     :adstore.stockpart,
        "imgpath" : adstore.imgpath
        }).execute()
        if response.data:
            return response.data
        raise HTTPException(status_code=404, detail="id not founf")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/getStorePart")
def getTask(getid:getID):
    try:
        response = supabase.table("store").select("*").eq("id", getid.id).execute()
        if response.data: 
            return response.data
        raise HTTPException(status_code=404, detail="ID not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/takestock")
def taskInput(Takestock:takestock):
    try:
        response = supabase.table("store").update({
        "stockpart"     :Takestock.stockpart
        }).eq("id",Takestock.id).eq("namepart",Takestock.namepart).eq("codepart",Takestock.codepart).execute()
        if response.data:
            return response.data
        raise HTTPException(status_code=404, detail="id not founf")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/takestorelist")
def taskInput(takestorel:takestorelist):
    try:
        response = supabase.table("storelist").insert({
        "id"    : takestorel.id,
        "namepart"    : takestorel.namepart,
        "codepart"    : takestorel.codepart,
        "typepart"    : takestorel.typepart,
        "prodtake"     :takestorel.stocktake,
        "date" : takestorel.date,
        "nameuser":takestorel.nameuser,
        "location":takestorel.location,
        "machine":takestorel.machine,
        "status" :takestorel.status
        }).execute()
        if response.data:
            return response.data
        raise HTTPException(status_code=404, detail="id not founf")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/getStoreList")
def getTask(getid:getID):
    try:
        response = supabase.table("storelist").select("*").eq("id", getid.id).execute()
        if response.data: 
            return response.data
        raise HTTPException(status_code=404, detail="ID not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8080)