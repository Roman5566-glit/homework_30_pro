import logging
import time
from typing import Any, Dict, Optional
import requests


logger = logging.getLogger("weather_integration")


def get_weather(city: str, api_key: str) -> Optional[Dict[str, Any]]:
    """Fetch current weather JSON payload from OpenWeatherMap API"""
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",
        "lang": "ua"
    }

    start_time = time.time()
    try:
        response = requests.get(url, params=params, timeout=10)
        execution_time = time.time() - start_time

        if response.status_code == 200:
            logger.info(
                "Success: Weather data fetched for city '%s' in %.2fs",
                city, execution_time
            )
            return response.json()

        logger.error(
            "Failed: API returned status %d for city '%s' in %.2fs. Info: %s",
            response.status_code, city, execution_time, response.text
        )
        return None

    except requests.RequestException as e:
        execution_time = time.time() - start_time
        logger.exception(
            "Exception: Network error for city '%s' after %.2fs: %s",
            city, execution_time, e
        )
        return None
    