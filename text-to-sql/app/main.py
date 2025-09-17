from utils.config_loader import config
from utils.logger import logger
from services import services_factory
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import StreamingResponse


# Initialize FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
    allow_methods=["*"],
)

security = HTTPBasic()

def verification(creds: HTTPBasicCredentials = Depends(security)):
    username = creds.username
    password = creds.password

    if username in config['users'] and password == config['users'][username]['password']:
        logger.info("User access is validated.")
        return True
    else:
        # From FastAPI
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
            headers={"WWW-Authenticate": "Basic"},
        )

factory = services_factory.ServiceFactory()

# Route to Query DB
@app.get("/query")
def query(query_text: str):
        #   Verification = Depends(verification)):
    
    # if Verification:
    sql_query = factory.generate_sql_query(query_text)
    data = factory.query_db(sql_query)
    data = factory.check_tokens(data)

    return StreamingResponse(factory.summarize_data(sql_query,data),
                                media_type="text/event-stream")