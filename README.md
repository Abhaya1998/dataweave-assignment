# Assignment
- Command [docker compose -f docker-compose-db.yaml up] will start all the database dependencies.
- Command [docker compose -f docker-compose.yaml up] will start up the processes.

We are currently running three apps.
1. Producer :- It is a one time run script, it will create table with schema, read data from json and will publish the message to rabbitmq taskqueue.
2. Consumer :- It will consume the message one by one, calculate score and update it in the postgres accordingly.
3. Api :- It will be used to fetch score, data throught GET method.

Celery Framework is being used here.