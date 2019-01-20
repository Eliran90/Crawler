import csv

import requests
from bs4 import BeautifulSoup


def crawler_spider(max_page):
    page = 1
    csv_file = 'links{}_20_pages_query_1.csv'.format('fQ')
    csvfile = open(csv_file,'w', encoding='utf-8')
    field_names = ['href', 'text']
    writer = csv.DictWriter(csvfile, delimiter=',', quotechar='\\', quoting=csv.QUOTE_MINIMAL, fieldnames=field_names)
    CSV = open('count_word_per_page_20_pages_query_1.csv', 'w+', encoding='utf-8')
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
        for h3 in soup.findAll('h3', {'class': 'm-MediaBlock__a-Headline'} ):
            for link in h3.findAll('a'):
                href = link.get('href')
                flag = 0
                try:
                    sorce2 = requests.get("https:"+href)
                except:
                    print("page: "+str(page)+"\nhref: "+str(href)+"\n")
                    flag = 1
                    break
                plan_text2 = sorce2.text
                soup2 = BeautifulSoup(plan_text2, 'html.parser')
                a = soup2.findAll('span', {'class': 'o-RecipeInfo__a-Description'} )
                if a.__len__() == 0:
                    flag = 1
                    break
                b = str(a[0])
                if b.find("Intermediate") == -1:
                    flag = 1
                    break
                text = link.string
                split_text = text.split()
            if flag == 0:
                for word in split_text:
                        word_page.append(word.lower())
                data = dict(href=href.strip(), text=text.strip())
                writer.writerow(data)
                print(data)

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