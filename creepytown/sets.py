from dotdict import dotdict

from api import API
from photo import Photo
from util import normalize_json

def get_sets(user_id):
    """Retrieve a listing of the specified user's sets."""
    sets = normalize_json(API.photosets_getList(user_id=user_id))
    return dotdict(sets['photosets'])

def index_all_set_photos(user_id, index):
    """Add all photos in all sets to the specified DownloadIndex."""
    print "Finding photosets for user %s..." % user_id

    sets = get_sets(user_id)

    # TODO: We need to add pagination support for large lists of sets.
    assert int(sets.total) == len(sets.photoset), "This user has too many photosets. Aborting."

    print "%s photosets found." % sets.total

    for idx, item in enumerate(sets.photoset, start=1):
        item = dotdict(item)

        print "\n%s. %s (ID: %s)\n" % (idx, item.title['_content'], item.id)

        index_set_photos(item, index)

def index_set_photos(photoset, index):
    """Add all photos in photoset to the specified DownloadIndex."""
    photos = normalize_json(API.photosets_getPhotos(photoset_id=photoset.id))
    photos = dotdict(photos['photoset'])

    # TODO: We need to add pagination support for big sets.
    assert int(photos.total) == len(photos.photo), "This user has set with too many photos."

    print "Indexing the %s photos in this set:\n" % photos.total

    for idx, photo in enumerate(photos.photo, 1):
        photo = Photo(photo)

        print "%s. %s" % (idx, photo.details)

        index.add_to_index(photo, photoset)