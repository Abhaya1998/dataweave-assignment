from celery import Celery
import config
from celery.signals import after_task_publish
from datetime import datetime


app = Celery('worker_insert', broker = config.RABBITMQ_BROKER_URL, include = ['components.consumer'])

task_conf = {}

task_conf['worker_prefetch_multiplier'] = 1


task_conf['task_track_started'] = True


# task_conf['worker_max_tasks_per_child'] = 1


app.conf.update(task_conf)
app.conf.update(
    result_expires=3600,
)

app.conf.task_default_queue=config.TASK_QUEUE

if __name__ == '__main__':
    app.start()