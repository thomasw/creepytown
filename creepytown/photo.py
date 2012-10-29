import os

from dotdict import dotdict
import requests

from api import API
from util import normalize_json, slugify

from settings import SKIP_EXISTING

class Photo(object):
    """A Flickr Photo.

    This object can be instantiated with any dictionary reprsenting a Flickr
    photo that contains both a title and an id."""
    def __init__(self, photo):
        self._photo = dotdict(photo)

    def __unicode__(self):
        print self._photo

    def __getattr__(self, attr):
        try:
            return getattr(self._photo, attr)
        except:
            raise AttributeError()

    @property
    def photo_slug(self):
        """A slug describing the photo that is safe for filenames."""
        return "%s" % slugify(self.title or self.id)

    @property
    def details(self):
        "A human readable description of the photo."
        return "%s (id:%s)" % (self.title or self.id, self.id)

    @property
    def size_data(self):
        "Data about this photo from the getSizes endpoint."
        try:
            return self._sizes
        except AttributeError:
            sizes = normalize_json(API.photos_getSizes(photo_id=self.id))
            self._sizes = dotdict(sizes['sizes'])

        return self._sizes

    @property
    def largest(self):
        "Size data for the largest photo available for this image."
        size = 0
        biggest = None

        for x in self.size_data.size:
            x = dotdict(x)
            pixel_count = int(x.height) * int(x.width)
            if pixel_count >= size:
                biggest = x
                size = pixel_count

        # Save the file extension to the size object
        biggest.ext = biggest.source.partition('?')[0].rpartition('.')[2]
        if len(biggest.ext) > 5:
            biggest.ext = "unk"

        return biggest

    @property
    def smallest(self):
        "Size data for the smallest photo available for this image."
        size = 0
        smallest = None

        for x in self.size_data.size:
            x = dotdict(x)
            pixel_count = int(x.height) * int(x.width)
            if pixel_count < size or size == 0:
                smallest = x
                size = pixel_count

        # Save the file extension to the size object
        smallest.ext = smallest.source.partition('?')[0].rpartition('.')[2]
        if len(smallest.ext) > 5:
            smallest.ext = "unk"

        return smallest

    def save(self, outdir, prefix=""):
        """Saves photo to outdir and prefix the filename with prefix."""
        # Make the output directory if it doesn't already exist.
        if not os.path.exists(outdir):
            os.makedirs(outdir)

        out = os.path.join(outdir, "%s_%s.%s" % (prefix, self.photo_slug,
            self.largest.ext))

        if not SKIP_EXISTING or (SKIP_EXISTING and not os.path.exists(out)):
            print "Downloading %s to %s..." % (self.largest.source, out)

            request = requests.get(self.largest.source)
            with open(out, 'w') as f:
                f.write(request.content)
        else:
            print "Downloading %s to %s... SKIPPING FILE ALREADY EXISTS" % (self.largest.source, out)
