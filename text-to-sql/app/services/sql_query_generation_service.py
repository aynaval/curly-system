from utils.config_loader import config
from utils.logger import logger
from langchain_ibm import WatsonxLLM
from langchain_core.prompts.prompt import PromptTemplate
from services.prompts import SQLITE_QUERY_GENERATION_PROMPT, DATA_SUMMARY_PROMPT

class SQLQueryGenerationService:
    def __init__(self) -> None:
        
        ai_config = config['watsonxai']

        parameters = {
            "decoding_method": "greedy",
            "max_new_tokens": 2048,
            "repetition_penalty": 1.1,
            'random_seed':42,
        }

        self.wx_client = self.create_watsonx_llm_client(ai_config,parameters)

    def create_watsonx_llm_client(self, ai_config, parameters):
        watsonx_llm = WatsonxLLM(
            model_id=ai_config['model_id'],
            url=ai_config['url'],
            apikey=ai_config['api_key'],
            project_id=ai_config['project_id'],
            params=parameters,
        )

        wx_client = watsonx_llm.with_retry(
            retry_if_exception_type = (Exception,),
            stop_after_attempt = 4,
            wait_exponential_jitter = False
        )

        logger.info("%s model initialised successfully.",ai_config['model_id'])
        
        return wx_client

    def generate_sql_query(self, user_query):
        logger.info("Generating SQL query - User query: %s",user_query)
                
        generate_sql_query_template = PromptTemplate(
            input_variables=["query"],
            template=SQLITE_QUERY_GENERATION_PROMPT
        )
        generate_sql_query_chain = generate_sql_query_template | self.wx_client

        sql_query=generate_sql_query_chain.invoke({"query":user_query})

        logger.info("Generated SQL query is : %s",sql_query)
        
        sql_query = sql_query.replace('`','')
        sql_query = sql_query.replace('sql','')
        
        return sql_query
    
    def generate_summary(self, user_query, data):
        logger.info("Generating Summary of Data")

        generate_summary_template = PromptTemplate(
            input_variables=["query","data"],
            template=DATA_SUMMARY_PROMPT
        )
        generate_summary_chain = generate_summary_template | self.wx_client

        summary = generate_summary_chain.stream({"query":user_query, "data":data})

        logger.info("Generated Summary for user query")
        
        return summary