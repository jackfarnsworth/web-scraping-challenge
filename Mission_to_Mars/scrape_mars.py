from bs4 import BeautifulSoup
import requests
import pandas as pd
import pymongo
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    with Browser('chrome', **executable_path, headless=False) as browser:
        #get news items
        browser.visit('https://redplanetscience.com/')
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')

        news_title = soup.find('div', class_="content_title").text
        news_p = soup.find('div', class_="article_teaser_body").text

        #get featured image
        browser.visit('https://spaceimages-mars.com/')
        browser.links.find_by_partial_text('FULL IMAGE').click()
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        featured_image_url = f'https://spaceimages-mars.com/{soup.find("img", class_="headerimage")["src"]}'

        #get table
        browser.visit('https://galaxyfacts-mars.com/')
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        tables = pd.read_html('https://galaxyfacts-mars.com/')
        mars_df = tables[1]
        table = mars_df[:].to_html(index=False, header=False, border=2)
        table.replace('\n', '')

        #get hemisphere images
        url = 'https://marshemispheres.com/'
        browser.visit(url)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')

        links = soup.find_all('div', class_='item')

        hemisphere_image_urls = []
        for link in links:
            browser.visit(url + link.find("a")["href"])
            html = browser.html
            soup = BeautifulSoup(html, 'html.parser')
            hemisphere_image_urls.append({"title" : link.find('h3').text.replace(" Enhanced", ''), 
                                        "img_url": url + soup.find('div', class_='downloads').find('a')['href']})
    return {"newstitle" : news_title,
            "newsparagraph": news_p,
            "featuredimage": featured_image_url,
            "table": table,
            "hemispheres": hemisphere_image_urls}


