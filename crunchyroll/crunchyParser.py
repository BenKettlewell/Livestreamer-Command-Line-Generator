from urlparse import urlparse    
import re # Regular Expressions


def swapOutDashesForUnderscores(modify):
    ''' Improve legibility by substituting all - for _
    Given: food-wars-shokugeki-no-soma/episode-6-the-meat-invader-678171
    Return: food_wars_shokugeki_no_soma/episode_6_the_meat_invader_678171 
    '''
    dashLetter = re.compile('-')
    return dashLetter.sub("_", modify)
    
def findWordGroups (modify):
    ''' Searches through the URL path to find groups of words.
    Groups consist of anything seperated by any number of underscores with 
    numbers and backslashes '/' indicating the end of a word group. 
    The first word group should be the Anime Name and the third the episode name
    Exceptions exist if the anime has a number in the name.
    '''
    # KNOWN ERROR - Anime Titles or episodes with numbers in the name
    wordSets = re.compile('[a-z_]+')
    return wordSets.findall(modify)
    
def findEpisodeNumber (modify):
    ''' Given a URL extract the episode number and return it in 2-digit form
    Given: food-wars-shokugeki-no-soma/episode-6-the-meat-invader-678171
    Return: 06
    '''
    numberSet = re.compile('[0-9]+')
    episodeNumber = fixEpisodeNumber(numberSet.findall(modify)[0])
    return episodeNumber.strip('_')

def findLastNumberSet (modify):
    ''' Given a URL return the last number set delimited by an underscore
    '''
    # underscore followed by all(*) numbers([0-9]) not greedy(?) from end($)
    # 01_episode_title_33_12345 => grabs only _12345
    lastNumberFormat = re.compile('_[0-9]*?$') 
    
    # finadall returns a list. join it to a string then strip off any '_'
    return ''.join(lastNumberFormat.findall(modify)).strip('_')
    
def fixEpisodeNumber (modify):
    ''' Change single digit episodeNumbers to 2-digit eipsode numbers.
    If an anime has 3-digit episodes the first 99 may appear below the 3-digit episodes
    but this will not truncate any information.
    Given:   9
    Return: 09

    Given:  100
    Return: 100
    '''
    if len(modify) < 2:
        return "0" + modify 
    return modify.strip('_')
    
def removeThisFromString (removeThis, fromThis):
    return fromThis.strip(str(removeThis)).strip('_')
    
def parse_URL(fullURL):
    ''' Given a single Crunchyroll.com url, it will extract and format the relevant information
    needed to properly name the file.
    Relevant info: [ShowName, EpisodeTitle, EpisodeNumber, fullURL]

    Format is:
        Anime_Name      - First letter of each word capitalized sperated by underscores
        EpisodeNum      - 2 digit number with a leading 0 if single digit (e.g. 02)
        EpisodeTitle    - Same as Anime Name 
        fullURL         - Left exactly as provided by user
    '''
    fullURL = fullURL.strip()

    URLParsedObject = urlparse(fullURL)
    URLPath = URLParsedObject.path
    '''urlparse returns an object seperated into its parts. For this we only care about the .path part
    Given: http://www.crunchyroll.com/food-wars-shokugeki-no-soma/episode-6-the-meat-invader-678171
    The .path will be 'food-wars-shokugeki-no-soma/episode-6-the-meat-invader-678171'
    '''
    
    # start food-wars-shokugeki-no-soma/episode-6-the-meat-invader-100-678171
    URLPath = swapOutDashesForUnderscores(URLPath) 
    # food_wars_shokugeki_no_soma/episode_6_the_meat_invader_100_678171
    
    crunchyID = findLastNumberSet(URLPath) # 678171
    URLPath = removeThisFromString(crunchyID, URLPath)
    # food_wars_shokugeki_no_soma/episode_6_the_meat_invader_100
    
    numberInShowTitle = findLastNumberSet(URLPath) #100
    URLPath = removeThisFromString(numberInShowTitle, URLPath)
    # food_wars_shokugeki_no_soma/episode_6_the_meat_invader
    numberInShowTitle = '_' + numberInShowTitle if numberInShowTitle else  ''
    
    wordGroups = findWordGroups(URLPath) # [food_wars_shokugeki_no_soma, episode, the_meat_invader]
    showName = wordGroups[0] # food_wars_shokugeki_no_soma
    episodeTitle = wordGroups[2].strip('_')  + numberInShowTitle  # the_meat_invader_100
    episodeNumber = findEpisodeNumber(URLPath) # 06
    return {
        'showName':showName,\
        'episodeTitle':episodeTitle,\
        'episodeNumber':episodeNumber,\
        'crunchyID':crunchyID
        }