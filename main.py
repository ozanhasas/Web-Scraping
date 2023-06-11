import pandas as pd
from bs4 import BeautifulSoup as bs
from selenium import webdriver


def get_soup(link):
    driver = webdriver.Chrome()
    driver.get(link)
    html = driver.page_source
    return bs(html, 'html.parser')


def get_awards_data(soup):
    list_dict = []
    award_categories = soup.findAll("div", {"class": "event-widgets__award"})
    award_year = soup.find("div", {"class": "event-year-header__year"}).get_text()
    for i in award_categories:
        award_name = i.find("div", {"class": "event-widgets__award-name"}).get_text()
        for x in i.findAll("div", {"class": "event-widgets__award-category"}):
            if award_name == "Oscar":
                category_name = x.find("div", {"class": "event-widgets__award-category-name"}).get_text()
            else:
                category_name = "None"
            for z in x.findAll("div", {"class": "event-widgets__award-nomination"}):
                general_dict = {}
                a_tag = (z.find("div", {"class": "event-widgets__nominee-image"})).find("img", {"class": "event-widgets__nominee-image-poster"})
                poster_link = a_tag['src']
                nominee_name = a_tag['title']
                nominee_name_span = z.find("span", {"class": "event-widgets__nominee-name"})
                if nominee_name_span is not None:
                    nominee_link_tag = nominee_name_span.find("a", href=True)
                    nominee_link = "www.imdb.com" + str(nominee_link_tag["href"])
                else:
                    nominee_link = "None"
                winner_tag = z.find("div", {"class": "event-widgets__winner-badge"})
                if winner_tag is not None:
                    winner_badge = winner_tag.get_text()
                else:
                    winner_badge = "None"
                original_title_primary = (z.find("div", {"class": "event-widgets__original-title--primary"})).find("a", href=True)
                if original_title_primary is not None:
                    original_nominee_name = original_title_primary.text
                else:
                    original_nominee_name = nominee_name

                general_dict['Award Name'] = award_name
                general_dict['Category Name'] = category_name
                general_dict['Poster Link'] = poster_link
                general_dict['Nominee Name'] = nominee_name
                general_dict['Nominee Link'] = nominee_link
                general_dict['Winner'] = winner_badge
                general_dict['Original Nominee Name'] = original_nominee_name
                general_dict['Year'] = award_year
                list_dict.append(general_dict)
    return list_dict


list_results = []

for number in range(2023,1928,-1):
    soup = get_soup('https://www.imdb.com/event/ev0000003/' + str(number) + '/1')
    if soup.find("div", {"class": "event-year-header"}) is None:
        continue
    list_results += get_awards_data(soup)
    print(number)

df = pd.DataFrame(list_results)
df.to_excel("awards.xlsx")
