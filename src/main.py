# src/main.py
# src/main.py
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import threading
import os

app = FastAPI(title="Danelfin API Explorer")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def start_streamlit():
    streamlit_path = os.path.join(os.path.dirname(__file__), "streamlit_app.py")
    subprocess.run(["streamlit", "run", streamlit_path], check=True)


@app.on_event("startup")
async def startup_event():
    # Start Streamlit in a separate thread
    threading.Thread(target=start_streamlit, daemon=True).start()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
