import boto3
from src.configuration.aws_connection import s3Client
from io import StringIO
from typing import Union, List
import os,sys
from src.logger import logger
from mypy_boto3_s3.service_resource import Bucket
from src.exception import MyException
from botocore.exceptions import ClientError
from pandas import DataFrame,read_csv
import pickle


class SimpleStorageService:
    def __init__(self):
        s3_client=s3Client()
        self.s3_resource=s3_client.s3_resource
        self.s3_client=s3Client.s3_client
        
        
    def s3_key_path_available(self,bucket_name,s3_key)->bool:
        try:
            bucket=self.get_bucket(bucket_name)
            file_objects=[file_object for file_object in bucket.objects.filter(Prefix=s3_key)]
            return len(file_objects)>0
        except Exception as e:
            raise MyException(e,sys)
        
    @staticmethod
    def read_object(object_name:str,decode:bool=True,make_redable:bool=False)->Union[StringIO,str]:
        try:
            func=(
                lambda:object_name.get()["body"].read().decode()
                if decode else object_name.get()["Body"].read()
            )
            
            conv_func=lambda:StringIO(func()) if make_redable else func()
            
            return conv_func()
        
        except Exception as e:
            raise MyException(e,sys) from e
        
        
    def get_bucket(self,bucket_name:str)->Bucket:
        try:
            bucket=self.s3_resource.Bucket(bucket_name)
            logger.info("Exited the get_bucket method of class SimpleStorageClass")
            return bucket
        
        except Exception as e:
            raise MyException(e,sys) from e
        
        
    def get_file_object(self,file_name:str,bucket_name:str)->Union[List[object],object]:
        logger.info("Entered the get_file_object of class SimpleStorageService")
        
        try:
            bucket=self.get_bucket(bucket_name=bucket_name)
            file_objects=[file_object for file_object in bucket.objects.filter(Prefix=file_name)]
            func=lambda x: x[0] if len(x)==1 else x
            file_objs=func(file_objects)
            logger.info("Exited the get_file_object method of class SimpleStorageService")
            return file_objs
        
        except Exception as e:
            raise MyException(e,sys) from e
        
        
    def load_model(self,model_name:str,bucket_name:str,model_dir:str=None)->object:
        logger.info("Entered the load_model method of class SimpleStorageService")
        try:
            model_file=model_dir + "/" + model_name if model_dir else model_name
            file_object=self.get_file_object(model_file,bucket_name)
            model_obj=self.read_object(file_object,decode=False)
            model=pickle.loads(model_obj)
            logger.info("Exited the load_model method of class SimpleStorageService")
            return model
        except Exception as e:
            raise MyException(e,sys) from e
        
        
    def create_folder(self,folder_name:str,bucket_name:str)->None:
        logger.info("Entered create_folder method of class SimpleStorageService.")
        try:
            self.s3_resource.Object(bucket_name,folder_name)
            
        except Exception as e:
            if e.response["Error"]["Code"]=="404":
                folder_obj=folder_name + "/"
                self.s3_client.put_object(Bucket=bucket_name,Key=folder_obj)
            logger.info("Exited the create_folder method of class SimpleStorageService")
            
    def upload_file(self,from_file:str,to_file:str,bucket_name:str,remove:bool=True):
        logger.info("Entered upload_file method of Class SimpleStorageService")
        try:
            logger.info(f"Uploading file from path {from_file} to file{to_file} in bucket {bucket_name}")
            self.s3_resource.meta.client.upload_file(from_file,bucket_name,to_file)
            logger.info("Successfully uploaded file")
            
            if remove:
                os.remove(from_file)
                logger.info(f"File is removed from {from_file} and uploaded to {to_file}")
        except Exception as e:
            raise MyException(e,sys)

    def upload_df_as_csv(self,data_frame:DataFrame,local_file_name:str,bucket_file_name:str,bucket_name:str):
        logger.info("Entered to upload_df_as_csv method of class SimpleStorageServive.")
        try:
            data_frame.to_csv(local_file_name,index=None,header=True) 
            self.upload_file(local_file_name,bucket_file_name,bucket_name)   
            logger.info("Exited the method upload_df_as_csv of class SimpleStorageService")
            
        except Exception as e:
            raise MyException(e,sys) from e
    
    def get_df_from_object(self,object:object)->DataFrame:
        logger.info("Entered to get_df_from_object method of class SimpleStorageService.")
        try:
            content=self.read_object(object_name=object,make_redable=True)
            df=read_csv(content,na_values="na")
            logger.info("Exited the get_df_from_object method of class SimpleStorageService")
            
        except Exception as e:
            raise MyException(e,sys) from e
        
    def read_csv(self,file_name:str,bucket_name:str)->DataFrame:
        logger.info("Entered to method read_csv of class SimpleStorageSerivce.")
        try:
            csv_obj=self.get_file_object(file_name=file_name,bucket_name=bucket_name)
            df=self.get_df_from_object(csv_obj)
            logger.info("Exited read_csv method of class SimpleStorageService")
            return df
            
        except Exception as e:
            raise MyException(e,sys) from e
        
        
        
        
        
                