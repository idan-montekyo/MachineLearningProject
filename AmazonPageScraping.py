import requests
from bs4 import BeautifulSoup
import time
import re
import urllib.request
from urllib.request import build_opener, HTTPCookieProcessor, Request

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


game_url = "https://www.amazon.com/Madden-22-Standard-Steam-Online/dp/B09CDHZ1DD/ref=sr_1_1?keywords=PC-compatible%2BGames&qid=1641063855&s=videogames&sr=1-1&th=1"

headers = ({'User-Agent':
                'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})


### Get html from selenium
def get_source_code_from_selenium(url):
    options = Options()
    options.add_argument("--lang=en")
    options.headless = True  # open browser unseen
    chrome_driver_path = "C:\Program Files (x86)\chromedriver.exe"
    driver = webdriver.Chrome(chrome_driver_path, options=options)
    time.sleep(2)
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup)
    driver.quit()
    return soup


### Gets url for main Amazon page, and headers
### Returns html (source-code) for main Amazon page
def get_source_code_throws_exception(url):
    headers = ({'User-Agent':
                    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
                'Accept-Language': 'en-US, en;q=0.5'})
    time.sleep(5)
    response = requests.get(url, headers=headers)
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
        opener = urllib.request.build_opener(HTTPCookieProcessor())
        opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
        website = opener.open(url)
        html = website.read()
        soup = BeautifulSoup(html, "html.parser")

        # opener = build_opener(HTTPCookieProcessor())
        # request = Request(url)
        # print(request.data)
        # response = opener.open(request, timeout=30)
        # content = response.read()
        # print(content)
        # soup = BeautifulSoup(content, "html.parser")

        return (soup)
    except:
        raise Exception('Request to get url`s source-code failed.')


### '[\d]+' finds integers 123
### '[\d]*[.][\d]+' finds floats 0.123 | .123
### '[\d]+[.,\d]+' finds commas 12,300 | 12,300.00
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
### Gets a game's url, list of rejected games (failed to scrape), and 21 lists, one for each feature (column)
### Appending game's data to the fitting features.
def scrape_single_game(gameUrl, rejectedGamesList,
                       name, price, discount, final_rating, number_of_ratings,
                       number_of_5star, number_of_4star, number_of_3star, number_of_2star, number_of_1star,
                       brand, genre, sub_genre, publication_day, publication_month, publication_year,
                       operating_system, sub_operating_system, format, platform, other, product_description):

    temp_name = temp_price = temp_discount = temp_final_rating = temp_number_of_ratings = 0
    temp_5star = temp_4star = temp_3star = temp_2star = temp_1star = temp_description = 0
    temp_brand = temp_genre = temp_sub_genre = temp_day = temp_month = temp_year = 0
    temp_operating_system = temp_sub_operating_system = temp_format = temp_platform = temp_other = 0

    try:  # Try getting soup object
        soup = get_source_code_from_selenium(gameUrl)
        # try:
        #     soup = get_source_from_urllib(gameUrl)
        # except:
        #     soup = get_source_code_throws_exception(gameUrl)
        ### Checks if this url belongs to a game, by checking if the html contains the word 'Genre'
        isGame = soup.find(text='Genre')
        if isGame:
            ### Gets product name
            try:  # Try getting game's name
                title = soup.find('span', attrs={'class': 'a-size-large product-title-word-break'}).get_text().strip()
                if title:
                    temp_name = str(title)
                else:
                    raise Exception('No title found, probably got blocked.')


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
                try:
                    temp_price = pricesList[1]
                    temp_discount = pricesList[2]
                except (IndexError, ValueError):
                    temp_price = pricesList[0]
                    temp_discount = float(0)
                except:
                    temp_price = float(0)
                    temp_discount = float(0)


                ### Gets final product rating and number of ratings
                ratings = soup.find('div', attrs={'id': 'gameReviewsFeatureGroup'})
                finalRatingAsString = ratings.find('span', attrs={'class': 'a-icon-alt'}).get_text()
                numOfRatingsAsString = ratings.find('span', attrs={'class': 'a-size-base'}).get_text()
                finalRating = extract_number_from_string_get_location_0_from_list(finalRatingAsString)[0]
                numOfRatings = int(extract_number_from_string_get_location_0_from_list(numOfRatingsAsString)[0])
                try:
                    temp_final_rating = finalRating
                except:
                    temp_final_rating = 0
                try:
                    temp_number_of_ratings = numOfRatings
                except:
                    temp_number_of_ratings = 0


                ### Gets rating percentage for each star (out of 100% total)
                ### ONLY IF VAR-numOfRatings > 0 !
                ratingPercentTable = soup.find('table', attrs={'class': 'a-normal a-align-center a-spacing-base'})
                ratingPercentRows = ratingPercentTable.findAll('td', attrs={'class': 'a-text-right a-nowrap'})
                ratingAmountListHoldingEachStar = []
                for row in ratingPercentRows:
                    pString = row.get_text()
                    percentage = int(extract_number_from_string_get_location_0_from_list(pString)[0])
                    amount = int(numOfRatings * percentage / 100)
                    ratingAmountListHoldingEachStar.append(amount)
                temp_numberOfStarsList = [temp_5star, temp_4star, temp_3star, temp_2star, temp_1star]
                for i in range(5):
                    try:
                        temp_numberOfStarsList[i] = ratingAmountListHoldingEachStar[i]
                    except:
                        temp_numberOfStarsList[i] = 0


                ### Gets data-table with variables such as - Brand, Genre, Publication Date, Operating System, Computer Platform
                dataTable = soup.find('table', attrs={'class': 'a-normal a-spacing-micro'})
                dataRows = dataTable.findAll('tr', attrs={'class': 'a-spacing-small'})
                ### description -> details (key -> value)
                for tr in dataRows:
                    descriptionAndDetail = tr.findAll('td')
                    if(descriptionAndDetail[0].get_text().strip() == 'Brand'):
                        try:
                            temp_brand = descriptionAndDetail[1].get_text().strip()
                        except:
                            temp_brand = 0
                    elif(descriptionAndDetail[0].get_text().strip() == 'Genre'):
                        genresList = descriptionAndDetail[1].get_text().strip().split(',')
                        try:
                            if len(genresList) > 1:
                                temp_genre = str(genresList[0])
                                temp_sub_genre = str(genresList[1])
                            else:
                                temp_genre = str(genresList[0])
                                temp_sub_genre = 0
                        except:
                            temp_genre = temp_sub_genre = 0
                    elif(descriptionAndDetail[0].get_text().strip() == 'Publication Date'):
                        dayAndYear = extract_day_and_year_for_publication_date(descriptionAndDetail[1].get_text().strip())
                        day = int(dayAndYear[0])
                        year = int(dayAndYear[1])
                        month = (re.findall(r'[a-zA-Z]+', descriptionAndDetail[1].get_text().strip()))[0]
                        try:
                            temp_day = day
                        except:
                            temp_day = 0
                        try:
                            temp_month = str(month)
                        except:
                            temp_month = 0
                        try:
                            temp_year = year
                        except:
                            temp_year = 0
                    elif (descriptionAndDetail[0].get_text().strip() == 'Operating System'):
                        operatingSystemsList = descriptionAndDetail[1].get_text().strip().split(',')
                        try:
                            temp_operating_system = str(operatingSystemsList[0])
                            if len(operatingSystemsList) > 1:
                                temp_sub_operating_system = str(operatingSystemsList[1])
                            else:
                                temp_sub_operating_system = 0
                        except:
                            temp_operating_system = temp_sub_operating_system = 0
                    elif (descriptionAndDetail[0].get_text().strip() == 'Format'):
                        try:
                            temp_format = descriptionAndDetail[1].get_text().strip()
                        except:
                            temp_format = 0
                    elif (descriptionAndDetail[0].get_text().strip() == 'Computer Platform' or
                            descriptionAndDetail[0].get_text().strip() == 'Hardware Platform'):
                        if temp_platform == 0:  # Assign if var hasn't been touched yet.
                            try:
                                temp_platform = descriptionAndDetail[1].get_text().strip()
                            except:
                                temp_platform = 0
                    else:  # Other feature (column)
                        try:
                            temp_other = descriptionAndDetail[1].get_text().strip()
                        except:
                            temp_other = 0


                ### Gets 'About this item' - aka Description
                aboutThisItem = soup.find('ul', attrs={'class': 'a-unordered-list a-vertical a-spacing-mini'})
                aboutThisItemBullets = aboutThisItem.findAll('span')
                productDescription = ''
                for bullet in aboutThisItemBullets:
                    productDescription = productDescription + bullet.get_text().strip() + '\n'
                productDescription = productDescription[:-1]
                try:
                    temp_description = productDescription
                except:
                    temp_description = 0


                ### Data appending into lists
                name.append(temp_name)
                price.append(temp_price)
                discount.append(temp_discount)

                final_rating.append(temp_final_rating)
                number_of_ratings.append(temp_number_of_ratings)
                number_of_5star.append(temp_numberOfStarsList[0])
                number_of_4star.append(temp_numberOfStarsList[1])
                number_of_3star.append(temp_numberOfStarsList[2])
                number_of_2star.append(temp_numberOfStarsList[3])
                number_of_1star.append(temp_numberOfStarsList[4])

                brand.append(temp_brand)
                genre.append(temp_genre)
                sub_genre.append(temp_sub_genre)
                publication_day.append(temp_day)
                publication_month.append(temp_month)
                publication_year.append(temp_year)
                operating_system.append(temp_operating_system)
                sub_operating_system.append(temp_sub_operating_system)
                format.append(temp_format)
                platform.append(temp_platform)
                other.append(temp_other)
                product_description.append(temp_description)

            except:  # No title found. probably got blocked.
                rejectedGamesList.append(gameUrl)
                # raise Exception('No title found, probably got blocked. gameUrl added to rejectedPagesList')
                print('No title found, probably got blocked. gameUrl added to rejectedPagesList\n', gameUrl)

        else:
            print('Not a game - ' + gameUrl)

    except:  # Failed to get <Response [200]>
        rejectedGamesList.append(gameUrl)
        # raise Exception('Failed to get <Response [200]>')
        print('Failed to get <Response [200]>\n', gameUrl)




# # Check if soup if valid
# soup = get_source_code_from_selenium(game_url, driver)
# print(soup)
# print('\n-------------------------------------------------------------------------------'
#       '\n-------------------------------------------------------------------------------'
#       '\n-------------------------------------------------------------------------------\n')
# print(soup.get_text())

