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
import getopt # Parse CLI Args
import re # Regular Expressions
from CrunchyCSV import CrunchyCSV

def main (argv):
    ''' This program has 3 distinct stages. 
    1. Request a set of urls from the user and store them
    2. Parse and formulate the compiled Livestreamer command
    3. Return the string to the user
    '''
    urls = 'x'
    # parse command line options
    try:
        opts, args = getopt.getopt(argv, "hu:", ["help","url="])
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
    # process arguments
    for arg in args:
        process(arg) # process() is defined elsewhere
    

    crunchyCSV = CrunchyCSV('./DataFiles/animeData.csv')
    print crunchyCSV
    #userProvidedURLs = getURLsFromUser()
    #parsedList = parseURLs (userProvidedURLs)
    #completeLivestreamerCommand = generateMultipleLivestreamerCommandLine(parsedList)

    #print completeLivestreamerCommand
    done = raw_input()


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




if __name__ == "__main__":
    main(sys.argv[1:])
