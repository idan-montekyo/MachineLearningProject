import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from AmazonGetAllPageUrls import get_pages_1_to_400
import os
import urllib.request

headers = ({'User-Agent':
                'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})


### Gets a list (of our game links)
### prints each game in a line, then prints the number of games in the list
def print_list(myList):
    for i in myList:
        print(i)
    print("size =", len(myList))


### Gets url for main Amazon page, and headers
### Returns html (source-code) for main Amazon page
def get_source_code_throws_exception(url, h):
    time.sleep(5)
    response = requests.get(url, headers=h)
    print(response)
    if str(response) != '<Response [200]>':
        raise Exception('requests.get failed (not Response [200]')
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup


### Gets url for main Amazon page
### Returns soup object representing the url's html (source-code)
def get_source_from_urllib(url):
    time.sleep(5)
    try:
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
        website = opener.open(url)
        html = website.read()
        soup = BeautifulSoup(html, "html.parser")
        return (soup)
    except:
        raise Exception('Request to get url`s source-code failed.')

### Gets main Amazon page html (source-code), and our main list that holds all our game links
### appends 16 game links for each page
def get_game_urls_from_one_page_and_append_to_list(soup, gameUrlList, runNumber):
    try:
        allGameSections = soup.findAll('div', attrs={'class': 's-include-content-margin s-latency-cf-section s-border-bottom s-border-top'})
        specificPageUrls = []
        for gameSection in allGameSections:
            isSponsored = gameSection.find('span', attrs={'class': 'a-color-base'}).get_text()
            if(isSponsored != 'Sponsored'):
                url = gameSection.find('a', attrs={'class': 'a-link-normal s-no-outline'})
                link = 'https://www.amazon.com/' + url['href']
                gameUrlList.append(link)
                specificPageUrls.append(link)
        ### Concatenates single page's game-url-links to the specific run's csv.
        save_lists_progress_to_specific_csv_files_axis0(specificPageUrls, runNumber)
    except:
        raise Exception('No data found, probably got blocked, broken html.')


### Gets a series of 50 pages, run numbers (from 0 to 7), and a User-Agent (headers).
### Checks existence of file with same run number as runNumber. if yes - deletes it to re-write.
### Creates two list, one to hold 800 game urls from 50 pages, and one to hold the rejected ones that failed along the way.
### Sends a request to the server, gets each page html, gets the links to all the games, and appends to gameUrlList.
### Then saves all ~800 games in a new column in the complete-csv with all urls from all 8 runs.
def extract_game_urls_from_50_pages_to_main_urls_list(pages, runNumber, headers):
    ### If the specific run's file already exists, delete it to re-make it, instead of concatenating.
    specificRunNameForGameUrlListCsv = 'LinksForEachRun\gameUrlList_' + str(runNumber) + '.csv'
    if (os.path.exists(specificRunNameForGameUrlListCsv) and os.path.isfile(specificRunNameForGameUrlListCsv)):
        os.remove(specificRunNameForGameUrlListCsv)
        print("file deleted")

    gameUrlList = []
    rejectedPagesList = []
    for i, pageUrl in enumerate(pages):
        time.sleep(0.1)
        try:
            try:
                soup = get_source_from_urllib(pageUrl)
            except:
                soup = get_source_code_throws_exception(pageUrl, headers)
            try:
                get_game_urls_from_one_page_and_append_to_list(soup, gameUrlList, runNumber)
                print('Page ' + str(i) + ' succeeded.')
            except:  # No data found, broken html.
                rejectedPagesList.append(pageUrl)
                print('Page ' + str(i) + ' failed.')
        except:  # Response != <Response [200]>
            rejectedPagesList.append(pageUrl)
            print('Page ' + str(i) + ' failed.')
    ### Save new 50 urls in a new column in the complete-game-urls-list-csv.
    save_lists_progress_to_complete_csv_files_axis1(gameUrlList, rejectedPagesList)
    print('\n---------------------------------\n\nGame url links for run ' + str(runNumber) + ':')
    print_list(gameUrlList)
    print('\n---------------------------------\n\nRejected pages list for run ' + str(runNumber) + ':')
    print_list(rejectedPagesList)
    print('\n50 pages - done. (run ' + str(runNumber) + ')')


### Gets game-list of a specific run (of 50 pages).
### concatenates the new game links to the saved Data-Frames and updates the CSVs.
### Updates 50 times a run, after every page. Adds a single page's list to the specific run's CSV.
def save_lists_progress_to_specific_csv_files_axis0(gameUrlList, runNumber):
    specificRunNameForGameUrlListCsv = 'LinksForEachRun\gameUrlList_' + str(runNumber) + '.csv'
    try:
        savedGameUrlListCsv = pd.read_csv(specificRunNameForGameUrlListCsv)

        newGameUrlListDf = pd.DataFrame({'gameUrlList': gameUrlList})
        concatenatedGameUrlListDf = pd.concat([savedGameUrlListCsv, newGameUrlListDf])
        concatenatedGameUrlListDf.to_csv(specificRunNameForGameUrlListCsv, index=False)
    except:  # for the first run, in case 'gameUrlList.csv' or 'rejectedPagesList.csv' does not exist.
        firstGameUrlListDf = pd.DataFrame({'gameUrlList': gameUrlList})
        firstGameUrlListDf.to_csv(specificRunNameForGameUrlListCsv, index=False)


### Gets lists of a specific run (of 50 pages)
### concatenates the new game links to the saved Data-Frames and updates the CSVs.
### Updates once a run, at the end. Adds every 50-pages-list to it's own column in the complete CSV.
def save_lists_progress_to_complete_csv_files_axis1(gameUrlList, rejectedPagesList):
    try:
        savedCompleteGameUrlListCsv = pd.read_csv('completeGameUrlList.csv')
        savedCompleteRejectedPagesListCsv = pd.read_csv('completeRejectedPagesList.csv')

        new50PageGameUrlListDf = pd.DataFrame({'completeGameUrlList': gameUrlList})
        concatenatedCompleteGameUrlListDf = pd.concat([savedCompleteGameUrlListCsv,
                                                       new50PageGameUrlListDf], axis=1)
        concatenatedCompleteGameUrlListDf.to_csv('completeGameUrlList.csv', index=False)

        new50PageRejectedPagesListDf = pd.DataFrame({'completeRejectedPagesList': rejectedPagesList})
        concatenatedCompleteRejectedPagesListDf = pd.concat([savedCompleteRejectedPagesListCsv,
                                                             new50PageRejectedPagesListDf], axis=1)
        concatenatedCompleteRejectedPagesListDf.to_csv('completeRejectedPagesList.csv', index=False)
    except:  # for the first run, in case 'gameUrlList.csv' or 'rejectedPagesList.csv' does not exist.
        first50PageGameUrlListDf = pd.DataFrame({'completeGameUrlList': gameUrlList})
        first50PageGameUrlListDf.to_csv('completeGameUrlList.csv', index=False)

        first50PageRejectedPagesListDf = pd.DataFrame({'completeRejectedPagesList': rejectedPagesList})
        first50PageRejectedPagesListDf.to_csv('completeRejectedPagesList.csv', index=False)


### Returns array of all 400 Amazon pages.
def get_all_pages_in_array():
    pagesDf = get_pages_1_to_400()
    pages_1_50 = pagesDf.iloc[:, 0]  # Done (got rejections - but got treated.)
    pages_51_100 = pagesDf.iloc[:, 1]  # Done
    pages_101_150 = pagesDf.iloc[:, 2]  # Done
    pages_151_200 = pagesDf.iloc[:, 3]  # Done
    pages_201_250 = pagesDf.iloc[:, 4]  # Done
    pages_251_300 = pagesDf.iloc[:, 5]  # Done
    pages_301_350 = pagesDf.iloc[:, 6]  # Done
    pages_351_400 = pagesDf.iloc[:, 7]  # Done

    return [pages_1_50, pages_51_100, pages_101_150, pages_151_200,
            pages_201_250, pages_251_300, pages_301_350, pages_351_400]





allPagesList = get_all_pages_in_array()  # Done
pages_rejected_Df = pd.read_csv('completeRejectedPagesList.csv')
rejList = pages_rejected_Df.iloc[:, 0]  # Done


# ### Run all 400 pages
# for runNum, pages in enumerate(allPagesList):
#     if runNum > 0:
#         time.sleep(60)
#     extract_game_urls_from_50_pages_to_main_urls_list(pages, runNum, headers)
