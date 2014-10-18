

from __future__ import unicode_literals
from urllib import urlopen
import re
import os.path
import time


INPUT_FOLDER = "OutputHTML"
OUT_FOLDER_PATH = "OutputSongFiles"

inforegex = r'<A href="(http.*?mp3)">(.*?) ::: (.*?)</A>'


def read_download_write( fname ):
    finput = os.path.join( INPUT_FOLDER, fname )
    data = []

    with open( finput, "Urb" ) as thefile:
        for line in thefile:
            data_match = re.match( inforegex, unicode(line, encoding="CP1251") )

            if data_match:
                data.append( data_match.groups() )

    print "Finished reading data, now will start to download."
    print "Total to download: {} items.".format( len(data) )
    count = 0
    errors = 0

    for info in data:
        url, artist, name = info
        fname = (artist + " " + name + ".mp3").strip()
        fpath = os.path.join( OUT_FOLDER_PATH, fname )
        count += 1

        t1 = time.time()
        try:
            req = urlopen( url )
            song_stream = req.read()
        except IOError:
            t3 = time.time()
            print "*"*40, "Got Error while downloading {}/{}: {} ::: {}; This download has been going for {} seconds or {} minutes".format( count, len(data)-count, artist, name, t3-t1, (t3-t1)/60.0 )
            errors += 1
            continue

        t2 = time.time()


        print "Finished download {}/{}: {} ::: {} in {} seconds or {} minutes".format( count, len(data)-count, artist, name, t2-t1, (t2-t1)/60.0 )

        with open( fpath, "wb" ) as thefile:
            thefile.write( song_stream )

    print "\n\n\nTOTAL NUMBER OF ERRORS: {} \n\n\n".format( errors )


if __name__ == "__main__":
    info = """

    Use this to download a bunch of songs using an analysed vk.com source file.
    It will prompt you for a file to read from, enter the full name with
    extension. This file should be in the OutputHTML folder. Filenames
    can not start and/or end with spaces.

    Here is a list of files:
    """
    print info
    for f in os.listdir( INPUT_FOLDER ):
        print f

    fname = raw_input( "Choose one: " )
    read_download_write( fname.split() )
