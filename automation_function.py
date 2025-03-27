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
    def open_gmail():
        # Open Gmail in the default web browser
        webbrowser.open("https://mail.google.com")

    @staticmethod
    def get_system_info():
        #Get system resource usage information
        return {
            "cpu_usage": psutil.cpu_percent(),
            "memory_usage": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage("/").percent
        }

    @staticmethod
    def get_network_interfaces():
        """Get network interface information"""
        import psutil
        
        try:
            interfaces = psutil.net_if_addrs()
            return {
                name: [
                    {'family': addr.family, 'address': addr.address, 'netmask': addr.netmask}
                    for addr in addrs
                ]
                for name, addrs in interfaces.items()
            }
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def run_shell_command(command):
        #Extract command from the description if not provided
        if command is None:
            return {"error": "No command provided"}
        
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