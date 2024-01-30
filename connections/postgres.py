import imp
import time
import config
from datetime import datetime,timedelta
from psycopg2.extensions import AsIs
import psycopg2.extras
import psycopg2
import sys
import pytz
import os
import json
import random
import string
from config import logger
sys.path.append(".")


class Postgres:
    def __init__(self, connection_string = None):
        '''Initialize by making a connection
        '''
        if connection_string:
            self.CONNECTION_URL = connection_string
        else:
            self.CONNECTION_URL = config.POSTGRES_URL
        self.connect()

    def connect(self):
        """
            This will establish a connection to tsdb.
        """
        self.conn = psycopg2.connect(
            self.CONNECTION_URL
        )

    def closeConnection(self):
        self.conn.close()

    def query(self, sql):
        '''
            This will execute the sql query. If an exception occurs it will reconnect and execute again.
        '''
        try:
            cursor = self.conn.cursor(
                cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute(sql)
        except (AttributeError, psycopg2.Error, NameError):
            self.connect()
            cursor = self.conn.cursor(
                cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute(sql)
        return cursor

    def createTableFromSchema(self,table_name,schema):
        try:
            query="CREATE TABLE IF NOT EXISTS {} (".format(table_name)
            for key,val in schema.items():
                query=query+'"'+key+'"'+" "+val+","
            query=query[:-1]
            query=query+");"

            cursor = self.query(query)
            self.conn.commit()
            cursor.close()
            print("Table Created")
        except Exception as e:
            logger.error("Error in Creating Table : "+str(e))
            return False

        return True


    def fetchByAccountCode(self, table_name, accountCode):
        get_statement = """SELECT * from {} where account_code='{}';""".format(
            table_name, accountCode)

        cursor = self.query(get_statement)
        items = [dict(item) for item in cursor]

        cursor.close()
        return items



    def insert(self,table_name,index,final_data):
        query=""
        for data in final_data:
            query=query+"UPDATE \"{}\" SET ".format(table_name)
            for key,value in data.items():
                query=query+"\"{}\"='{}',".format(key,str(value).replace("'",""))

            query=query[:-1]
            query=query+" WHERE index={};".format(index)
            # print(query)
        cursor = self.query(query)
        self.conn.commit()
        cursor.close()



    def insertInitialData(self,table_name,columns,final_data):
        column_query = ''
        for column_name in columns:
            column_query = column_query+'"{}",'.format(column_name)
            
        column_query=column_query[:-1]

        query='INSERT INTO {} ({}) VALUES '.format(table_name,column_query)
        for data in final_data:
            data_query="("
            for column_name in columns:
                data_query=data_query+"'{}',".format(data[column_name])
            data_query=data_query[:-1]+")"
        query=query[:-1]+data_query+";"

        cursor = self.query(query)
        self.conn.commit()
        cursor.close()
        
    def getAccountScore(self,table_name,account_code):
        query="select avg(availability_score) from {} where account_code='{}';".format(table_name,account_code)
        cursor = self.query(query)
        items = [dict(item) for item in cursor]

        cursor.close()
        return items