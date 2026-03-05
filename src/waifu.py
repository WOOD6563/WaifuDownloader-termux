import requests


class WaifuDownloaderAPI:

    def __init__(self):
        self.base_url = "https://api.waifu.im/images"
        self.info = None

    def get_page(self, nsfw=False):
        # choose endpoint
        url = self.base_url
        if nsfw:
            url += "?IsNsfw=All"

        try:
            r = requests.get(url, timeout=10)
            if r.status_code != 200:
                print("API returned:", r.status_code)
                return None
            return r.json()

        except Exception as e:
            print("Failed to reach API:", e)
            return None

    def get_page_url(self, data):
        if not data:
            return None

        self.info = data

        items = data.get("items")
        if not items:
            print("API response missing items:", data)
            return None

        return items[0].get("url")

    def get_neko(self, nsfw=False):
        data = self.get_page(nsfw)
        return self.get_page_url(data)

    def get_image(self, url):
        if not url:
            return None

        try:
            r = requests.get(url, timeout=20)
            if r.status_code == 200:
                return r.content
            else:
                print("Image download failed:", r.status_code)
                return None

        except Exception as e:
            print("Error downloading image:", e)
            return None
