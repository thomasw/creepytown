from dotdict import dotdict

from api import API
from photo import Photo
from util import normalize_json, Paginator

def index_all_photostream_photos(user_id, index):
    """Add the user's photostream photos to the specified DownloadIndex"""
    print "Inspecting photostream of user %s..." % user_id

    count = 1

    for output in Paginator(API.people_getPublicPhotos, user_id=user_id):
        stream = normalize_json(output)
        stream = dotdict(stream['photos'])

        print "\nIndexing page %s of %s:\n" % (stream.page, stream.pages)

        total = stream.total

        for photo in stream.photo:
            photo = Photo(photo)

            print "%s. %s" % (count, photo.details)

            index.add_to_index(photo)
            
            count += 1

    print "\n%s photostream photos found." % total