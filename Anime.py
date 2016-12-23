from crunchyroll import crunchyParser

class Anime(object):
    
    def __init__(self, anime_url, sub_url, season):
        self.anime_url = anime_url
        self.sub_url = sub_url
        self.season = season
        self.parse_url()
        
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