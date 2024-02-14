import requests
from bs4 import BeautifulSoup
import re
import time as tm
import random
import csv

possible_headers = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.3"
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604."
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115."
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0."
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.4"
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.2"
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.1"
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.6"
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121."
        ] 

csv_name = "all_the_reviews.csv"

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}

def sleep(mini=0, maxi=1000):
    howMuch = random.uniform(mini, maxi)
    tm.sleep(20 + howMuch / 1000)

months = ["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "ноября", "декабря"]

def get_num_of_month_from_str(month):
    m_num = months.index(month) + 1
    if m_num < 10:
        return "0" + str(m_num)
    else:
        return str(m_num)


def get_page(url):
    headers = {'User-Agent': random.choice(possible_headers), 
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", 
    "Accept-Encoding": "gzip, deflate, br", 
    "Accept-Language": "en-US,en;q=0.5", 
    "Sec-Fetch-Dest": "document", 
    "Sec-Fetch-Mode": "navigate", 
    "Sec-Fetch-Site": "none", 
    "Sec-Fetch-User": "?1", 
    "Upgrade-Insecure-Requests": "1", 
    "X-Amzn-Trace-Id": "Root=1-65ca5482-0cb000122bb10f5538269c8d"}
    pg = requests.get(URL,headers=headers)
    return pg



pattern_good_evil = re.compile('comment_num_vote_\\d+">(\\d+) \\/ (\\d+)<\\/li>')
pattern_isPositive = re.compile('<div\\sclass="response\\s([\\w]+)"\\sid="div_review')
pattern_time = re.compile('(\d+:\d+)$')
pattern_date = re.compile('^(\d+)\s([а-я]+)\s(\d+)')



num = 1 

# Получаем первую страницу чтобы не возиться с всякими do while
URL = "https://www.kinopoisk.ru/film/326/reviews/ord/date/status/all/perpage/10/page/" + str(num) + "/"
num = num + 1
page = get_page(URL)

soup = BeautifulSoup(page.content, 'html.parser')
reviews = soup.find_all("div", class_="reviewItem userReview")

file_csv = open(csv_name, 'w', newline='')
writer = csv.writer(file_csv)
writer.writerow(["date", "time", "Was review helpful", "Was review unhelpful", "Author", "Title", "Review text", "Length of review text", "Was review positive"])
# row = [fecha, time, good, evil, author, title, text, length, isPositive_str]

while len(reviews) != 0:
    for review in reviews:
        
        # Я хочу узнать где упало, если упадет
        print("$ PAGENUMBER : " + str(num) + "\n")
        print("$ REVIEW FULLTEXT : " + str(review) + "\n")

        if title := review.find("p", class_="sub_title"): 
            title = title.text
        else:
            title = "NOT FOUND"
        if author := review.find("p", class_="profile_name"):
            author = author.text
        else:
            author = "NOT FOUND"

        # Переводим дату в нормальный формат yyyymmdd

        if datetime := review.find("span", class_="date"):
            datetime = datetime.text
            time = re.search(pattern_time, datetime).group(1)
            if date := re.search(pattern_date, datetime):
                fecha = date.group(3) + get_num_of_month_from_str(date.group(2)) + date.group(1)
            else:
                date = "NOT FOUND"

        else:
            datetime = "NOT FOUND"
        if text := review.find("span", class_="_reachbanner_"):
            text = text.text
        else:
            text = "NOT FOUND"

        length = len(text)

        fulltext = str(review)

        if match := re.search(pattern_good_evil, fulltext):
            good = match.group(1)
            evil = match.group(2)
        else:
            good = "NOT FOUND"
            evil = "NOT FOUND"

        if match := re.search(pattern_isPositive, fulltext):
            isPositive_str = match.group(1)
        else:
            isPositive = "NOT FOUND"

        row = [fecha, time, good, evil, author, title, text, length, isPositive_str]
        writer.writerow(row)

        




    
    URL = "https://www.kinopoisk.ru/film/326/reviews/ord/date/status/all/perpage/10/page/" + str(num) + "/"
    num = num + 1
    page = get_page(URL) 

    soup = BeautifulSoup(page.content, 'html.parser')
    reviews = soup.find_all("div", class_="reviewItem userReview")
    print("$ " + URL + " : " + str(len(reviews)))
    #print(str(reviews))
    # Делаем паузу, чтобы снизить шанс проблем с автозащитой(?) кинопоиска. 20 секунд умножить на 57 страниц отзывов = 19 минут ожидания
    sleep()


file_csv.close()

"""
Возможность уменьшить детекцию далее:

1.Указать реферер - сайт, с которого я пришел(?)
2.Сделать ротацию всех хедеров с браузера, а не только юзерагента / поустанавливать браузеры и позаписывать их хедеры https://httpbin.org/anything
3.Прогрузка жаваскрипта - уменьшить детекцию + получить возможность работать с жаваскрипт pagination
4.Прокси и их ротацию - самое муторное, снизит детекцию по айпи(использовать tor/бесплатные впн?)
"""

# Очень странно - на сайте доступно 57 страниц обзоров, но путем 'ручного' редактирования URL я получил секретные 58, 59 и 60-ю страницу отзыва)
