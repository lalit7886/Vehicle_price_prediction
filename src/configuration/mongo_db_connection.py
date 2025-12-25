import os
import sys
import pymongo
import certifi

from src.exception import MyException
from src.logger import logger
from src.constants import DATABASE_NAME, MONGODB_URL_KEY

ca=certifi.where() #Loads Certificate authority file to avoid timeout error while connecting to MongDB.

class MongoDBClient():
    '''
    Responsible for connection eastblishment with mongDB.
    
    Attribute:
    client: MongoClient
        A shared MongoClient instance.
        
    database: Database
        A specific istance of database that MongoDBClient connects to
        
    Methods:
    __init__(self,database_name:str=DATABASE_NAME):
        method that initialzes mongoDB connection using given Database Name
    '''
    client= None
    def __init__(self,database_name:str=DATABASE_NAME)->None:
        try:
            if MongoDBClient.client is None:
                mongo_db_url=os.getenv(MONGODB_URL_KEY)
                
                if mongo_db_url is None:
                    raise Exception (f"Environment vaariable {MONGODB_URL_KEY} is not set")
            
            MongoDBClient.client=pymongo.MongoClient(mongo_db_url,tlsCAFile=ca)
            self.client=MongoDBClient.client
            self.database=self.client(database_name)
            self.database_name=database_name
            logger.info("MongDB connection is successful ")
        except Exception as e:
            raise MyException(e,sys)