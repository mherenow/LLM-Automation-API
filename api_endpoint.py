from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ValidationError
import traceback
import re
from function_retrieval import FunctionRetrieval
from code_generator import CodeGenerator

app = FastAPI()
function_retriever = FunctionRetrieval()
code_generator = CodeGenerator()

class ExecutionRequest(BaseModel):
    prompt: str

def extract_command_from_prompt(prompt: str):
    # Try to extract the command from the prompt
    command_match = re.search(r"run\s*command\s*['\"](.+)['\"]", prompt, re.IGNORECASE)
    if command_match:
        return command_match.group(1)
    return None

@app.post("/execute")
async def execute_function(request: ExecutionRequest):
    try:
        # Log the incoming prompt for debugging
        print(f"Received prompt: {request.prompt}")
        
        # Retrieve the most relevant function
        function_metadata = function_retriever.retrieve_function(request.prompt)
        print(f"Retrieved function metadata: {function_metadata}")

        # For shell command, extract the actual command
        if function_metadata['name'] == 'run_shell_command':
            extracted_command = extract_command_from_prompt(request.prompt)
            if not extracted_command:
                raise ValueError("No command found in the prompt")
            
            # Generate the execution script with the extracted command
            execution_script = code_generator.generate_execution_script(
                function_metadata['name'], 
                additional_args=[extracted_command]
            )
        else:
            # Generate standard execution script
            execution_script = code_generator.generate_execution_script(function_metadata['name'])
        
        print(f"Generated execution script for: {function_metadata['name']}")

        # Execute the script
        execution_result = code_generator.execute_script(execution_script)

        return {
            "function": function_metadata['name'],
            "code": execution_script,
            "execution_result": execution_result
        }
    except ValidationError as ve:
        # Handle Pydantic validation errors
        print(f"Validation Error: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # Catch-all for any other unexpected errors
        print(f"Unexpected Error: {e}")
        print(traceback.format_exc())
        raise HTTPException(status_code=400, detail=f"Unexpected error: {str(e)}")