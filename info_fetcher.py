''' Hand a comma separated list anime titles in format 'anime-name-separated-by-hyphens',...

    This program will go to 'crunchyroll.com/anime-name-separated-by-hyphens',
    check when the last update was, and scavenge through the html source to 
    determine when the next update is meant to be released.  

    If an update has occured, it will then check if it is currently available.
    If it is, an attempt to retrieve and store the url for the new update for 
    livestreamerCLG.

    If successful, return 'anime-name-separated-by-hyphens' and datetime.now()
    as timeLastUpdated to the showList to keep checking for updates on.

    Continue down the list until nothing is left.  Send the list of URLs to
    livestreamerCLG.

    Possible features to add eventually include:
        if TimeLastUpdated exceeds a certain amount of time, tell showList
        to remove this title.

        
    '''
from datetime import datetime
import urllib2

def main ():




'''plan of attack:
    
    Get handed 'anime-name-separated-by-hyphens', episodeNumber

    Create link crunchyroll.com/'anime-name-separated-by-hyphens'/, access its source.

    a link to the URL can always be found on the FIRST line that has 'Episode ##' on it, where ## is episodeNumber.  
    The link can be properly retrieved by creating createdLink + anime-name-separated-by-hyphens' + 'text until " '

    So if handed an episode number "11", turn it into 'Episode 11' and find the first line in HTML with 'Episode 11'.
    Then find everything after anime-name-separated-by-hyphens up until the ".  This will give us the URL to the page with the video on it,
    ready to be given to livestreamerCLG.
        Test if Python can 'click', because if it can, this link is 'clickable' and brings us to the correct page already.
        If we're looking for an episode that hasn't been released yet, the line after 'Episode ##' will have a 'no_image_beta_wide.jpg'
            Needs confirmation for consistency.  Possible that they add a non-default image but still don't have an episode airing.
            Try and find a show about an hour, 30 mins, and even 10 mins before it's released to confirm.  
                Picture HAD been changed only 30 mins after a show came out, but still unsure of if it changes beforehand.
        

    Calculating dates:
        Crunchyroll uses the format 'x day(s) from now' and 'Simulcast on dayName Timeam/pm PST'
        Use time from Simulcast on X, and X day(s) from now
            Calculate datetime.now() + X days.
            Set datetime's TIME to Simulcast on X's time + a 1 or 2 hour buffer.
            Return altered datetime to our information list as the time to check for updates, and datetime.now() as the time last checked for updates.
'''