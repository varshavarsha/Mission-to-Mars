from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape(): 
    #executable_path = {'executable_path': 'chromedriver.exe'}
    #browser = Browser('chrome', **executable_path)
    browser = Browser('chrome', headless=True)

    news_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(news_url)
    time.sleep(1)
    news_html = browser.html
    soup = BeautifulSoup(news_html, 'html.parser')

    #code to loop through all latest articles on first page

    #articles = soup.find_all('li', class_='slide')

    #for article in articles:
    #    text = article.find('div', class_='list_text')
    #    news_title = text.find('div', class_='content_title').text
    #    news_p = text.find('div', class_='article_teaser_body').text

    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='article_teaser_body').text

    print(news_title)
    print(news_p)

    img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(img_url)
    img_html = browser.html
    soup = BeautifulSoup(img_html, 'html.parser')

    featured_image = soup.find('a', class_ = 'button fancybox')['data-fancybox-href']
    featured_image_url = 'https://www.jpl.nasa.gov' + featured_image
    print(featured_image_url)

    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)
    weather_html = browser.html
    soup = BeautifulSoup(weather_html, 'html.parser')

    mars_weather = soup.find('p', class_ ="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    print(mars_weather)

    table_url = 'https://space-facts.com/mars/'

    table = pd.read_html(table_url)[0]
    table.columns = ["Description", "Value"]
    table = table.set_index("Description", drop= True,  inplace=False)
    table_html = table.to_html()
    print(table_html)

    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemi_url)
    hemi_html = browser.html
    soup = BeautifulSoup(hemi_html, 'html.parser')

    links = soup.find_all('div', class_='item')

    hemi_base = "https://astrogeology.usgs.gov"
    hemi_urls = [str(hemi_base + link.a['href']) for link in links]

    hemisphere_image_urls = []

    for hemi_url in hemi_urls:
        browser.visit(hemi_url)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        img_url = soup.find('div', class_= 'downloads').a['href']
        title = soup.find('h2', class_= "title").text.rsplit(' ', 1)[0]
        entry = {"title" : title , "img_url" : img_url}
        hemisphere_image_urls.append(dict(entry))

    print(hemisphere_image_urls)

    mars_data = {
    'newsTitle' : news_title,
    'newsParagraph' : news_p,
    'featuredImage' : featured_image_url,
    'marsWeather' : mars_weather,
    'tableHtml' : table_html,
    'hemisphereImages' : hemisphere_image_urls
    }

    return mars_data

