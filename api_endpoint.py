from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from function_retrieval import FunctionRetrieval
from code_generator import CodeGenerator

app = FastAPI()
function_retriever = FunctionRetrieval()
code_generator = CodeGenerator()

class ExecutionRequest(BaseModel):
    prompt: str

@app.post("/execute")
async def execute_function(request: ExecutionRequest):
    try:
        #Retrieve the most relevant function
        function_metadata = function_retriever.retrieve_function(request.prompt)

        #Generate the execution script
        execution_script = code_generator.generate_execution_script(function_metadata['name'])

        return {
            "function": function_metadata['name'],
            "code": execution_script
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))