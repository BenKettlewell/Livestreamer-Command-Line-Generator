import csv
from Anime import Anime

class CrunchyCSV(object):
    ''' Reads a CSV file and builds a list of Anime objects populated with
    data from, or derived from, the file
    CSV format: crunchyroll_anime_url, subtitle_url, season_number
    '''
    def __init__(self, file_path=''):
        self.file_path = file_path
        self.list = []
        self._parse_CSV()
        
    def __repr__(self):
        string = ''
        i = 0
        for anime in self.list:
            string += "Item #%s\n" % (i)
            string += anime.__repr__()
            i += 1
        return string
            
    def _parse_CSV(self):
        with open(self.file_path, 'rb') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                self.list.append(Anime(row[0], row[1], row[2]))
