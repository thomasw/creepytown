import flickrapi

from settings import FLICKR_KEY, FLICKR_SECRET

API = flickrapi.FlickrAPI(FLICKR_KEY, FLICKR_SECRET, format='json')