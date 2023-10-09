import requests
import json

class WaifuDownloaderAPI:
	def __init__(self):
		self.endpoint = "https://api.waifu.im/search?is_nsfw="
	def get_page(self, nsfw = False):
		try:
			r = requests.get(self.endpoint + str(nsfw).lower(), timeout=10)
			if r.status_code == 200:
				return r.text
			else:
				return None
		except Exception as e:
			print(e)
			return None

	def get_page_url(self, response):
		data = json.loads(response)
		self.info = data
		return data["images"][0]['url']

	def get_neko(self, nsfw=False):
		return self.get_page_url(self.get_page(nsfw))

	def get_image(self, url):
		r = requests.get(url, timeout=20)
		return r.content
