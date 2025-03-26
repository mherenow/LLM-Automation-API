import inspect
from automation_function import AutomationFunction

class CodeGenerator:
    @staticmethod
    def generate_execution_script(function_name: str):
        #Generate executable script for the function
        function_map = {
            name: func for name, func in inspect.getmembers(AutomationFunction, predicate=inspect.isfunction)
        }

        if function_name not in function_map:
            raise ValueError(f"Function '{function_name}' not found")
        
        script = f"""

from automation_function import AutomationFunction

def main():
    try:
        result = AutomationFunction.{function_name}()
        print(f"Function '{function_name}' executed successfully")
        print(f"Result: {{result}}")
    except Exception as e:
        print(f"Error executing function: {{e}}")

if __name__ == "__main__":
    main()
"""
        return script