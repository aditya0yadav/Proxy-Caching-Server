import time
from typing import Any
from cache import CacheManager
from cache import CacheStorage


# Function to simulate fetching data with a delay (e.g., from an external API)
def fetch_data_from_api():
    print("Fetching data from API...")
    time.sleep(2)  # Simulate network delay
    return "Data from API"


def test_cache():
    cache = CacheStorage(ttl=5)  # Cache TTL of 5 seconds

    # First request (data will be fetched from API)
    start_time = time.time()
    data = cache.get("data_key")
    if data is None:
        data = fetch_data_from_api()
        cache.set("data_key", data)
    print(f"First request: {data} (Took {time.time() - start_time:.2f} seconds)")

    # Second request (data will be fetched from cache)
    time.sleep(1)  # Wait for 1 second before the next request
    start_time = time.time()
    data = cache.get("data_key")
    if data is None:
        data = fetch_data_from_api()
        cache.set("data_key", data)
    print(f"Second request: {data} (Took {time.time() - start_time:.2f} seconds)")

    # Third request (cache expired, data will be fetched from API again)
    time.sleep(5)  # Wait for 5 seconds to let the cache expire
    start_time = time.time()
    data = cache.get("data_key")
    if data is None:
        data = fetch_data_from_api()
        cache.set("data_key", data)
    print(f"Third request: {data} (Took {time.time() - start_time:.2f} seconds)")


if __name__ == "__main__":
    test_cache()
