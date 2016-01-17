''' This program receives www.crunchyroll.com episode urls and parses them to auto generate 
livestreamer command line arguments to download them to a file. It uses the information found in 
URL to autogenerate the appropriate name in the Format Anime_Name_EpisodeNumber_Episode title
It can receive one or more urls seperately or simultaneously as long as they are all seperated by 
a carriage return (enter).

-q, --quality  Specify the desired quality. Default is best # Not Implemented
-h, --help     Output this help document
    '''
from urlparse import urlparse
import sys # Command Line Arguments
import re # Regular Expressions
import getopt

#This Is a Banana
def main ():
    ''' This program has 3 distinct stages. 
    1. Request a set of urls from the user and store them
    2. Parse and formulate the compiled Livestreamer command
    3. Return the string to the user
    '''
    # parse command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
    except getopt.error, msg:
        print msg
        print "for help use --help"
        sys.exit(2)
    # process options
    for o, a in opts:
        if o in ("-h", "--help"):
            print __doc__
            sys.exit(1)
    # process arguments
    for arg in args:
        process(arg) # process() is defined elsewhere

    userProvidedURLs = getURLsFromUser()
    parsedList = parseURLs (userProvidedURLs)
    completeLivestreamerCommand = generateMultipleLivestreamerCommandLine(parsedList)

    print completeLivestreamerCommand

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
    episodeNumber = fixEpisodeNumber (numberSet.findall(modify)[0])
    return episodeNumber

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
    return modify

def upperAfterSpaceCharacter (modify):
    ''' Capitalize the start of each word and remove trailing characters.
    The beginning of a word is indicated by the very first letter found in a string, or 
    a letter proceeded by underscore, dash, space, or backslash ('_','-', ' ','/')
    Given:  food_wars_shokugeki_no_soma/episode_6_the_meat_invader_678171 
    Return: Food_Wars_Shokugeki_No_Soma/Episode_6_The_Meat_Invader_678171 
    '''
    spaceCharacters = ['-','_',' ','/']
        
    afterSpaceCharacter = False  # TRUE when spaceCharacter found. FALSE when character capitalized
    myList = list(modify) # Strings are immutable, therefore make a list of the characters so we can modify them

    for i in xrange (0, len(myList)):
        if afterSpaceCharacter == True or (i == 0 and myList[i] not in spaceCharacters):
            myList[i] = str.capitalize(myList[i])  
            afterSpaceCharacter = False
        if myList[i] in spaceCharacters:
            afterSpaceCharacter = True
    if myList[len(myList)-1] in spaceCharacters: # Remove a trailing _,-,/
        myList.pop(len(myList)-1)
    return "".join(myList)

def generateMultipleLivestreamerCommandLine(parsedListOfLists):
    ''' Iterates through a list of lists and compiles the command to download all urls sequentially
    Given:
        List
            URL #1: Component Parts
            URL #2: Component Parts
    Returns: 'complete command to download URL #1; complete line command for URL #2; etc...'
    '''

    completeCommand = ""
    index = 0
    for item in parsedListOfLists:
        nextCommand = generateLivestreamerCommand(parsedListOfLists[index])
        completeCommand = completeCommand + nextCommand
        index = index + 1
    return completeCommand

def generateLivestreamerCommand (parsedList):
    ''' Takes a list of relevant URL components and constructs the livestreamer command 
    Given:  [show, title, number, url]
    Return: livestreamer -o Anime_Name_##_Episode_Title url best;
    '''

    # Original URL: http://www.crunchyroll.com/food-wars-shokugeki-no-soma/episode-6-the-meat-invader-678171
    show   = parsedList [0] # Food_Wars_Shokugeki_No_Soma
    title  = parsedList [1] # _The_Meat_Invader
    number = parsedList [2] # 06
    url    = parsedList [3] # http://www.crunchyroll...6-the-meat-invader-678171

    # Finished Command: 'livestreamer -o Food_Wars_Shokugeki_No_Soma_06__The_Meat_Invader http://www.crunchyroll.com/food-wars-shokugeki-no-soma/episode-6-the-meat-invader-678171 best;'
    # ; tells command line to execute each livestreamer command sequentially
    return "livestreamer -o " + show + "_" + number + title + ".mp4 " + url + " best; "  

def generateDebugURLs ():
    ''' Return a list of 3 sample URLS
    '''
    return ['http://www.crunchyroll.com/engaged-to-the-unidentified/episode-1-its-important-to-start-off-on-the-right-foot-648831',
            'http://www.crunchyroll.com/baby-steps/episode-14-moonlight-and-the-sound-of-waves-678323',
            'http://www.crunchyroll.com/food-wars-shokugeki-no-soma/episode-6-the-meat-invader-678171']

def getURLsFromUser():
    ''' Accept and store raw URLS provided by the user then return all as a list
    '''
    prompt = """Please provide Crunchyroll URLS. 
    You may paste each url one at a time hitting Enter after each,
    or you may paste several URLs at once, each separated by an Enter
    When you have entered all the URLs you wish to process,
    press enter on a blank line or type 'Done' """
    print prompt

    listOfURLs = [] # Array of URLs to be filled with user provided URLS 
    seasonTag = ""
    while True:
        userInput = raw_input()
        if (userInput.lower() == "debug"): # DEBUG option for convenient testing
            listOfURLs.extend(generateDebugURLs())
            break
        elif (userInput.lower() == "done" or userInput == ""):  # Finished input
            break
        elif (userInput.lower().split()[0] in ("--season","-s")):  # Set the season tag for the next set of URLs
                                                                   # Toggle On / Off
            '''Determine what season they want the next set of urls or stop season mode etc.
            '''
            seasonTag = userInput.split()[1]
            if (seasonTag.lower() in ("off","stop","")):
                seasonTag = ""
            else:
                seasonTag = seasonTag + " "
        elif ("www.crunchyroll.com" not in userInput.lower()): # Initial validation that it is a Crunchyroll URL
            raise TypeError ("Input must be a crunchyroll url")
            break
        else:                                               # Add URL to the List
            userInput = seasonTag + userInput; # Season tag will be extracted in parseOneURL first
                                               # User provided seasonTag placed infront of the url followed with a -s marker
            listOfURLs.append(userInput)
    return listOfURLs

def parseOneURL(fullURL):
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
    seasonTag = ""
    if (" " in fullURL): # Indicates a "Seasong_Tag URL"
        seasonTag = "_" + fullURL.split()[0] # Store Season Tag
        fullURL = fullURL.split()[1] # Removes Season Tag
        fullURL = fullURL.strip() # Make sure no spaces were left behind

    URLParsedObject = urlparse(fullURL)
    URLPath = URLParsedObject.path
    '''urlparse returns an object seperated into its parts. For this we only care about the .path part
    Given: http://www.crunchyroll.com/food-wars-shokugeki-no-soma/episode-6-the-meat-invader-678171
    The .path will be 'food-wars-shokugeki-no-soma/episode-6-the-meat-invader-678171'
    '''
    # start food-wars-shokugeki-no-soma/episode-6-the-meat-invader-678171
    URLPath = swapOutDashesForUnderscores(URLPath)          # food_wars_shokugeki_no_soma/episode_6_the_meat_invader_678171
    wordGroups = findWordGroups(URLPath)                    # [food_wars_shokugeki_no_soma, eipsode, the_meat_invader]
    ShowName = upperAfterSpaceCharacter(wordGroups[0]) \
                                           + seasonTag      # _Food_Wars_Shokugeki_No_Soma_[SnTg]
    EpisodeTitle = upperAfterSpaceCharacter(wordGroups[2])  # The_Meat_Invader
    EpisodeNumber = findEpisodeNumber (URLPath)             # 06
    return [ShowName, EpisodeTitle, EpisodeNumber, fullURL]

def parseURLs (listOfURLs): 
    ''' Returns a List of Lists of URL components. For each item in the list, it will contain the
    information about the anime name, the episode number, the episode title, and the url to find it.
    All components will be formatted properly.
    '''
    i = 0
    for url in listOfURLs:
        listOfURLs[i] = parseOneURL(url) #extracted info
        i = i + 1
    return listOfURLs

if __name__ == "__main__":
    main()
