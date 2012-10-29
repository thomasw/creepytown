import json
import re
import unicodedata

from dotdict import dotdict

def slugify(title):
    """Generate a filename safe version of a string that is still readable."""
    slug = unicodedata.normalize('NFKD', title)
    slug = slug.encode('ascii', 'ignore').lower()
    slug = re.sub(r'[^a-z0-9]+', '-', slug).strip('-')
    slug = re.sub(r'[-]+', '-', slug)

    return slug

def normalize_json(json_string):
    """Convert JSON output from the flickrapi into a dictionary."""
    return json.loads(json_string.lstrip('jsonFlickrApi(').rstrip(')'))

class Paginator(object):
    """An iterator for parsing pages of Flickr photostream results."""
    def __init__(self, method, **args):
        self.method = method
        self.page = 1
        self.pages = None
        self.args = args

    def __iter__(self):
        return self

    def __get_pages(self, output):
        output = normalize_json(output)
        output = dotdict(output['photos'])
        return output.pages

    def next(self):
        if self.pages == None:
            out = self.method(**self.args)
            self.pages = self.__get_pages(out)
        elif self.page <= self.pages:
            # Add page to the args array.
            args = dict(self.args)
            args['page'] = self.page

            out = self.method(**args)
        else:
            raise StopIteration

        self.page += 1
        return out