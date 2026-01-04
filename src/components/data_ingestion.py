import os
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact
from src.exception import MyException
from src.logger import logger
from src.data_access.proj1_data import proj1Data


class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig=DataIngestionConfig()):
        try:
            self.data_ingestion_config=data_ingestion_config
            
        except Exception as e:
            raise MyException(e,sys)
        
    def export_data_into_feature_store(self)->pd.DataFrame:
        try:
            logger.info(f"Exporting data from MongoDB")
            my_data=proj1Data()
            dataframe=my_data.export_collection_as_dataframe(collection_name=self.data_ingestion_config.collection_name)
            logger.info(f"Shape of dataframe from mongoDB is: {dataframe.shape}")
            
            feature_store_file_path=self.data_ingestion_config.feature_store_file_path
            dir_path=os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            logger.info(f"Saving Exported data into file path {feature_store_file_path}")
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            return dataframe
        except Exception as e:
            raise MyException(e,sys)
        
    def split_data_as_train_test(self,dataframe:pd.DataFrame)->None:
        logger.info("Entered to split data as train test")
        
        try:
            train_set,test_set=train_test_split(dataframe,test_size=self.data_ingestion_config.train_test_split_ratio)
            logger.info("Perfromed train test split on dataframe")
            
            dir_path=os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path,exist_ok=True)
            
            logger.info(f"Exporting train and test file path")
            train_set.to_csv(self.data_ingestion_config.training_file_path,index=False,header=True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path,index=False,header=True)
            logger.info("Exported file to respective file path")
            
        except Exception as e:
            raise MyException(e,sys) from e
        
    def initiate_data_ingestion(self)->DataIngestionArtifact:
        try:
            dataframe=self.export_data_into_feature_store()
            logger.info("Got the dataframe from MongoDB ")
            
            self.split_data_as_train_test(dataframe)
            logger.info("Perfromed train test split on dataset ")
            
            data_ingestion_artifacts=DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,test_file_path=self.data_ingestion_config.testing_file_path)
            logger.info(f"Data ingestion Artifacts: {data_ingestion_artifacts}")
            return data_ingestion_artifacts
        
        except Exception as e:
            raise Exception(e,sys) from e
            