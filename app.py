from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse
import asyncio
import uuid
import random
import json

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store for active tasks
tasks = {}

@app.post("/start-task")
async def start_task():
    """Start a new task and return its ID"""
    task_id = str(uuid.uuid4())
    tasks[task_id] = {
        "progress": 0,
        "status": "initialized"
    }
    return {"task_id": task_id}

async def progress_generator(task_id):
    """Generator that yields task progress"""
    try:
        progress = 0
        while progress < 100:
            # Simulate task work
            await asyncio.sleep(1)  # Simulate work being done

            # Update progress
            progress += random.randint(5, 15)
            progress = min(progress, 100)

            # Update status message based on progress
            if progress < 30:
                status = "Processing initial phase..."
            elif progress < 60:
                status = "Performing main calculations..."
            elif progress < 90:
                status = "Finalizing results..."
            else:
                status = "Completing task..."

            if progress == 100:
                status = "Task completed!"

            # Store current progress
            tasks[task_id] = {
                "progress": progress,
                "status": status
            }

            # Yield event data in the correct SSE format
            yield {
                "event": "message",
                "data": json.dumps({
                    "progress": progress,
                    "status": status
                })
            }

    except Exception as e:
        yield {
            "event": "message",
            "data": json.dumps({
                "progress": -1,
                "status": f"Error: {str(e)}"
            })
        }
    finally:
        # Cleanup task data after completion
        if task_id in tasks:
            del tasks[task_id]

@app.get("/task-progress/{task_id}")
async def task_progress(task_id: str):
    """SSE endpoint for task progress updates"""
    if task_id not in tasks:
        return Response(
            content="Task not found",
            status_code=404
        )

    return EventSourceResponse(
        progress_generator(task_id)
    )

@app.get("/")
async def root():
    """Basic endpoint to verify API is running"""
    return {"message": "Task Progress API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)