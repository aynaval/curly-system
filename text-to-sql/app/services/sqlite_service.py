from utils.config_loader import config
from sqlalchemy import create_engine,text
from tqdm import tqdm
from utils.logger import logger
from sqlalchemy.orm import sessionmaker

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from tqdm import tqdm
from utils.logger import logger

class SQLiteDBService:
    def __init__(self):
        # Path to your SQLite DB
        db_path = "data/resilinc.db"
        
        # SQLite connection
        self.db_client = create_engine(f'sqlite:///{db_path}', echo=False)
        self.chunk_size = 1000  # Define a reasonable chunk size

        logger.info("SQLite DB Service Initialized")
        
    def fetch_records(self, query, params=None):
        """
        Execute a query and return results as a list of dictionaries.
        """
        logger.info("Fetching Records for Query")

        engine = self.db_client
        Session = sessionmaker(bind=engine)
        session = Session()

        try:
            with engine.connect() as connection:
                if params:
                    result = connection.execute(text(query), params)
                else:
                    result = connection.execute(text(query))
                    
                fetched_data = result.fetchall()
                data_as_dict = [dict(zip(result.keys(), row)) for row in fetched_data]
                return data_as_dict

        except Exception as e:
            logger.error(f"Error executing query {query} due to {e}", exc_info=True)

        finally:
            session.close()
