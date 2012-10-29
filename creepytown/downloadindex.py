import os

from util import slugify

class DownloadIndex(list):
    def __init__(self, outdir, *args, **kwargs):
        self.out = outdir
        self.__photoset_counts = {}

        return super(list, self).__init__(*args, **kwargs)

    def add_to_index(self, photo, photoset=None):
        """Add image/photoset pair to index if the image hasn't been added."""
        if self.search_index(photo.id) == False:
            self.append((photo, photoset))
            return True

        return False

    def search_index(self, photo_id):
        """Search the index for the specified photo_id.

        Returns: the index or False if not found."""
        for idx, x in enumerate(self):
            if x[0].id == photo_id:
                return idx

        return False

    def download(self):
        """Download all images in the index."""
        for image, photoset in self:
            subdir = "__photostream"
            subdir = slugify(photoset.title['_content']) if photoset != None else subdir
            out_path = os.path.join(self.out, subdir)

            current_set_count = self.__photoset_counts.get(subdir, 0)
            self.__photoset_counts[subdir] = current_set_count + 1
            prefix = "%.4d" % self.__photoset_counts[subdir]

            image.save(outdir=out_path, prefix=prefix)
