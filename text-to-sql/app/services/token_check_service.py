from utils.logger import logger
from utils.enums import Tokens
import tiktoken

class CheckTokenCount():
    def __init__(self) -> None:
        self.encoding = tiktoken.get_encoding('cl100k_base')

    def check_tokens(self, data):
        num_tokens = len(self.encoding.encode(str(data)))

        logger.info("Number of Tokens in Data: %s", num_tokens)

        if num_tokens > Tokens.MAX_TOKENS.value:
            data = self.reduce_token_count(data)

        return data


    def reduce_token_count(self, data):
        logger.info("Reducing Token Count")

        tokens = self.encoding.encode(str(data))

        truncated_tokens = tokens[:Tokens.MAX_TOKENS.value]
        data = self.encoding.decode(truncated_tokens)

        return data
