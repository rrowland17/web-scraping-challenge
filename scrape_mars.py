#Convert your Jupyter notebook file into a .py file

#import dependencies
from bs4 import BeautifulSoup 
import requests
import pandas as pd
from splinter import Browser
from selenium import webdriver

#set up browser (I am using Windows)
def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

#execute all of your scraping code from above
# and return one Python dictionary containing all of the scraped data
def scrape ():
    browser = init_browser()

   #URL of NASA News Page
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
    html = browser.html

    # create a soup object from the news html
    nasa_news = BeautifulSoup(html, 'html.parser')
    news_title = nasa_news.find('div', class_='content_title').text
    news_p = nasa_news.find('div', class_='rollover_description_inner').text

    #URL of NASA Images
    images_url = 'https://www.jpl.nasa.gov/spaceimages/'
    browser.visit(images_url)
    html = browser.html

    #create a soup object from the images html
    nasa_images = BeautifulSoup(html, 'html.parser')
    featured_image = nasa_images.find('a', class_='fancybox')
    url = featured_image.get('data-fancybox-href')
    featured_image_url = 'https://www.jpl.nasa.gov' + url

    #URL of Mars Twitter
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)
    html = browser.html

    #create a soup object from the Twitter HTML
    mars_twitter = BeautifulSoup(html, 'html.parser')
    mars_weather = mars_twitter.find('div', class_="js-tweet-text-container").get_text()

    #URL of Nasa Facts read to HTML, then made to table
    facts_url = 'https://space-facts.com/mars/'
    facts_table = pd.read_html(facts_url)
    mars_table = facts_table[1]
    mars_table.columns = ['Mars', 'Data']
    mars_table = mars_table.replace("\n", "")
    facts_html = mars_table.to_html()

    #Mars hemispheres URL
    import time
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)
    hemispheres = []

    #hemispheres loop
    for i in range(4):
        time.sleep(3)
        images = browser.find_by_tag('h3')
        images[i].click()
        html = browser.html
        hemi_soup = BeautifulSoup(html, 'html.parser')
        image_title = hemi_soup.find("h2", class_=  "title").get_text()
        back_half_url = hemi_soup.find('img', class_="wide-image")['src']
        img_url = 'https://astrogeology.usgs.gov/' + back_half_url
        dictionary = {"title": image_title, "img_url":img_url}
        hemispheres.append(dictionary)
        browser.back()


# Store data in a dictionary
    mars_info = {
        "News_Title": news_title,
        "News_Text": news_p,
        "Featured_Image_URL": featured_image_url,
        "Mars_Weather": mars_weather,
        "Mars_Table": mars_table,
        "Hemisphere_Image_URLs": hemispheres
    }

# Close the browser after scraping
    browser.quit()

# Return results
    return mars_info