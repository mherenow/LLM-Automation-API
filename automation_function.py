import os
import webbrowser
import psutil
import subprocess

class AutomationFunction:
    @staticmethod
    def open_browser():
        # Open the default web browser
        webbrowser.open("https://www.google.com")

    @staticmethod
    def open_calculator():
        # Open the calculator
        if os.name == "nt": #Windows
            os.system("calc")
        elif os.name == "posix": #Linux/macOS
            os.system("gnome-calculator")

    @staticmethod
    def get_system_info():
        #Get system resource usage information
        return {
            "cpu_usage": psutil.cpu_percent(),
            "memory_usage": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage("/").percent
        }
    
    @staticmethod
    def run_shell_command(command):
        #Execute a shell command
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
        except Exception as e:
            return {"error": str(e)}