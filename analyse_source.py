#!/usr/bin/env python2.6

"""
IMPORTANT!
If try to open the output file (with song names and url links) but see nonsense or gibberish which are
the same thing. Its because this program preserves the original
encoding of the song name. So try opening the output file using different
encodings. (TextWrangler can do this, internet browsers can do this (probably))
"""



from sys import exit
import os.path
import re
from pprint import pprint

import html_generator as htmlgen


OUTPUT_FOLDER_PATH = """OutputHTML"""
INPUT_FOLDER_PATH = """pages_source_code"""



vk_music_url_grep_search = """[ ]*<input type="hidden" id="audio_.*?" value="(.*?)\?.*?" """
vk_music_info_grep_search1 = r"""[ ]*<div class="title_wrap fl_l" .*?<a href=".*return false">(.*?)</a>.*<span class="title">[ ]*<a.*?>(.*?)</a>[ ]*</span>.*"""
vk_music_info_grep_search2 = r"""[ ]*<div class="title_wrap fl_l" .*?<a href=".*return false">(.*?)</a>.*<span class="title">(.*?)</span>.*"""

html_decode_pattern = r"&quot;|&amp;|&gt;|&lt;"



class ReaderWriter(object):
    def __init__(self, input_fname, output_fname):
        self.input_fpath = os.path.join( INPUT_FOLDER_PATH, input_fname)

        output_fname = output_fname + ".html" if ("." not in output_fname) else output_fname
        self.output_fpath = os.path.join( OUTPUT_FOLDER_PATH, output_fname )


    def grep_search(self, grep_list, data ):
        assert type(grep_list)==tuple, "You are feeding me a {0}, instead give me a tuple! ".format( type(grep_list) )

        for pattern in grep_list:
            match = re.search( pattern, data )
            if match:
                return match.groups()
        return None


    def _replace_html(self, matchobj):
        """ Function to replace all html specifics with local signs.
        See: http://www.w3.org/MarkUp/HTMLPlus/htmlplus_13.html """

        if matchobj.group(0) == "&quot;":
            return '"'
        elif matchobj.group(0) == "&amp;":
            return '&'
        elif matchobj.group(0) == "&lt;":
            return '<'
        elif matchobj.group(0) == "&gt;":
            return '>'


    def analyse_file(self):
        output_list = []

        with open( self.input_fpath, "r" ) as the_file:

            for line in the_file:
                url_match = re.match( vk_music_url_grep_search, line )

                if url_match:
                    print "matched URL"
                    print url_match
                    url = url_match.group(1)
                    # after finding the url, we start looking for the song's name and artist, but since they are never in the same line, so we can skip analysing the rest of this line.
                    continue


                info_match = self.grep_search( (vk_music_info_grep_search1, vk_music_info_grep_search2), line)

                # time to dump info, because we have all the puzzle pieces
                if info_match:
                    artist, name = info_match
                    url = url or "Not found"
                    artist = re.sub( html_decode_pattern,  self._replace_html, artist )
                    name = re.sub( html_decode_pattern,  self._replace_html, name )
                    output_list.append( (url, artist, name) )

                    pprint( output_list )
                    print
                    print "___"+artist+"___", "____"+name+"____"
                    print

        return output_list


    def write_output_file(self, all_songs_info ):
        htmlbody = htmlgen.BODY()

        for song_info_tuple in all_songs_info:
            url, artist, name = song_info_tuple
            text = "{} :::  {}".format( artist, name )
            htmlbody <= htmlgen.A(text, href=url) + htmlgen.BR() * 3

        htmldoc = htmlgen.HTML( htmlbody )
        htmlstring = htmldoc.__str__()


        with open( self.output_fpath, "w") as out:
            out.write( htmlstring  )





if __name__=="__main__":
    info = """

    This program is used to extract links to audio files form www.vk.com
    Save the Source Code (shortcut: cmd U with Mac Firefox)
    to the folder "Pages Source Code". You can save more than one at once.
    The output will be located in the "OutputHTML" folder.
    You will have to name the files one by one. (Default extension is ".html")
    Enter 's' or 'S' to skip a file.

    """

    print info

    for file_name in os.listdir( INPUT_FOLDER_PATH ):
        if "." == file_name[0]:
            continue

        output_fname = raw_input("Now working with file called   {0}   how shall I name the output file?: ".format( file_name ) )
        if output_fname.lower()=='s':
            continue

        r = ReaderWriter( file_name,  output_fname )
        data_list = r.analyse_file()
        r.write_output_file( data_list )

    print
    print "Have finished processing all the files in the input folder. All Looks Good."
    print
