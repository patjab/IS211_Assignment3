import urllib.request, urllib.error, argparse, csv, re, datetime

# Downloads the file specified in the URL and stores it on the local drive
def downloadData(url):
    page = urllib.request.urlretrieve(url, filename='temp.csv')

# Opens the downloaded file and processes line by line into lists of strings
# Returns this line by line in the form of bytes
def processFile():
    f = open("temp.csv", 'rt')
    reader = None
    try:
        reader = csv.reader(f)
    finally:
        2+2

    return reader


# This is the helper function of findImages()
# It determines whether or not a file is an image depending upon the file extension
# .jpg .jpeg .gif .png were all considered to be images
def isImage(filename):
    if ( filename == None or filename == "" ):
        return False
    else:
        pattern = '^.*\.jpg$|^.*\.jpeg$|^.*\.gif$|^.*\.png$'

        if ( re.search(pattern, filename, re.IGNORECASE) != None ):
            return True
        else:
            return False


# Iterates through all rows and adds one everytime isImage() == True (has an image file extension)
# Adds one for every row to count total rows for the purposes of finding percentage
# Prints percentage results
def findImages():
    csvData = processFile()
    totalFiles = 0
    imageFiles = 0

    for row in csvData:

        if ( isImage(row[0]) ):
            imageFiles += 1
            totalFiles += 1
        elif ( not isImage(row[0]) ):
            totalFiles += 1

    percentage = (imageFiles/totalFiles)*100

    print("Image requests account for", percentage, "% of all requests")


# Iterates through all rows' UserAgent column, determines what browser, and keeps count
def whichBrowser():

    # Load temporarily downloaded file
    csvData = processFile()

    # Regex searching for these to determine what browser accessed file
    internetExplorer = 'MSIE'
    firefox = 'Firefox'
    chrome = 'Chrome'
    safari = 'Safari'

    # Set all counters for different browsers
    internetExplorerCounter = 0
    firefoxCounter = 0
    chromeCounter = 0
    safariCounter = 0

    # Run through each row and row[2] for UserAgent and searches to see what browser string matches, adds to respective counter
    for row in csvData:
        userAgent = row[2]

        if ( userAgent == None or userAgent == "" ):
            print("Empty")
        elif ( re.search(internetExplorer, userAgent, re.IGNORECASE) != None ):
            internetExplorerCounter += 1
        elif ( re.search(firefox, userAgent, re.IGNORECASE) != None ):
            firefoxCounter += 1
        elif ( (re.search(chrome, userAgent, re.IGNORECASE) != None) and (re.search(safari, userAgent, re.IGNORECASE) != None) ):
            chromeCounter += 1
        elif ( (re.search(chrome, userAgent, re.IGNORECASE) == None) and (re.search(safari, userAgent, re.IGNORECASE) != None) ):
            safariCounter += 1

    # Creates a dictionary of counters and browsers
    browserCount = {}
    browserCount['Internet Explorer'] = internetExplorerCounter
    browserCount['Firefox'] = firefoxCounter
    browserCount['Chrome'] = chromeCounter
    browserCount['Safari'] = safariCounter

    # Reverses the keys and contents of the dictionaries to compare the contents for the greatest number of hits and stores the name of the browser
    mostUsedBrowser = (max(zip(browserCount.values(), browserCount.keys())))[1]

    print("The most popular browser of the day is", mostUsedBrowser)

# Looks at time accessed column and places in a datetime object to scan through hours while keeping track in a counter of hits
def hitsByHour():
    csvData = processFile()
    counter = []

    # Set an array counter full of zeroes, 24 represents the amount of hours in the day
    for x in range(24):
        counter.append(0)

    # Regex splits
    for row in csvData:
        timeComponents = re.split('-|\s|:', row[1])     # Regex splits date/time string into components by splitting at hyphens, white space, and colons

        # Takes array of split components and places them into a datetime object
        t = datetime.datetime(int(timeComponents[0]), int(timeComponents[1]), int(timeComponents[2]), int(timeComponents[3]), int(timeComponents[4]), int(timeComponents[5]))

        # Adds one to the corresponding hour of each row in an array
        counter[t.hour] += 1

    # Prints the results of the array
    for y in range(24):
        print("Hour", y, "has", counter[y], "hits")

def main():

    data = None

    # Pass in an argument through the command prompt for URL of csv file
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="Read a file at this URL")
    args = parser.parse_args()

    # Make sure URL is inputted and connection and server can be found
    if args.url == None:
        print("URL is required. Program exiting.")
        exit()
    elif args.url:
            try:
                data = downloadData(args.url)
            except urllib.error.HTTPError:
                print("HTTPError: Server not found. Please check the address and try again.")
                quit()
            except urllib.error.URLError:
                print("URLError: No network connection found. Please check your connection and try again.")
                quit()

    # List of functions to process through, represents one part of the homework
    print()
    findImages()
    whichBrowser()
    hitsByHour()
    print()

if __name__ == '__main__': main()



