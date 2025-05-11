import json
import asyncio
import aiohttp

async def start_task():
    async with aiohttp.ClientSession() as session:
        async with session.post('http://localhost:8000/start-task') as response:
            task_data = await response.json()
            return task_data['task_id']

async def monitor_progress(task_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'http://localhost:8000/task-progress/{task_id}') as response:
            print("Starting to monitor progress...")

            # Read the SSE stream
            async for line in response.content:
                line = line.decode('utf-8')

                # SSE format: each message is separated by double newlines
                # and starts with "data: "
                if line.startswith('data: '):
                    # Parse the JSON data
                    data = json.loads(line[6:])  # Skip "data: " prefix
                    progress = data['progress']
                    status = data['status']

                    # Print progress
                    print(f"Progress: {progress}% - Status: {status}")

                    # Break if task is complete
                    if progress == 100:
                        print("Task completed!")
                        break

async def main():
    try:
        # Start a new task
        task_id = await start_task()
        print(f"Started task with ID: {task_id}")

        # Monitor the task progress
        await monitor_progress(task_id)

    except KeyboardInterrupt:
        print("\nMonitoring stopped by user")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())