import json
import requests
from sseclient import SSEClient

def start_task():
    # Start a new task
    response = requests.post('http://localhost:8000/start-task')
    task_data = response.json()
    return task_data['task_id']

def monitor_progress(task_id):
    # Connect to SSE endpoint
    url = f'http://localhost:8000/task-progress/{task_id}'

    print("Starting to monitor progress...")
    try:
        # Create SSE client
        response = requests.get(url, stream=True)
        client = SSEClient(response)

        # Iterate over events using client.events()
        for event in client.events():
            # Parse the JSON data
            data = json.loads(event.data)
            progress = data['progress']
            status = data['status']

            # Print progress
            print(f"Progress: {progress}% - Status: {status}")

            # Break if task is complete
            if progress == 100:
                print("Task completed!")
                break

    except KeyboardInterrupt:
        print("\nMonitoring stopped by user")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    # Start a new task
    task_id = start_task()
    print(f"Started task with ID: {task_id}")

    # Monitor the task progress
    monitor_progress(task_id)

if __name__ == "__main__":
    main()