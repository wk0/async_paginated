# Aysnc Paginated

Mostly useful when the number of pages for an endpoint is not provided due to questionable API design, though can be used for more explicitly paginated endpoints (but likely suboptimal).

Fairly bad case is one of the last items having an outsized number of pages.

- TODO: Modify api-specific details like auth token lifecycle, endpoints in /lib/ApiClient.py
- TODO: Adjust rate-limit and batch size in main.py
- TODO: Adjust how to determine if there is a next page in batch_fetch_paginated_items


## Run
```
pipenv install
pipenv run start
```
