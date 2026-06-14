# code related to reading the dataset from some dat source. That source can be created by big data team,cloud team or something
# read the data and split it to train,test
import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd

from sklearn.model_selection import train_test_split
from dataclasses import dataclass

# Whenever we are performing data ingestion,the input(where to probably save the train data,test data,raw data) will be creating in this class
# The @dataclass decorator in Python automates the creation of boilerplate code like __init__(), __repr__(), and __eq__() for classes that primarily store data. It is useful if we just want to initialize variable names like train_test_path,test,raw etc. If we have to initailiz functions also, then use standard init() etc
@dataclass
class DataIngestionConfig:
    #All the outputs of train_data will be in this file(train.csv) in this path and same for test,raw
    train_data_path: str=os.path.join('artifacts',"train.csv")
    test_data_path: str=os.path.join('artifacts',"test.csv")
    raw_data_path: str=os.path.join('artifacts',"data.csv")

class DataIngestion:
    def __init__(self):
        # All 3 paths in DataIngestionConfig class will get saved in self.ingestion_config variable
        self.ingestion_config=DataIngestionConfig()
    # this will read code from database
    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion or component")
        try:
            df=pd.read_csv('notebook\data\stud.csv')
            logging.info('Read the dataset as dataframe')
            # Making the folder for artifacts to store train,test,raw data
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)
            # wrt raw data path also 
            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)

            logging.info("Train test split initiated")
            train_set,test_set=train_test_split(df,test_size=0.2,random_state=42)
            # Train dataset
            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            # Test dataset
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)
            
            logging.info("Ingestion of data is completed")
            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
        except Exception as e:
            raise CustomException(e,sys)
        
if __name__=="__main__":
    obj=DataIngestion()
    obj.initiate_data_ingestion()
