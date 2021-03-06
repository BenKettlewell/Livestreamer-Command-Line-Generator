''' Parses crunchyroll URLs and provides a string command line argument to 
download them.
Utilizing youtube-dl to split sub and video files but livestreamer functionality
can be added with minimal effort

-h, --help      Output this help document
-u, --url       Provide a single url
-f, --file      Provide location of csv file 
                File format (do not include headers)
                crunchyroll_url,subtitle_url,season#
                #subtitle_url not implemented yet
-c,             Use cookie file located at $COOKIES instead of password auth
--cookie-auth
'''

from urlparse import urlparse
import sys # Command Line Arguments
import getopt # Parse CLI Args
import re # Regular Expressions
from CrunchyCSV import CrunchyCSV
from Anime import Anime
from crunchyroll import outputer
from shell import downloader

def main (argv):
    ''' This program has 3 distinct stages. 
    1. Request a set of urls from the user and store them
    2. Parse and formulate the compiled Livestreamer command
    3. Return the string to the user
    '''
    urls = ''
    file_csv = ''
    auth_method = 'password'
    # parse command line options
    try:
        opts, args = getopt.getopt(argv, "hu:f:c", ["help","url=","file=","cookie-auth"])
    except getopt.error, msg:
        print msg
        print "for help use --help"
        sys.exit(2)
    # process options
    for o, a in opts:
        if o in ("-h", "--help"):
            print __doc__
            sys.exit(1)
        if o in ("-u", "--url"):
            urls = a
            print'urls are :', a
        if o in ("-f", "--file"):
            file_csv = a
            print'csv_file :', a
        if o in ("-c","--cookie-auth"):
            auth_method = 'cookies'
            print'using cookies'

    # process arguments
    for arg in args:
        process(arg) # process() is defined elsewhere

    if file_csv != '':
        crunchyCSV = CrunchyCSV(file_csv)
        print outputer.youtube_dl_string_for_CrunchyCSV(crunchyCSV, auth_method)
        print outputer.list_of_anime_filenames(crunchyCSV)
    else:
        anime = Anime(urls, '', '')
	print outputer.youtube_dl_string_for_Anime(anime, auth_method)

print downloader.sub_call()
if __name__ == "__main__":
    main(sys.argv[1:])
