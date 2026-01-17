from configurator import Configurator
import requests

IMAGES_URL = "https://api.unsplash.com"


class API:
    def __init__(self):
        self.configurator = Configurator()
        self.__api_key = self.configurator.get("api_key")

    def get_wallpaper(self):
        return self.__get_wallpaper()

    def __get_wallpaper(self, query_params=None) -> bytes | None:
        if not self.__api_key:
            return None

        headers = {
            "Authorization": f"Client-ID {self.__api_key}"
        }

        query_params_string = ""
        if query_params:
            query_params_string = "&".join(f"{key}={value}" for key, value in query_params.items())

        response = requests.get(f"{IMAGES_URL}/photos/random{query_params_string}", headers=headers,
                                params={"orientation": "landscape"})
        if response.status_code != 200:
            return None

        data = response.json()
        image_url = data.get("urls", {}).get("regular")
        if not image_url:
            return None
        image_response = requests.get(image_url)
        if image_response.status_code != 200:
            return None

        return image_response.content
