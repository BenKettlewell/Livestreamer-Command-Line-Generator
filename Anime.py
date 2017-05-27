from crunchyroll import crunchyParser

class Anime(object):
    
    def __init__(self, anime_url, sub_url, season):
        self.anime_url = anime_url
        self.sub_url = sub_url
        self.season = '' if season == '' else 'S'+season+'_'
        self.parse_url()
        self.file_name = self.showName.title() +'_'+ self.season +'E'+ \
                          self.episodeNumber +'_'+ self.episodeTitle.title() 
        
    def __repr__(self):
        return \
        """\tShow        : %s
        Episode     : %s 
        Ep #        : %s
        CrunchID    : %s
        Anime_url   : %s
        Sub_url     : %s 
        Season#     : %s\n""" % \
        (self.showName, self.episodeTitle, self.episodeNumber, self.crunchyID, \
        self.anime_url, self.sub_url, self.season)
        
    def parse_url(self):
        dict = crunchyParser.parse_URL(self.anime_url)
        self.showName       = dict['showName']
        self.episodeTitle   = dict['episodeTitle']
        self.episodeNumber  = dict['episodeNumber']
        self.crunchyID      = dict['crunchyID']

    def generate_youtube_dl(self, auth_method='password'):
        ''' Returns string for youtube-dl command
        Downloads subtitle file as .ass with video as .mp4 highest quality
        '''
        auth_string = ''
	platform = 'acer'
        if (auth_method == "cookies"):
            auth_string = "--cookies $COOKIES"
        else:
            auth_string = "-u $CRUNCHY_UNAME -p $CRUNCHY_PASS"
        if (platform == 'acer'):
		return """python /usr/bin/youtube-dl %s -f best \
%s -o %s.mp4 --write-sub --sub-lang enUS --sub-format ass \
--max-downloads 1""" \
        	% (self.anime_url, auth_string, self.file_name, )
	else:
		return """/usr/bin/python3 /usr/local/bin/youtube-dl %s \
-o %s.mp4 --write-sub --sub-lang enUS --sub-format ass %s""" \
        	% (auth_string, self.file_name, self.anime_url)

        
    def generateLivestreamerCommand(self):
        ''' Returns string for livestreamer command
        
        '''
        return "livestreamer -o %s.mp4 %s best" % (self.file_name, self.anime_url)
