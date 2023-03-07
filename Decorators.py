import time
import asyncio
from functools import wraps

def get_time(func):
    """Times any function"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        if asyncio.iscoroutinefunction(func):
            await func(*args, *kwargs)
        else:
            func(*args, *kwargs)
        end_time = time.perf_counter()
        total_time = round(end_time - start_time, 2)
        print('Time', total_time, 'seconds')

    return wrapper

def get_args(func):
    """Get args of any function"""

    @wraps(func)
    async def wrapper(*args, **kwargs):
        if asyncio.iscoroutinefunction(func):
            await func(*args, *kwargs)
        else:
            func(*args, *kwargs)
        print(func.__name__, args, kwargs)

    return wrapper

