#!/usr/bin/env python3
""" Take the code from wait_n and alter 
    it into a new function task_wait_n.  
"""

import asyncio
from typing import List
task_wait_random = __import__('3-tasks').task_wait_random

async def task_wait_n(n: int, max_delay: int) -> List[float]:
    delays = []
    tasks = []

    for i in range(n):
        task = task_wait_random(max_delay)
        tasks.append(task)

    for task in tasks:
        delay = await task
        delays.append(delay)

    delays.sort()

    return delays
