#!/usr/bin/env python3
""" Tasks """

import asyncio
task_wait_random = __import__('3-tasks').Task_wait_random

async def task_wait_n(n, max_delay):
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