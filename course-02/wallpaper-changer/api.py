from configurator import Configurator, get_config_path
import requests
import os
from datetime import datetime

IMAGES_URL = "https://api.unsplash.com"


class API:
    def __init__(self):
        self.configurator = Configurator()
        self.__api_key = self.configurator.get("api_key")

    def get_wallpaper(self) -> str | None:
        image = self.__get_wallpaper(query_params={"orientation": "landscape"})
        if not image:
            return None

        previous_image_path = self.configurator.get("downloaded_wallpaper")
        if previous_image_path and os.path.exists(previous_image_path):
            os.remove(previous_image_path)

        config_path = get_config_path()
        image_path = f"{config_path}/wallpaper_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        self.configurator.set("downloaded_wallpaper", image_path)
        with open(image_path, "wb") as f:
            f.write(image)
        return image_path

    def get_api_key(self) -> str | None:
        return self.__api_key

    def set_api_key(self, api_key: str) -> None:
        self.__api_key = api_key
        self.configurator.set("api_key", api_key)

    def __get_wallpaper(self, query_params=None) -> bytes | None:
        if query_params is None:
            query_params = {}

        if not self.__api_key:
            print("API key is not set.")
            return None

        headers = {
            "Authorization": f"Client-ID {self.__api_key}"
        }

        query_params_string = ""
        if query_params:
            query_params_string = "&".join(f"{key}={value}" for key, value in query_params.items())

        url = f"{IMAGES_URL}/photos/random?{query_params_string}"
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            return None

        data = response.json()
        image_url = data.get("urls", {}).get("full")
        if not image_url:
            print("Image URL not found in the response.")
            return None
        image_response = requests.get(image_url)
        if image_response.status_code != 200:
            print("Failed to download the image.")
            return None

        return image_response.content
