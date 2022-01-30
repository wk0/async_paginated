import asyncio
from typing import Coroutine, List


async def gather_in_chunks(fcn_list, sleeptime: float):  # max_together: int=None):
    results = await asyncio.gather(*fcn_list)
    # for rate limit!
    await asyncio.sleep(sleeptime)
    return results


async def batch_caller(
    functions_to_call: List[Coroutine],
    batch_size: int = 10,
    sleeptime: float = 1.5,
) -> list:
    """
    Batch caller utilizes gather_in_chunks to accumulate results
    from the async calls, while respecting the rate limit with batch_size
    and sleeptime
    -> Input is a list of awaitable functions (coroutines)
    -> Then returns all of the data in a results list
    """
    all_results = []
    while len(functions_to_call) > 0:
        # logger.info(f"{function_log_str}: {len(functions_to_call)}")
        if len(functions_to_call) > batch_size:
            to_call_next = functions_to_call[:batch_size]
            del functions_to_call[:batch_size]
            results = await gather_in_chunks(to_call_next, sleeptime=sleeptime)
            all_results.extend(results)
        else:
            to_call_next = functions_to_call[:]
            functions_to_call = []
            results = await gather_in_chunks(to_call_next, sleeptime=sleeptime)
            all_results.extend(results)

    return all_results
