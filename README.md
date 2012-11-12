# Creepytown

Creepytown is a Flickr account archival utility. Given a user ID, it'll download the user's public sets and photos and save them into appropriately named folders. It will then download any images in the photostream that weren't already downloaded into set folders.

## How to:

Make sure you have Python 2.6 and pip installed, then do the following:

1. Clone the repo.
2. CD into the directory that was created.
3. Run `pip install -r requirements.txt`
4. Configure `creepytown/settings.py` in the repo. You'll need to create an app via Flickr's App Garden to get a key and secret. You can use http://idgettr.com/ to lookup a user's Flickr ID by the url to their photostream.
5. Run `python creepytown`.