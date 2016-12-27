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

    def generate_youtube_dl(self):
        """
        youtube-dl -u $u_name \
        -o Haikyu_S03_E06_The_Chemical_Change_of_Encounters --write-sub \ 
        --sub-lang enUS --sub-format ass \
        http://www.crunchyroll.com/haikyu/episode-6-the-chemical-change-of-encounters-721869
        """
        return """/usr/bin/python3 /usr/local/bin/youtube-dl -u $CRUNCHY_UNAME \
-p $CRUNCHY_PASS -o %s.mp4 --write-sub --sub-lang enUS --sub-format ass %s""" \
        % (self.file_name, self.anime_url) 
        
