import ConfigFile
import urllib.request
import time
import logging

continuePeriodCheck = 1
checkCounter = 1

logging.basicConfig(filename='WebMonitorLog.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

def periodMonit():

    reqSearchResult = []
    for webCounter in range(0,len(ConfigFile.webPagesList)):

        if (len(ConfigFile.webPagesList) != len(ConfigFile.requiredPageContent)):
            print('Lenght of lists of websites and requirements is different!')
            break
        try:

            requestedPage = urllib.request.urlopen(ConfigFile.webPagesList[webCounter])
            startTime = time.time()
            openedPage = requestedPage.read()
            endTime = time.time()
            websiteCode = urllib.request.urlopen(ConfigFile.webPagesList[webCounter]).getcode()
            requestedPage.close()
            openTime = round(endTime-startTime, 3)*1000

            logging.info('Website %s is loaded properly. Code: %d',ConfigFile.webPagesList[webCounter], websiteCode)
            logging.info('Whole response time of %s is %d ms',ConfigFile.webPagesList[webCounter], openTime)

            openedPage = str(openedPage)
            for reqCounter in range(0,len(ConfigFile.requiredPageContent[webCounter])):
                reqSearchResult.append(openedPage.find(ConfigFile.requiredPageContent[webCounter][reqCounter]))
                if openedPage.find(ConfigFile.requiredPageContent[webCounter][reqCounter]) == -1:
                    logging.error('Website %s does not contain the required phrase: "%s"',ConfigFile.webPagesList[webCounter],ConfigFile.requiredPageContent[webCounter][reqCounter])
                else:
                    logging.info('Website %s contains required phrase: "%s"',ConfigFile.webPagesList[webCounter],ConfigFile.requiredPageContent[webCounter][reqCounter])
        except urllib.error.URLError as e:
            logging.error('It is not possible to open %s because %s', ConfigFile.webPagesList[webCounter],e.reason)
        except:
            logging.error('Error for %s website is not known',ConfigFile.webPagesList[webCounter])



while continuePeriodCheck:
    time.sleep(ConfigFile.delayBetweenCheck)
    logging.info('*--------------------------------- Check %d ---------------------------------*', checkCounter)
    periodMonit()
    logging.info('Check number %d is done', checkCounter)
    if checkCounter >= ConfigFile.amountOfChecks:
        continuePeriodCheck = 0
        logging.info('Set amount of checks is done!')
    checkCounter = checkCounter + 1






