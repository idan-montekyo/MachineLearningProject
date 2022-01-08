import requests
from bs4 import BeautifulSoup
import time
import re
import urllib.request

game_url = "https://www.amazon.com/Madden-22-Standard-Steam-Online/dp/B09CDHZ1DD/ref=sr_1_1?keywords=PC-compatible%2BGames&qid=1641063855&s=videogames&sr=1-1&th=1"

### with several types of 'Genre' and 'Operating System'
game_2 = 'https://www.amazon.com/Seek-Find-Adventures-Game-Pack-PC/dp/B00OAOD8PG/ref=sr_1_28_sspa?keywords=PC-compatible+Games&qid=1641591018&s=videogames&sr=1-28-spons&psc=1' \
         '&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUExOEtUWjlHTTdBQTUxJmVuY3J5cHRlZElkPUEwNzA4MzUxM0RCSURBR00xSjk3RiZlbmNyeXB0ZWRBZElkPUEwNDY0NDIwM0E5V00zT1NKRFlSMCZ3aWRnZXROYW1lPXNwX210ZiZhY3Rpb249Y2xpY2tSZWRpcmVjdCZkb05vdExvZ0NsaWNrPXRydWU='

### with several types of 'Operating System' and 'Hardware Platform'
game_3 = 'https://www.amazon.com/Lost-Cases-Sherlock-Holmes-PC-Mac/dp/B002MFOGBU/ref=sr_1_9_sspa?keywords=PC-compatible%2BGames&qid=1641591031&s=videogames&sr=1-9-spons' \
         '&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUExVjZWQTNXUDc2Qk1KJmVuY3J5cHRlZElkPUEwMjA5ODEyMzExU1lWQTJSR0pDUiZlbmNyeXB0ZWRBZElkPUEwMzU1MDg2MjJWQVQyNFA2WFRINiZ3aWRnZXROYW1lPXNwX210ZiZhY3Rpb249Y2xpY2tSZWRpcmVjdCZkb05vdExvZ0NsaWNrPXRydWU&th=1'

headers = ({'User-Agent':
                'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2288.0 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})

##### SEARCH FOR 'GENRE' TO CONFIRM IT'S A GAME !


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


### '[\d]+' finds integers 123
### '[\d]*[.][\d]+' finds floats 0.123 | .123
### '[\d]+[.,\d]+' finds commas 12,300 | 12,300.00
### '[(]*[\d]*[%]*[)]+' to find '(d%)'
def extract_number_from_string_get_location_0_from_list(string):
    if not isinstance(string, str):
        return float(0)
    elif len(string) == 0:
        return float(0)
    else:
        p = '[\d]+[.,\d]+|[\d]*[.][\d]+|[\d]+'
        numbersList = []
        if re.search(p, string) is not None:
            for catch in re.finditer(p, string):
                numbersList.append(float(catch[0]))  # catch is a match object
            return numbersList
        else:
            return float(0)


def extract_day_and_year_for_publication_date(string):
    if not isinstance(string, str):
        return float(0)
    elif len(string) == 0:
        return float(0)
    else:
        p = '[\d]*[.][\d]+|[\d]+'
        numbersList = []
        if re.search(p, string) is not None:
            for catch in re.finditer(p, string):
                numbersList.append(float(catch[0]))  # catch is a match object
            return numbersList
        else:
            return float(0)


### Scraping a single game page, fills all of it's features in a data-frame line
### Returns a one-line data-frame for a specific game
def scrape_single_game(gameUrl, rejectedGamesList, headers):

    try:  # Try getting soup object
        time.sleep(5)
        try:
            soup = get_source_from_urllib(gameUrl)
        except:
            soup = get_source_code_throws_exception(gameUrl, headers)
        ### Checks if this url belongs to a game, by checking if the html contains the word 'Genre'
        isGame = soup.find(text='Genre')
        if isGame:
            ### Gets product name
            try:  # Try getting game's name
                title = soup.find('span', attrs={'class': 'a-size-large product-title-word-break'}).get_text().strip()
                print('Product name: ' + str(title))

                ### Gets data-table with variables such as - Brand, Genre, Publication Date, Operating System, Computer Platform
                dataTable = soup.find('table', attrs={'class': 'a-normal a-spacing-micro'})
                dataRows = dataTable.findAll('tr', attrs={'class': 'a-spacing-small'})
                ### description -> details (key -> value)
                for tr in dataRows:
                    descriptionAndDetail = tr.findAll('td')
                    if(descriptionAndDetail[0].get_text().strip() == 'Brand'):
                        print('Brand: ' + descriptionAndDetail[1].get_text().strip()) ###########################################################################################################
                    elif(descriptionAndDetail[0].get_text().strip() == 'Genre'):
                        genresList = re.findall(r'[a-zA-Z]+[\s]*[a-zA-Z]*', descriptionAndDetail[1].get_text().strip())
                        try:
                            print('Genre: ' + str(genresList[0]))
                            print('Sub-Genre: ' + str(genresList[1]))
                        except (IndexError, ValueError):  #################### CHECK IF IT'S THE RIGHT EXCEPTION!
                            print('Genre: ' + str(genresList[0]))
                            print('Sub-Genre: 0')
                        except:
                            print('Genre & Sub-Genre = 0')
                    elif(descriptionAndDetail[0].get_text().strip() == 'Publication Date'):
                        dayAndYear = extract_day_and_year_for_publication_date(descriptionAndDetail[1].get_text().strip())
                        day = int(dayAndYear[0])
                        year = int(dayAndYear[1])
                        month = (re.findall(r'[a-zA-Z]+', descriptionAndDetail[1].get_text().strip()))[0]
                        print('Publication Day: ' + str(day))
                        print('Publication Month: ' + str(month))
                        print('Publication Year: ' + str(year))
                    elif (descriptionAndDetail[0].get_text().strip() == 'Operating System'):
                        operatingSystemsList = re.findall(r'[\w+]+[\s]*[\d]*[\w+]*[\s]*[\w+]*', descriptionAndDetail[1].get_text().strip())
                        try:
                            print('Operating System: ' + str(operatingSystemsList[0]))
                            print('Sub-Operating System: ' + str(operatingSystemsList[1]))
                        except (IndexError, ValueError):  #################### CHECK IF IT'S THE RIGHT EXCEPTION!
                            print('Operating System: ' + str(operatingSystemsList[0]))
                            print('Sub-Operating System: 0')
                        except:
                            print('Operating System & Sub-Operating System = 0')
                    elif (descriptionAndDetail[0].get_text().strip() == 'Format'):
                        print('Format: ' + descriptionAndDetail[1].get_text().strip()) ##################################################################################################
                    elif (descriptionAndDetail[0].get_text().strip() == 'Computer Platform' or
                            descriptionAndDetail[0].get_text().strip() == 'Hardware Platform'):
                        # if dict = null, then replace
                        print('Computer Platform / Hardware Platform: ' + descriptionAndDetail[1].get_text().strip()) ##############################################################################################
                    else:
                        print('*OTHER: ' + descriptionAndDetail[0].get_text().strip() + " -> " + descriptionAndDetail[1].get_text().strip())


                ### Gets final product rating and number of ratings
                ratings = soup.find('div', attrs={'id': 'gameReviewsFeatureGroup'})
                finalRatingAsString = ratings.find('span', attrs={'class': 'a-icon-alt'}).get_text()
                numOfRatingsAsString = ratings.find('span', attrs={'class': 'a-size-base'}).get_text()
                finalRating = extract_number_from_string_get_location_0_from_list(finalRatingAsString)[0]
                numOfRatings = int(extract_number_from_string_get_location_0_from_list(numOfRatingsAsString)[0])
                print('Final rating = ' + str(finalRating))
                print('Number of ratings = ' + str(numOfRatings))


                ### Gets rating percentage for each star (out of 100% total)
                ### ONLY IF VAR-numOfRatings > 0 !
                ratingPercentTable = soup.find('table', attrs={'class': 'a-normal a-align-center a-spacing-base'})
                ratingPercentRows = ratingPercentTable.findAll('td', attrs={'class': 'a-text-right a-nowrap'})
                ratingPercentageListHoldingEachStar = []
                for row in ratingPercentRows:
                    pString = row.get_text()
                    percentage = int(extract_number_from_string_get_location_0_from_list(pString)[0])
                    amount = int(numOfRatings * percentage / 100)
                    ratingPercentageListHoldingEachStar.append(amount)
                # print(ratingPercentageForEachStar)
                for i in range(5):
                    print(str(5-i) + " stars -> " + str(ratingPercentageListHoldingEachStar[i]))


                ### Gets prices (price, discount, etc...)
                ### if len(pricesList) == 1 -> original price = lst[0]
                ### if len(pricesList) == 4 -> final price = lst[1], discount percentage = lst[3]
                priceTable = soup.find('div', attrs={'id': 'price'})
                allTds = priceTable.findAll('td')
                pricesList = []
                for td in allTds:
                    pString = td.get_text()
                    pFloat = extract_number_from_string_get_location_0_from_list(pString)
                    if isinstance(pFloat, float):
                            if pFloat > 0:  # To remove all zeros
                                pricesList.append(pFloat)
                    else:
                        for p in pFloat:
                            if p > 0:  # To remove all zeros
                                pricesList.append(p)
                # print('prices: ' + str(pricesList))
                try:
                    print('Price: ' + str(pricesList[1]))
                    print('Discount: ' + str(pricesList[2]))
                except (IndexError, ValueError):  ################################# CHECK IF IT'S THE RIGHT EXCEPTION!
                    print('Price: ' + str(pricesList[0]))
                    print('Discount: 0')
                except:
                    print('Price & Discount = 0')


                ### Gets 'About this item' - aka Description
                # aboutThisItem = soup.find('ul', attrs={'class': 'a-unordered-list a-vertical a-spacing-mini'}).get_text().strip()
                aboutThisItem = soup.find('ul', attrs={'class': 'a-unordered-list a-vertical a-spacing-mini'})
                aboutThisItemBullets = aboutThisItem.findAll('span')
                productDescription = ''
                for bullet in aboutThisItemBullets:
                    productDescription = productDescription + bullet.get_text().strip() + '\n'
                productDescription = productDescription[:-1]
                print('Description:\n' + productDescription)

            except:  # No title found. probably got blocked.
                rejectedGamesList.append(gameUrl)
                # raise Exception('No title found, probably got blocked. gameUrl added to rejectedPagesList')
                print('No title found, probably got blocked. gameUrl added to rejectedPagesList')

        else:
            print('Not a game - ' + gameUrl)

    except:  # Failed to get <Response [200]>
        rejectedGamesList.append(gameUrl)
        # raise Exception('Failed to get <Response [200]>')
        print('Failed to get <Response [200]>')


### How to deal with multiple values for a key ?
### maybe hold several keys for different genres for example.
### every field should be covered with try-except.
Row = ['y', 'game name',
       'y', 'Price / List Price / With Deal',
       'y', 'discount(amount) (You Save)',
       'y', 'final_rating', 'Will be our y-value (tagging). 3.5 or above = `1`, below 3.5 = `0`',
       'y', 'number_of_ratings',
       'y', '5star_numbers', 'NOT FOR LEARNING!!!',
       'y', '4star_numbers', 'NOT FOR LEARNING!!!',
       'y', '3star_numbers', 'NOT FOR LEARNING!!!',
       'y', '2star_numbers', 'NOT FOR LEARNING!!!',
       'y', '1star_numbers', 'NOT FOR LEARNING!!!',
       'y', 'Brand',
       'y', 'Genre', 'Search for `Genre` to confirm it`s a game!!!',
       'y', 'Sub-Genre',
       'y', 'Publication-day',
       'y', 'Publication-month',
       'y', 'Publication-year',
       'y', 'Operating System',
       'NO', 'Sub-OS',
       'y', 'Format',
       'y', 'Computer Platform', 'probably same... Platform',
       'y', 'Hardware Platform', 'probably same... Platform',
       'y', 'About this item (Description)', 'make all points one sentence. important to add.',
       '']




# rej = []
# scrape_single_game(game_url, rej, headers)

