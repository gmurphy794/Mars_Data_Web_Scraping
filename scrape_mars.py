import pandas as pd
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pymongo




def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    master_dic = {
        'news':[],
        'jpl':'',
        'weather':'',
        'facts':'',
        'hemispheres':[]
    }
    ###Mars News

    #Initializing
    browser = init_browser()
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #Gathering Data
    titles = soup.find_all('div', class_='content_title')
    paragraphs = soup.find_all('li', class_='slide')
    results = soup.find_all('li', class_='slide')
    for result in results:
        title = result.find('div', class_='content_title').text
        paragraph = result.find('div', class_='article_teaser_body').text

    # Dictionary to be inserted into MongoDB
        post = {
            'title': title,
            'paragraph': paragraph
        }
        master_dic['news'].append(post)
    browser.quit()

    
    ### JPL Mars Space Images - Featured Image
    #Initializing
    browser = init_browser()
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #Gathering Data
    image_text = soup.find('article')['style']
    image_url = image_text.split("'")[1]
    image_url_full = 'https://www.jpl.nasa.gov' + image_url
    master_dic['jpl'] = image_url_full
    browser.quit()

    
    ###Mars Weather
    #Initializing
    browser = init_browser()
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #Gathering Data
    mars_weather = soup.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text" ).text
    master_dic['weather'] = mars_weather
    browser.quit()

    
    
    ###Mars Facts
    #Initializing
    browser = init_browser()
    url = 'https://space-facts.com/mars/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #Gathering Data
    table = soup.find('tbody')
    table_rows = table.find_all('tr')
    pd_data = []
    for tr in table_rows:
        td = tr.find_all('td')
        row = [tr.text for tr in td]
        pd_data.append(row)
    mars_df = pd.DataFrame(pd_data, columns=['Description','Value'])
    mars_df = mars_df.set_index('Description')
    mars_table = mars_df.to_html()
    master_dic['facts'] = mars_table
    browser.quit()


    ###Mars Hemispheres
    #Creating Lists to store dictionaries and urls
    hemi_list = []
    urls = [
        'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced',
        'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced',
        'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced',
        'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced'
    ]   
    #Loop through urls and collect data
    for url in urls:
        browser = init_browser()
        browser.visit(url)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        tif = soup.find('div', class_='wide-image-wrapper')
        img = 'https://astrogeology.usgs.gov' + tif.find('img', class_='wide-image')['src']
        titles = soup.head.title.text.split(' ')
        title = titles[0] + ' ' + titles[1]
        hemi_dic = {"title":title, "img_url":img}
        master_dic['hemispheres'].append(hemi_dic)
        browser.quit()

    #Return Scraped Data
    return master_dic

