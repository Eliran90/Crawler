import csv

import requests
from bs4 import BeautifulSoup
import re


def crawler_spider(max_page):
    page = 1
    csv_file = 'links{}_20_pages_query_2.csv'.format('fQ')
    csvfile = open(csv_file,'w', encoding='utf-8')
    field_names = ['href', 'text']
    writer = csv.DictWriter(csvfile, delimiter=',', quotechar='\\', quoting=csv.QUOTE_MINIMAL, fieldnames=field_names)
    CSV = open('count_word_per_page_20_pages_query_2.csv', 'w+', encoding='utf-8')
    fieldnames = ['word', 'count', 'page']
    writer1 = csv.DictWriter(CSV, fieldnames=fieldnames)

    url = 'https://www.foodnetwork.com/search/beef-/CUSTOM_FACET:RECIPE_FACET'
    word_page = []
    count_word = []
    sorce = requests.get(url)
    plan_text = sorce.text
    soup = BeautifulSoup(plan_text, 'html.parser')
    soup.encode("utf-8")
    while page < max_page:
        for div in soup.findAll('div', {'class': 'm-MediaBlock__m-TextWrap'} ):
            try:
                a = div.findAll('a')
                b = div.findAll('span', {'class': 'gig-rating-ratingsum'})
                c = str(b[0].contents[0])
                d = int(re.search(r'\d+', c).group())
                href = a[0].get('href')
                text = a[0].string
                split_text = text.split()
                if d > 50:
                    for word in split_text:
                            word_page.append(word.lower())
                    data = dict(href=href.strip(), text=text.strip())
                    writer.writerow(data)
                    print(data)
            except:
                continue

        try:
            page += 1
            url = 'https://www.foodnetwork.com/search/beef-/p/' + str(page)+'/CUSTOM_FACET:RECIPE_FACET'
            sorce = requests.get(url)
            plan_text = sorce.text
            soup = BeautifulSoup(plan_text, 'html.parser')
            for word in word_page:
                if word_page.count(word) != 0:
                    count_word.append(dict(word=word, count=word_page.count(word), page=page-1))
                word_page = list(filter(lambda a: a != word, word_page))
            newlist = sorted(count_word, key=lambda k: k['count'], reverse=True)
            for i in range(len(newlist)):
                writer1.writerow(newlist[i])
                if i == 10:
                    break
            word_page = []
            count_word = []
        except:
            print("no more pages")
            page = max_page

crawler_spider(21)