#import dependencies
from bs4 import BeautifulSoup as bs
import requests
import pymongo
from splinter import Browser
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pandas as pd


# Create a browser instance using splinter
def init_browser():
    executable_path = {'executable_path': 'chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser=init_browser()
    mars_info = {}

    # Visit the Mars News url
    MarsNews_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(MarsNews_url)

    # Create HTML object
    html = browser.html

    # Parse HTML with BeautifulSoup
    soup = bs(html, 'html.parser')

    # Save the news title as variable
    news_title = soup.find('div', class_='content_title').text
    print(news_title)

    # Save the paragraph text as variable
    news_p = soup.find('div', class_='article_teaser_body').text
    print(news_p)


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
    featured_image_url


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
    featured_image_url


    #use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    url = 'https://space-facts.com/mars/'

    #Use Pandas to convert the data to a HTML table string.
    tables = pd.read_html(url)
    tables


    # Find the correct DataFrame in the list of DataFrames as assign it to `mars_df`
    mars_df = tables[0]
    mars_df.columns = ['Description', 'Value']
    mars_df


    # Find location of all hemisphere titles and thumbnails
    items = soup.find_all('div', class_='item')

    #Make empty lists to store the hemisphere name and thumbnail url
    names = []
    urls = []

    #Loop through items and store hemisphere name and thumbnail url in lists
    for item in items:
        urls.append(base_url + item.find('a')['href'])
        names.append(item.find('h3').text.strip())
    print(names + urls)


    # Visit https://astrogeology.usgs.gov
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    #Make empty list to store the hemisphere name and image url as dictionaries
    hemisphere_dict_list = []

    # Get all elements that contain image information
    items = soup.find_all("div", class_="item")

    # Iterate through each image
    for item in items:
        # Get the Hemisphere name
        name = item.find("h3").text
        # Set up to go to hemisphere pages to get full image url
        end_url = item.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_url
        # Visit Individual hemisphere page   
        browser.visit(image_link)
        # Scrape page into Soup
        html = browser.html
        soup = bs(html, "html.parser")
        # Get full image url
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        # Save hemisphere name and image url to empty list as 4 dictionaries
        hemisphere_dict_list.append({"Name": name, "img_url": image_url})

    # Print image title and url
    print(hemisphere_dict_list)


    # Create dictionary for all info scraped from sources above
    mars_info={
        "news_title":news_title,
        "news_p":news_p,
        "featured_image_url":featured_image_url,
        "fact_table":mars_df,
        "hemisphere_images":hemisphere_dict_list
    }

    # Close the browser after scraping
    browser.quit()

    # retuen Dictionary
    return mars_info


