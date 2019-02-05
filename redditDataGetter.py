import requests as r
import json
import time
import csv

#===================================================================================

global url
url = "https://api.pushshift.io/reddit/search/submission?is_self=true&size=1000&author!=[deleted]&subreddit=%s&after=%i&before=%i"

#===================================================================================

# convert DD MM YYY into an epoch timestamp to be used in the API request
def dateToEpoch(day, month, year):
    cleanDate = '.'.join([str(day), str(month), str(year)])
    date_time = cleanDate + ' 12:00:00'
    pattern = '%d.%m.%Y %H:%M:%S'
    epoch = int(time.mktime(time.strptime(date_time, pattern)))
    return epoch

# get the API data from pushshift
def getContent(subreddit, beforeEpoch, afterEpoch):
    finalURL = url % (subreddit, afterEpoch, beforeEpoch)
    apiReturn = r.get(finalURL).content
    toReturn = json.loads(apiReturn)['data']
    return toReturn

def cleanContent(singleEntry):
    # make a dict in case we need to use it later (default value is None)
    toReturnDict = { x:None for x in ['author', 'created_utc', 'domain', 'full_link', 'id', 'permalink', 'retrieved_on', 'score', 'subreddit', 'title', 'selftext'] }
    try:
        toReturnDict['author'] = singleEntry['author']
        toReturnDict['created_utc'] = singleEntry['created_utc']
        toReturnDict['domain'] = singleEntry['domain']
        toReturnDict['full_link'] = singleEntry['full_link']
        toReturnDict['id'] = singleEntry['id']
        toReturnDict['permalink'] = singleEntry['permalink']
        toReturnDict['retrieved_on'] = singleEntry['retrieved_on']
        toReturnDict['score'] = singleEntry['score']
        toReturnDict['subreddit'] = singleEntry['subreddit']
        toReturnDict['title'] =singleEntry['title']
        toReturnDict['selftext'] = singleEntry['selftext']
    except:
        return toReturnDict
    print("Found post with id " + toReturnDict['id'] + ", title: " + str(toReturnDict['title']))
    return list(toReturnDict.values())

#===================================================================================

def controller(subreddit, requestEpochs):
    outfile = open("redditPosts/" + subreddit + '_redditArchive.csv', 'w')
    writer = csv.writer(outfile)
    writer.writerow(['author', 'created_utc', 'domain', 'full_link', 'id', 'permalink', 'retrieved_on', 'score', 'subreddit', 'title', 'selftext'])

    for i in range(len(requestEpochs)-1):
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("========= STARTING EPOCH " + str(requestEpochs[i+1]) + " -> " + str(requestEpochs[i]) + " =========")
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        entries = getContent(subreddit, requestEpochs[i+1], requestEpochs[i])
        rowToWrite = [cleanContent(singleEntry) for singleEntry in entries]
        writer.writerows(rowToWrite)

    outfile.close()

#===================================================================================

def getInputs():
    # ask for subreddit
    subreddit = input("Which subreddit to you want to archive? (Don't include 'r/'): ")

    # ask for start date
    startDay, startMonth, startYear =\
        [int(i) for i in input("Enter the date from which to look for posts (DD/MM/YYYY): ").split('/')]
    startEpoch = dateToEpoch(startDay, startMonth, startYear)

    # ask for end date
    endDay, endMonth, endYear =\
        [int(i) for i in input("Enter the date to stop looking for posts (DD/MM/YYYY): ").split('/')]
    endEpoch = dateToEpoch(endDay, endMonth, endYear)

    WEEK_IN_EPOCH = 604800

    # create a range of dates to use for API requests
    requestEpochs = range(startEpoch, endEpoch+WEEK_IN_EPOCH, WEEK_IN_EPOCH)

    return (subreddit, requestEpochs)

#===================================================================================

colleges = ['MTSU',
'waynestate',
'ualbany',
'Lehigh',
'LoyolaChicago',
'UNC',
'uml',
'villanova',
'UMiami',
'BallState',
'AmericanU',
'Marquette',
'FAU',
'SMU',
'BGSU',
'IUPUI',
'ODU',
'MSUcats',
'Ashland',
'UniversityofArkansas',
'standrews',
'UNLincoln',
'ColoradoSchoolOfMines',
'UAH',
'usu',
'LouisianaTech',
'unh',
'ULL',
'Fordham',
'fresnostate',
'emu',
'SHSU',
'NDSU',
'uwyo',
'easternshoremd',
'IIT',
'uofi',
'montclair',
'und',
'UTEP',
'LibertyUniversity',
'UMKC',
'uofdayton',
'denveru',
'UofMemphis',
'nmsu',
'SIUC',
'tntech',
'wfu',
'muohio',
'bsu',
'wrightstate',
'brandeis',
'oaklanduniversity',
'IUP',
'utulsa',
'UniversityofMontana',
'usfca',
'uwf',
'USD',
'usouthal',
'umaine',
'Hofstra',
'Merced',
'UNO',
'univRI',
'UAF',
'southernmiss',
'UMSL',
'ClarkU',
'LamarUniversity',
'UNCO',
'UWG',
'Duquesne',
'utrgv',
'Pepperdine',
'UALR',
'ClarksonU',
'UoP',
'STJOHNS',
'gcu',
'pace',
'tamuc',
'TheNewSchool',
'SHU',
'Biola',
'stthomas',
'valdostastate',
'mercer',
'Kingsville',
'Kingsville',
'apu',
'USouthDakota',
'SUNY_ESF',
'TexasSouthern',
'sjfc',
'CUA',
'AUC',
'Widener',
'laverne',
'YeshivaUniversity',
'witchastateuniversity',
'dallasbaptist',
'SuffolkU',
'NovaSoutheastern',
'ShenandoahUniversity',
'gardnerwebb',
'stritch',
'Trevecca',
'EdgewoodCollege']
requestEpochs = [1388595600, 1548781200]
for college in colleges:
    print('\n\n\n\n\n')
    print('+++++++++++++++++++ STARTING COLLEGE: ' + college)
    controller(college, requestEpochs)