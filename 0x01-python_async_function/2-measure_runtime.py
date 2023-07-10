#!/usr/bin/env python3
""" Measure the runtime """

import asyncio
import time
wait_n = __import__('1-concurrent_coroutines').wait_n

def measure_time(n, max_delay):
    start_time = time.time()
    delays = wait_n(n, max_delay)
    total_time = time.time() - start_time
    average_time = total_time / n
    return average_time