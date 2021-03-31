#import dependencies
from bs4 import BeautifulSoup as bs
import requests
import pymongo
from splinter import Browser
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    # executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    # return Browser("chrome", **executable_path, headless=False)
    
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=True)

def scrape():
    browser=init_browser()
    mars_info = {}

    # Visit the Mars News url
    MarsNews_url = "https://mars.nasa.gov/news/"
    browser.visit(MarsNews_url)
    # Create HTML object
    html = browser.html
    # Parse HTML with BeautifulSoup
    soup = bs(html, 'html.parser')
    article = soup.find("div", class_='list_text')
    news_title = article.find("div", class_="content_title").text
    news_p = article.find("div", class_ ="article_teaser_body").text
    # # Save the news title as variable
    # news_title = soup.find('div', class_='content_title')
    # print(news_title)
    # # Save the paragraph text as variable
    # # news_p = soup.find('div', class_='article_teaser_body').text
    # news_p = soup.find('div', class_='article_teaser_body')
    # print(news_p)


    # Visit the Mars News url
    jpl_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    browser.visit(jpl_url)
    # Create HTML object
    html = browser.html
    # Parse HTML with BeautifulSoup
    soup = bs(html, 'html.parser')
    # Save the hero image url as variable
    base_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/'
    #Find the src of the correct image (hero Image)
    relative_image_path = soup.find_all('img')[1]["src"]
    # Complete the featured image url by adding the base url ---
    featured_image_url = base_url + relative_image_path


    # Visit the Mars News url
    jpl_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    browser.visit(jpl_url)
    # Create HTML object
    html = browser.html
    # Parse HTML with BeautifulSoup
    soup = bs(html, 'html.parser')
    # Save the hero image url as variable
    base_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/'
    #Find the src of the correct image (hero Image)
    relative_image_path = soup.find_all('img')[1]["src"]
    # Complete the featured image url by adding the base url ---
    featured_image_url = base_url + relative_image_path
 

    #use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    url = 'https://space-facts.com/mars/'
    #Use Pandas to convert the data to a HTML table string.
    tables = pd.read_html(url)
    # Find the correct DataFrame in the list of DataFrames as assign it to `mars_df`
    mars_df = tables[0]
    mars_df.columns = ['Description', 'Value']
    mars_html_df = mars_df.to_html()



    base_url = "https://astrogeology.usgs.gov"
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    # Find location of all hemisphere titles and thumbnails
    mars_hemispheres =soup.find('div', class_='collapsible results')
    items = mars_hemispheres.find_all('div', class_='item')    
    #Make empty list to store the hemisphere name and image url as dictionaries
    hemisphere_dict_list = []
    # Iterate through each hemisphere
    for item in items:
        # Get the Hemisphere name
        hemisphere = item.find('div', class_="description")
        name = hemisphere.h3.text
        # Set up to go to hemisphere pages to get full image url
        hemisphere_link = hemisphere.a["href"]
        # Visit Individual hemisphere page
        browser.visit(base_url + hemisphere_link)
        # Scrape page into Soup
        html = browser.html
        soup = bs(html, "html.parser")
        # Get full image url
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("li").a["href"]
        # Save hemisphere name and image url to empty list as 4 dictionaries
        image_dict = {}
        image_dict["name"] = name
        image_dict["img_url"] = image_url
        hemisphere_dict_list.append(image_dict)


    # Create dictionary for all info scraped from sources above
    mars_info={
        "news_title":news_title,
        "news_p":news_p,
        "featured_image_url":featured_image_url,
        "fact_table": str(mars_html_df),
        "hemisphere_images":hemisphere_dict_list
    }
    print(mars_info)
    # Close the browser after scraping
    browser.quit()

    # retuen Dictionary
    return mars_info


if __name__=="__main__":
    scrape()
