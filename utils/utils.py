from connections.client import postgresClient
import config
from utils.schema import TABLE_SCHEMA

def getAvailabilityScore(accountCode:str):
    score = 0
    totaInStock = 0
    
    data = postgresClient.fetchByAccountCode(config.TABLE_NAME,accountCode)
    for item in data:
        if item['stock']=='In Stock':
            totaInStock+=1
            
    score = round(totaInStock/len(data),3)
    # print(data,score)
    
    return score
    
def insertInitialData(event):
    # index = event['index']
    # event.pop('index')
    
    postgresClient.insertInitialData(config.TABLE_NAME,TABLE_SCHEMA.keys(),[event])
    
    print("Data Inserted Successfully.")
    
def updateScore(score,index):
    postgresClient.insert(config.TABLE_NAME,index,[{'availability_score':score}])
    
    print("Score Updated Successfully.")