import inspect
import os
import sys
import subprocess

class CodeGenerator:
    @staticmethod
    def generate_execution_script(function_name: str, additional_args=None):
        # Get the absolute path to the project directory
        project_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Prepare the function call with additional arguments
        if additional_args:
            args_str = ', '.join(repr(arg) for arg in additional_args)
            function_call = f"AutomationFunction.{function_name}({args_str})"
        else:
            function_call = f"AutomationFunction.{function_name}()"
        
        script = f"""
import sys
import os

# Add the project directory to Python path
project_dir = r"{project_dir}"
sys.path.insert(0, project_dir)

from automation_function import AutomationFunction

def main():
    try:
        result = {function_call}
        print(f"Function '{function_name}' executed successfully")
        print(f"Result: {{result}}")
        return 0
    except Exception as e:
        print(f"Error executing function: {{e}}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
"""
        return script

    @staticmethod
    def execute_script(script_content: str):
        """
        Execute the generated script
        """
        try:
            # Write the script to a temporary file
            import tempfile

            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.py') as temp_script:
                temp_script.write(script_content)
                temp_script_path = temp_script.name

            # Execute the script
            result = subprocess.run([sys.executable, temp_script_path], 
                                    capture_output=True, 
                                    text=True)

            # Clean up the temporary script
            os.unlink(temp_script_path)

            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode
            }
        except Exception as e:
            return {
                "error": str(e),
                "return_code": 1
            }