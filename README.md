# Real-Time Task Progress Tracking with FastAPI and SSE

This project demonstrates real-time task progress tracking using Server-Sent Events (SSE) with a FastAPI backend and multiple client implementations. It showcases how to implement real-time progress updates without WebSocket complexity.

## Project Overview

The project consists of a FastAPI server that simulates long-running tasks and streams progress updates to clients using SSE. It includes three different Python client implementations to demonstrate how to connect to and consume these SSE streams.

## Features

- **FastAPI Backend**: A robust and high-performance backend built with FastAPI.
- **Server-Sent Events (SSE)**: Real-time progress updates streamed from the server to clients.
- **Multiple Client Implementations**:
    - Asynchronous client using `aiohttp` (`client.py`).
    - Asynchronous client demonstrating monitoring of multiple concurrent tasks (`multiple_task.py`).
    - Synchronous client using `requests` and `sseclient-py` (`sse_client.py`).
- **Task Management**: Simple in-memory task management to track progress.

## File Structure

- **`app.py`**: The FastAPI application. It handles starting tasks and streaming progress updates via SSE.
- **`client.py`**: An asynchronous client that starts a single task and monitors its progress using `aiohttp`.
- **`multiple_task.py`**: An asynchronous client that demonstrates starting and monitoring multiple tasks concurrently using `aiohttp` and `asyncio.gather`.
- **`sse_client.py`**: A synchronous client that uses the `requests` library and `sseclient-py` to connect to the SSE stream and monitor task progress.
- **`requirements.txt`**: A list of Python dependencies required to run the project.
- **`README.md`**: This file.

## Getting Started

### Prerequisites

- Python 3.7+
- `pip` (Python package installer)

### Installation

1.  **Clone the repository (if applicable) or download the files.**
2.  **Navigate to the project directory:**
    ```bash
    cd path/to/Progress_tracking
    ```
3.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```
4.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

1.  **Start the FastAPI Server:**
    Open a terminal and run:
    ```bash
    python app.py
    ```
    Alternatively, you can use Uvicorn for more production-like features (e.g., auto-reload):
    ```bash
    uvicorn app:app --reload
    ```
    The server will start on `http://localhost:8000`.

2.  **Run a Client:**
    Open a new terminal (while the server is running) and choose one of the client scripts to run:

    *   **To run the single asynchronous client (`client.py`):**
        ```bash
        python client.py
        ```

    *   **To run the multiple tasks asynchronous client (`multiple_task.py`):**
        ```bash
        python multiple_task.py
        ```

    *   **To run the synchronous SSE client (`sse_client.py`):**
        ```bash
        python sse_client.py
        ```

    Each client will start a task (or multiple tasks) on the server and print real-time progress updates to the console.

## How It Works

1.  **Starting a Task**:
    - Clients send a POST request to the `/start-task` endpoint on the FastAPI server.
    - The server generates a unique `task_id` and initializes the task's progress.

2.  **Monitoring Progress**:
    - Clients connect to the `/task-progress/{task_id}` SSE endpoint.
    - The server uses `EventSourceResponse` from `sse-starlette` to stream progress updates.
    - The `progress_generator` in `app.py` simulates work being done by incrementally updating the task's progress and status, yielding JSON-formatted SSE messages.
    - Clients receive these messages and display the progress and status in real-time.
    - Once a task reaches 100% progress, the stream for that task ends, and the server cleans up the task data.

## Key Components

### `app.py` (FastAPI Server)
-   **`/start-task` (POST)**: Endpoint to initiate a new task. Returns a `task_id`.
-   **`/task-progress/{task_id}` (GET)**: SSE endpoint that streams progress updates for a given `task_id`.
-   **`progress_generator(task_id)`**: An asynchronous generator function that simulates task execution and yields progress updates.
-   **CORS Middleware**: Enabled to allow requests from any origin (configurable for production).

### Client Scripts
-   **`client.py`**: Uses `aiohttp` for asynchronous HTTP requests. It starts one task and monitors it.
-   **`multiple_task.py`**: Also uses `aiohttp`. It demonstrates starting several tasks and using `asyncio.gather` to monitor them concurrently.
-   **`sse_client.py`**: Uses the synchronous `requests` library along with `sseclient-py` for handling SSE events.

This project provides a clear example of implementing real-time updates with FastAPI and SSE, suitable for scenarios where WebSocket might be an overkill.
