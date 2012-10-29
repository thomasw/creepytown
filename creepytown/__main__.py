from sets import index_all_set_photos
from photostream import index_all_photostream_photos
from downloadindex import DownloadIndex
from settings import USER_ID, OUT_DIR

print "Building download index...\n"

download_index = DownloadIndex(OUT_DIR)
index_all_set_photos(USER_ID, download_index)
print ""
index_all_photostream_photos(USER_ID, download_index)

print "\nIndexing complete.\n"

s = raw_input("Ready to save %s images to %s... Type 'yes' to continue: "
              % (len(download_index), download_index.out))

if s == "yes":
    download_index.download()
else:
    print "Okay. Sorry. Maybe next time?"

