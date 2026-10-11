
# Project 2 Author:
#Maha Jornaz

#Last updated - 10/10/26

#Additions: Installed packages

import subprocess
import time
import webbrowser

output = subprocess.run(
    ["python3", "-m", "pip", "show", "pydantic", "fastapi", "uvicorn"],   #Maha installed extra packages as the file didn't work while running
    capture_output=True,
    text=True
)

versions = subprocess.run(
    ["grep", "-i", "version"],
    input=output.stdout,
    capture_output=True,
    text=True
)

count = 0
for line in versions.stdout.splitlines():
    count+=1

if count < 3:
    subprocess.run(["python3", "-m", "pip", "install", "-r", "requirements.txt"])   #Maha installed more packages here as well

server = subprocess.Popen([
    "python3",
    "-m",
    "uvicorn",
    "main:app",
    "--reload"
])

time.sleep(2)

webbrowser.open("http://localhost:8000/")

try:
    server.wait()
except KeyboardInterrupt:
    print("\nShutting down...")
    server.terminate()
    server.wait()
