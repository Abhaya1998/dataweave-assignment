import sys
sys.path.append('.')

import pandas as pd
from connections.client import postgresClient
import config
from utils.schema import TABLE_SCHEMA
from consumer import execute
import json



class Producer:
    data = None
    def __init__(self) -> None:
        '''
            Initializing Table
        '''
        postgresClient.createTableFromSchema(config.TABLE_NAME,TABLE_SCHEMA)
        
    def readData(self):
        df = pd.read_json('data/data.json')
        self.data = df.to_dict('records')
        
    def publishData(self):
        for item in self.data:
            execute.apply_async(args=(json.dumps(item),),queue=config.TASK_QUEUE)
            print("All Data Published Successfully.")
            
    def process(self):
        self.readData()
        self.publishData()
        
Producer().process()