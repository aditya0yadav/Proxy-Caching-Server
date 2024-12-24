import uvicorn
from fastapi import FastAPI, Request
import threading

app = FastAPI()

@app.get("/")
def read_root(request: Request):
    query_param = request.query_params.get("name", "Guest")
    return {
        "message": "Welcome to the latest version of our API!",
        "secure": "What is your security processor? Let me help you with that.",
        "query_param": query_param,
        "status": "success"
    }

def run_app_on_port(port: int):
    uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    # Run FastAPI server on ports from 7000 to 7100
    threads = []
    for port in range(7000, 7101):
        thread = threading.Thread(target=run_app_on_port, args=(port,))
        threads.append(thread)
        thread.start()
    print(threads)
    # Join threads so the program waits for all servers to finish
    for thread in threads:
        thread.join()
