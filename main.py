import asyncio

from lib.utils.batch import gather_in_chunks, batch_caller
from lib.ApiClient import AsyncAPIClient


async def batch_fetch_items(
    api, item_ids: list, batch_size: int = 10, sleeptime: float = 2.0
):
    # create coroutines
    functions_to_call = [api.endpoint(item_id) for item_id in item_ids]

    # batch calls functions
    all_results = await batch_caller(
        functions_to_call=functions_to_call,
        batch_size=batch_size,
        sleeptime=sleeptime,  # hacky rate limiting
    )

    return all_results


async def batch_fetch_paginated_items(
    api, item_ids: list, batch_size: int = 10, sleeptime: float = 2.0
):
    """Useful for paginated items when each item has unknown number of pages"""
    functions_to_call = [api.paginated_endpoint(item_id) for item_id in item_ids]
    all_results = []

    while len(functions_to_call) > 0:
        # logger.info(f"Items left to fetch: {len(functions_to_call)}")

        # create next batch, then delete those being called
        if len(functions_to_call) > batch_size:
            to_call_next = functions_to_call[:batch_size]
            del functions_to_call[:batch_size]

            # actually call the endpoint
            results = await gather_in_chunks(
                to_call_next, sleeptime=sleeptime
            )  # max_together=10,)
            all_results.extend(results)

            # check if page, if page then add those functions to the queue
            for page_data in results:
                # TODO: boolean for determining if next page is present
                next_page = page_data.get("next_page_indicator", None)
                if next_page:
                    functions_to_call.append(
                        api.paginated_endpoint(
                            page_data["item_id"],
                            page=page_data["page"]
                            + 1,  # example api has current page in data
                        )
                    )
        # less than full batch remaining
        else:
            to_call_next = functions_to_call[:]
            functions_to_call = []

            # run last group (could have children, eg. one with very large # of pages )
            results = await gather_in_chunks(to_call_next, sleeptime=sleeptime)
            all_results.extend(results)

            # then call and check
            for page_data in results:
                # TODO: boolean for determining if next page is present
                next_page = page_data.get("next_page_indicator", None)
                if next_page:
                    functions_to_call.append(
                        api.paginated_endpoint(
                            page_data["item_id"],
                            page=page_data["page"]
                            + 1,  # example api has current page in data
                        )
                    )

    return all_results


async def main():
    api = AsyncAPIClient()
    api.get_initial_auth_token()
    item_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    await batch_fetch_items(api, item_ids, batch_size=5, sleeptime=1)
    await batch_fetch_paginated_items(api, item_ids)
    await api.close()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
