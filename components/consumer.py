from workers.insertWorker import app as appOperation
import config
import json
from utils.utils import getAvailabilityScore,insertInitialData,updateScore

@appOperation.task(bind=True,name=config.TASK_QUEUE,max_retries=0)
def execute(self,event):
    try:
        event = json.loads(event)
        # print(event)
        metaInfo = event['meta_info']
        event.pop('meta_info')
        
        event.update(json.loads(metaInfo.replace("'",'\"')))
        
        event['availability_score']=0
        accountCode = event['account_code']
        
        insertInitialData(event)
        
        event['availability_score'] = getAvailabilityScore(accountCode)
        updateScore(event['availability_score'],event['index'],)
        # print(event)
    except Exception as e:
        raise