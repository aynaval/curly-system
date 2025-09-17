from utils.logger import logger
from services.sql_query_generation_service import SQLQueryGenerationService
from services.token_check_service import CheckTokenCount


from utils.logger import logger
from services.sql_query_generation_service import SQLQueryGenerationService
from services.sqlite_service import SQLiteDBService  # Updated import
from services.token_check_service import CheckTokenCount


class ServiceFactory:
    def __init__(self):
        logger.info("Service Factory Initializing")

        self.watsonx = SQLQueryGenerationService()
        self.sqlite = SQLiteDBService()  # Updated to use SQLite
        self.encoding = CheckTokenCount()

        logger.info("All Services Initialized")


    def generate_sql_query(self, query_text):
        """
        Generate SQL query for the user query.
        """
        sql_query = self.watsonx.generate_sql_query(query_text)
        return sql_query
    

    def query_db(self, sql_query):
        """
        Fetch records from SQLite database.
        """
        data = self.sqlite.fetch_records(sql_query)
        return data
    
    def check_tokens(self, data):
        """
        Check token count in the data.
        """
        data = self.encoding.check_tokens(data)
        return data

    def summarize_data(self, user_query, data):
        """
        Generate summary of the fetched data based on user query.
        """
        summary = self.watsonx.generate_summary(user_query, data)
        return summary
