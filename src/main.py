import subprocess
import os
import time

# Define paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FASTAPI_MODULE = "src.main:app"  # Adjusted to match new structure
STREAMLIT_SCRIPT = os.path.join(BASE_DIR, "src", "streamlit_app.py")


# Function to start FastAPI server
def start_fastapi():
    print("Starting FastAPI server...")
    return subprocess.Popen(
        ["uvicorn", FASTAPI_MODULE, "--reload"],
        cwd=BASE_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )


# Function to start Streamlit app
def start_streamlit():  # Note: This function was missing in the original code
    print("Starting Streamlit app...")
    return subprocess.Popen(
        ["streamlit", "run", STREAMLIT_SCRIPT],
        cwd=BASE_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )


if __name__ == "__main__":
    # Start FastAPI server
    fastapi_process = start_fastapi()

    # Wait for FastAPI to initialize
    time.sleep(2)

    # Start Streamlit app
    streamlit_process = start_streamlit()

    try:
        # Keep processes running
        fastapi_process.wait()
        streamlit_process.wait()
    except KeyboardInterrupt:
        print("\nShutting down servers...")
        fastapi_process.terminate()
        streamlit_process.terminate()
