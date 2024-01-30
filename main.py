from fastapi import FastAPI
from connections.client import postgresClient
import config
import uvicorn

app= FastAPI()

@app.get("/getScore")
def getScore(account_code:str=None):
    try:
        if not account_code:
            return {
                "data":None,
                "success":False,
                "error":"Account Code Cant be Empty"
            }
        data = postgresClient.getAccountScore(config.TABLE_NAME,account_code)
        if not len(data) or not data[0]['avg']:
            return {
                "data":None,
                "success":False,
                "error":"Account Code doesnot exist"
            }
            
        return {
            "data":{
                "availability_score":data[0]['avg']
            },
            "success":True,
            "error":None
        }
    except Exception as e:
        print("Error in getScore",e)
        return {
            "data":None,
            "success":False,
            "error":"Internal Server Error"
        }
        
@app.get("/getProducts")
def getProducts(account_code:str=None):
    try:
        if not account_code:
            return {
                "data":None,
                "success":False,
                "error":"Account Code Cant be Empty"
            }
        data = postgresClient.fetchByAccountCode(config.TABLE_NAME,account_code)
        if not len(data):
            return {
                "data":None,
                "success":False,
                "error":"Account Code doesnot exist"
            }
            
        return {
            "data":data,
            "success":True,
            "error":None
        }
    except Exception as e:
        print("Error in getScore",e)
        return {
            "data":None,
            "success":False,
            "error":"Internal Server Error"
        }
        
if __name__=='__main__':
    uvicorn.run("main:app",host="0.0.0.0",port=8000,reload=False)