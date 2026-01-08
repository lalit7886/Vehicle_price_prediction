import sys
from src.exception import MyException
from src.logger import logger
from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.entity.config_entity import (DataIngestionConfig,DataValidationConfig,DataTransformationConfig,
                                      ModelTrainerConfig)
from src.entity.artifact_entity import (DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact,
                                        ModelTrainerArtifact)

class TrainPipeline:
    def __init__(self):
        self.data_ingestion_config=DataIngestionConfig()
        self.data_validation_config=DataValidationConfig()
        self.data_transformation_config=DataTransformationConfig()
        self.model_trainer_config=ModelTrainerConfig()
        
        
        
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
        
    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact)->DataValidationArtifact:
        logger.info("Enterd the start data validation method of training pipline")
        try:
            data_validation=DataValidation(data_ingestion_artifact=data_ingestion_artifact,
                                           data_validation_config=self.data_validation_config)
            data_validation_artifact=data_validation.initiate_data_validation()
            
            logger.info("Performed data validation operation")
            logger.info("Exited the start_data_validation method of training pipeline")
            return data_validation_artifact
        
        except Exception as e:
            raise MyException(e,sys) from e
    
    def start_data_transformation(self,data_ingestion_artifact:DataIngestionArtifact,data_validation_artifact:DataValidationArtifact)->DataTransformationArtifact:
        logger.info("Enterd the start_data_transformation method of Trainpipeline class")
        try:
            data_transformation=DataTransformation(data_ingestion_artifact=data_ingestion_artifact,
                                                   data_transformation_config=self.data_transformation_config,
                                                   data_validation_artifact=data_validation_artifact)
            data_transformation_artifact=data_transformation.intiate_data_transformation()
            
            logger.info("Performed data transformation")
            logger.info("exited data start_data_transformation method of training pipeline")
            return data_transformation_artifact
        
        except Exception as e:
            raise MyException(e,sys) from e
        
    def start_model_trainer(self, data_transformation_artifact: DataTransformationArtifact) -> ModelTrainerArtifact:
        """
        This method of TrainPipeline class is responsible for starting model training
        """
        try:
            model_trainer = ModelTrainer(data_transformation_artifact=data_transformation_artifact,
                                         model_trainer_config=self.model_trainer_config
                                         )
            model_trainer_artifact = model_trainer.initiate_model_training()
            return model_trainer_artifact

        except Exception as e:
            raise MyException(e, sys)

        
            
            
            
    def run_pipeline(self)->None:
        try:
            data_ingestion_artifact=self.start_data_ingestion()
            data_validation_artifact=self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact=self.start_data_transformation(data_ingestion_artifact=data_ingestion_artifact,data_validation_artifact=data_validation_artifact)
            model_trainer_artifact=self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)
            
        except Exception as e:
            raise MyException(e,sys)