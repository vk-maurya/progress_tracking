import json
import asyncio
import aiohttp
from datetime import datetime

async def start_task():
    async with aiohttp.ClientSession() as session:
        async with session.post('http://localhost:8000/start-task') as response:
            task_data = await response.json()
            return task_data['task_id']

async def monitor_task(task_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'http://localhost:8000/task-progress/{task_id}') as response:
            print(f"[Task {task_id[:8]}] Starting to monitor progress...")

            async for line in response.content:
                line = line.decode('utf-8')

                if line.startswith('data: '):
                    data = json.loads(line[6:])
                    progress = data['progress']
                    status = data['status']

                    timestamp = datetime.now().strftime('%H:%M:%S')
                    print(f"[{timestamp}] Task {task_id[:8]}: {progress}% - {status}")

                    if progress == 100:
                        print(f"[Task {task_id[:8]}] Completed!")
                        break

async def main():
    try:
        # Start multiple tasks
        num_tasks = 3
        task_ids = []

        print("Starting multiple tasks...")
        for _ in range(num_tasks):
            task_id = await start_task()
            task_ids.append(task_id)

        # Monitor all tasks concurrently
        monitoring_tasks = [monitor_task(task_id) for task_id in task_ids]
        await asyncio.gather(*monitoring_tasks)

        print("\nAll tasks completed!")

    except KeyboardInterrupt:
        print("\nMonitoring stopped by user")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())