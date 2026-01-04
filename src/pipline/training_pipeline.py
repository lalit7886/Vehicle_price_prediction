import sys
from src.exception import MyException
from src.logger import logger
from src.components.data_ingestion import DataIngestion
from src.entity.config_entity import (DataIngestionConfig)
from src.entity.artifact_entity import (DataIngestionArtifact)

class TrainPipeline:
    def __init__(self):
        self.data_ingestion_config=DataIngestionConfig()
        
        
    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            logger.info("Entered th start data ingestion method of training pipeline.")
            logger.info("Getting data from mongoDB")
            
            data_ingestion=DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
            
            logger.info("Go train test data")
            logger.info("Exited start data ingestion")
            
            return data_ingestion_artifact
        except Exception as e:
            raise MyException(e,sys) from e
            
            
    def run_pipeline(self)->None:
        try:
            data_ingestion_artifact=self.start_data_ingestion()
            
        except Exception as e:
            raise MyException(e,sys)