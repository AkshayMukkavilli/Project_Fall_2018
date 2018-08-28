
import requests
from bs4 import BeautifulSoup
import random

users = [
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.2 (KHTML, like Gecko) Chrome/4.0.223.3 Safari/532.2',
    'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/540.0 (KHTML,like Gecko) Chrome/9.1.0.0 Safari/540.0',
    'Mozilla/5.0 (X11; U; Windows NT 6; en-US) AppleWebKit/534.12 (KHTML, like Gecko) Chrome/9.0.587.0 Safari/534.12',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.45 Safari/535.19',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/530.5 (KHTML, like Gecko) Chrome/2.0.173.1 Safari/530.5',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7',
    'Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.66 Safari/535.11',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.600.0 Safari/534.14',
     'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/540.0 (KHTML,like Gecko) Chrome/9.1.0.0 Safari/540.0'
     'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
     'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
     'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
     'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
     'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
     'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
     'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
     'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
     'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
]
header = {'User-Agent': users[random.randint(0, len(users) - 1)]}
ASIN_list = []
with open('asins.txt','r') as fi:
    ASIN_list = fi.read().splitlines()
total_reviews = " "
i = 0
for asin in ASIN_list:
    print("Working on the product wiith ASIN: ",ASIN_list[i])
    url = "https://www.amazon.com/dp/" + ASIN_list[i]
    source_code = requests.get(url, headers=header)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "lxml")

    # Getting the link that says see all reviews
    all_reviews_link = soup.find('a',{'class': "a-link-emphasis a-text-bold", 'data-hook': "see-all-reviews-link-foot"})
    print("The all reviews link is: " , all_reviews_link)
    only_link = (all_reviews_link['href'])
    total_link = "https://www.amazon.com" + only_link + "&pageNumber="
    print(total_link)

    # For getting the total number of pages with reviews
    see_all_reviews_text = all_reviews_link.text
    list_after_splitting = see_all_reviews_text.split()[2]
    try:
        str_no_of_reviews = int(list_after_splitting)
    except:
        str_no_of_reviews = int(list_after_splitting.replace(',', ''))
    iterator = int(str_no_of_reviews/10) + 1
    print("The product has ", iterator , "pages of reviews")


    page = 1
    fw = open(asin + '.txt', 'w', encoding="utf-8")
    while page <= iterator:
        print("Now, working on page: ", page)
        review_link_with_pageno = total_link + str(page)
        header_1 = {'User-Agent': users[random.randint(0, len(users) - 1)]}
        source_code_1 = requests.get(review_link_with_pageno, headers=header_1)
        plain_code = source_code_1.text
        soup_1 = BeautifulSoup(plain_code, "lxml")
        reviews = soup_1.findAll('span', {'class': "a-size-base review-text", 'data-hook': "review-body"})
        str_reviews = str(reviews)
        if len(str_reviews) < 3:
            print("the data could not be retrieved from the page: ", page)
        total_reviews = total_reviews + "\n" + str_reviews
        page += 1
    i += 1
    fw.write(total_reviews)
    fw.close()






