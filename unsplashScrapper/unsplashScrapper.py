from unsplash.api import Api
from unsplash.auth import Auth
from pprint import pprint


class UnsplashScrapper:
    def __init__(self, keyword):
        client_id = "e1f37996871427d8a491cda804e65e9fde2e1ae55c7e6996a34bb1216ea25471"
        client_secret = "810ea5b466bd7b5cd6a93103cf71430e38ca423e000b00b2446d857b2547875a"
        redirect_uri = "urn:ietf:wg:oauth:2.0:oob"
        auth = Auth(client_id, client_secret, redirect_uri)
        self.api = Api(auth)
        self.photos_urls = self.get_photos_urls_by_keyword(keyword)
    
    def get_photos_urls_by_keyword(self, keyword):
        photos_urls = []
        photos = self.api.search.photos(query = keyword, per_page=30)
        for photo in photos['results']:
            photos_urls.append(photo.urls.raw)
        return photos_urls
