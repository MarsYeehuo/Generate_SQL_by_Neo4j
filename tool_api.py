from fastapi import FastAPI, Request
from pydantic import BaseModel
from hybrid_retriever import HybridRetriever
from llm_sql_generator import generate_sql_from_question

'''
Use the command:
uvicorn tool_api:app --host 0.0.0.0 --port 8081
to run the api tool and open the port.'''

app = FastAPI()
retriever = HybridRetriever()


class SQLRequest(BaseModel):
    question: str


@app.post("/generate_sql")
async def generate_sql(req: SQLRequest):
    q = req.question
    units = retriever.find_units(q)
    sql = generate_sql_from_question(q)
    return {"sql": sql, "units": units}
