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

OUTPUT_FOLDER_PATH = "Output"
INPUT_FOLDER_PATH = "Pages Source Code"



vk_music_url_grep_search = r"""[ ]*<input type="hidden" id="audio_.*?" value="(.*?),[1-9]{3}" """
vk_music_info_grep_search1 = r"""[ ]*<div class="title_wrap fl_l" .*?<a href=".*return false">(.*?)</a>.*<span class="title">[ ]*<a.*?>(.*?)</a>[ ]*</span>.*"""
vk_music_info_grep_search2 = r"""[ ]*<div class="title_wrap fl_l" .*?<a href=".*return false">(.*?)</a>.*<span class="title">(.*?)</span>.*"""




class ReaderWriter(object):
    def __init__(self, input_fname, output_fname):
        self.input_fpath = os.path.join( INPUT_FOLDER_PATH, input_fname)
        self.output_fpath = os.path.join( OUTPUT_FOLDER_PATH, output_fname + ".txt" )
        self.result = []

        #open( self.output_fpath, "w").write( "\n" )


    def analyse_file(self):
        with open( self.input_fpath, "r" ) as the_file:
            url_string_buffer = None
            time_to_write = False

            count = 0
            for line in the_file:
                count += 1
                url_match = re.search(vk_music_url_grep_search, line )
                if url_match:
                    print "matched URL"
                    print repr(url_match)
                    print count

                    # get the
                    url_string_buffer = url_match.group(1)[:]       # use "print url.match.groups()" to see all matched parts
                    print url_match.groups()
                    print url_string_buffer

                    # after finding the url, we start looking for the song's name and artist, but since they are never in the same line, we just skip analysing the rest of the line.
                    continue


                song_info_match1 = re.search(vk_music_info_grep_search1, line)
                song_info_match2 = re.search(vk_music_info_grep_search2, line)

                if song_info_match1:         # time to dump info, because we have all the puzzle pieces
                    song_artist = song_info_match1.group(1)
                    song_name = song_info_match1.group(2)
                    time_to_write = True

                elif song_info_match2:
                    song_artist = song_info_match2.group(1)
                    song_name = song_info_match2.group(2)
                    time_to_write = True


                if time_to_write == True:
                    time_to_write = False
                    print
                    print repr( song_artist )
                    print
                    print "___"+song_artist+"___", "____"+song_name+"____"
                    print

                    with open( self.output_fpath, "a") as out:
                        out.write( song_artist + "\r" )
                        out.write( song_name + "\r" )
                        out.write( url_string_buffer + 3*"\r")

                    continue



if __name__=="__main__":
    count = 0

    info = """

    This program is used to extract links to audio files form www.vk.com
    Save the Source Code (shortcut: cmd U with Mac Firefox)
    to the folder "Pages Source Code". You can save more than one at once.
    The output will be located in the "Output" folder.
    You will have to name the files one by one. (Default extension is ".txt")

    """



    for file_name in os.listdir( INPUT_FOLDER_PATH ):
        if "." == file_name[0]: continue

        output_fname = raw_input("Now working with file called   {0}   how shall I name the output file?: ".format( file_name ) )
        r = ReaderWriter( file_name,  output_fname )
        r.analyse_file()

    print
    print "Have finished processing all the files in the input folder. All Looks Good."
    print
