
import os
from dotenv import find_dotenv, load_dotenv
from requests import session
import logging

#payload dictionary for logging into kaggle
payload = {

    'action': 'login',

    'username': os.environ.get("KAGGLE_USERNAME"),

    'password': os.environ.get("KAGGLE_PASSWORD")

}

def extract_data(url, file_path):
    with session() as c:
        c.post('https://www.kaggle.com/account/login', data = payload)
        with open(file_path, 'wb') as handle_1:
            response = c.get(url, stream= True)
            for block in response.iter_content(1024):
                handle_1.write(block)
                

def main(project_dir):
    #get logger for logging messages as code is executed. create an instance of logger before using it
    logger = logging.getLogger(__name__)
    logger.info('getting raw data')
    
    #urls
    #train_url = 'https://www.kaggle.com/c/titanic/download/train.csv'
    #test_url = 'https://www.kaggle.com/c/titanic/download/test.csv'
    train_url = 'https://www.kaggle.com/c/titanic/data/train.csv'
    test_url = 'https://www.kaggle.com/c/titanic/data/test.csv'

    #specify paths to store train and test file, under /data/raw
    raw_data_path = os.path.join(os.path.pardir, 'data', 'raw')
    train_data_path = os.path.join(raw_data_path, 'train.csv')
    test_data_path = os.path.join(raw_data_path, 'test.csv')
    
    #extract data
    extract_data(train_url, train_data_path)
    extract_data(test_url, test_data_path)
    logger.info('getting training and test data')

 
if __name__ == '__main__':
    #get the root directory Sharmistha_titanic_python by travelling two levels up 
    project_dir = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
    
    #setup logger
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt) 
    
    #walk up directories to find the environment variables..load them
    dotenv_path = find_dotenv()
    print(dotenv_path)
    load_dotenv(dotenv_path)
    
    main(project_dir)