#!/usr/bin/env python3
""" Execute multiple coroutines at the same time with async """

import asyncio
import random
wait_random = __import__('0-basic_async_syntax').wait_random

async def wait_n(n, max_delay):
    delays = []
    tasks = []

    for i in range(n):
        task = asyncio.create_task(wait_random(max_delay))
        tasks.append(task)

    for task in tasks:
        delay = await task
        delays.append(delay)

    delays.sort()

    return delays