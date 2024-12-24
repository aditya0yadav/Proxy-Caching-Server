from fastapi import FastAPI
import time
from cache import cache_manager

class WeatherAPI:
    def __init__(self):
        self.register_routes(FastAPI())

    def register_routes(self, app: FastAPI):
        app.add_api_route("/weather/{city}", self.get_weather, methods=["GET"])
        app.add_api_route("/weather/uncached/{city}", self.get_uncached_weather, methods=["GET"])
        app.add_api_route("/test-cache-performance/{city}", self.test_cache_performance, methods=["GET"])
        return app

    def fetch_weather(self, city: str) -> dict:
        return {
            "city": city,
            "temperature": "22°C",
            "condition": "Clear"
        }

    @cache_manager.cached(ttl=120)
    async def get_weather(self, city: str):
        print(self.fetch_weather(city))
        return self.fetch_weather(city)

    async def get_uncached_weather(self, city: str):
        return self.fetch_weather(city)

    async def test_cache_performance(self, city: str):
        start_cached = time.time()
        await self.get_weather(city)
        cached_time = time.time() - start_cached
        
        start_uncached = time.time()
        await self.get_uncached_weather(city)
        uncached_time = time.time() - start_uncached
        
        time_saved = max(uncached_time - cached_time, 0)
        percentage_saved = (time_saved / uncached_time * 100) if uncached_time else 0
        
        return {
            "cached_time": f"{cached_time:.4f} seconds",
            "uncached_time": f"{uncached_time:.4f} seconds",
            "time_saved": f"{time_saved:.4f} seconds",
            "percentage_saved": f"{percentage_saved:.2f}%"
        }

app = FastAPI()

weather_api = WeatherAPI()
app = weather_api.register_routes(app)